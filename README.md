# wemmick

This is a small Data quality CLI written in python that includes Great Expectations extensions.

The main command in this project is `wemmick` which has many uses:

- Create suites from AVRO files
- Create suites from JSON Schema files
- Run any existing expectations suite against any table in any existing datasource

This repo provides the library which can be run within a local python environment and docker images for portable runtimes.

## wemmick command reference

Note that these commands can be invoked directly in python or by invoking a docker image.
If using docker substitute `docker run -v "$(pwd):/ge" beradev/wemmick:latest` for `wemmick` in the list below:

- Run the CLI with `wemmick --help` to see available of commands
- Create a suite from a JSON Schema file run `wemmick jsonschema file <YOUR_FILE.json> <SUITE_NAME>`
- Create a suite from a AVRO Schema file run `wemmick avro file <YOUR_FILE.avsc> <SUITE_NAME>`
- Create a suite from all AVRO Schema files matching a glob pattern run `wemmick avro glob *.avsc <SUITE_NAME>`
- To run a validation use the subcommand `validation`.
  - For example, to validate the `resp.warning` expectations suite (which is the expectations suite that must exist in `.great_expectations/expectations` directory) on `resp` table in the `release` datasource (which must be defined in `great_expectations.yml` file):

    ```bash
    wemmick validate \
    --datasource release \
    --table resp \
    --suite resp.warning
    ```

## Great Expectations common command reference

Great Expectations has a full featured command line interface.
To find out more run `great_expectations --help`. Here are a few of the most commonly used commands:
If using docker substitute `docker run -v "$(pwd):/ge" beradev/wemmick:ge-0.11.7` for `great_expectations` in the list below:

- Adding a new datasource: `great_expectations datasource new`
- List datasources: `great_expectations datasource list`
- List expectation suites: `great_expectations suite list`
- Scaffold a new expectation suite: `great_expectations suite scaffold <SUITE_NAME>`
- Adding a new expectations suite: `great_expectations suite new`
- Editing expectations suite: `great_expectations suite edit <SUITE_NAME>`
- Adding a new checkpoint: `great_expectations checkpoint new <CHECKPOINT_NAME> <SUITE_NAME>`
- Run a checkpoint: `great_expectations checkpoint run <CHECKPOINT_NAME>`

## Wemmick gRPC interface

See [wemmick.proto]("src/wemmick/protos/wemmick.proto") for interface definitions.

Examples of running Wemmick operations using [grpcurl](https://github.com/fullstorydev/grpcurl) hosted locally on port 50051

- Create a suite from a JSON Schema file: `grpcurl -plaintext -d '{"file_path": "file:///example.json", "suite_name": "example"}' localhost:50051 wemmick.Wemmick.CreateExpectationSuiteFromJsonSchema`
- Create a suite from a AVRO Schema file: `grpcurl -plaintext -d '{"file_path": "file:///example.avsc", "suite_name": "example"}' localhost:50051 wemmick.Wemmick.CreateExpectationSuiteFromAvroSchema`
- Run a validation: `grpcurl -plaintext -d '{"datasource": "release", "table": "resp", "suite_name": "resp.warning"}' localhost:50051 wemmick.Wemmick.RunValidation`

## Great Expectations gRPC interace

See [wemmick.proto]("src/wemmick/protos/wemmick.proto") for interface definitions.

Examples of running Great Expectation operations using [grpcurl](https://github.com/fullstorydev/grpcurl) hosted locally on port 50051

- List datasources: `grpcurl -plaintext localhost:50051 wemmick.Wemmick/ListDataSources`
- List expectation suites: `grpcurl -plaintext localhost:50051 wemmick.Wemmick/ListExpectationSuites`

## Docker images

This project provides portable runtimes in the form of docker images.

### GE images

#### Running GE images

Run this with: `docker run -v "$(pwd):/ge" beradev/wemmick:ge-0.11.7`

This image assumes that your project's root is mounted at `/ge` so Great Expectations can find the `great_expectations` folder inside the container at `/ge/great_expectations`.

#### Building GE images

To build the GE image:
    - From the repo root run `docker build -t beradev/wemmick:ge-0.11.7 -f ge/Dockerfile ge`

Ideally images are only pushed from CI/CD.
To push the GE image:
    - run `docker push beradev/wemmick:ge-0.11.7`

### Wemmick images

#### Running wemmick images

This image assumes that your project's root is mounted at `/ge` so Great Expectations can find the `great_expectations` folder inside the container at `/ge/great_expectations`.

**To use this image as a Great Expectations CLI:**
- run this with: `docker run -v "$(pwd):/ge" --entrypoint great_expectations beradev/wemmick:latest`

**To use this image as a CLI:**
- run this with: `docker run -v "$(pwd):/ge" beradev/wemmick:latest`

**To use this image as an HTTP server:**
- run this with: `docker run -p 8080:8080 -v "$(pwd):/ge" --entrypoint /app/src/wemmick/start_server.py beradev/wemmick:latest`

**To use this image as an gRPC server:**
- run this with `docker run -p 50051:50051 -v "$(pwd):/ge" --entrypoint /app/src/wemmick/grpc_server.py beradev/wemmick:latest`

#### Building wemmick images

To build the wemmick image, run from repo root:
1. `(cd src; python -m grpc_tools.protoc -I wemmick/protos --python_out=. --grpc_python_out=. wemmick/protos/wemmick/*.proto)`
1. `docker build -t beradev/wemmick:latest -f Dockerfile .`

Ideally images are only pushed from CI/CD.
To push the wemmick image:
    - run `docker push beradev/wemmick:latest`

## Installation via python

- Create a new python virtualenv `make venv`
- Activate the environment by running: `source venv/bin/activate`
- From the package root run `make install`
- This package installs a cli command called `wemmick`. Run this to verify installation.

## Development Setup

1. Follow the installation instructions above.
2. From the package root run `pip install -r requirements-dev.txt`
3. Run your tests with `make test`

## Debugging / Troubleshooting

Make a new virtualenv

1. `make venv` (this deactivates the venv, deletes it, and makes a new one)
2. repeat development setup instructions


## Misc deployment notes

- Google Cloud Run has a limit of 15 minutes of execution.
- Cloud Run also assumes containers are stateless, therefore we store Great Expectations `Validation Results` on GCS in production.

