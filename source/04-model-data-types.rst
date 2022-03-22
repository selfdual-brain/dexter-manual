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

Fixed-point arithmetic
^^^^^^^^^^^^^^^^^^^^^^

``FPNumber`` implements fixed-point arithmetic. The decimal precision (i.e. number of places after decimal point)
is statically configured via constant ``io.onomy.commons.FIXED_POINT_ARITHMETIC_PRECISION: Int``.
This class is tailored to represent "money" values, i.e. it works mostly like integers. There are some cases when
rounding occurs (these places are marked below).

The signature of ``FPNumber`` class is as follows:

.. code:: scala

case class FPNumber(pips: BigInt) extends Ordered[FPNumber] {

  /** Sum of two numbers.*/
  def +(amount: FPNumber): FPNumber

  /** Difference of two numbers.*/
  def -(amount: FPNumber): FPNumber

  /** x ---> -x */
  def negated: FPNumber

  /** Returns -1 for negative values, 1 for positive values, 0 for zero.*/
  def signum: Int

  /**
   * Shifts the decimal point given number of places (left or right).
   * @param p number of decimal places (positive = shift right, negative = shift left)
   */
  def decimalShift(p: Int): FPNumber

  /**
   * Fixed-point multiplication.
   * Caution: rounding can occur here.
   */
  def *(other: FPNumber): FPNumber

  /**
   * Fixed-point division.
   * Caution: rounding can occur here.
   */
  def /(other: FPNumber): FPNumber

  /** x ---> 1/x */
  def reciprocal: FPNumber

  /**
  * Multiplication by a fraction.
  * Caution: rounding can occur here.
  */
  def **(fraction: Fraction): FPNumber

  /**
   * Conversion to floating-point arithmetic.
   * Caution: this is precision-losing operation.
   */
  def toDouble: Double

  /**
   * Conversion to Fraction.
   * This is a precise conversion, as Fraction has unlimited precision.
   */
  def toFraction: Fraction

  /** Rounding towards positive infinity.*/
  def ceiling: BigInt

  /** Rounding towards negative infinity. */
  def floor: BigInt

  /** Returns fractional part of the value, ignoring sign.*/
  def unsignedFractionalPart: FPNumber

  /**
   * Rounding towards zero.
   * This is just cutting away the fractional part of this value.
   */
  def roundTowardsZero: BigInt

  /** Rounding away from zero.*/
  def roundAwayFromZero: BigInt

  /** Mathematical ordering.*/
  override def compare(that: FPNumber): Int

  /** Standard distance between numbers.*/
  def distanceTo(that: FPNumber): FPNumber
}

Additionally, there are some class-level functions associated with ``FPNumber``:

.. code:: scala

  private def power(n: Long, k: Int): BigInt = {
    val b: BigInt = BigInt(n)
    (1 to k).map(x => b).product
  }

  val SCALING_FACTOR: BigInt = power(10, FIXED_POINT_ARITHMETIC_PRECISION)
  val SCALING_FACTOR_BIG_DECIMAL: BigDecimal = BigDecimal(SCALING_FACTOR)
  val SCALING_FACTOR_DOUBLE: Double = SCALING_FACTOR.toDouble

  val fractionalPartPaddingString: String = "0" * FIXED_POINT_ARITHMETIC_PRECISION

  val zero: FPNumber = FPNumber(0)
  val half: FPNumber = FPNumber(SCALING_FACTOR / 2)
  val one: FPNumber = FPNumber(SCALING_FACTOR)


  def parse(s: String): FPNumber = fromBigDecimal(BigDecimal(s))

  /**
   * Conversion Long ---> CoinAmount.
   * For example, when precision is set to 5:
   * fromLong(123).toString == "123.00000"
   */
  def fromLong(n: Long): FPNumber = FPNumber(n * SCALING_FACTOR)

  def fromBigDecimal(x: BigDecimal): FPNumber = new FPNumber((x * SCALING_FACTOR_BIG_DECIMAL).toBigInt)

  /**
   * Conversion Double ---> CoinAmount.
   */
  def fromDouble(a: Double): FPNumber = FPNumber((a * SCALING_FACTOR_DOUBLE).round)

  def fromDoubleRoundingDown(a: Double): FPNumber = FPNumber((a * SCALING_FACTOR_DOUBLE).floor.toLong)

  def fromDoubleRoundingUp(a: Double): FPNumber = FPNumber((a * SCALING_FACTOR_DOUBLE).ceil.toLong)

  def fromFraction(f: Fraction): FPNumber = FPNumber(f.numerator) / FPNumber(f.denominator)

  def min(a: FPNumber, b: FPNumber): FPNumber = if (a < b) a else b

  def max(a: FPNumber, b: FPNumber): FPNumber = if (a > b) a else b

  def abs(a: FPNumber): FPNumber = if (a >= FPNumber.zero) a else a.negated

  /**
   * Smallest value that could be represented with FPNumber, given the configured arithmetic precision
   */
  val quantum: FPNumber = FPNumber.one.decimalShift(- FIXED_POINT_ARITHMETIC_PRECISION)




Fractions
^^^^^^^^^



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

Caution: when running Dexter in command-line mode (see chapter 15), there is no proper simulation of time in place,
hence the simulation clock is mocked. Therefore time-related statistics are meaningless in command-line.

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