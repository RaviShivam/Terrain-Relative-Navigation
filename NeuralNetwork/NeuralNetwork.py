import numpy as np
import os, pickle

class Network:
    def __init__(self, neurons, alpha=0.1, beta=0.9, Lambda=0.001):
        self.neurons = neurons
        self.alpha = alpha
        self.beta = beta
        self.Lambda = Lambda
        self.layers = []
        self.out = [0] * (len(neurons) - 1)
        self.tresholds = []
        for i in range(len(neurons) - 1):
            self.layers.append(np.array(self.random_weights(neurons[i], neurons[i+1])))
            self.tresholds.append(np.array(self.random_tresholds(neurons[i+1])))

    def random_weights(self, r, c):
        return 0.5 * np.random.rand(r, c) - 0.25

    def random_tresholds(self, c):
        return 0.5 * np.random.rand(1, c) - 0.25

    def feed(self, values):
        self.out[0] = self.sigmoid(np.dot(values, self.layers[0]) - self.tresholds[0])
        for i in range(1, len(self.layers)):
            f = np.dot(self.out[i-1], self.layers[i]) - self.tresholds[i]
            self.out[i] = self.sigmoid(f)
        return self.out[-1]

    def train(self, values, target):
        self.feed(values)
        error = np.array(target) - np.array(self.out[-1])
        delta_k = self.train_output_layer(error)
        delta_k = self.train_hidden_layers(delta_k)
        self.train_first_layer(delta_k, values)

    def train_output_layer(self, error):
        dout = np.array(self.out[-1]) * np.array(1 - np.array(self.out[-1]))
        delta_k = dout * error
        deltaw = self.alpha * ((self.transpose(self.out[-2])).dot(delta_k))
        self.layers[-1] += deltaw
        self.tresholds[-1] += self.alpha * delta_k
        return delta_k

    def train_hidden_layers(self, delta_k):
        for i in range(len(self.layers)-2, 0, -1):
            delta_j = (self.layers[i+1].dot(self.transpose(delta_k))).T
            delta_j *= np.array(self.out[i]) * (1 - np.array(self.out[i]))
            deltaw = self.alpha * self.transpose(np.array(self.out[i-1])).dot(delta_j)
            self.layers[i] += deltaw
            self.tresholds[i] += self.alpha * delta_j
            delta_k = delta_j.copy()
        return delta_k

    def train_first_layer(self, delta_k, values):
        delta_j = (self.layers[1].dot(self.transpose(delta_k))).T
        delta_j *= np.array(self.out[0]) * (1 - np.array(self.out[0]))
        deltaw = self.alpha * self.transpose(np.array(values)).dot(delta_j)

    def transpose(self, m):
        return np.atleast_2d(m).T

    def classify(self, input):
        out = self.feed(input)
        i = reduce(lambda a, i: a if out[0][a] > out[0][i] else i, range(out.shape[1]))
        return i+1

    def sigmoid(self, m):
        return 1 / (1 + np.exp(-m))

    def save_network(self, dir):
        dir_path = os.path.join(os.curdir, "data", dir)

        layers_file = os.path.join(dir_path, "layers")
        layers_data = pickle.dumps(self.layers, protocol=0)
        f = open(layers_file, "wb")
        f.write(layers_data)
        f.close()

        biases_file = os.path.join(dir_path, "biases")
        biases_data = pickle.dumps(self.tresholds, protocol=0)
        f = open(biases_file, "wb")
        f.write(biases_data)
        f.close()

    def read_network(self, dir):
        f = open(os.path.join(os.curdir, "data", dir, "layers"), "rb")
        layers_data = f.read()
        self.layers = pickle.loads(layers_data)

        f = open(os.path.join(os.curdir, "data", dir, "biases"), "rb")
        biases_data = f.read()
        self.tresholds = pickle.loads(biases_data)