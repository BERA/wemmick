import pytest

from wemmick.avro_schema_profiler import AvroSchemaFileProfiler


def test_instantiable():
    profiler = AvroSchemaFileProfiler()
    assert isinstance(profiler, AvroSchemaFileProfiler)


def test_raise_error_on_missing_parameters():
    profiler = AvroSchemaFileProfiler()
    with pytest.raises(ValueError):
        profiler.run(filename=None, glob_pattern=None)


def test_raise_error_on_both_parameters():
    profiler = AvroSchemaFileProfiler()
    with pytest.raises(ValueError):
        profiler.run(filename="foo", glob_pattern="foo")
