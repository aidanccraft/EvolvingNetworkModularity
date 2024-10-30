import itertools


def toposortVisit(graph, u, color, toposort):
    color[u] = 'g'

    for v in graph[u]:
        if color[v] == 'w':
            toposort = toposortVisit(graph, v, color, toposort)
            if not toposort:
                return False
        elif color[v] == 'g':
            return False

    color[u] = 'b'
    toposort.append(u)
    return toposort


def toposortGraph(graph):
    toposort = []
    color = {}
    for u in graph.keys():
        color[u] = 'w'

    for u in graph.keys():
        if color[u] == 'w':
            toposort = toposortVisit(graph, u, color, toposort)
            if not toposort:
                return False

    return toposort


def reverseGraph(graphReverse):
    graph = {}

    for u, neighbors in graphReverse.items():
        for v in neighbors:
            if v in graph:
                graph[v].append(u)
            else:
                graph[v] = [u]

            if not u in graph:
                graph[u] = []

    return graph


def createGraph(genome, n, numInputs, connectionSize):
    graphReverse = {}
    numNand = 0

    for i in range(n):
        pointer = i * (connectionSize * 2 + 2)

        gate = genome[pointer] * 2 + genome[pointer+1]
        connection1 = 0
        connection2 = 0

        for j in genome[pointer+2:pointer+2+connectionSize]:
            connection1 = 2 * connection1 + j

        for j in genome[pointer+2+connectionSize:pointer+2+2*connectionSize]:
            connection2 = 2 * connection2 + j

        if gate != 3:
            graphReverse[i+numInputs] = [connection1, connection2]
            numNand += 1

    output = 0
    for j in genome[-connectionSize:]:
        output = 2 * output + j
    graphReverse[n+numInputs] = [output]

    return numNand, graphReverse


def evaluateCircuit(graphReverse, n, toposort, inputs):
    circuit = {}

    for i in range(len(inputs)):
        circuit[i] = inputs[i]

    for i in range(len(inputs), n+len(inputs)):
        circuit[i] = False

    for u in toposort[::-1]:
        if u < len(inputs):
            continue
        else:
            if u in graphReverse:
                if len(graphReverse[u]) == 1:
                    circuit[u] = circuit[graphReverse[u][0]]
                else:
                    circuit[u] = not (circuit[graphReverse[u][0]]
                                      and circuit[graphReverse[u][1]])

    return circuit[n+len(inputs)]


def calculateFitness(genome, goal, numInputs, connectionSize, effectiveGates):
    n = int((len(genome) - numInputs) / (2*connectionSize+2))
    numNAND, graphReverse = createGraph(genome, n, numInputs, connectionSize)
    graph = reverseGraph(graphReverse)
    toposort = toposortGraph(graph)

    if not toposort:
        return 0

    correct = 0

    for inputs in itertools.product(*[[True, False]]*numInputs):
        circuitEval = evaluateCircuit(graphReverse, n, toposort, inputs)
        goalEval = goal(inputs)

        if circuitEval == goalEval:
            correct += 1

    fitness = correct / (2**numInputs)

    if numNAND > effectiveGates:
        fitness -= 0.025 * (numNAND - effectiveGates)

    return fitness


def goal1(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return (x ^ y) & (z ^ w)


def goal2(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return (x ^ y) | (z ^ w)


def goal3(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) | (z ^ w)) & ((x ^ z) | (y ^ w))


def goal4(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) & (z ^ w)) | ((x ^ z) & (y ^ w))


def goal5(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) & (z ^ w)) & ((x ^ y) | (z ^ w))


def goal6(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) & (z ^ w)) | ((x ^ y) | (z ^ w))


def goal7(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) | (z ^ w)) & ((x ^ y) | (z ^ w))


def goal8(inputs):
    x = inputs[0]
    y = inputs[1]
    z = inputs[2]
    w = inputs[3]

    return ((x ^ y) & (z ^ w)) | ((x ^ y) & (z ^ w))


if __name__ == '__main__':
    numInputs = 4  # number of inputs into network
    effectiveGates = 11  # optimal number of nodes
    connectionSize = 4  # num bits per connection

    genome = [0, 0,     0, 0, 0, 0,     0, 0, 0, 1,
              0, 0,     0, 0, 0, 0,     0, 1, 0, 0,
              0, 0,     0, 0, 0, 1,     0, 1, 0, 0,
              0, 0,     0, 1, 0, 1,     0, 1, 1, 0,
              0, 0,     0, 0, 1, 0,     0, 0, 1, 1,
              0, 0,     0, 0, 1, 0,     1, 0, 0, 0,
              0, 0,     0, 0, 1, 1,     1, 0, 0, 0,
              0, 0,     1, 0, 0, 1,     1, 0, 1, 0,
              0, 0,     0, 1, 1, 1,     1, 0, 1, 1,
              0, 0,     0, 1, 1, 1,     1, 0, 1, 1,
              0, 0,     1, 1, 0, 0,     1, 1, 0, 1,
              1, 0,     1, 1, 0, 1,     1, 0, 0, 1,
              0, 1,     1, 0, 1, 0,     0, 0, 0, 1,
              1, 1, 1, 0]  # sample genome from Fig 2b ([0, 0] means that a NAND gate is on)

    genome2 = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,
               1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]

    genome3 = '1111100110100101011010001101101010110101111000110100001000000100011000101101100010000010001110110111101110010110100111101111101000110011001000110110010001011001000000010001100001011101011001110101111110011100101101011110010011110101101100011111001000110100010010011110100000011000000010001100000111110101001000110001011100111101111111010000'
    genome4 = [int(x) for x in genome3]

    print(calculateFitness(genome4, goal2,
                           numInputs, connectionSize=5, effectiveGates=25))
