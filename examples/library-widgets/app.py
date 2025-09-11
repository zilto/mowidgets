import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # Loading external widgets

    `mowidgets` makes it easy for libraries to distribute custom-built widgets for marimo notebooks.

    This notebook shows how to use a widget packaged with the [dlt](https://github.com/dlt-hub/dlt) Python library. The widget allows to view the pipeline state.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ## Running a `dlt` pipeline
    First, we run a `dlt` pipeline to ingest data from a REST API. This will produce data to render with our widget.
    """
    )
    return


@app.cell
def _():
    import dlt
    from dlt.sources.rest_api import rest_api_source
    return dlt, rest_api_source


@app.cell
def _(dlt, rest_api_source):
    jaffle_source = rest_api_source({
        "client": {"base_url": "https://jaffle-shop.dlthub.com/api/v1"},
        "resources": ["customers", "products", "stores"],
    })

    pipeline = dlt.pipeline("jaffle_shop", destination="duckdb")

    pipeline.run(jaffle_source)
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ## Use a dlt widget
    Import `mowidgets` and retrieve the widget from `dlt.hepers.marimo`
    """
    )
    return


@app.cell
def _():
    import mowidgets
    from dlt.helpers.marimo import load_package_viewer
    return load_package_viewer, mowidgets


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""As required, by `mowidgets.widgetize()`, the object `schema_viewer` is a `marimo.App` object. In other words, it represents an entire marimo notebook.""")
    return


@app.cell
def _(load_package_viewer):
    type(load_package_viewer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Call `mowidgets.widgetize()` on it to assign it to a variable. Use `await` in front of the object to render it!""")
    return


@app.cell
def _(load_package_viewer, mowidgets):
    load_package_viewer_widget = mowidgets.widgetize(load_package_viewer)
    return (load_package_viewer_widget,)


@app.cell
async def _(load_package_viewer_widget):
    await load_package_viewer_widget
    return


if __name__ == "__main__":
    app.run()
