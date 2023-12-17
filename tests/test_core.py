# -*- coding: utf-8 -*-

import pytest
from tt4human.core import to_bool, TruthTable, InvalidCaseError, generate_initial_csv
from tt4human.paths import dir_unit_test

dir_tmp = dir_unit_test.joinpath("tmp")
dir_tmp.mkdir(parents=True, exist_ok=True)


def test_to_bool():
    assert to_bool("True") is True
    with pytest.raises(ValueError):
        to_bool("unknown")


class TestTruthTable:
    def test(self):
        tt = TruthTable.from_csv(dir_unit_test.joinpath("go_out.tsv"))
        assert tt.evaluate(case=dict(weather="is_sunny", get_up="before_10")) is True
        assert tt.evaluate(case=dict(weather="is_sunny", get_up="10_to_2")) is True
        assert tt.evaluate(case=dict(weather="is_sunny", get_up="after_2")) is False
        assert tt.evaluate(case=dict(weather="not_sunny", get_up="before_10")) is False
        assert tt.evaluate(case=dict(weather="not_sunny", get_up="10_to_2")) is False
        assert tt.evaluate(case=dict(weather="not_sunny", get_up="after_2")) is False

        with pytest.raises(InvalidCaseError):
            _ = tt.evaluate(case=dict(weather="rain", get_up="before_8"))

        with pytest.raises(InvalidCaseError):
            _ = tt.evaluate(case=dict(weekday="monday"))

    def test_generate_module(self):
        tt = TruthTable.from_csv(dir_unit_test.joinpath("go_out.tsv"))

        tt.generate_module(
            dir_path=dir_tmp,
            module_name="do_you_go_out",
            overwrite=True,
        )

        with pytest.raises(FileExistsError):
            tt.generate_module(
                dir_path=dir_tmp,
                module_name="do_you_go_out",
                overwrite=False,
            )


def test_generate_initial_csv():
    conditions = {
        "weather": ["is_sunny", "not_sunny"],
        "get_up": ["before_10", "10_to_2", "after_2"],
    }
    path = dir_tmp.joinpath("initial_go_out.tsv")
    generate_initial_csv(
        conditions=conditions,
        flag_name="go_out",
        path=path,
        overwrite=True,
    )

    tt = TruthTable.from_csv(path)
    assert tt.evaluate(case=dict(weather="is_sunny", get_up="before_10")) is False
    assert tt.evaluate(case=dict(weather="is_sunny", get_up="10_to_2")) is False
    assert tt.evaluate(case=dict(weather="is_sunny", get_up="after_2")) is False
    assert tt.evaluate(case=dict(weather="not_sunny", get_up="before_10")) is False
    assert tt.evaluate(case=dict(weather="not_sunny", get_up="10_to_2")) is False
    assert tt.evaluate(case=dict(weather="not_sunny", get_up="after_2")) is False


if __name__ == "__main__":
    from tt4human.tests import run_cov_test

    run_cov_test(__file__, "tt4human.core", preview=False)
