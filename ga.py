# ga.py
# Member 3: Genetic Algorithm
#
# Steps of the algorithm:
#   1. create a random population
#   2. evaluate every timetable (cost)
#   3. keep the best ones (elitism)
#   4. select parents (tournament), crossover, mutation -> new population
#   5. repeat for a number of generations

import random
from timetable import random_timetable, copy_timetable
from fitness import get_cost
from timetable import count_hard_violations
import data


def make_population(size):
    population = []
    for i in range(size):
        population.append(random_timetable())
    return population


def tournament_selection(population, costs, tournament_size):
    # pick some random timetables and return the best of them
    chosen = random.sample(range(len(population)), tournament_size)
    best = chosen[0]
    for i in chosen:
        if costs[i] < costs[best]:
            best = i
    return population[best]


def crossover(parent1, parent2, kind="one_point"):
    # returns two children made from the two parents
    n = len(parent1)
    child1 = []
    child2 = []

    if kind == "one_point":
        point = random.randint(1, n - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    else:
        # uniform: every session comes from a random parent
        for i in range(n):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])

    return copy_timetable(child1), copy_timetable(child2)


def mutate(timetable, mutation_rate):
    # every session has a small chance to get a new slot and/or a new room
    for i in range(len(timetable)):
        if random.random() < mutation_rate:
            what = random.choice(["slot", "room", "both"])
            if what == "slot" or what == "both":
                timetable[i][0] = random.randrange(data.TOTAL_SLOTS)
            if what == "room" or what == "both":
                timetable[i][1] = random.randrange(len(data.ROOMS))


def run_ga(pop_size=60, generations=150, crossover_rate=0.8, mutation_rate=0.03,
           tournament_size=3, elite_count=2, crossover_type="one_point", seed=None):
    if seed is not None:
        random.seed(seed)

    population = make_population(pop_size)
    history = {"best_cost": [], "avg_cost": [], "best_hard": []}

    for generation in range(generations):
        costs = [get_cost(t) for t in population]

        # save numbers for the convergence chart
        best_index = costs.index(min(costs))
        history["best_cost"].append(costs[best_index])
        history["avg_cost"].append(sum(costs) / len(costs))
        history["best_hard"].append(count_hard_violations(population[best_index]))

        # elitism: the best timetables go to the next generation unchanged
        order = sorted(range(pop_size), key=lambda i: costs[i])
        new_population = []
        for i in order[:elite_count]:
            new_population.append(copy_timetable(population[i]))

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, costs, tournament_size)
            parent2 = tournament_selection(population, costs, tournament_size)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2, crossover_type)
            else:
                child1 = copy_timetable(parent1)
                child2 = copy_timetable(parent2)

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population[:pop_size]

    # final evaluation
    costs = [get_cost(t) for t in population]
    best_index = costs.index(min(costs))
    best = population[best_index]
    history["best_cost"].append(costs[best_index])
    history["avg_cost"].append(sum(costs) / len(costs))
    history["best_hard"].append(count_hard_violations(best))

    return best, history
