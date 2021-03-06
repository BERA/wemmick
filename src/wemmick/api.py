import json
import os
from urllib.parse import urlparse
from abc import ABC, abstractmethod
import great_expectations as ge
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
from wemmick.avro_schema_profiler import AvroSchemaFileProfiler
from wemmick.utils import check_file_exists, get_file


def get_data_context():
    try:
        data_context = ge.DataContext()
        return data_context
    except ge.exceptions.GreatExpectationsError as e:
        raise Exception(f"Failed to load GE data context: {e}")


def list_datasources(data_context):
    return data_context.list_datasources()


def list_expectation_suites(data_context):
    return data_context.list_expectation_suites()


class ProfilerCreateExpectationSuiteBaseClass(ABC):
    def __init__(
        self,
        data_context,
        file_path: str,
        suite_name: str = None,
        verbose: bool = False,
    ):
        self.file_path = file_path
        self.suite_name = suite_name if suite_name else os.path.basename(file_path)
        self.data_context = data_context
        self.verbose = verbose

    @abstractmethod
    def get_schema(self):
        pass

    @abstractmethod
    def get_profiler(self):
        pass

    def verbose_print(self, string):
        print(string)

    def create_suite(self):
        profiler = self.get_profiler()
        schema = self.get_schema()
        suite = profiler.profile(schema, suite_name=self.suite_name)
        if self.verbose:
            self.verbose_print(str(suite))
        self.data_context.save_expectation_suite(suite)

    def build_docs(self):
        self.data_context.build_data_docs()

    def open_docs(self):
        self.data_context.open_data_docs()

    def run(self):
        self.create_suite()
        self.build_docs()
        self.open_docs()


class CreateExpectationSuiteFromAvroSchema(ProfilerCreateExpectationSuiteBaseClass):
    def get_schema(self):
        file_path = urlparse(self.file_path).path
        check_file_exists(file_path)
        return file_path

    def get_profiler(self):
        return AvroSchemaFileProfiler(verbose=self.verbose)

    def create_suite(self):
        profiler = self.get_profiler()
        schema = self.get_schema()
        suite = profiler.run(filename=schema)[0]
        self.data_context.save_expectation_suite(suite)


class CreateExpectationSuiteFromJsonSchema(ProfilerCreateExpectationSuiteBaseClass):
    def get_schema(self):
        raw_file = get_file(self.file_path)

        try:
            if self.verbose:
                self.verbose_print(raw_file)
            json_schema = json.loads(raw_file)
            return json_schema
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON file: {e}")

    def get_profiler(self):
        return JsonSchemaProfiler()


class RunValidation:
    def __init__(
        self,
        datasource: str,
        table: str,
        suite_name: str,
        data_context,
        verbose: bool = False,
    ):
        self.datasource = datasource
        self.table = table
        self.suite_name = suite_name
        self.data_context = data_context
        self.verbose = verbose

    def get_batch(self):
        batch_kwargs = {"table": self.table, "datasource": self.datasource}
        return self.data_context.get_batch(batch_kwargs, self.suite_name)

    def run_validation_operator(self, batch):
        return self.data_context.run_validation_operator(
            "action_list_operator", assets_to_validate=[batch],
        )

    def on_success(self):
        pass

    def on_failure(self):
        pass

    def run(self):
        batch = self.get_batch()
        results = self.run_validation_operator(batch)

        if not results["success"]:
            self.on_failure()
        else:
            self.on_success()
