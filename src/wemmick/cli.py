#!/usr/bin/env python
import json
import os
import sys

import click_spinner
import great_expectations as ge
import typer
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer

from wemmick.utils import file_relative_path
from wemmick.avro_schema_profiler import AvroSchemaFileProfiler
from wemmick.api import (
    CreateExpectationSuiteFromJsonSchema,
    CreateExpectationSuiteFromAvroSchema,
    RunValidation,
)
import wemmick.api

app = typer.Typer()
avro = typer.Typer()
jsonschema = typer.Typer()
app.add_typer(avro, name="avro", help="Create suites from avro schema files.")
app.add_typer(
    jsonschema, name="jsonschema", help="Create suites from JSONSschema files."
)


def get_data_context():
    typer.echo("Loading Great Expectations project...")
    with click_spinner.spinner():
        data_context = wemmick.api.get_data_context()
    return data_context


class CLICreateExpectationSuiteFromAvroSchema(CreateExpectationSuiteFromAvroSchema):
    def get_schema(self):
        typer.echo("Loading schema...")
        with click_spinner.spinner():
            avro_schema = super().get_schema()
        return avro_schema

    def create_suite(self):
        typer.echo("Generating suite...")
        with click_spinner.spinner():
            super().create_suite()

    def build_docs(self):
        typer.echo("Building docs...")
        with click_spinner.spinner():
            super().build_docs()


@avro.command(name="file")
def avro_file(filename: str, verbose: bool = False):
    """Create an Expectation Suite from an avro schema file."""
    data_context = get_data_context()

    create_suite = CLICreateExpectationSuiteFromAvroSchema(
        file_path=filename, data_context=data_context, verbose=verbose
    )
    try:
        create_suite.run()
    except ValueError as e:
        typer.secho(
            str(e), fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Abort()


@avro.command(name="glob")
def avro_glob(pattern: str, verbose: bool = False):
    """Create Suites avro schema files matching a glob pattern."""
    typer.echo(f"Profiling files matching pattern {pattern}...")
    with click_spinner.spinner():
        context = ge.DataContext()
        base_dir = file_relative_path(__file__, ".")
        profiler = AvroSchemaFileProfiler(
            base_directory=base_dir, verbose=verbose, printer=typer.echo
        )
        suites = profiler.run(glob_pattern=pattern)
        for suite in suites:
            context.save_expectation_suite(suite)
            typer.echo(f"Saved expectation suite {suite.expectation_suite_name}")

    typer.secho(f"Processed {len(suites)} avro files.", fg=typer.colors.BRIGHT_GREEN)


# TODO: add missing functionality that was present in cli code that was refactored
class CLICreateExpectationSuiteFromJsonSchema(CreateExpectationSuiteFromJsonSchema):
    def get_schema(self):
        typer.echo("Loading schema...")
        with click_spinner.spinner():
            json_schema = super().get_schema()
        return json_schema

    def create_suite(self):
        typer.echo("Generating suite...")
        with click_spinner.spinner():
            super().create_suite()

    def build_docs(self):
        typer.echo("Building docs...")
        with click_spinner.spinner():
            super().build_docs()

    def verbose_print(self, string):
        typer.echo(highlight(string, JsonLexer(), Terminal256Formatter()))


@jsonschema.command(name="file")
def json_file(filename: str, suite_name: str, verbose: bool = False):
    """Create an Expectation Suite from a JSONSchema file."""
    data_context = get_data_context()

    create_suite = CLICreateExpectationSuiteFromJsonSchema(
        file_path=filename,
        suite_name=suite_name,
        data_context=data_context,
        verbose=verbose,
    )
    try:
        create_suite.run()
    except ValueError as e:
        typer.secho(
            str(e), fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Abort()


class CLIRunValidation(RunValidation):
    def get_batch(self):
        typer.echo(
            f"Loading batch from datasource: {self.datasource} table: {self.table}..."
        )
        with click_spinner.spinner():
            batch = super().get_batch()
        return batch

    def run_validation_operator(self, batch):
        typer.echo(f"Running validations against suite {self.suite_name}...")
        with click_spinner.spinner():
            super().run_validation_operator(batch)

    def on_success(self):
        typer.secho("validation succeeded", fg=typer.colors.BRIGHT_GREEN)
        sys.exit(0)

    def on_failure(self):
        typer.secho("validation failed", fg=typer.colors.BRIGHT_RED)
        sys.exit(1)


@app.command()
def validate(
    datasource: str = typer.Option(
        ..., "--datasource", "-d", help="datasource name from great_expectations.yml"
    ),
    table: str = typer.Option(..., "--table", "-t", help="table name"),
    suite: str = typer.Option(..., "--suite", "-s", help="expectation suite name"),
):
    data_context = get_data_context()
    run_validation = CLIRunValidation(
        datasource=datasource, table=table, suite_name=suite, data_context=data_context
    )
    run_validation.run()


if __name__ == "__main__":
    app()
