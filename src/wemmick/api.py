import json
import os
from urllib.parse import urlparse
from abc import ABC, abstractmethod
import great_expectations as ge
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
from wemmick.avro_schema_profiler import AvroSchemaFileProfiler
from wemmick.utils import file_relative_path, get_file


def get_data_context():
    try:
        context = ge.data_context.DataContext()
        return context
    except ge.exceptions.GreatExpectationsError as e:
        raise Exception(f'Failed to load GE data context: {e}')


def list_datasources():
    context = get_data_context()
    return context.list_datasources()


def list_expectation_suites():
    context = get_data_context()
    return context.list_expectation_suites()


class ProfilerCreateExpectationSuiteBaseClass(ABC):
    def __init__(self, file_path: str, suite_name: str = None, data_context=None):
        self.file_path = file_path
        self.suite_name = suite_name if suite_name else os.path.basename(file_path)
        self.data_context = data_context if data_context else get_data_context()

    @abstractmethod
    def get_schema(self):
        pass

    @abstractmethod
    def get_profiler(self):
        pass

    def create_suite(self):
        profiler = self.get_profiler()
        schema = self.get_schema()
        suite = profiler.profile(schema, suite_name=self.suite_name)
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
        return urlparse(self.file_path).path

    def get_profiler(self):
        base_dir = file_relative_path(__file__, ".")
        return AvroSchemaFileProfiler(base_directory=base_dir, verbose=True)

    def create_suite(self):
        profiler = self.get_profiler()
        schema = self.get_schema()
        suite = profiler.run(filename=schema)[0]
        self.data_context.save_expectation_suite(suite)


class CreateExpectationSuiteFromJsonSchema:
    def __init__(self, file_path: str, suite_name: str):
        self.file_path = file_path
        self.suite_name = suite_name

    def get_data_context(self):
        try:
            context = ge.data_context.DataContext()
            return context
        except ge.exceptions.GreatExpectationsError as e:
            raise Exception(f'Failed to load GE data context: {e}')

    def get_json_schema(self):
        raw_file = get_file(self.file_path)

        try:
            json_schema = json.loads(raw_file)
            return json_schema
        except json.decoder.JSONDecodeError as e:
            raise Exception(f'Failed to parse JSON file: {e}')

    def create_suite(self, context, json_schema: str, suite_name: str):
        profiler = JsonSchemaProfiler()
        suite = profiler.profile(json_schema, suite_name)
        context.save_expectation_suite(suite)

    def build_docs(self, context):
        context.build_data_docs()

    def open_docs(self, context):
        context.open_data_docs()

    def run(self):
        context = self.get_data_context()
        json_schema = self.get_json_schema()
        self.create_suite(context, json_schema, self.suite_name)
        self.build_docs(context)
        self.open_docs(context)


class RunValidation:
    def __init__(self, datasource: str, table: str, suite_name: str):
        self.datasource = datasource
        self.table = table
        self.suite_name = suite_name
        self.data_context = self.get_data_context()

    def get_data_context(self):
        return get_data_context()

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
