import numpy as np

# activation function: sigmoid
def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))

# input data, X
# player total, dealer upcard
X = np.array([[10,10],[20,5],[20,10],[5,5]])

# output data, Y
# stand/hit (0/1)
Y = np.array([[1],[0],[0],[1]])

layer3error = np.random.random_integers(1,1,Y.__len__())  # initialize array same size as Y, fill with 1's
for i in layer3error:
    while abs(layer3error[i]) > .5:  # if any error is greater than .5, re-initialize & re-train
        # initialize weights
        weight1 = np.random.random((2, Y.__len__()))  # (# of arrays, # of items in each array)
        weight2 = np.random.random((Y.__len__(), 1))  # try (2*random) - 1

        # train, use for loop 1000s of times.
        number_of_training_iterations = 50000
        for iteration in range(number_of_training_iterations):
            layer1 = X  # input
            layer2 = sigmoid(np.dot(layer1, weight1))  # multiply input by weight. if > than threshold, activate.
            layer3 = sigmoid(np.dot(layer2, weight2))  # layer2 * weight2

            # backpropagate
            layer3error = Y - layer3
            layer3change = layer3error * sigmoid(layer3, deriv=True)
            layer2error = layer3change.dot(weight2.T)  # layer3change * weight2
            layer2change = layer2error * sigmoid(layer2, deriv=True)

            # update weights
            weight2 += layer2.T.dot(layer3change)  # layer2 * layer3change
            weight1 += layer1.T.dot(layer2change)  # layer1 * layer2change

            if iteration%10000 == 0:
                print("Error: ", layer3error)

# prediction
p = np.array([15,7])
layer1p = p
layer2p = sigmoid(np.dot(layer1p, weight1))
layer3p = sigmoid(np.dot(layer2p, weight2))
print("Given: ", p)
print("Prediction: ", layer3p)