07. Executors
=============

In this chapter we specify the algorithms of all executors currently supported in Dexter. The dynamic behaviour of these
algorithms and especially the comparative measurements of their statistics is the primary motivation behind creating
Dexter.

An executor can be seen as a manager of position's lifetime. More specifically, the goal of an executor is to
satisfy traders so that their orders are (eventually) filled. Because a filling can be partial, a lifetime of a position
can comprise several swaps. It is the executor who decides about the chronology of swaps to be performed.

Technically, an executor is a piece of software responsible for deciding what will be the next swap to execute.

Within the universe of possible executor algorithms, we distinguish a subset most interesting to us. We will say that
an executor is **fair-play** if the following conditions hold:

**Rule #1: Exchange in not biased on traders**

Swaps sequence for a position depends only on the market state and the position parameters. In particular, it does NOT
depend on any traders data.

In lame terms it means that all traders are considered "equal" by the executor - i.e. front the perspective of an executor
a trader is seen as "just an account number" (similar concept to "all citizens are considered equal by law in a democracy"),
and there is no extra bonus or preference in executing swaps based on account number.

**Rule #2: Higher limit price implies higher priority**

A trader ready to pay more is served first.

**Rule #3: Longer waiting implies higher priority**

In case of a tie in rule #3, a trader waiting longer is served first.

Notation
--------

This chapter is the only mathematically-involved part of Dexter documentation. We assume set theory (ZCF)
and basic mathematical notation (first-order logic). On top of this we borrow from TLA+ the syntax for records, i.e.:

 - :math:`[a -> 1, b -> true, c -> "snake"]` - this is a sample record
 - :math:`[a: String, b: Boolean, c: String]` - this is a set of records with given structure

We make a distinction between mathematical sets of numbers like :math:`\mathbb{N}`, :math:`\mathbb{R}` vs
implementation-level types like ``Int``, ``Double``.

Arithmetic precision
--------------------

In Dexter implementation we use ``FPNumber`` type for fixed-point numbers and ``Fraction`` for unlimited-precision
quotient numbers. ``FPNumber`` is mostly used for amounts of tokens, while ``Fraction`` is mostly used for prices.

From the point of view of mathematical derivations of executor algorithms, fixed point arithmetic introduces an extra
layer of complication. To keep the derivations easier, we introduce algorithms using unlimited precision of mathematical
real numbers. Then in the last sub-chapter we describe additional complications needed because of the implemented
arithmetic.

Mathematical framing
--------------------

We start with the following definitions:

 - :math:`Coins` - the (finite) set of coins
 - :math:`Orders = []`
 - 


----

Let :math:`A` and :math:`B` be coins on the market under consideration. Let :math:`a` and :math:`b` be the corresponding
balances of the liquidity pool. We can write this state concisely as:

.. math::

 <a:A, b:B>

We consider an order :math:`p` with direction :math:`B \rigtharrow A`, i.e. the trader wants to sell some amount
of tokens :math:`B` and receive corresponding amount of :math:`A`. Let :math:`amount` be the amount of :math:`B` tokens
declared in :math:`p`.

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~




Mathematics
~~~~~~~~~~~

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

