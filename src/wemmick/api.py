import json
import great_expectations as ge
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
import utils


def list_datasources():
    context = ge.DataContext()
    return context.list_datasources()


def list_expectation_suites():
    context = ge.DataContext()
    return context.list_expectation_suites()


def create_expectation_suite_from_json_schema(json_file_path: str, suite_name: str):
    try:
        context = ge.data_context.DataContext()
    except ge.exceptions.GreatExpectationsError as e:
        raise Exception(f'Failed to load GE data context: {e}')

    raw_file = utils.get_file(json_file_path)

    try:
        json_schema = json.loads(raw_file)
    except json.decoder.JSONDecodeError as e:
        raise Exception(f'Failed to parse JSON file: {e}')

    profiler = JsonSchemaProfiler()
    suite = profiler.profile(json_schema, suite_name)
    context.save_expectation_suite(suite)
    context.build_data_docs()
    context.open_data_docs()