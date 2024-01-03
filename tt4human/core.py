# -*- coding: utf-8 -*-

import typing as T
import csv
import dataclasses
import itertools
from pathlib import Path

from .vendor.strutils import under2camel, slugify
from ._version import __version__
from .compat import cached_property

if T.TYPE_CHECKING:
    import pandas as pd


bool_mapper = {
    "true": True,
    "false": False,
    "t": True,
    "f": False,
    "yes": True,
    "no": False,
    "y": True,
    "n": False,
    "1": True,
    "0": False,
    "": False,
}


def to_bool(v: str) -> bool:
    """
    Convert a "bool" like string to a boolean value.
    """
    try:
        return bool_mapper[v.lower()]
    except KeyError:
        raise ValueError(f"Cannot convert {v} to bool.")


class InvalidCaseError(ValueError):
    pass


SEP = "____"


def _ensure_path_not_exists(path: Path, overwrite: bool):
    if path.exists():
        if overwrite is False:
            raise FileExistsError(f"{path} already exists.")


@dataclasses.dataclass
class TruthTable:
    """
    `Truth Table <https://en.wikipedia.org/wiki/Truth_table>`_ is a lookup
    table that can return a boolean value by given a set of conditions.
    A set of conditions is called a case.

    For example, we have two types of conditions: ``weather`` and
    ``get_up`` (when you get up). And we want to determine if you will go out.
    ``weather`` has two possible values: ``is_sunny`` and ``not_sunny``.
    ``get_up`` has three possible values: ``before_10``, ``10_to_2``, ``after_2``.

    Below is the truth table::

        weather	    get_up	    go_out
        is_sunny	before_10	1
        is_sunny	10_to_2	    1
        is_sunny	after_2	    0
        not_sunny	before_10	0
        not_sunny	10_to_2	    0
        not_sunny	after_2	    0

    :param headers: the last column is the "target", others are "conditions".
    :param rows: list of "cases", for each row, the last item is the "target",
        others are "conditions".
    """

    headers: T.List[str] = dataclasses.field()
    rows: T.List[list] = dataclasses.field()

    @cached_property
    def conditions(self) -> T.List[str]:
        """
        Condition types.
        """
        return self.headers[:-1]

    @cached_property
    def sorted_conditions(self) -> T.List[str]:
        """
        Sorted condition types.
        """
        conditions = list(self.conditions)
        conditions.sort()
        return conditions

    @cached_property
    def dict_view(self) -> T.Dict[str, T.Iterable]:
        """
        A dict view of the truth table.

        Example::

            {
                'weather': ('is_sunny', 'is_sunny', 'is_sunny', 'not_sunny', 'not_sunny', 'not_sunny'),
                'get_up': ('before_10', '10_to_2', 'after_2', 'before_10', '10_to_2', 'after_2'),
                'go_out': (True, True, False, False, False, False)
            }
        """
        dct_view = dict()
        for tp in zip(self.headers, zip(*self.rows)):
            dct_view[tp[0]] = tp[1]
        return dct_view

    @cached_property
    def lookup(self) -> T.Dict[str, bool]:
        """
        Return a dict to map the conditions to the result.

        Sample lookup::

            {
                'before_10____is_sunny': True,
                '10_to_2____is_sunny': True,
                'after_2____is_sunny': False,
                'before_10____not_sunny': False,
                '10_to_2____not_sunny': False,
                'after_2____not_sunny': False
            }
        """
        flags = self.dict_view[self.headers[-1]]
        lookup = dict()
        for condition_values, flag in zip(
            zip(*[self.dict_view[condition] for condition in self.sorted_conditions]),
            flags,
        ):
            key = SEP.join(condition_values)
            lookup[key] = flag

        return lookup

    @classmethod
    def new(
        cls,
        headers: T.List[str],
        rows: T.List[list],
    ):
        """
        Create a new truth table.

        :param headers: the last column is the "target", others are "conditions".
        :param rows: list of "cases", for each row, the last item is the "target",
            others are "conditions".
        """
        new_rows = list()
        for row in rows:
            new_row = list(row[:-1])
            new_row.append(to_bool(str(row[-1])))
            new_rows.append(new_row)
        return cls(headers, new_rows)

    @classmethod
    def from_csv(
        cls,
        path,
        sep: str = "\t",
    ):
        """
        Read truth table data from a CSV file.
        The first row is the types of condition, and the last column
        has to be the name of the result.

        The value in the last column can be any "bool" liked value, such as
        "true", "false", "t", "f", "yes", "no", "y", "n", "1", "0", etc.

        :param path: path-like object, path to the CSV file.
        :param sep: str, separator of the CSV file, by default we use tab,
            because TSV can be copied into Excel / GoogleSheet easily.
        """
        rows = list()
        with Path(path).open("r", newline="") as f:
            reader = csv.reader(f, delimiter=sep)
            headers = next(reader)
            for row in reader:
                rows.append(row)
        return cls.new(headers=headers, rows=rows)

    @classmethod
    def from_pandas_df(cls, df: "pd.DataFrame"): # pragma: no cover
        """
        Create a truth table from a pandas DataFrame.
        """
        headers = list(df.columns)
        rows = df.values.tolist()
        return cls.new(headers=headers, rows=rows)

    def evaluate(self, case: T.Dict[str, str]) -> bool:
        """
        Evaluate a case and return the result.
        A case is a key value pair that the key is the condition type, and the
        value is the condition value.

        :param case: example, ``{"weather": "is_sunny", "get_up": "before_10"}``
        """
        conditions = list()
        for condition in self.sorted_conditions:
            try:
                conditions.append(case[condition])
            except KeyError:
                raise InvalidCaseError(
                    f"Cannot find condition {condition!r} in case {case}"
                )
        key = SEP.join(conditions)
        try:
            return self.lookup[key]
        except KeyError:
            raise InvalidCaseError(f"Cannot find case {case} in truth table.")

    def generate_module(
        self,
        dir_path: Path,
        module_name: str,
        overwrite: bool = False,
    ):
        """
        Human usually create a truth table in Excel or GoogleSheet. This function
        can generate a Python module from a truth table that can be imported and
        used in your code.

        :param truth_table: TruthTable, the truth table to be converted.
        :param dir_path: Path, path to the directory to save the generated module.
        :param module_name: str, name of the generated Python module.
        :param overwrite: bool, if True, overwrite the existing module.
        """
        path_csv = dir_path.joinpath(f"{module_name}.tsv")
        path_py = dir_path.joinpath(f"{module_name}.py")

        _ensure_path_not_exists(path_csv, overwrite)
        _ensure_path_not_exists(path_py, overwrite)

        with path_csv.open("w", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(self.headers)
            for row in self.rows:
                writer.writerow(row)

        lines = [
            "# -*- coding: utf-8 -*-",
            "",
            '"""',
            f"this module is generated by https://pypi.org/project/tt4human = {__version__}",
            '"""',
            "",
            "from pathlib import Path",
            "from tt4human.api import BetterStrEnum, TruthTable",
            "",
            "",
        ]
        test_case = dict()
        for condition in self.conditions:
            class_name = under2camel(slugify(condition, delim="_", lower=True))
            lines.append(f"class {class_name}Enum(BetterStrEnum):")
            values = self.dict_view[condition]
            distinct_values = list({value: 0 for value in values})
            test_case[condition] = distinct_values[0]
            for value in distinct_values:
                key = slugify(value, delim="_", lower=True)
                if key[0].isalpha() is False:
                    key = "_" + key
                lines.append(f'    {key} = "{value}"')
            lines.append("")
            lines.append("")

        flag = self.evaluate(test_case)

        lines.extend(
            [
                "truth_table = TruthTable.from_csv(",
                f'    path=Path(__file__).absolute().parent.joinpath("{module_name}.tsv"),',
                ")",
                "",
                'if __name__ == "__main__":',
                f"    assert truth_table.evaluate(case={test_case}) is {flag}",
            ]
        )

        module_content = "\n".join(lines)
        path_py.write_text(module_content)


def generate_initial_csv(
    conditions: T.Dict[str, T.List[str]],
    flag_name: str,
    path: Path,
    sep: str = "\t",
    default_flag: str = "0",
    overwrite: bool = False,
):
    """
    Generate an initial CSV file from a dict of conditions. So human can copy
    it into Excel or GoogleSheet and fill the truth table.

    :param conditions: dict, key is the condition type, value is a list of
        condition values.
    :param flag_name: str, name of the flag column.
    :param path: path-like object, path to the CSV file.
    :param sep: str, separator of the CSV file, by default we use tab,
        because TSV can be copied into Excel / GoogleSheet easily.
    :param overwrite: bool, if True, overwrite the existing CSV file.
    """
    _ensure_path_not_exists(path, overwrite)
    headers = list(conditions.keys())
    headers.append(flag_name)
    rows = list(itertools.product(*conditions.values()))
    rows = [[str(value) for value in row] for row in rows]
    rows = [[*row, default_flag] for row in rows]
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter=sep)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
