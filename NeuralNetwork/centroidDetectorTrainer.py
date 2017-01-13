from NeuralNetwork import Network

network = Network([5,6,4,2],  alpha=0.1, beta=0.1, Lambda=0.9)
intrainingdata = map(lambda line: map(int, line.split()), open('training/centroidin', 'r'))
outtrainingdata = map(lambda line: map(int, line.split()), open('training/centroidout', 'r'))
map(lambda i: i.append(i[0]*i[0]), intrainingdata)
map(lambda i: i.append(i[1]*i[1]), intrainingdata)
# map(lambda i: i.append(i[0]*i[1]), intrainingdata)
outmax = max(max(outtrainingdata))
normaloutdata = []
map(lambda x: normaloutdata.append(map(lambda j: float(j)/float(outmax), x)), outtrainingdata)
for it in range(0,20000):
    for i in range(0,len(intrainingdata)):
        network.train(intrainingdata[i], normaloutdata[i])

# network.save_network(dir="neural_network_configuration")

network.read_network(dir="neural_network_configuration")

print network.feed(intrainingdata[1])*57