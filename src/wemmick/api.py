import json
import great_expectations as ge
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
import wemmick.utils


def list_datasources():
    context = ge.DataContext()
    return context.list_datasources()


def list_expectation_suites():
    context = ge.DataContext()
    return context.list_expectation_suites()


class CreateExpectationSuiteFromJsonSchema:
    def __init__(self, json_file_path: str, suite_name: str):
        self.json_file_path = json_file_path
        self.suite_name = suite_name

    def get_data_context(self):
        try:
            context = ge.data_context.DataContext()
            return context
        except ge.exceptions.GreatExpectationsError as e:
            raise Exception(f'Failed to load GE data context: {e}')

    def get_json_schema(self):
        raw_file = wemmick.utils.get_file(self.json_file_path)

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






