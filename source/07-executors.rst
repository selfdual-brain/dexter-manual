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

Thanks to the rules enumerated in previous chapter, the job of an executor loop can be largely simplified and described
as follows:

 1. :math:`A` and :math:`B` are coins on the market under consideration. :math:`\langle A, B \rangle` is the market
    where the last new order was added.

 2. Following the cascade of swaps triggered by adding the new order, we already executed :math:`k` iterations of
    the executor loop, where :math:`k \geq 0`.

 3. Current AMM balances on the market :math:`\langle A, B \rangle` are :math:`\langle a:A, b:B \rangle`.

 4. We have 2 queues of limit orders on the market :math:`\langle A, B \rangle`:

      - orders with direction :math:`A \rightarrow B`
      - orders with direction: :math:`B \rightarrow A`

 5. Follow this sequence:

      - **[A]** Should we stop the stop the loop or continue ?
      - If continue: pick the queue
      - Let :math:`p` be the position at the head of picked queue
      - **[B]** Pick two numbers defining the swap to be made in the context of position :math:`p`: :math:`x` and :math:`y`,
        where :math:`x` will be the "sold" amount and :math:`y` will be the "bought" amount of the resulting swap.
      - create the swap

 6. Run another iterator of step 5.

Variants of executor implementation we discuss below are specified by providing the logic to be applied in steps
5.A and 5.B.

Variant 1: TEAL executor
------------------------

This executor is based on a proprietary algorithm created in Onomy Protocol.


Variant 2: TURQUOISE executor
-----------------------------

TURQUOISE executor does not support stop orders, hence the market state is composed of:

 - limit orders on the ASK side (sellers)
 - limit orders on the BIS side (buyers)
 - two liquidity pool balances (one balance for each coin)

Basic idea of the algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^




Mathematics
^^^^^^^^^^^

We will now derive the mathematical formulas to

The main idea of the algorithm is to execute every swap using the limit price declared in the order. This in contrary
to a FOREX-style exchanges, where every swap is executed using the current market price. While executing swaps this way,
the limiting factor is the "real" price, which we establish as :math:`\frac{a}{b}`, where :math:`A` and :math:`B`





Variant 3: UNISWAP_HYBRID executor
----------------------------------


f


Complications caused by finite precision
----------------------------------------

sfsdfs

