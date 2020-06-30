# wemmick

Wemmick is character in both Great Expectations and our data validation story.
This project deliveries a portal GE runtime to use in our various data validation/quality checkpoints. 

All code should be generic and appropriate to an open source repo - no bundled expectations that hint at our schemata or survey structure.

## What are the requirements for this repo?

- [ ] It is a public GH Project with CI/CD.
- [ ] It contains a docker image with vanilla Great Expectations.
- [ ] It contains a docker image with our CLI wrapper (currently called 'dataquality' in sdap/qa).
- [ ] It should **not** contain anything proprietary.

## Vanilla Great Expectations Docker Image

### Requirements

- [ ] This image should include pinned versions of Great Expectations.
- [ ] The entrypoint should be `great_expectations` command and can be overridden in a child image if needed.
- [ ] This image should include enough drivers to run validations against many types of datasources, including flat files, GCP backends, etc.


## Wemmick Docker Image

### Requirements

- [ ] This image should inherit from the vanilla Great Expectations image.
- [ ] This image should include pinned versions of `dataquality`.
- [ ] The entrypoint should be flexible enough to run any `great_expectations` command and commands from `dataquality`.
- [ ] This image should include the http server for use with Google Cloud Run validations.

## CI/CD

- [ ] This repo should use the official GH action as CI/CD. It supports targets, so a single multi-stage dockerfile https://github.com/marketplace/actions/build-and-push-docker-images#target can be used.
- [ ] This repo should use semantic release for tagging and dependabot bumping the wemmick image when there is a new base image released.
- [ ] **Question: Should the CI/CD build and publish images to an image registry? If so, which one?**
    - GCR for fast pull in our GCP clients. If needed, we are fine with GitHub and Docker Hub too.i
- [ ] This repo should use the GitHub super linter action against all code.

