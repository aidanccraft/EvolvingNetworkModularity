import random
import time
import json
import multiprocessing as mp
import numpy as np
from functools import partial

import fitness


def mutateGenome(genome):
    ind = random.choice(range(len(genome)))
    genome[ind] = genome[ind] ^ 1

    return genome


def evolveGenomes(n_genomes, n_generations, elite_frac, P_mutate):
    fit_stats = np.zeros((n_generations, 2))
    new_genomes = np.zeros((n_genomes, 124), dtype=int)
    fitnesses = np.zeros(n_genomes)

    perfect = set()

    split_index = n_genomes - int(n_genomes*elite_frac)
    mutate_index = int((elite_frac+0.2)*n_genomes)

    optimalGenCount = 0
    foundOptimal = False
    gen = 0

    pool = mp.Pool()

    while gen < n_generations and optimalGenCount < 8:
        genomes = new_genomes

        fitnesses[:split_index] = pool.map(partial(fitness.calculateFitness, goal=fitness.goal1,
                                                   numInputs=4, connectionSize=4, effectiveGates=10),
                                           genomes[:split_index], chunksize=50)

        fit_stats[gen, 0] = np.max(fitnesses)
        fit_stats[gen, 1] = np.average(fitnesses)

        ranks = np.argsort(fitnesses)

        genomes = np.take(genomes, ranks, axis=0)
        fitnesses = np.take(fitnesses, ranks, axis=0)

        mutate, elite = np.split(genomes, [split_index], axis=0)

        for i in range(np.size(mutate, axis=0)):
            mutate[i, :] = genomes[random.choice(
                range(mutate_index, np.size(genomes, axis=0))), :]
            if random.random() <= P_mutate:
                mutate[i, :] = mutateGenome(mutate[i, :])

        new_genomes = np.concatenate((mutate, elite))

        if gen % 100 == 0:
            print(f'{(gen / n_generations * 100):.1f}%')

        if gen % 10 == 9:
            # print(gen, fit_stats[gen, 0], fit_stats[gen, 1])
            if fitnesses[-1] == 1:
                optimalGenCount += 1
                foundOptimal = True

                if optimalGenCount == 8:
                    perfect = genomes[np.array(fitnesses) == 1]
                    for genome in perfect:
                        out = ''
                        for bit in genome:
                            out += str(bit)
                        perfect.add(out)
            else:
                optimalGenCount = 0
                perfect = set()

        gen += 1

    pool.close()

    data = {'numberGenerations': gen, 'foundOptimal': foundOptimal,
            'maxFitness': list(fit_stats[:, 0]), 'avgFitness': list(fit_stats[:, 1]),
            'perfect': list(perfect)}
    return data


if __name__ == '__main__':
    start = time.time()

    jsonData = {}

    for i in range(1):
        seed = random.randint(0, 1000000)
        random.seed(seed)

        print(f'Iteration: {i}, Seed: {seed}')
        data = evolveGenomes(2000, 100000, 0.5, 0.7)
        print(
            f'Optimal Found: {data["foundOptimal"]}, Number of Generations: {data["numberGenerations"]}\n')

        data['seed'] = seed

        jsonData[str(i)] = data

        with open('FG.json', 'w') as f:
            json.dump(jsonData, f)

    end = time.time()
    print(f'Total Time (min): {((end-start)/60.0):.2f}')
