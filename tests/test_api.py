import wemmick.api
import json
from great_expectations.core import ExpectationSuite


def test_list_datasources(mocker, basic_in_memory_data_context):
    mocked_list_datasources = mocker.patch(
        "great_expectations.data_context.BaseDataContext.list_datasources",
        return_value=[],
    )
    wemmick.api.list_datasources(basic_in_memory_data_context)
    mocked_list_datasources.assert_called_once()


def test_CreateExpectationSuiteFromJsonSchema(
    mocker, basic_in_memory_data_context, basic_json_schema_object, tmpdir
):
    suite_name = "mock"
    mock_suite = ExpectationSuite(suite_name)
    mocked_profile = mocker.patch(
        "great_expectations.profile.base.Profiler.profile", return_value=mock_suite,
    )
    mocked_save_expectation_suite = mocker.patch(
        "great_expectations.data_context.BaseDataContext.save_expectation_suite",
        return_value=None,
    )
    mocked_build_data_docs = mocker.patch(
        "great_expectations.data_context.BaseDataContext.build_data_docs",
        return_value=None,
    )
    mocked_open_data_docs = mocker.patch(
        "great_expectations.data_context.BaseDataContext.open_data_docs",
        return_value=None,
    )

    path = tmpdir.mkdir("foo").join(f"{suite_name}.json")
    path.write(json.dumps(basic_json_schema_object))

    create_suite = wemmick.api.CreateExpectationSuiteFromJsonSchema(
        file_path=f"file://{path}",
        suite_name=suite_name,
        data_context=basic_in_memory_data_context,
    )
    create_suite.run()

    mocked_profile.assert_called_once()
    mocked_save_expectation_suite.assert_called_once_with(mock_suite)
    mocked_build_data_docs.assert_called_once()
    mocked_open_data_docs.assert_called_once()
