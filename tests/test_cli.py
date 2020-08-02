import pytest
import typer
from wemmick.cli import avro_file, json_file


def test_json_file_raises_error_if_file_not_found(mocker, basic_in_memory_data_context):
    mocker.patch(
        "wemmick.cli.get_data_context", return_value=basic_in_memory_data_context
    )
    with pytest.raises(typer.Abort):
        json_file("file://foo.json", "foo")


def test_avro_file_raises_error_if_file_not_found(mocker, basic_in_memory_data_context):
    mocker.patch(
        "wemmick.cli.get_data_context", return_value=basic_in_memory_data_context
    )
    with pytest.raises(typer.Abort):
        avro_file("file://foo.json")
