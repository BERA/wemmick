import pytest
import typer
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from wemmick.cli import avro_file, json_file


def mock_get_data_context():
    config = DataContextConfig(
        config_version=2,
        datasources={},
        data_docs_sites={},
        plugins_directory=None,
        expectations_store_name="expectations_store",
        validations_store_name="validation_result_store",
        evaluation_parameter_store_name="evaluation_parameter_store_name",
        stores={
            "expectations_store": {"class_name": "ExpectationsStore"},
            "evaluation_parameter_store": {"class_name": "EvaluationParameterStore"},
            "validation_result_store": {"class_name": "ValidationsStore"},
            "metrics_store": {"class_name": "MetricStore"},
        },
        validation_operators={
            "store_val_res_and_extract_eval_params": {
                "class_name": "ActionListValidationOperator",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {
                            "class_name": "StoreValidationResultAction",
                            "target_store_name": "validation_result_store",
                        },
                    },
                    {
                        "name": "extract_and_store_eval_parameters",
                        "action": {
                            "class_name": "StoreEvaluationParametersAction",
                            "target_store_name": "evaluation_parameter_store",
                        },
                    },
                ],
            },
            "errors_and_warnings_validation_operator": {
                "class_name": "WarningAndFailureExpectationSuitesValidationOperator",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {
                            "class_name": "StoreValidationResultAction",
                            "target_store_name": "validation_result_store",
                        },
                    },
                    {
                        "name": "extract_and_store_eval_parameters",
                        "action": {
                            "class_name": "StoreEvaluationParametersAction",
                            "target_store_name": "evaluation_parameter_store",
                        },
                    },
                ],
            },
        },
    )
    return BaseDataContext(config)


def test_json_file_raises_error_if_file_not_found(mocker):
    mocker.patch("wemmick.api.get_data_context", mock_get_data_context)
    with pytest.raises(typer.Abort):
        json_file("file://foo.json", "foo")


def test_avro_file_raises_error_if_file_not_found(mocker):
    mocker.patch("wemmick.api.get_data_context", mock_get_data_context)
    with pytest.raises(typer.Abort):
        avro_file("file://foo.json")
