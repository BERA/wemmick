import glob
import json
import os
import re
from typing import Callable, List, Union

from great_expectations.core import (
    ExpectationConfiguration,
    ExpectationKwargs,
    ExpectationSuite,
)


class AvroSchemaFileProfiler:
    """
    Create basic Expectation Suites from avro schema files.
    """

    # TODO update to inherit from Profiler after release of 0.11.x

    def __init__(
        self,
        base_directory: str = None,
        verbose: bool = False,
        printer: Callable = print,
    ):
        self.base_directory = base_directory
        self.verbose = verbose
        self.print = printer

    def run(
        self, filename: str = None, glob_pattern: str = None
    ) -> List[ExpectationSuite]:
        """
        Create a suite or suites from a avro_file or glob pattern of files.

        Args:
            filename: Given a filename create a single suite
            glob_pattern: If given a glob pattern create a list of suites
        """
        if filename is not None and glob_pattern is not None:
            raise ValueError(
                "Please specify either filename or glob pattern, not both."
            )

        if filename is None and glob_pattern is None:
            raise ValueError("Please specify a filename or glob pattern.")

        if filename is not None:
            return [self._create_suite_from_file(filename)]

        if glob_pattern is not None:
            suites: List[ExpectationSuite] = []
            for file in glob.glob(glob_pattern):
                file = os.path.join(str(self.base_directory), file)
                file_name = os.path.basename(file)
                suite: ExpectationSuite = self._create_suite_from_file(file_name)
                suites.append(suite)
            return suites

        return []

    def _create_suite_from_file(self, filename: str) -> ExpectationSuite:
        schema = self._load_avro_schema_file(filename)
        suite: ExpectationSuite = self._create_suite_from_schema(schema, filename)
        return suite

    def _load_avro_schema_file(self, filename: str) -> dict:
        """
        Load an avro schema avro_file.
        Some schema files have comments which break json parsing so remove them
        """
        with open(filename, "r") as f:
            raw_file = f.read()
        cleaned_file = re.sub(r"//.*", "", raw_file)
        result = dict(json.loads(cleaned_file))
        if self.verbose:
            self.print(f"File {filename} loaded!")
        return result

    def _create_suite_from_schema(
        self, schema: dict, filename: str
    ) -> ExpectationSuite:
        """Create an ExpectationSuite from an avro dictionary."""
        base_file_name = os.path.basename(filename)
        suite: ExpectationSuite = ExpectationSuite(base_file_name)

        for field in schema["fields"]:
            field_name = field["name"]
            if self.verbose:
                self.print(f"  - {field_name}")

            for subfield in field["type"]["items"]["fields"]:
                subfield_name: str = subfield["name"]
                subfield_type: Union[str, List[str]] = subfield["type"]
                if self.verbose:
                    self.print(f"    + {subfield_name}: {subfield_type}")
                kwargs = ExpectationKwargs(column=subfield_name)

                for expectation_type in [
                    "expect_column_values_to_not_be_null",
                    "expect_column_to_exist",
                ]:
                    expectation = ExpectationConfiguration(expectation_type, kwargs)
                    suite.append_expectation(expectation)

        suite.meta["notes"] = {
            "format": "markdown",
            "content": [
                f"## This suite was created from an avro source avro_file: {base_file_name}"
            ],
        }
        return suite
