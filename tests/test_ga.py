# Tests for ga.py (Member 3)

import random
import data
from ga import make_population, tournament_selection, crossover, mutate, run_ga
from timetable import random_timetable, count_hard_violations
from fitness import get_cost


def test_make_population():
    population = make_population(10)
    assert len(population) == 10
    for t in population:
        assert len(t) == len(data.SESSIONS)


def test_tournament_returns_best_when_everyone_competes():
    population = make_population(8)
    costs = [get_cost(t) for t in population]
    winner = tournament_selection(population, costs, 8)
    assert get_cost(winner) == min(costs)


def test_crossover_genes_come_from_parents():
    for kind in ["one_point", "uniform"]:
        p1 = random_timetable()
        p2 = random_timetable()
        c1, c2 = crossover(p1, p2, kind)
        assert len(c1) == len(p1) and len(c2) == len(p1)
        for i in range(len(p1)):
            assert c1[i] in [p1[i], p2[i]]
            assert c2[i] in [p1[i], p2[i]]


def test_crossover_does_not_change_parents():
    p1 = random_timetable()
    p2 = random_timetable()
    p1_before = [g[:] for g in p1]
    c1, c2 = crossover(p1, p2)
    c1[0][0] = (c1[0][0] + 1) % data.TOTAL_SLOTS
    assert p1 == p1_before


def test_mutation_rate_zero_changes_nothing():
    t = random_timetable()
    before = [g[:] for g in t]
    mutate(t, 0)
    assert t == before


def test_mutation_rate_one_changes_something_and_stays_in_range():
    random.seed(5)
    t = random_timetable()
    before = [g[:] for g in t]
    mutate(t, 1)
    assert t != before
    for slot, room in t:
        assert 0 <= slot < data.TOTAL_SLOTS
        assert 0 <= room < len(data.ROOMS)


def test_run_ga_history_length():
    best, history = run_ga(pop_size=20, generations=10, seed=1)
    assert len(history["best_cost"]) == 11   # 10 generations + the final one
    assert len(history["avg_cost"]) == 11
    assert len(history["best_hard"]) == 11


def test_best_cost_never_gets_worse():
    # elitism keeps the best timetable, so the best cost can only go down
    best, history = run_ga(pop_size=30, generations=20, seed=2)
    costs = history["best_cost"]
    for i in range(1, len(costs)):
        assert costs[i] <= costs[i - 1]


def test_ga_improves_a_lot():
    best, history = run_ga(pop_size=40, generations=40, seed=3)
    assert history["best_cost"][-1] < history["best_cost"][0] / 2


def test_same_seed_gives_same_result():
    best1, h1 = run_ga(pop_size=20, generations=10, seed=7)
    best2, h2 = run_ga(pop_size=20, generations=10, seed=7)
    assert best1 == best2
    assert h1["best_cost"] == h2["best_cost"]


def test_returned_best_matches_history():
    best, history = run_ga(pop_size=20, generations=10, seed=4)
    assert get_cost(best) == history["best_cost"][-1]


def test_ga_finds_a_valid_timetable_with_default_settings():
    best, history = run_ga(seed=1)
    assert count_hard_violations(best) == 0
