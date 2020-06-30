# wemmick

Wemmick is character in both Great Expectations and our data validation story.
This project deliveries a portal GE runtime to use in our various data validation/quality checkpoints. 

All code should be generic and appropriate to an open source repo - no bundled expectations that hint at our schemata or survey structure.


This repo:

- is a public GH Project with CICD
- contains a docker image with vanilla Great Expectations
- contains a docker image with our CLI wrapper (currently called 'dataquality' in sdap/qa)
- should **not** contain anything non-proprietary

