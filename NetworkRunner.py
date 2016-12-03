def train(self):
    c = 0
    total_size = len(self.training_data)
    for (image, result) in self.training_data:
        self.update_progress(float(c), total_size)
        self.network.train(image, result)
        c += 1
    self.update_progress(1.0, 1)


def validate(self):
    c = 0
    total_size = len(self.validation_data)
    for (image, result) in self.validation_data:
        self.update_progress(float(c), total_size)
        self.network.train(image, result)
        c += 1
    self.update_progress(1.0, 1)


def test_network(self):
    c = 1
    s = 0
    total_size = len(self.test_data)
    for (image, result) in self.test_data:
        self.update_progress(float(c), total_size)
        res = self.network.classify(image) - 1
        # print "Predicted: {}".format(res)
        # self.plot_mnist_digit(image)
        # print "Actual: {}".format(result)
        if (result == res):
            s += 1
            # print "Out: {}".format(self.network.feed(image))
            # print result
            # print res
        c += 1
    # self.update_progress(1, 1)
    print "Succes     : {}".format(s)
    print "Succes rate: {:.2f}".format(float(s) / total_size * 100)