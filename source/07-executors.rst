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

Common setup
------------

dsdadasd


Variant 1: TEAL executor
------------------------

This executor is based on a proprietary algorithm created in Onomy Protocol. The key idea of this


Variant 2: TURQUOISE executor
-----------------------------

TURQUOISE executor does not support stop orders, hence the market contains




Variant 3: UNISWAP_HYBRID executor
----------------------------------

