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
1. Addition of project specific dependencies such as sql drivers must also be built into the docker image. This is a
high maintenance task.
1. Great Expectations project comes configured for local storage for expectation suites, validation results, and data
docs. This can result in data loss in stateless execution of containers.

Technical Debt areas:
1. While Wemmick CLI and gRPC interface share the same code for the same operations the REST API does not. This can
result in unexpected differences for the same operation done through different interfaces.
1. Docker base Python image size could be minimized. This will allow for a small footprint.
1. Wemmick dependencies are not pinned. This can result in a working project breaking in a new image build.

## Considered Options:
1.
