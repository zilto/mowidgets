import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import mowidgets

    from file_browser import app as file_browser_app
    from multiply import app as multiply_app
    return file_browser_app, mowidgets, multiply_app


@app.cell
async def _(file_browser_app, mowidgets):
    file_brower_widget = mowidgets.widgetize(file_browser_app)
    await file_brower_widget
    return


@app.cell
async def _(mowidgets, multiply_app):
    multiply_widget = mowidgets.widgetize(multiply_app, data_access="r")
    await multiply_widget
    return (multiply_widget,)


@app.cell
def _(multiply_widget):
    multiply_widget.data
    return


@app.cell
def _(multiply_widget):
    multiply_widget["number2"]
    return


if __name__ == "__main__":
    app.run()
