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
from wemmick.api import CreateExpectationSuiteFromJsonSchema, RunValidation

app = typer.Typer()
avro = typer.Typer()
jsonschema = typer.Typer()
app.add_typer(avro, name="avro", help="Create suites from avro schema files.")
app.add_typer(
    jsonschema, name="jsonschema", help="Create suites from JSONSschema files."
)


@avro.command(name="file")
def avro_file(filename: str, verbose: bool = False):
    """Create an Expectation Suite from an avro schema file."""
    if not os.path.isfile(filename):
        typer.secho(
            f"File {filename} was not found. Please check the path and try again.",
            fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Abort()

    typer.echo(f"Profiling {filename}..")
    with click_spinner.spinner():
        context = ge.DataContext()
        base_dir = file_relative_path(__file__, ".")
        profiler = AvroSchemaFileProfiler(
            base_directory=base_dir, verbose=verbose, printer=typer.echo
        )
        suites = profiler.run(filename=filename)

        for suite in suites:
            typer.echo(f"Saving expectation suite {suite.expectation_suite_name}")
            context.save_expectation_suite(suite)

    typer.secho(f"Processed {len(suites)} avro files.", fg=typer.colors.BRIGHT_GREEN)


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
    def get_data_context(self):
        typer.echo("Loading Great Expectations project...")
        with click_spinner.spinner():
            data_context = super().get_data_context()
        return data_context

    def get_json_schema(self):
        typer.echo("Loading schema...")
        with click_spinner.spinner():
            json_schema = super().get_json_schema()
        return json_schema

    def create_suite(self, context, json_schema: str, suite_name: str):
        typer.echo("Generating suite...")
        with click_spinner.spinner():
            super().create_suite(
                context, json_schema=json_schema, suite_name=suite_name
            )

    def build_docs(self, context):
        typer.echo("Building docs...")
        with click_spinner.spinner():
            super().build_docs(context)


@jsonschema.command(name="file")
def json_file(filename: str, suite_name: str, verbose: bool = False):
    """Create an Expectation Suite from a JSONSchema file."""
    create_suite = CLICreateExpectationSuiteFromJsonSchema(
        file_path=filename, suite_name=suite_name
    )
    create_suite.run()


class CLIRunValidation(RunValidation):
    def get_data_context(self):
        typer.echo("Loading Great Expectations project...")
        with click_spinner.spinner():
            data_context = super().get_data_context()
        return data_context

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
    run_validation = CLIRunValidation(
        datasource=datasource, table=table, suite_name=suite
    )
    run_validation.run()


if __name__ == "__main__":
    app()
