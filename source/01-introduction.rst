Introduction
============


Motivation
----------

Decentralized exchange (or "DEX" in short) is an exchange running on a blockchain. While DEXes are a hot topic over last
years, so far there is no well established "standard design" of a DEX. Rather, attempting various DEX designs happens to
be a field of active research around the world.

Onomy project is one of such attempts. Dexter was build as a research-level tool for supporting internal Onomy research.
The idea was to create a laboratory environment where several variants of DEX design can be tested.


Goals
-----

1. Implement a general framework for DEX designs.
2. Allow pluggable implementations of "executor" (the core part of DEX, where orders are executed).
3. Implement a behaviour of traders, so that the simulation will cover both DEX itself and the surrounding trading traffic.
4. Establish rich set of metrics, so that performance of different DEX variants can be comparatively measured.
5. Visualize a running DEX with rich collection of charts and stats, so that team members can get a better insight
   into the internals of DEX design.
6. Provide a command-line interface and a small scripting language, so that the simulator can be also used as
   a testing environment (where a collection of test cases written as scripts is maintained).
7. Simulate the blockchain layer - at least up to the point of having explicit control on network and consensus delays.

Key design decisions
--------------------

1. Use Anylogic as the main development platform.
2. Use agent-based simulation as the simulator construction paradigm.
3. Maintain a separate JVM-based library for data model and core business logic.
