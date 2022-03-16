07. Executors
=============

As a DEX operates on top of a blockchain, it follows the basic principle of blockchains: there is a decentralized
ledger of transactions which validators are building. So, one can see a DEX as an evolving state of a sequential
computer.

As was explained in chapter 6, we fixed a certain set of transaction types and we fixed their semantics for all but one.
The single exceptional case being ``add-order`` transaction. On the technical level, a single ``add-order`` execution
must be resolved to a sequence of swaps. This is the job of an **executor**. We consider an executor to be pluggable
part of DEX implementation.

In this chapter we specify the algorithms of all executors currently supported in Dexter. The dynamic behaviour of these
algorithms and especially the comparative measurements of their statistics is the primary motivation behind creating
Dexter.

Space of executors research
---------------------------

In the current version of Dexter we limit our attention to certain natural space of most simplistic executors. Our
limiting conditions are:

**Rule #1: Equality of traders**
  Swaps chronology can depend only on the state of markets (i.e. it is not allowed that it depends on the state of
  traders).

  This rule means that the exchange in not "biased" on trader's identity or other trader properties (such as wealth
  for example).
  In lame terms it means that all traders are considered "equally important" by the executor - i.e. from the perspective
  of an executor, any trader is seen as "just an account number" (similar concept to "all citizens are considered equal
  by law in a democracy"). Current balance of trader's account, past history of trading operations and trader's name
  - all this cannot influence the path of DEX evolution that an executor is creating.

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
so the market is :math:`AAA \rightarrow BBB` and orders have direction :math:`AAA \rightarrow BBB` or
:math:`BBB \rightarrow AAA`. We will further refer to this market as ``market`` (see the scripts below).

Thanks to the rules enumerated in previous chapter, the job of an executor loop can be largely simplified. Let us
outline the template of such loop by extending the activity diagram in from previous chapter:

.. image:: pictures/07/executor-loop.png
    :width: 100%
    :align: center

Places marked above with red asterisk are where non-trivial logic must be plugged-in:

**1: Half-market selection**
  At this point, one of two half-markets must be picked. This is equivalent to selecting a direction: :math:`AAA \rightarrow BBB`
  or :math:`BBB \rightarrow AAA`. In the context of "oriented" market, this means selecting "asks" or "bids" side
  of the order book.

**2: Swap preconditions**
  At this point swap preconditions are checked. Red light will abort swap creation and terminate the executor loop.

**3: Swap amounts**
  Deciding on amounts of the next swap to be executed. Because of **Rule #5: Natural trading priority**, the next swap
  to be executed must relate to the position at the head of the positions list (because the positions list is ordered
  by price-then-order-time.

**4: Executor loop termination**
  Deciding if the executor loop should continue or exit.

In the algorithms of the executor loop we outline below, ``pos`` is the just-added position. We follow attributes
and methods as defined in the UML model.

Variant 1: TEAL executor
------------------------

This executor is based on a proprietary algorithm created in Onomy Protocol. This executor follows this TLA+
specification:

https://github.com/onomyprotocol/specs/

1. Half-market selection
^^^^^^^^^^^^^^^^^^^^^^^^

We select the same half-market where ``pos`` belongs:

.. code:: scala

  val selectedHalfMarket = pos.halfMarket

2: Swap preconditions
^^^^^^^^^^^^^^^^^^^^^

.. code:: scala

    val limitHead: Position = selectedHalfMarket.limitBook.head
    val r: Fraction = limitHead.exchangeRate
    val a: FPNumber = market.ammBalanceOf(limitHead.order.askCoin)
    val b: FPNumber = market.ammBalanceOf(limitHead.order.bidCoin)
    val ammPrice: Fraction = Fraction(a, b)

    if (ammPrice <= r)
      return RED_LIGHT
    else {
      val maxBidAmt: FPNumber = (a - b * r) * ((r + 1).reciprocal)
      val strikeBidAmt: FPNumber = FPNumber.min(limitHead.outstandingAmount, maxBidAmt)
      val strikeAskAmt: FPNumber = strikeBidAmt * r
      if (strikeBidAmt > 0 && strikeAskAmt > 0)
        return GREEN_LIGHT
      else
        return RED_LIGHT
    }

3: Swap amounts
^^^^^^^^^^^^^^^

.. code:: scala

    val limitHead: Position = selectedHalfMarket.limitBook.head
    val r: Fraction = limitHead.exchangeRate
    val a: FPNumber = market.ammBalanceOf(limitHead.order.askCoin)
    val b: FPNumber = market.ammBalanceOf(limitHead.order.bidCoin)
    val ammPrice: Fraction = Fraction(a, b)
    val maxBidAmt: FPNumber = (a - b * r) * ((r + 1).reciprocal)
    val x: FPNumber = FPNumber.min(limitHead.outstandingAmount, maxBidAmt)
    val y: FPNumber = x * r

4: Executor loop termination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We terminate unconditionally. This means that the executor loop has always only one iteration.


Variant 2: TURQUOISE executor
-----------------------------

This executor is based on an idea that we execute orders always using the limit price as declared in the order itself.

1. Half-market selection
^^^^^^^^^^^^^^^^^^^^^^^^

We select the same half-market where ``p`` belongs:

.. code:: text

  val selectedHalfMarket = p.halfMarket


2: Swap amounts
^^^^^^^^^^^^^^^


3: Executor loop termination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We terminate unconditionally. This means that the executor loop has always only one iteration.


Variant 3: UNISWAP_HYBRID executor
----------------------------------




Complications caused by finite precision
----------------------------------------

sfsdfs

