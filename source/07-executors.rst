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

**Rule #1: Equality of traders**
  This rule means that the exchange in not "biased" on trader's identity. Swaps sequence for a position depends only
  on the state od the exchange (i.e. does not depend on the identity of traders).

  In lame terms it means that all traders are considered "equal" by the executor - i.e. from the perspective of an
  executor, any trader is seen as "just an account number" (similar concept to "all citizens are considered equal by law
  in a democracy") and there is no extra bonus or preference in executing swaps based on account number.

**Rule #2: Funds locking**
  fsdsd


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


Executor loop overview
----------------------

In the current version of Dexter we further limit our attention to a most "simplistic" (implementation-wise) space of
executors. Namely, we expect these conditions to hold:

 4. **Funds locking** - sfsdf

Given these conditions, the job of executor loop can be pinpointed as the following task:

 1. Given the current state of

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

