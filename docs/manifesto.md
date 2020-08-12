# Wemmick Manifesto
This manifesto is a means to share the vision of Wemmick through principles that help guide present and future product
development. This is an evolving piece that will grow with new learnings.

### Problem
Setting up and running a Great Expectations project locally is a low difficulty task that can be done fairly quickly.
When it comes to integrating the same project into a team's data workflow it proves to be quite challenging. It requires
setting up a compatible python environment, related dependencies, compute infrastructure, and Python scripts that enable
running checkpoints (validations) on event or ad-hoc triggers.

In short although the tool is simple to integrate into a local development workflow it is far more difficult to setup
in a teams automated workflow. This is the problem that Wemmick seeks to solve.

### Desired Characteristics
In the product development of Wemmick it will aim to be a service layer for Great Expectations. A self-hosted setup-once
software that makes integrating Great Expectations into a team's data workflow far simpler. To fit this requirement it
shall have the following characteristics:

- **low-maintenance**: requires near zero maintenance tasks for the user and easy updates
- **containerized**: comes packaged and ready to run on any cloud environment
- **zero code**: minimizes custom code or development knowledge for most uses cases
- **configurable**: easy to configure without code while offering more advanced configuration through custom code
  modules
- **easy**: interface is intuitive as possible with sensible defaults

### Features Fitment Checklist:

- [ ] will this feature introduce any user maintenance?
- [ ] will this feature introduce any backwards compatibility issues?
- [ ] are interfaces setup to configure this feature without custom code?
- [ ] can this feature be configured for advanced use cases?
- [ ] is the feature's interface intuitive?
- [ ] are all parameters set with sensible defaults?