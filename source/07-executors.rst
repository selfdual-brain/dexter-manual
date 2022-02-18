07. Executors
=============

In this chapter we specify the algorithms of all executors currently supported in Dexter. The dynamic behaviour of these
algorithms and especially the comparative measurements of their statistics is the primary motivation behind creating
Dexter.

An executor can be seen as a manager of position's lifetime. More specifically, the goal of an executor is to
satisfy traders so that their orders are (eventually) filled. Because a filling can be partial, the lifetime of
a position can comprise several swaps. It is the executor who decides about the chronology of swaps to be performed.

Space of executors research
---------------------------

In the current version of Dexter we limit our attention to certain natural space of most simplistic executors. Our
limiting conditions are as follows:

**Rule #1: Funds locking**
  Trader can place an order on the DEX only if the balance of tokens to be sold is covered by trader's account. Upon
  placing an order, the executor will "lock" the tokens to be sold. Locked tokens cannot be reused in another order.
  Locked tokens get unlock on order expiration or cancellation.

**Rule #2: Equality of traders**
  Swaps sequence for a position can depend only on the state of markets (i.e. it is not allowed that it depends on the
  state of traders).

  This rule means that the exchange in not "biased" on trader's identity or wealth. In lame terms it means that all
  traders are considered "equally important" by the executor - i.e. from the perspective of an executor, any trader is
  seen as "just an account number" (similar concept to "all citizens are considered equal by law in a democracy").
  Current balance of trader's account, past history of trading operations a trader did or a trader name - all this
  cannot influence the operations of the executor.

**Rule #3: Natural trading priority**
  Execution prioritizes a trader happy to accept less attractive exchange rate (i.e. an exchange rate that gives him
  less profit). In case of a tie, a trader waiting longer is served first.

**Rule #4: Isolation of markets**
  Arrival of a new order generates swaps only on the market where this order belongs to.

**Rule #5: Isolation of traders**
  Every swap involves only one order.

**Rule #6: Isolation of swaps**
  An executor makes next-swap decision based only on the current state of the market and number of swaps executed in
  the current executor loop. The intention here is that the executor is not allowed to decide based on the history of
  executes swaps.

Motivation for above rules comes from various sources:

  - Rules #2 and #3 seem to be very natual and go along the general expectations of the wide public; any DEX violating
    these rules would be really a weird one.
  - Rule #1 is a completely arbitrary business-level decision made in Onomy; DEXes violating this rule are probably
    quite useful and interesting, although it must be said that their trading mechanics would be even more distant
    from Forex tradition than the mechanics of those following #1. Therefore the motivation behind #1 can be seen as
    "let's keep things mentally closer to Forex community for now" (please notice that Dexter is all about simulating
    hybrid exchanges, so the analogy to Forex is going to be always around).
  - Rules #4, #5, #6 delineate the boundary of "simplest executors one can consider"; anything beyond this region
    immediately becomes complex and sophisticated. From this perspective the mission of Dexter can be understood as
    "let's see how far we can get with those simplistic executors before we delve into sophisticated ones". A good
    motivation for cancelling #4 would be making a DEX where arbitrage is impossible. A good motivation for cancelling
    #5 would be borrowing from Forex the idea of direct trader-to-trader swaps, i.e. bypassing the AMM interaction
    when possible.

Executor loop overview
----------------------

Thanks to the rules enumerated in previous chapter, the job of an executor loop can be largely simplified and pinpointed
as the following task:

 1. :math:`A` and :math:`B` are coins on the market under consideration. :math:`\langle A, B \rangle` is the market
    where the last new order was added.
 2. Following the cascade of swaps triggered by adding the new order, we already executed :math:`k` iterations of
    the executor loop, where :math:`k \geq 0`.
 3. Current AMM balances on the market :math:`\langle A, B \rangle` are :math:`\langle a:A, b:B \rangle`.
 4. We have 2 queues of limit orders on the market :math:`\langle A, B \rangle`:
      - direction :math:`A \rigtharrow B`
      - direction: :math:`B \rigtharrow A`


Common notation
---------------

While defining various executors we will share the same notation:

 - :math:`A` and :math:`B` are coins on the market under consideration
 - :math:`a` and :math:`b` are the corresponding balances of :math:`A` and :math:`B` in the liquidity pool We will write
   this state concisely as:

.. math::

 <a:A, b:B>

We consider arrival of an order :math:`p` with direction :math:`B \rigtharrow A`, i.e. the trader wants to sell some
amount of tokens :math:`B` and receive corresponding amount of tokens :math:`A`. Let :math:`amount` be the amount of
:math:`B` tokens declared in :math:`p`.

We will consider execution of a single swap :math:`s=<y:B \rightarrow x:A>`, i.e. :math:`y` is the amount of :math:`B`
tokens the trader sold and :math:`x` is the amount of :math:`A` tokens the trader obtained in reply. This swap is
supposed to be a (possibly partial) execution of :math:`p`.

To simplify the mathematics we will NOT use the normalized view of the market. Rather, we will use the direction-based
view, so the limit price :math:`e` declared in :math:`p` is interpreted as the following condition imposed by the trader:

.. math::

 \frac{x}{y} >= e

Because we do not use the normalized view, the concept of "current price on the market" (or just **ammPrice** in short)
depends on order's direction. For :math:`p` the direction is :math:`B \rigtharrow A` and the current price on the
market (with direction :math:`B \rigtharrow A`) is defined as:

.. math::

 ammPrice_{B \rigtharrow A} = \frac{a}{b}

After the execution of swap :math:`p` the state of the liquidity pool will change to:

 <a-x: A, b+y:B>

Hence, after the execution of :math:`s`, the directed ammPrice will change to: \frac{a}{b}


Variant 1: TEAL executor
------------------------

This executor is based on a proprietary algorithm created in Onomy Protocol. The key idea of this


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

