# wemmick

Wemmick is character in both Great Expectations and our data validation story.
This project deliveries a portal GE runtime to use in our various data validation/quality checkpoints.

All code should be generic and appropriate to an open source repo - no bundled expectations that hint at our schemata or survey structure.

## What are the requirements for this repo?

- [x] It is a public GH Project with CI/CD.
- [x] It contains a docker image with vanilla Great Expectations.
- [x] It contains a docker image with our CLI wrapper (currently called 'wemmick' in sdap/qa).
- [x] It should **not** contain anything proprietary.

## Vanilla Great Expectations Docker Image

- [x] This image should include pinned versions of Great Expectations.
- [x] The entrypoint should be `great_expectations` command and can be overridden in a child image if needed.
- [x] This image should include enough drivers to run validations against many types of datasources, including flat files, GCP backends, etc.

## Wemmick image

- [x] This image should inherit from the vanilla Great Expectations image.
- [x] The entrypoint should be flexible enough to run any `great_expectations` command and commands from `wemmick`.

## Wemmick HTTP server image

- [ ] This image should inherit from the wemmick image.
- [ ] The entrypoint should run the server process for use with Google Cloud Run validations.

## CI/CD

- [x] This repo should use the [official GH action](https://github.com/marketplace/actions/build-and-push-docker-images#target) as CI/CD. It supports targets, so a single multi-stage dockerfile can be used.
- [ ] This repo should use semantic release for tagging and dependabot bumping the wemmick image when there is a new base image released.
- [ ] **Question: Should the CI/CD build and publish images to an image registry? If so, which one?**
  - GCR for fast pull in our GCP clients. If needed, we are fine with GitHub and Docker Hub too.
- [x] This repo should use the GitHub super linter action against all code.
