06. DEX model
=============

There is a general model of a DEX (derived from the TLA+ spec we mentioned before) which sits at the conceptual center
of Dexter design. Only one part of this model - the executor - is pluggable, so that comparative simulation of various
executors ca nbe achieved.

In this chapter we describe this common base model, while the next chapter is devoted to the various executors
pre-installed in the current version of Dexter.

This chapter covers perspective (4) according to the list of perspectives explained in chapter 5.

This UML diagram covers the whole model:

.. image:: pictures/06/dex-uml-model.png
    :width: 100%
    :align: center

Coins and tokens
----------------

We use the term **coin** meaning "type of cryptocurrency". For example, in our lingo, BTC and ETH are coins. On the
other hand, we use the term **token** when we talk about amounts of coins. In practice: when I sell 1.305
bitcoins, we say that the the coin of that transaction is "bitcoin" and the number of tokens transferred is 1.305.

Coins are represented with ``Coin`` type, while token amounts are represented with ``FPNumber`` type.

We frequently need to talk about pairs of coins. When ``AAA`` and ``BBB`` are some coins, we want to be able to form
the pairs ``(AAA,BBB)`` and ``(BBB,AAA)``. This concept is represented with ``CoinPair`` type.

We also sometimes need 2-element coin sets. This is different than a coin pair, because a pair is ordered, while a set is
not. However, to keep things simpler, we represent a 2-element coin set as a **normalized coin pair**. This normalization
works as follows: because every coin has an id (hash), we consider a CoinPair to be **normalized** if coins in this
pair are ordered along their hashes.

**Example**

With number of coins configured to 7, at the beginning of the simulation the following information will show up in the
console:

|coins in use:
|  code=AAA id=ee93-992a-dbdd-6168 description=Sample coin AAA
|  code=BBB id=9853-0e3b-6c5e-fd60 description=Sample coin BBB
|  code=CCC id=aea4-0d22-8e88-7e5b description=Sample coin CCC
|  code=DDD id=ba32-7373-3682-7484 description=Sample coin DDD
|  code=EEE id=e999-5a44-0ea6-4d46 description=Sample coin EEE
|  code=FFF id=1531-f159-e87b-6776 description=Sample coin FFF
|  code=GGG id=a8f4-8174-5e0a-3c25 description=Sample coin GGG

These are automatically generated coins. For coins AAA and BBB, two coin pairs are possible: ``CoinPair(AAA,BBB)`` and
``CoinPair(BBB,AAA)``. Now let us look at the hashes. A hash is printed using hex encoding of corresponding byte array
and the comparison of hashes is lexicographic-per-byte. First byte of coin AAA identifier is ``ee`` in hex, which is
number 238. First byte of coin BBB identifier is ``98`` in hex, which is number 152. Hence, BBB has smaller hash than
AAA so we can conclude that ``CoinPair(BBB,AAA)`` is the normalized and ``CoinPair(AAA, BBB)`` is normalized.

DEX core
--------

sfsd

Trader accounts
---------------

We assume trader account is just the same as blockchain account. DEX becomes aware of a trader account while executing
first **deposit** operation for this account.

An account stores the following information:

 - current balance of tokens (per each coin)
 - current free balance of tokens (per each coin)
 - current balance of liquidity tokens (per market)
 - opened positions

Reserve
-------

Reserve is the way we represent total tokens supply (per coin). Money


Markets
-------
fsdf


AMM
---


Orders
------

sfsd

Market orientation
------------------

sdf

Liquidity providers
-------------------

fsfs

Representation of an order book
-------------------------------
sfsd


Data stored in a trader account
-------------------------------
sfsd


Execution of orders
-------------------







