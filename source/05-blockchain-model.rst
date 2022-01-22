05. Blockchain model
====================

A DEX - as being deployed on a blockchain - has 4 conceptual "perspectives":

 1. End-user perspective: this covers the view of an end-user, so how the usage of the DEX looks like in practice; this
    would normally coincide with the GUI of the DEX client.
 2. Client-api perspective: this covers the view of a client-developer; is is composed of APIs available to the DEX client
    software; this APIs may communicate to on-chain and off-chain components
 3. Blockchain perspective: this covers the view of a DEX developer and includes all the blockchain-specific solutions.
    used to implement the DEX.
 4. Internal DEX model perspective: this covers the internal working of a DEX, abstracting away from design choices specific
    to a given blockchain where the DEX will be deployed; in the implementation phase this model would typically be
    mapped to a smart-contract.

Here we focus on the the way we mock blockchain architecture in the simulator. This covers perspectives (2) and (3).

Real blockchain vs blockchain mock
----------------------------------

A real blockchain is a P2P network of nodes (validators) building blocks and collectively running a consensus protocol
to come up with ever-growing sequence of blocks. The goal of underlying consensus protocol is to ensure that the
sequence of blocks - once established up to position N - is visible to every node as such (i.e. is "finalized") and
the sequence can never be changed.

Surrounding the network of validators is the (usually much larger) network of blockchain clients. Every blockchain
client picks (arbitrarily) some validator and uses it as a gateway to the blockchain. In theory this selection should
not influence the operation of a client, because all validators offer semantically equivalent API for clients.

.. image:: pictures/06/real-blockchain-network.png
    :width: 100%
    :align: center

For the purpose of DEX simulation we do not simulate the actual network of validators. Instead we just have a single
agent representing the blockchain, while clients are also represented as agents, and the communication between
agents and the blockchain is materialized as agent-to-agent message passing.

.. image:: pictures/06/mocked-blockchain-network.png
    :width: 100%
    :align: center

Caution: there are some additional agents involved in the design so to accommodate the simulation of Internet. Go to
chapter 10 for more details on this.


Blockchain accounts
-------------------

sfsd

Client-Blockchain communication protocol
----------------------------------------

vdvd

Transaction types
-----------------


fsdf

Queries types
-------------

sfsd

