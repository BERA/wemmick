import pytest

from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig


@pytest.fixture(scope="module")
def basic_data_context_config():
    return DataContextConfig(
        config_version=2,
        plugins_directory=None,
        evaluation_parameter_store_name="evaluation_parameter_store",
        expectations_store_name="expectations_store",
        datasources={},
        stores={
            "expectations_store": {"class_name": "ExpectationsStore"},
            "evaluation_parameter_store": {"class_name": "EvaluationParameterStore"},
            "validation_result_store": {"class_name": "ValidationsStore"},
            "metrics_store": {"class_name": "MetricStore"},
        },
        validations_store_name="validation_result_store",
        data_docs_sites={},
        validation_operators={},
    )


@pytest.fixture(scope="module")
def basic_in_memory_data_context(basic_data_context_config):
    return BaseDataContext(basic_data_context_config)


@pytest.fixture(scope="module")
def basic_json_schema_object():
    return {
        "description": "Test table",
        "type": "object",
        "properties": {
            "rating": {
                "description": "Rating on a scale of 1 to 7",
                "type": "integer",
                "minimum": 1,
                "maximum": 7,
            }
        },
        "required": ["rating"],
        "$schema": "http://json-schema.org/draft-07/schema#",
    }
