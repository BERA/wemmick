import great_expectations as ge


def list_datasources():
    context = ge.DataContext()
    return context.list_datasources()


def list_expectation_suites():
    context = ge.DataContext()
    return context.list_expectation_suites()
