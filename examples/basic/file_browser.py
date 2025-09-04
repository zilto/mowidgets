import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import pathlib

    import marimo as mo


@app.cell
def _():
    cwd = pathlib.Path().cwd()
    file_browser = mo.ui.file_browser(initial_path=cwd, selection_mode="file")
    file_browser
    return


if __name__ == "__main__":
    app.run()
