07. Executors
=============

The executor runs the lifetimes of positions. It also executes all swaps. The general goal of an executors is to
satisfy traders so that their orders are filled. Ideally, an solid executor implementation should serve traders so that
the following desirable properties hold:

  **equality of traders** -
  **transparent yield** -
 - **supply/demand coherent** -
 - **quick convergence** -
 - **stable price** -
 - **short filling delay** -
 - **small average overhang** -
 - **resistance to extremes** -

In this chapter we specify the algorithms of all executors currently supported in Dexter. The dynamic behaviour of these
algorithms and especially the comparative measurements of their statistics is the primary goal of Dexter.

Teal executor
-------------

This executor is based on a proprietary algorithm created in Onomy Protocol. The key idea of this


Turquoise executor
------------------




Uniswap Hybrid executor
-----------------------

