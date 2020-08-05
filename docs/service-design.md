# Service Design
- Status: Draft
- Deciders: Hammad, Taylor, Tom
- Date: 2020-08-03

## Context and Problem:
Wemmick is a containerized runtime for running Great Expectations projects. It was developed to ease the barrier to
entry in getting started with Great Expectations by providing a working runtime environment. This ADR intends to further
the mission of Wemmick more towards a service layer for Great Expectations. It will address areas for improvement that
can make Wemmick the easiest way to integrate Great Expectations into a team's automated or semi-automated data
workflow.

As of current there are a multiple interfaces to perform tasks on Wemmick:
- Great Expectations CLI
- Wemmick CLI
- Wemmick gRPC Interface
- Wemmick REST API

Room for improvement areas:
1. For a serverless compute environments a Great Expectations project must be built into the docker image. This is a
high maintenance task.
1. Addition of project specific python dependencies such as sql drivers must also be built into the docker image. This
is a high maintenance task.
1. Great Expectations project comes with stores configured for local storage of expectation suites, validation results,
and data docs. This can result in data loss in stateless execution of containers.

Technical Debt areas:
1. While Wemmick CLI and gRPC interface share the same code for the same operations the REST API does not. This can
result in unexpected differences for the same operation done through different interfaces.
1. Docker base Python image size could be minimized. This will allow for a small footprint.
1. Wemmick dependencies are not pinned. This can result in a working project breaking in a new image build.

## Considered Options:

### Loading Great Expectations Project:
a. Configure Great Expectation project by setting GE_GIT_URL environment variable for project's git source and related
credentials (i.e Github token). Add a custom entrypoint script that performs shallow clone on container start. If the
entrypoint parameter is set on docker run, it would override the entrypoint script and break functionality.

b. Configure Great Expectation project by setting GE_GIT_URL environment variable for project's git source and related
credentials (i.e Github token). On server start it would perform a shallow clone of the project. For Wemmick CLI it
would check in `get_data_context` method and perform a shallow clone if project is missing. Unfortunately the Great
Expectations CLI would still require mounting or building the project into the image and be broken without it.

c. Leave it as-is. Add a note in README advising teams to setup CI/CD to automate build and deploy of their Wemmick
images with their Great Expectations project included.

### Adding Project Specific Python Dependencies
a. Add a custom entrypoint script that performs pip on container start. If the entrypoint parameter is set on docker
run, it would override the entrypoint script and break functionality.

b. On server start run install of python dependencies from `requirements-extras.txt` in Great Expectation project
directory by utilizing [subprocess install]https://stackoverflow.com/a/50255019/2722398). This won't work for Great
Expectations CLI.

c. Move `requirements-extras.txt` into Great Expectations project directory and add install step in Dockerfile. Add a
note in README advising teams to setup CI/CD to automate build and deploy of their Wemmick images with their Great
Expectations project included.

### Stores Configuration:
a.
