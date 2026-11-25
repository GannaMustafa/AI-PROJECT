# Tests for ga.py (Member 3)
import random
import pytest
import ga
from timetable import make_table, sessions, check_constraints


def fake_cost(table):
    return sum(gene[0] for gene in table)


@pytest.fixture
def fast_cost(monkeypatch):
    monkeypatch.setattr(ga, "get_cost", fake_cost)


def test_make_population():
    population = ga.make_population(10)
    assert len(population) == 10
    for t in population:
        assert len(t) == len(sessions)


def test_tournament_returns_best_when_everyone_competes(fast_cost):
    population = ga.make_population(8)
    costs = [ga.get_cost(t) for t in population]
    winner = ga.tournament_selection(population, costs, 8)
    assert ga.get_cost(winner) == min(costs)


def test_crossover_genes_come_from_parents():
    for kind in ["one_point", "uniform"]:
        p1 = make_table()
        p2 = make_table()
        c1, c2 = ga.crossover(p1, p2, kind)
        assert len(c1) == len(p1) and len(c2) == len(p1)
        for i in range(len(p1)):
            assert c1[i] in [p1[i], p2[i]]
            assert c2[i] in [p1[i], p2[i]]


def test_crossover_does_not_change_parents():
    p1 = make_table()
    p2 = make_table()
    p1_before = [g[:] for g in p1]
    c1, c2 = ga.crossover(p1, p2)
    c1[0][0] = (c1[0][0] + 1) % ga.NUM_SLOTS
    assert p1 == p1_before


def test_mutation_rate_zero_changes_nothing():
    t = make_table()
    before = [g[:] for g in t]
    ga.mutate(t, 0)
    assert t == before


def test_mutation_rate_one_changes_something_and_stays_in_range():
    random.seed(5)
    t = make_table()
    before = [g[:] for g in t]
    ga.mutate(t, 1)
    assert t != before
    for slot, room in t:
        assert 0 <= slot < ga.NUM_SLOTS
        assert 0 <= room < ga.NUM_ROOMS


def test_run_ga_history_length(fast_cost):
    best, history = ga.run_ga(pop_size=20, generations=10, seed=1)
    assert len(history["best_cost"]) == 11   
    assert len(history["avg_cost"]) == 11
    assert len(history["best_hard"]) == 11


def test_best_cost_never_gets_worse(fast_cost):
    best, history = ga.run_ga(pop_size=30, generations=20, seed=2)
    costs = history["best_cost"]
    for i in range(1, len(costs)):
        assert costs[i] <= costs[i - 1]


def test_ga_improves_a_lot(fast_cost):
    best, history = ga.run_ga(pop_size=40, generations=40, seed=3)
    assert history["best_cost"][-1] < history["best_cost"][0] / 2


def test_same_seed_gives_same_result(fast_cost):
    best1, h1 = ga.run_ga(pop_size=20, generations=10, seed=7)
    best2, h2 = ga.run_ga(pop_size=20, generations=10, seed=7)
    assert best1 == best2
    assert h1["best_cost"] == h2["best_cost"]


def test_returned_best_matches_history(fast_cost):
    best, history = ga.run_ga(pop_size=20, generations=10, seed=4)
    assert ga.get_cost(best) == history["best_cost"][-1]


def test_ga_with_the_real_constraint_check():
    best, history = ga.run_ga(pop_size=6, generations=2, seed=1)
    assert history["best_cost"][-1] == check_constraints(best)
    assert history["best_hard"][-1] == check_constraints(best)
