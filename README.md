# wemmick

This is a small Data quality CLI written in python that includes Great Expectations extensions.

The main command in this project is `wemmick` which has many uses:

- Create suites from AVRO files
- Create suites from JSON Schema files
- Run any existing expectations suite against any table in any existing datasource

## Installation

- Create a new python virtualenv `make venv`
- Activate the environment by running: `source venv/bin/activate`
- From the package root run `make install`
- This package installs a cli command called `wemmick`. Run this to verify installation.

## Running commands in python

- Run the CLI with `wemmick --help` to see available of commands
- Create a suite from a JSON Schema file run `wemmick jsonschema file <YOUR_FILE.json> <SUITE_NAME>`
- Create a suite from a AVRO Schema file run `wemmick avro file <YOUR_FILE.avsc> <SUITE_NAME>`
- Create a suite from all AVRO Schema files matching a glob pattern run `wemmick avro glob *.avsc <SUITE_NAME>`

### Validations

To run a validation use the subcommand `validation`.

For example, to validate the `resp.warning` expectations suite on `resp` table in the `release` database:

```bash
wemmick validate \
--datasource release \
--table resp
--suite resp.warning
```

Data source must be defined in `great_expectations.yml` file.
Suite is the expectations suite that must exist in `./expectations` path.

## Development Setup

1. Follow the installation instructions above.
2. From the package root run `pip install -r requirements-dev.txt`
3. Run your tests with `make test`

## Debugging / Troubleshooting

Make a new virtualenv

1. `make venv` (this deactivates the venv, deletes it, and makes a new one)
2. repeat development setup instructions
