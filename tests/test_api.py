# -*- coding: utf-8 -*-

from tt4human import api


def test():
    _ = api
    _ = api.BetterStrEnum
    _ = api.to_bool
    _ = api.InvalidCaseError
    _ = api.TruthTable
    _ = api.generate_initial_csv


if __name__ == "__main__":
    from tt4human.tests import run_cov_test

    run_cov_test(__file__, "tt4human.api", preview=False)
