import pytest
import typer

from dataquality.cli import avro_file, json_file


def test_json_file_raises_error_if_file_not_found():
    with pytest.raises(typer.Abort):
        json_file("foo.json", "foo")


def test_avro_file_raises_error_if_file_not_found():
    with pytest.raises(typer.Abort):
        avro_file("foo.json")
