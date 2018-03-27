"""File used solely to test methods and data structures."""

import numpy as np
import random

X = np.array([[11,10], [20,5]])
Y = np.array([[1], [0]])
P = np.array([])

print("X: ", X)
print("Y: ", Y)
print("P: ", P)

Y = np.resize(Y, (Y.__len__() + 1, 1))
X = np.resize(X, (Y.__len__(), 2))
Y[Y.__len__() - 1] = [1]
X[Y.__len__() - 1] = [15,7]

print("After append")
print("X: ", X)
print("Y: ", Y)
print("P: ", P)

weight1 = np.random.random((2, Y.__len__()))
weight2 = np.random.random((Y.__len__(), 1))

print("W1: ", weight1)
print("W2: ", weight2)