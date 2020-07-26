import wemmick.api
import json
from great_expectations.data_context.types.resource_identifiers import (
    ExpectationSuiteIdentifier,
)


def test_list_datasources(basic_in_memory_data_context):
    name = "test_sqlalchemy_datasource"
    class_name = "SqlAlchemyDatasource"

    data_asset_type_config = {
        "module_name": "custom_sqlalchemy_dataset",
        "class_name": "CustomSqlAlchemyDataset",
    }
    basic_in_memory_data_context.add_datasource(
        name,
        class_name=class_name,
        credentials={
            "connection_string": "postgresql://user:pass@localhost:5432/database"
        },
        data_asset_type_config=data_asset_type_config,
        batch_kwargs_generators={
            "default": {"class_name": "TableBatchKwargsGenerator"}
        },
        initialize=False,
    )

    result = wemmick.api.list_datasources(basic_in_memory_data_context)

    assert len(result) == 1
    assert result[0]["name"] == name
    assert result[0]["class_name"] == class_name


def test_CreateExpectationSuiteFromJsonSchema(
    basic_in_memory_data_context, basic_json_schema_object, tmpdir
):
    suite_name = "test"
    suite_identifier = ExpectationSuiteIdentifier(expectation_suite_name=suite_name)

    path = tmpdir.mkdir("foo").join(f"{suite_name}.json")
    path.write(json.dumps(basic_json_schema_object))

    create_suite = wemmick.api.CreateExpectationSuiteFromJsonSchema(
        file_path=f"file://{path}",
        suite_name=suite_name,
        data_context=basic_in_memory_data_context,
    )
    create_suite.create_suite()

    expectation_suites = basic_in_memory_data_context.list_expectation_suites()
    assert len(expectation_suites) == 1
    assert expectation_suites[0] == suite_identifier

    test_suite = basic_in_memory_data_context.get_expectation_suite(
        expectation_suite_name=suite_name
    )
    assert test_suite.expectation_suite_name == suite_name
    assert len(test_suite.expectations) == 3
    assert any(
        expectation["expectation_type"] == "expect_column_to_exist"
        for expectation in test_suite.expectations
    )
    assert any(
        expectation["expectation_type"] == "expect_column_values_to_be_in_type_list"
        for expectation in test_suite.expectations
    )
    assert any(
        expectation["expectation_type"] == "expect_column_values_to_be_between"
        for expectation in test_suite.expectations
    )
