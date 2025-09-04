import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell
def _():
    number1_ui = mo.ui.number()
    number1_ui
    return (number1_ui,)


@app.cell
def _():
    number2_ui = mo.ui.number()
    number2_ui
    return (number2_ui,)


@app.cell
def _(number1_ui, number2_ui):
    number1 = number1_ui.value
    number2 = number2_ui.value
    try:
        product = number1 * number2
    except TypeError:
        product = None
    product
    return


if __name__ == "__main__":
    app.run()
