import random
from timetable import make_table, copy_table, check_constraints, rooms

NUM_SLOTS = 40
NUM_ROOMS = len(rooms)


def get_cost(table):
    return check_constraints(table)


def make_population(size):
    population = []
    for i in range(size):
        population.append(make_table())
    return population


def tournament_selection(population, costs, tournament_size):
    chosen = random.sample(range(len(population)), tournament_size)
    best = chosen[0]
    for i in chosen:
        if costs[i] < costs[best]:
            best = i
    return population[best]


def crossover(parent1, parent2, kind="one_point"):
    n = len(parent1)
    child1 = []
    child2 = []

    if kind == "one_point":
        point = random.randint(1, n - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    else:
        for i in range(n):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])

    return copy_table(child1), copy_table(child2)


def mutate(table, mutation_rate):
    for i in range(len(table)):
        if random.random() < mutation_rate:
            what = random.choice(["slot", "room", "both"])
            if what == "slot" or what == "both":
                table[i][0] = random.randint(0, NUM_SLOTS - 1)
            if what == "room" or what == "both":
                table[i][1] = random.randint(0, NUM_ROOMS - 1)


def run_ga(pop_size=60, generations=150, crossover_rate=0.8, mutation_rate=0.03,
           tournament_size=3, elite_count=2, crossover_type="one_point", seed=None):
    if seed is not None:
        random.seed(seed)

    population = make_population(pop_size)
    history = {"best_cost": [], "avg_cost": [], "best_hard": []}

    for generation in range(generations):
        costs = [get_cost(t) for t in population]

        best_index = costs.index(min(costs))
        history["best_cost"].append(costs[best_index])
        history["avg_cost"].append(sum(costs) / len(costs))
        history["best_hard"].append(check_constraints(population[best_index]))

        order = sorted(range(pop_size), key=lambda i: costs[i])
        new_population = []
        for i in order[:elite_count]:
            new_population.append(copy_table(population[i]))

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, costs, tournament_size)
            parent2 = tournament_selection(population, costs, tournament_size)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2, crossover_type)
            else:
                child1 = copy_table(parent1)
                child2 = copy_table(parent2)

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population[:pop_size]

    costs = [get_cost(t) for t in population]
    best_index = costs.index(min(costs))
    best = population[best_index]
    history["best_cost"].append(costs[best_index])
    history["avg_cost"].append(sum(costs) / len(costs))
    history["best_hard"].append(check_constraints(best))

    return best, history
