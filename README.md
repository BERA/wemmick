# wemmick

Wemmick is character in both Great Expectations and our data validation story.
This project deliveries a portal GE runtime to use in our various data validation/quality checkpoints. 

All code should be generic and appropriate to an open source repo - no bundled expectations that hint at our schemata or survey structure.

## What are the requirements for this repo?

- [ ] It is a public GH Project with CI/CD.
- [ ] It contains a docker image with vanilla Great Expectations.
- [ ] It contains a docker image with our CLI wrapper (currently called 'dataquality' in sdap/qa).
- [ ] It should **not** contain anything non-proprietary.

## Vanilla Great Expectations Docker Image

### Requirements

- [ ] This image should include pinned versions of Great Expectations.
- [ ] The entrypoint should be flexible enough to run any `great_expectations` command and any other shell command.
- [ ] This image should include enough drivers to run validations against many types of datasources, including flat files, GCP backends, etc.


## Bera CLI Wrapper Docker Image

### Requirements

- [ ] This image should inherit from the vanilla Great Expectations image.
- [ ] This image should include pinned versions of `dataquality`.
- [ ] The entrypoint should be flexible enough to run any `great_expectations` command and commands from `dataquality`.

## CI/CD

- [ ] This repo should have CI/CD
- [ ] **Question: Should the CI/CD build and publish images to an image registry? If so, which one?**

