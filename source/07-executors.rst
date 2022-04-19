07. Executors
=============

Because a DEX operates on top of a blockchain, it follows the basic principle of blockchains: there is a decentralized
ledger of transactions which validators are building. So, one can see a DEX as an evolving state of a sequential
computer.

As was explained in chapter 6, we fixed a certain set of transaction types and we fixed their semantics for all but one.
The single exceptional case being ``add-order`` transaction.

On the technical level, a single ``add-order`` execution must be resolved to a sequence of swaps. This is the job of
an **executor**. We consider an executor to be pluggable part of DEX implementation.

In this chapter we specify the algorithms of all executors currently supported in Dexter. The dynamic behaviour of these
algorithms and especially the comparative measurements of their statistics is the primary motivation behind creating
Dexter.

Space of executors research
---------------------------

The space of all possible executor is vast. Dexter was created as a proof of concept tool for investigating the
contents of this space.

However, in the current version of Dexter, we limit our attention to rather "simplistic" class of executors,
specifically, we require executors to be compliant with the following rules:

**Rule #1: Equality of traders**
  Swaps chronology can depend only on the state of markets (i.e. it is not allowed that it depends on the state of
  traders).

  This rule means that the exchange in not "biased" on trader's identity or other trader properties (such as wealth
  of a trader for example).
  In lame terms it means that all traders are considered "equally important" by the executor - i.e. from the perspective
  of an executor, any trader is seen as "just an account number" (similar concept to "all citizens are considered equal
  by law in a democracy"). In particular - current balance of trader's account, past history of his trading activity
  and trader's name - all this cannot influence the path of DEX evolution that an executor is creating.

**Rule #2: Isolation of markets**
  Arrival of a new order generates swaps only on the market where this order belongs to.

**Rule #3: Isolation of traders**
  Every swap involves only one order.

**Rule #4: Isolation of swaps**
  An executor makes next-swap decision based only on the current state of the market and number of swaps executed in
  the current executor loop. The intention here is that the executor is not allowed to decide based on the history of
  executes swaps.

**Rule #5: Natural trading priority**
  Execution prioritizes traders happy to accept less attractive exchange rate (i.e. an exchange rate that gives him
  less profit). In case of a tie, a trader waiting longer is served first.

**Rule #6: Funds locking**
  Trader can place an order on the DEX only if the amount of tokens to be sold is covered by the balance of his
  account. Upon placing an order, the executor will issue a "lock" on the amount of tokens declared in the order
  as sell amount. Locked tokens cannot be reused in another order. Locked tokens get unlock on order expiration or
  cancellation.

Motivation for above rules comes from various sources:

  - **Equality of traders** and **Natural trading priority** seem to be very natual and go along the general
    expectations of the wide public; any DEX violating these rules would be really a weird one.
  - **Funds locking** is a business-level decision; DEXes violating this rule
    are probably quite useful and interesting, although it must be said that their trading mechanics would be more
    distant from Forex tradition. Therefore the motivation behind funds locking can be
    seen as "let's keep things mentally close to Forex community for now" (please notice that Dexter is all about
    simulating hybrid exchanges, so the analogy to Forex is going to be always around).
  - All 3 "isolation" rules delineate the boundary of "simplest executors one can consider"; anything beyond this region
    immediately becomes complex and sophisticated. From this perspective the mission of Dexter can be understood as
    "let's see how far we can get with those simplistic executors before we delve into sophisticated ones". A good
    motivation for dropping **isolation of markets** would be building a DEX where arbitrage is impossible. A good
    motivation for dropping **isolation of traders** would be borrowing from Forex the idea of direct trader-to-trader
    swaps, i.e. bypassing the AMM interaction when possible.

Executor loop overview
----------------------

Because we assume **Rule #2: Isolation of markets**, once a new order arrives to the DEX, we are going to process
the order book only for the market where the new order belongs. Let us fix the coins to be :math:`AAA` and :math:`BBB`,
so the market is :math:`AAA/BBB` and orders have direction :math:`AAA \rightarrow BBB` or
:math:`BBB \rightarrow AAA`. We will further refer to this market as ``market`` (see the scripts below).

Thanks to the rules enumerated in previous chapter, the job of an executor loop can be largely simplified. Let us
outline the template of such loop by extending the activity diagram in from previous chapter:

.. image:: pictures/07/executor-loop.png
    :width: 100%
    :align: center

Places marked above with red asterisk are where non-trivial logic must be plugged-in:

**1: Making next executor decision**
  At this point, one of two half-markets must be picked. This is equivalent to selecting a direction: :math:`AAA \rightarrow BBB`
  or :math:`BBB \rightarrow AAA`. In the context of "oriented" market, this means selecting "asks" or "bids" side
  of the order book.
  Additionally, the order type (``Limit`` vs ``Stop``) must be selected here.
  An executor is free to give up at this point, if the state of the market does not allow for executing of any order.

**2: Checking swap preconditions**
  At this point swap preconditions are checked. Red light will abort swap creation and terminate the executor loop.

**3: Calculating swap amount and executing the swap**
  Deciding on amounts of the next swap to be executed. Because of **Rule #5: Natural trading priority**, the next swap
  to be executed must be for the head position on the positions collection (because the positions list is ordered
  by price-then-order-time).

**4: Post-swap assertions**
  Extension point for plugging-in diagnostic assertions to be checked after every swap.

Arithmetic precision problems and their solution
------------------------------------------------

Internal working of the executor is vulnerable to "strange" effects caused by imperfectness of computer arithmetic.
This effects generally disrupt the operation of mathematical definitions of the executor. Two particular problems are:

  - When (at least one side of) the AMM balance becomes small enough, integer rounding effects can cause significant
     errors in calculated swap amounts.

  - When calculated swap amounts are small enough, integer rounding may cause limit-price invariant to fail.

To avoid such anomalies we generally apply a simple approach:

  1. Enforce that AMM balances are always above certain AMM_MIN_BALANCE (which is a parameter).

  2. Enforce that order amount is always above certain TRADING_MIN_AMOUNT (which is a parameter).

  3. Enforce that swap amounts are always above certain SWAP_MIN_AMOUNT (which is a parameter).

To work as expected, above parameters must be set accordingly to the arithmetic precision used by the implementation
of DEX. Please notice that arithmetic precision is also limited in the fixed-point arithmetic - because of the
necessary rounding in operations such as multiplication.

For example if the arithmetic precision is at the order 1e-18, then "reasonable" values for above params could be:

  - AMM_MIN_BALANCE = 1e-14

  - TRADING_MIN_AMOUNT = 1e-8

  - SWAP_MIN_AMOUNT = 1e-10


Executor loop details
---------------------

The general pattern of open-order processing is implemented in class ``ExecutorTemplate``. The executor loop is part
of this:

.. code:: scala

  def open(order: Order): Unit = {

    //log diagnostic info "new order arrived"
    if (coreCallsDump.isDefined)
      coreCallsDump.get.print(s"[btime $blockchainTime] [rtime ${clock.apply()}] open order: id=${order.id} type=${order.orderType} account=${order.accountAddress}" +
        s" askCoin=${order.askCoin} bidCoin=${order.bidCoin} price=${order.exchangeRate.toDouble} amount=${order.amount} exptime=${order.expirationTimepoint}")

    //check if the account address if valid
    precondition(hash2account.contains(order.accountAddress), s"unknown account: ${order.accountAddress}")

    //decode account address to account instance
    val account: Account = hash2account(order.accountAddress)

    //find relevant market and half-market
    val coinPairAB: CoinPair = CoinPair(order.askCoin, order.bidCoin)
    val halfMarketAB: HalfMarket = coinPair2HalfMarket(coinPairAB)
    val market: Market = coinPair2Market(coinPairAB.normalized)

    //purge expired orders on this market
    purgeExpiredPositionsOnMarket(market)

    //check if the trader has enough funds to place this order
    precondition (order.amount <= account.getFreeBalanceFor(order.sellCoin), s"order amount exceeds free balance for this account and coin: ${account.getFreeBalanceFor(order.sellCoin)}")

    //create new position instance (wrapping the order)
    val position = Position(order, market, account, blockchainTime, clock.apply())
    hash2position += order.id -> position

    //lock amount of tokens on trader's account corresponding to sell amount of this order
    account.addPosition(position)

    //add position to the order book
    halfMarketAB.addPosition(position)

    //update statistics
    market.onPositionOpened(position)

    //log diagnostic info "new position added"
    if (coreCallsDump.isDefined)
      coreCallsDump.get.print(s"[btime $blockchainTime] [rtime ${clock.apply()}] created new position for order ${position.id} normalized-amount=${position.normalizedAmount} normalized-price=${position.normalizedLimitPrice.toDouble}")

    //executor loop
    var n = 1
    var lastDecision: Option[(MarketSide, OrderType)] = executorNextDecision(market, position)
    var lastExecutionWasOk: Boolean = true
    while (n <= hamsterConstant & lastDecision.nonEmpty && lastExecutionWasOk && market.isAmmBalanceAboveTradingMinimum) {
      lastExecutionWasOk = lastDecision match {
        case Some((MarketSide.Asks, OrderType.Limit)) => attemptCreatingNextSwap(n, market, market.halfMarketAsks, OrderType.Limit)
        case Some((MarketSide.Bids, OrderType.Limit)) => attemptCreatingNextSwap(n, market, market.halfMarketBids, OrderType.Limit)
        case Some((MarketSide.Asks, OrderType.Stop)) => attemptCreatingNextSwap(n, market, market.halfMarketAsks, OrderType.Stop)
        case Some((MarketSide.Bids, OrderType.Stop)) => attemptCreatingNextSwap(n, market, market.halfMarketBids, OrderType.Stop)
      }
      n += 1
      if (lastExecutionWasOk)
        lastDecision = executorNextDecision(market, position)
    }
  }

Extension points - marked previously as red asterisks on the diagram - are encoded as corresponding abstract methods.
For implementing a specific executor, one needs to provide implementation of these methods only:

.. code:: scala

  def executorNextDecision(market: Market, newPositionThatTriggeredTheLoop: Position): Option[(MarketSide, OrderType)]

  def swapPreconditionsCheck(
                              market: Market,
                              halfMarketAB: HalfMarket,
                              askCoin: Coin, //buy coin
                              bidCoin: Coin, //sell coin
                              position: Position, //position for which the swap is to be executed
                              a: FPNumber, //AMM balance of ask coin
                              b: FPNumber, //AMM balance of bid coin
                              r: Fraction, //limit price as declared in the order
                              ammPrice: Fraction): Decision

  //returns (sellAmount, buyAmount) - where sell/buy meaning is from the perspective of the trader
  def calculateSwapAmounts(
                            market: Market,
                            halfMarketAB: HalfMarket,
                            askCoin: Coin, //buy coin
                            bidCoin: Coin, //sell coin
                            position: Position, //position for which the swap is to be executed
                            a: FPNumber, //AMM balance of ask coin
                            b: FPNumber, //AMM balance of bid coin
                            r: Fraction, //limit price as declared in the order
                            ammPrice: Fraction): (FPNumber, FPNumber)

  def postSwapAssertions(
                          market: Market,
                          halfMarket: HalfMarket,
                          position: Position,
                          sellAmount: FPNumber,
                          sellCoin: Coin,
                          buyAmount: FPNumber,
                          buyCoin: Coin,
                          ammPriceBeforeSwap: Fraction): Unit

Most complex part is the "attempt to create next swap". This was not covered in detail on the diagram above:

.. code:: scala

  def attemptCreatingNextSwap(hamsterLoopIteration: Int, market: Market, halfMarketAB: HalfMarket, orderType: OrderType): Boolean = {
    val askCoin: Coin = halfMarketAB.coinPair.left
    val bidCoin: Coin = halfMarketAB.coinPair.right

    lazy val headPosition: Position = orderType match {
      case OrderType.Limit => halfMarketAB.limits.head
      case OrderType.Stop => halfMarketAB.stops.head
    }

    val a: FPNumber = market.ammBalanceOf(askCoin)
    val b: FPNumber = market.ammBalanceOf(bidCoin)
    val r: Fraction = headPosition.exchangeRate
    val ammPrice: Fraction = market.currentPriceDirected(askCoin, bidCoin)

    if (coreCallsDump.isDefined)
      coreCallsDump.get.print(s"limit-execute: (iteration $hamsterLoopIteration) askCoin=$askCoin [balance $a] bidCoin=$bidCoin [balance $b] directed-amm-price=${ammPrice.toDouble}" +
        s" head-position=${headPosition.id} outstanding-amount=${headPosition.outstandingAmount} limit-price=${FPNumber.fromFraction(r)}")

    swapPreconditionsCheck(market, halfMarketAB, askCoin, bidCoin, headPosition, a, b, r, ammPrice) match {
      case Decision.GREEN =>
        val (sellAmount, buyAmount): (FPNumber, FPNumber) = calculateSwapAmounts(market, halfMarketAB, askCoin, bidCoin, headPosition, a, b, r, ammPrice)

        //negative amounts are considered a bug in 'calculateSwapAmounts'
        assert(sellAmount >= FPNumber.zero && buyAmount >= FPNumber.zero, s"calculateSwapAmounts() returned negative value: sellAmount=$sellAmount buyAmount=$buyAmount")

        //avoid "nano" swaps (below SWAP_MIN_AMOUNT), unless this is a complete filling case
        if (sellAmount <= swapMinAmount || buyAmount <= swapMinAmount)
          if (headPosition.amount > swapMinAmount)
            return false

        //zero amount is not considered a bug in 'calculateSwapAmounts', but we will not proceed with swap execution
        if (sellAmount == FPNumber.zero || buyAmount == FPNumber.zero)
          return false

        //we need to distinguish between partial filling and complete filling
        if (headPosition.amount == sellAmount) {
          //case 1: complete filling
          if (coreCallsDump.isDefined)
            coreCallsDump.get.print(s"executor decision: complete filling of $headPosition")
          val normalizedAmount: FPNumber = headPosition.normalizedAmount
          headPosition.registerCompleteFilling(sold = sellAmount, bought = buyAmount, blockchainTime)
          orderType match {
            case OrderType.Limit => halfMarketAB.limits.removeElementAtIndex(0)
            case OrderType.Stop => halfMarketAB.stops.removeElementAtIndex(0)
          }
          market.onPositionFilled(headPosition, normalizedAmount)
          headPosition.account.removePosition(headPosition)
          dumpFillingInfo(headPosition, sold = sellAmount, bought = buyAmount, isCompleteFilling = true)
        } else {
          //case 2: partial filling
          if (coreCallsDump.isDefined)
            coreCallsDump.get.print(s"executor decision: partial filling of $headPosition")
          val oldNormalizedAmount: FPNumber = headPosition.normalizedAmount
          headPosition.registerIncompleteFilling(sold = sellAmount, bought = buyAmount, blockchainTime)
          val delta: FPNumber = oldNormalizedAmount - headPosition.normalizedAmount
          market.onPositionPartiallyFilled(headPosition, delta)
          dumpFillingInfo(headPosition, sold = sellAmount, bought = buyAmount, isCompleteFilling = false)
        }

        //update statistics
        swapExecutionsCounter += 1

        //update account balances (to reflect the swap execution)
        headPosition.account.updateBalance(bidCoin, sellAmount.negated)
        headPosition.account.updateBalance(askCoin, buyAmount)

        //update the liquidity pool (to reflect the swap execution)
        market.updateLiquidityPool(bidCoin, sellAmount)
        market.updateLiquidityPool(askCoin, buyAmount.negated)

        //accumulation of some statistics for the AMM
        tokensExchangedIn.increment(bidCoin, sellAmount)
        tokensExchangedOut.increment(askCoin, buyAmount)

        //extension point for more assertions
        postSwapAssertions(market, halfMarketAB, headPosition, sellAmount, bidCoin, buyAmount, askCoin, ammPrice)

        //we completed the swap with success
        return true

      case Decision.RED =>
        //abort the swap
        return false
    }
  }

Variant 1: TEAL executor
------------------------

This executor is based on a proprietary algorithm created in Onomy Protocol. This executor follows this TLA+
specification:

https://github.com/onomyprotocol/specs/

On top of the specification we apply the "minimal trading balance" check on the AMM level. We just do not allow
either size of the liquidity pool to

1. Executor next decision
^^^^^^^^^^^^^^^^^^^^^^^^^

We select the same half-market where the position belongs.

In this variant, the value of ``HAMSTER_CONSTANT`` is hardcoded to 1, so the executor loop has always at most 1 iteration.

.. code:: scala

  override def executorNextDecision(market: Market, newPositionThatTriggeredTheLoop: Position): Option[(MarketSide, OrderType)] =
    Some(newPositionThatTriggeredTheLoop.normalizedMarketSide, newPositionThatTriggeredTheLoop.orderType)


2: Swap preconditions check
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The head of order book is ready for next swap if the current value of ``ammPrice`` exceeds the limit price of the order.
Please notice that we compare prices calculated in the same direction.


.. code:: scala

  override def swapPreconditionsCheck(
                                       market: Market,
                                       halfMarketAB: HalfMarket,
                                       askCoin: Coin,
                                       bidCoin: Coin,
                                       position: Position,
                                       a: FPNumber,
                                       b: FPNumber,
                                       r: Fraction,
                                       ammPrice: Fraction): Decision = {
    position.orderType match {
      case OrderType.Limit => if (ammPrice > r) Decision.GREEN else Decision.RED
      case OrderType.Stop => if (ammPrice < r) Decision.GREEN else Decision.RED
    }
  }

3: Calculate swap amounts
^^^^^^^^^^^^^^^^^^^^^^^^^

The "magic" formula of swap creation is defined here.

.. code:: scala

  override def calculateSwapAmounts(
                                     market: Market,
                                     halfMarketAB: HalfMarket,
                                     askCoin: Coin,
                                     bidCoin: Coin,
                                     position: Position,
                                     a: FPNumber,
                                     b: FPNumber,
                                     r: Fraction,
                                     ammPrice: Fraction): (FPNumber, FPNumber) =
    position.orderType match {
      case OrderType.Limit =>
        val maxBidAmt: FPNumber = (a - b ** r) ** ((r + 1).reciprocal)
        val strikeBidAmt: FPNumber = FPNumber.min(position.outstandingAmount, maxBidAmt)
        val strikeAskAmt: FPNumber = strikeBidAmt ** r
        (strikeBidAmt, strikeAskAmt)
      case OrderType.Stop =>
        val minMemberABal: FPNumber = a / FPNumber.fromLong(2)
        val maxMemberBBal: FPNumber = a + b - minMemberABal
        val maxMemberBAmt: FPNumber = maxMemberBBal - b
        val strikeBidAmt: FPNumber = FPNumber.min(position.outstandingAmount, maxMemberBAmt)
        val strikeAskAmt: FPNumber = (strikeBidAmt * (a - strikeBidAmt)) / (b + strikeBidAmt)
        (strikeBidAmt, strikeAskAmt)
    }

Variant 2: TURQUOISE executor
-----------------------------

This executor is based on the idea that we execute orders always using the limit price as declared in the order itself
- as long as the AMM-price allows to do so without introducing loss on DEX side. This approach is rather "unusual"
when compared to FOREX-style exchanges, where the swap price is always the current market price.

Here we allow the ``HAMSTER_CONSTANT`` to be arbitrary number bigger than zero.

Caution: STOP ORDERS are not supported.

Math derivation
^^^^^^^^^^^^^^^

We consider an execution of some limit order :math:`BBB \rightarrow AAA`, i.e. where BBB is the bid coin and AAA is the ask
coin. In effect of the execution, :math:`x:AAA` will be received from AMM and :math:`y:BBB` will be given to AMM. After
the execution, the new state of the AMM will be:

.. math::

    a-x: AAA, b+y: BBB

An order contains a declared limit price :math:`r`. The execution of an order is only allowed when :math:`ammprice \geq r`.

Additionally, we want to keep the constant conversion rate for every order and we want it to be equal to the declared
limit price. In other words we want the following condition to hold:

.. math::

    \frac{x}{y}=r

Let's assume that we have an order for which the condition :math:`ammprice \geq r` is true. We want to find the maximal
amount of swap which is possible.

For the maximal swap, the inequality will turn into equality, hence we will have:

.. math::

    ammprice = r

The ammprice after successful execution of the order will be:

.. math::

    ammprice = \frac{a-x}{b+y}

Effectively, we arrive to the following system of equations (where :math:`x` and :math:`y` are unknown):

.. math::

    \begin{cases}
    \dfrac{a-x}{b+y}=r\\
    \dfrac{x}{y}=r
    \end{cases}

Solving this leads to:

.. math::

    \begin{cases}
    x=\dfrac{a-br}{2}\\
    y=\dfrac{a-br}{2r}
    \end{cases}

1. Executor next decision
^^^^^^^^^^^^^^^^^^^^^^^^^

We check head positions of bids and asks half-markets to understand if they are possibly ready to execute next swap,
given the current AMM price value. Only-ask, only-bid and none-of-them are easy cases - we select the only side
which is possible. The only tricky case is when both head bid and head ask could be picked for execution in the next
step. In such case we pick the one with bigger overhang.

In case of a tie, we use a boolean variable ``flipper``, to pick one side, and then we negate ``flipper`` so that
in the case of next tie, the decision will be in favour of the other side.

.. code:: scala

  private var flipper: Boolean = false

  override def executorNextDecision(market: Market, newPositionThatTriggeredTheLoop: Position): Option[(MarketSide, OrderType)] = {
    if (market.limitOrderBookAsks.isEmpty && market.limitOrderBookBids.isEmpty)
      return None

    if (market.limitOrderBookBids.isEmpty)
      return Some((MarketSide.Asks, OrderType.Limit))

    if (market.limitOrderBookAsks.isEmpty)
      return Some((MarketSide.Bids, OrderType.Limit))

    val topBid: Fraction = market.limitOrderBookBids.head.normalizedLimitPrice
    val bottomAsk: Fraction = market.limitOrderBookAsks.head.normalizedLimitPrice
    val ammPrice: Fraction = market.currentPriceNormalized

    if (topBid <= ammPrice && ammPrice <= bottomAsk)
      return None

    if (bottomAsk < ammPrice && topBid <= ammPrice)
      return Some((MarketSide.Asks, OrderType.Limit))

    if (topBid > ammPrice && bottomAsk >= ammPrice)
      return Some((MarketSide.Bids, OrderType.Limit))

    val bidOverhang = topBid - ammPrice
    val askOverHang = ammPrice - bottomAsk

    if (bidOverhang > askOverHang)
      return Some((MarketSide.Bids, OrderType.Limit))

    if (bidOverhang < askOverHang)
      return Some((MarketSide.Asks, OrderType.Limit))

    //they are equal, so we pick one pointed by the flipper
    flipper = ! flipper
    flipper match {
      case true => return Some((MarketSide.Bids, OrderType.Limit))
      case false => return Some((MarketSide.Asks, OrderType.Limit))
    }
  }

2: Swap preconditions check
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Same as in TEAL variant, but without stop orders support.

.. code:: scala

  override def swapPreconditionsCheck(
                                       market: Market,
                                       halfMarketAB: HalfMarket,
                                       askCoin: Coin,
                                       bidCoin: Coin,
                                       position: Position,
                                       a: FPNumber,
                                       b: FPNumber,
                                       r: Fraction,
                                       ammPrice: Fraction): Decision =
    if (ammPrice > r)
      Decision.GREEN
    else
      Decision.RED

3: Calculate swap amounts
^^^^^^^^^^^^^^^^^^^^^^^^^

Following the math derivation above.

.. code:: scala

  override def calculateSwapAmounts(
                                     market: Market,
                                     halfMarketAB: HalfMarket,
                                     askCoin: Coin,
                                     bidCoin: Coin,
                                     position: Position,
                                     a: FPNumber,
                                     b: FPNumber,
                                     r: Fraction,
                                     ammPrice: Fraction): (FPNumber, FPNumber) = {

    val x: BigInt = r.numerator
    val y: BigInt = r.denominator
    val maxBidAmt: FPNumber = FPNumber((a.pips * y - b.pips * x) / (2 * x))
    val maxAmountOfBidCoinThatWillNotDrainAmmBelowMargin: FPNumber = (market.ammBalanceOf(askCoin) -  ammMinBalance) ** r.reciprocal
    val strikeBidAmt: FPNumber = FPNumber.min(FPNumber.min(position.outstandingAmount, maxBidAmt), maxAmountOfBidCoinThatWillNotDrainAmmBelowMargin)
    val strikeAskAmt: FPNumber = strikeBidAmt ** r
    return (strikeBidAmt, strikeAskAmt)
  }

Variant 3: UNISWAP_HYBRID executor
----------------------------------



