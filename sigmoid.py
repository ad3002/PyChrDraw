# -*- coding: utf-8 -*-
#
#@created: 17.10.2013
#@author: Gaik Tamazian
#@contact: gaik.tamazian@gmail.com

from math import sqrt, pow


def sigmoid(x, a):
    """Implements a sigmoid function which maps real numbers to the interval
    from -1 to 1.

    @param x: a real number
    @param a: the function steepness parameter
    @type x: float
    @type a: float
    @return: the transformed value
    @rtype: float
    """

    return (a*x)/sqrt(1 + pow(a, 2)*pow(x, 2))


def estimate_sigmoid_parameter(xmax, epsilon=0.05):
    """Given the maximum value which must be discernible and the
    discenibility threshold, return an estimate for the sigmoid function
    parameter.

    @param xmax: the greatest value to be discenrible among lesser values
    @param epsilon: the discernibility threshold (a small positive value)
    @type xmax: float
    @type epsilon: float
    @return: a sigmoid parameter estimate
    @rtype: float
    """

    return sqrt((pow(epsilon, -2./3) - 1)/pow(xmax, 2))
