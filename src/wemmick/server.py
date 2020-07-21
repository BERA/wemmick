"""
This super bare bones http server triggers great_expectations.

Google Cloud Run requires that docker containers run http servers. Furthermore,
Google Cloud Scheduler can only trigger Run jobs via http or pub/sub. Hence the
creation of this ultra-bare bones server that wraps a few functions of the
great_expectations DataContext.

https://cloud.google.com/run/docs/reference/container-contract#port
"""

import great_expectations as ge
import sqlalchemy
from fastapi import BackgroundTasks, FastAPI, HTTPException
from great_expectations.data_asset import DataAsset
from great_expectations.exceptions import DataContextError

app = FastAPI()


def load_ge_datacontext() -> ge.DataContext:
    context = ge.DataContext()
    print(f"Using {context.root_directory} as GE project root")
    return context


# Force loading of a datacontext to catch failures before server starts
context = load_ge_datacontext()


@app.get("/health")
def health():
    context = load_ge_datacontext()
    return isinstance(context, ge.DataContext)


@app.get("/datasources")
def datasource_list():
    context = load_ge_datacontext()
    return {"datasources": context.list_datasources()}


@app.get("/suites")
def suite_list():
    context = load_ge_datacontext()
    return {"datasources": context.list_expectation_suites()}


@app.get("/checkpoints")
def checkpoint_list():
    context = load_ge_datacontext()
    return {"checkpoints": context.list_checkpoints()}


@app.get("/validate")
async def validate(
    datasource: str, table: str, suite: str, background_tasks: BackgroundTasks
):
    """
    Trigger a validation to run in the background.
    """
    context = load_ge_datacontext()
    batch_kwargs = {"table": table, "datasource": datasource}
    try:
        batch = context.get_batch(batch_kwargs, suite)
        assert isinstance(batch, DataAsset)
    except sqlalchemy.exc.NoSuchTableError:
        raise HTTPException(
            status_code=404,
            detail=f"The table {table} could not be found. Please verify datasource and table.",
        )
    except AssertionError:
        raise HTTPException(
            status_code=404,
            detail="The batch failed to load. Please verify datasource, table and suite.",
        )
    except DataContextError as e:
        raise HTTPException(status_code=404, detail=str(e))

    message = f"Validation of a batch ({batch.batch_id}) from datasource: {datasource} table: {table} against suite {suite} running in the background."
    background_tasks.add_task(
        context.run_validation_operator,
        "action_list_operator",
        assets_to_validate=[batch],
    )

    return {
        "datasource": datasource,
        "table": table,
        "suite": suite,
        "message": message,
    }


# TODO add Checkpoint runner
