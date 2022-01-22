04. Model data types
====================

In this chapter we do an overview of data types used in the simulator. This is pretty technical but needed to properly
explain the data model underpinning Dexter. Skip this chapter (and following two chapters) if you are not interested
in that many technical details.

Basic java types
----------------

As Anylogic is based on Java, there are several data types we take as granted and we use them throughout this
documentation:

 - Int: the type of 32-bit signed integers
 - Long: the type of 64-bit signed integers
 - Boolean: the type of boolean values (true/false)
 - Double: the type of floating-point values

Amounts and prices
------------------

We follow the TLA+ spec in making arithmetic representation decisions:

 - fixed-point numbers are used for representing amounts of tokens (see ``FPNumber`` class)
 - fractions are used for representing prices (see ``Fraction`` class)

Time
----

There are two notions of time in use:

 - **simulation time**: this is the time simulated by Anylogic engine, following the DES model of events queue; timepoints
   are represented as Double values and are interpreted as seconds
 - **blockchain time**: this the blockchain-implementation-specific "internal" time of a blockchain, represented as
   Long value

Blockchains in general do not have the idea of "real" time - this is due to the very nature of what a blockchain is.
However every blockchain has some notion of "internal" time-like concept, which corresponds to the chronology of
transactions execution, namely the following invariant holds:

  if transaction :math:`t_1` can see transaction :math:`t_2` in its past, then :math:`bTime(t_1)>bTime(t_2)`

Hash
----

Hashes show up naturally as identifiers of transactions, coins and accounts. This is typically how identifiers
of various thing appear on a blockchain.

Internally, hash is just a binary array. We use ``Hash`` type to represent it. We frequently use the fact that hashes
have natural ordering (by lexicographic comparison).

Battery of counters
-------------------

This is a collection of FPNumber values indexed by some index type. In other words,
``BatteryOfCounters[T]`` is equivalent to ``Map[T,FPNumber]``, where ``T`` is the type of indexes.