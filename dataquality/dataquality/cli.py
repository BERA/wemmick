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

from dataquality.avro_schema_profiler import AvroSchemaFileProfiler
from dataquality.utils import file_relative_path

app = typer.Typer()
avro = typer.Typer()
jsonschema = typer.Typer()
app.add_typer(avro, name="avro", help="Create suites from avro schema files.")
app.add_typer(
    jsonschema, name="jsonschema", help="Create suites from JSONSschema files."
)


@app.command()
def validate(
    datasource: str = typer.Option(
        ..., "--datasource", "-d", help="datasource name from great_expectations.yml"
    ),
    table: str = typer.Option(..., "--table", "-t", help="table name"),
    suite: str = typer.Option(..., "--suite", "-s", help="expectation suite name"),
):
    """Run great_expectations on a table."""
    typer.echo(f"Loading Great Expectations...")
    with click_spinner.spinner():
        context = ge.DataContext()

    typer.echo(f"Loading batch from datasource: {datasource} table: {table}...")
    with click_spinner.spinner():
        batch_kwargs = {"table": table, "datasource": datasource}
        batch = context.get_batch(batch_kwargs, suite)

    typer.echo(f"Running validations against suite {suite}...")
    with click_spinner.spinner():
        results = context.run_validation_operator(
            "action_list_operator", assets_to_validate=[batch],
        )

    if not results["success"]:
        typer.secho("validation failed", fg=typer.colors.BRIGHT_RED)
        sys.exit(1)

    typer.secho("validtion succeeded", fg=typer.colors.BRIGHT_GREEN)
    sys.exit(0)


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


@jsonschema.command(name="file")
def json_file(filename: str, suite_name: str, verbose: bool = False):
    """Create an Expectation Suite from a JSONSchema file."""
    if not os.path.isfile(filename):
        typer.secho(
            f"File {filename} was not found. Please check the path and try again.",
            fg=typer.colors.BRIGHT_RED,
        )
        raise typer.Abort()

    typer.echo("Loading Great Expectations project...")
    with click_spinner.spinner():
        try:
            context = ge.data_context.DataContext()
        except ge.exceptions.GreatExpectationsError as e:
            typer.secho(e.message, fg=typer.colors.BRIGHT_RED)
            raise typer.Abort()

    typer.echo("Loading schema...")
    with open(filename, "r") as f:
        try:
            raw_json = f.read()
            schema = json.loads(raw_json)
        except json.decoder.JSONDecodeError as e:
            typer.secho(f"JSON Failed to parse: {e}", fg=typer.colors.BRIGHT_RED)
            raise typer.Abort()
        if verbose:
            typer.echo(highlight(raw_json, JsonLexer(), Terminal256Formatter()))

    typer.echo("Generating suite...")
    with click_spinner.spinner():
        profiler = JsonSchemaProfiler()
        suite = profiler.profile(schema, suite_name)
        context.save_expectation_suite(suite)
        if verbose:
            typer.echo(highlight(str(suite), JsonLexer(), Terminal256Formatter()))

    typer.echo("Building docs...")
    with click_spinner.spinner():
        context.build_data_docs()
        context.open_data_docs()


if __name__ == "__main__":
    app()
