02. Technological context
=========================

In this chapter we do a short overview of relevant technologies - either used in the simulator or related to the
simulated solutions.

Blockchain
----------

A peer-2-peer network of computers materializing together an idea of consensus-based **virtual computer**. The consensus
protocol protect this virtual computer against hacking attacks (as opposed to physical computers that can always
be hacked).

The operations of this virtual computer are called **transactions**. The history of all transactions executed on the
blockchain virtual computer since its launch is what is called the "shared ledger". The ledger is typically partitioned
into **blocks**, hence it can be seen as a sequence of blocks.

Examples of (public) blockchains: Bitcoin, Ethereum, Cardano.

Cryptocurrency
--------------

The idea of money re-established on top of a blockchain.

Examples of cryptocurrencies: BTC,, ETH, DOT, USDC.


Decentralized exchange (DEX)
----------------------------

Know also as "DEX". This is just an exchange (i.e. a market) operating on a blockchain, where cryptocurrencies can
be traded.

Can be seen as blockchain-based analogy of Forex (however Forex is a relatively homogenous solution in terms of
orders execution mechanics, while every DEX may be based on a completely different algorithm).

A primordial example of a DEX is Uniswap: https://uniswap.org/


Discrete event simulation (DES)
-------------------------------

A method of building simulators centered around the priority queue of events. Every event has a timestamp and the queue
is ordered by these timestamps. Events are processed sequentially. Processing of an event E with timestamp T can produce
arbitrary number of new events with timestamps bigger or equal T. All these events are then enqueued to the central
events queue.

This technique effectively materializes "virtualization of time", i.e. allows accurate simulation of timing while
optimally utilizing resources of the computer running the simulation.

In lame terms, DES allows simulating months of operation of target system within couple of hours of your computer
(provided your computer is fast enough).

https://en.wikipedia.org/wiki/Discrete-event_simulation


Agent-based simulation
----------------------

A method of building DES simulators, where components of the simulated system are represented as message-passing entities.
This technique can be seen as a merger of actor model and DES.

https://en.wikipedia.org/wiki/Agent-based_model


JVM
---

Java Virtual Machine. This is the cornerstone of Java Platform.
Collection of programing languages compiled to JVM is quite large and includes (among others): Java, Groovy, Kotlin,
Scala, Clojure.

JVM languages usually allow interoperability with Java, which is considered the "root" language of JVM.

JAR is the packaging format on JVM. A library written for JVM is distributed as JAR file.

Anylogic
--------

A java-based development platform for building agent-based simulators.

https://www.anylogic.com/

