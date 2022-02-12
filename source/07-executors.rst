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

 - :math:`[a \mapsto 1, b \mapsto true, c \mapsto "snake"]` - this is a sample record
 - :math:`[a: String, b: Boolean, c: String]` - this is a set of records with given structure
 - :math:`e.h` - the :math:`h` field of record :math:`e`

We explicitly mark introduction of new symbols by using symbol :math:`triangleq` at the beginning:

:math:`a \triangleq 2`

In such case equality sign is just the market of where the definition begins.

We use :math:`where` keyword as a syntax sugar for subset selection in definitions. This:

:math:`A \triangleq SomePossiblyLongSetDefinition \ where \forall{x in SomeSet} SomeCondition(x)`

is supposed to mean:

:math:`A \triangleq \{x \in SomePossiblyLongSetDefinition: SomeCondition(x)\}`

We also borrow TLA+ syntax for function spaces and we write :math:`[S \rightarrow T]` instead of more traditional
:math:`T^S`.

We make a distinction between mathematical sets of numbers like :math:`\mathbb{N}`, :math:`\mathbb{R}` vs
implementation-level types like ``Int``, ``Double``.

Additionally:

 - :math:`P(A)` is the powerset of :math:`A`
 - :math:`\mathbb{R}_+` is the set of positive real numbers
 - :math:`Time` is just alias for :math:`\mathbb{R}_+ \cup \{ 0 \}`
 - :math:`Amount` is just alias for :math:`\mathbb{R}_+ \cup \{ 0 \}`
 - :math:`Price` is just alias for :math:`\mathbb{R}_+ \cup \{ 0 \}`

Arithmetic precision
--------------------

In Dexter implementation we use ``FPNumber`` type for fixed-point numbers and ``Fraction`` for unlimited-precision
quotient numbers. ``FPNumber`` is mostly used for amounts of tokens, while ``Fraction`` is mostly used for prices.

We specify executors using real numbers, so withing the idealized formal arithmetic provided by pure math. Fixed-point
arithmetic adds an extra layer of complexity that could obscure the mathematical clarity of ideas, so we describe
this layer separately.

Mathematical framing
--------------------

For specifying executors, we re-establish here the DEX model again - but this time using mathematical formalism. Because
all we need is to specify execution of orders, we ignore reserve operations (deposit/withdraw) and liquidity management
(add-liquidity/withdraw-liquidity). We also get rid of identifiers and hashes (mathematical identity does the job).

To bootstrap things we need the following definitions:

Coins
^^^^^

We assume :math:`Coin` is some given fixed set of coins. This is just an arbitrary non-empty finite set.

Caution: Please note the naming convention here is borrowed from programming, where the singular form of nouns is used
as a type name. We consider sets in ZFC as something conceptually corresponding to types in programming.

Accounts
^^^^^^^^

We assume :math:`Account` is some given set of trader accounts. This is just an arbitrary non-empty set and we need it to
represent the identity of traders.

We also need a trader state, which simply tracks the trader's balance for every coin:

:math:`AccountState \triangleq [Coin \rightarrow Amount]`

Coin pairs
^^^^^^^^^^

Similarly to the implementation layer, we need both ordered and unordered pairs of coins. Unordered pairs play the role
of market identifiers, while ordered pairs are needed to identify trading direction.

Unordered pairs can be just represented as 2-element sets of coins:

:math:`CoinPair \triangleq \{p \in P(Coin): a \neq b \}`

Ordered pairs can be found as a subset of the cartesian product:

:math:`Direction \triangleq \{ <a,b> \in Coin \times Coin: a \neq b \}`

Every direction can be converted to coin pair with the following function:

:math:`toPair: Direction \rightarrow CoinPair:`

:math:`toPair(<a,b>) \triangleq {a,b}`

Limit orders and Positions
^^^^^^^^^^^^^^^^^^^^^^^^^^

We materialize orders as records.

:math:`LimitOrder \triangleq [account: Account, direction: Direction, price: Price, amount: Amount, expTime: Time]`

For positions, we really only need to track the amount of tokens sold. Please notice that contrary to the implementation
model, we are inside of pure math here so everything is immutable by nature:

:math:`Position \triangleq [order: LimitOrder, creationTime: BTime, soldSoFar: Amount]`

DEX state
^^^^^^^^^

Market state is composed of market id, AMM balance and a collection of positions, plus we need to make sure that
positions are coherent with market id

.. math::

  let MarketState = [marketId: CoinPair, ammBalance: [marketId \rightarrow Amount], positions: P(Position)]
  where \forall{s \in MarketState} \forall{p \in s.positions} toPair(p.order.direction) = s.marketId

Then the whole DEX state is composed of account states and markets:

.. math::

  let DexState = [accounts: [Account \rightarrow AccountState], markets: CoinPair \rightarrow MarketState]
  where \forall{s \in DexState} \forall{p \in CoinPair} s.markets(p).marketId = p

Executors and swaps
^^^^^^^^^^^^^^^^^^^

At the most general level an executor is a machinery to transform DEX states on new order arrival:

:math:`Executor \triangleq [MarketState \times Order \rightarrow MarketState]`

However in the current version of Dexter we limit our attention to a narrow sub-family of executors that can be
defined via swaps. A **swap** is an "atomic" conversion of tokens done via AMM on behalf of a specified order:

:math:`Swap \triangleq [order: Order, amountSold: Amount, amountBought: Amount]`

We think of a swap as a trade done against the liquidity pool where only one order is involved. This is in contrary to
Forex-style exchanges, where an atomic trading action involves always 2 orders.

Given a swap :math:`swap \in Swap` and a Dex s, we

Swap-based executor is defined by providing a sequence of swaps upon new order arrival:

:math:`SwapBasedExecutor \triangleq [MarketState \times Order \rightarrow MarketState]`


:math:`Swap = []`

Executor
^^^^^^^^

Now we are reade to express the concept of an executor. this is just any recipe for evolving DEX state after a new order
arrived:

:math:`Executor = \{ex \in [MarketState \times Order \rightarrow MarketState]\}`

Fair-play conditions
^^^^^^^^^^^^^^^^^^^^

As an example of th formal setup, we will formalize the fair-play conditions introduced in the beginning of this chapter.

Let :math:`ex \ Executor` be the executor in question.

**Rule #1**

.. math::

  \forall{p \in Perm(Account)}{}




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

