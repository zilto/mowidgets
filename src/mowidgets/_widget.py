from __future__ import annotations

from types import ModuleType
from typing import TYPE_CHECKING, Any, final

import marimo as mo
from marimo._plugins.ui._core.ui_element import UIElement

if TYPE_CHECKING:
    from collections.abc import Mapping


class _MoWidgetBase:
    """Base class to create widgets. Implements common functionalities"""
    def __init__(self, app: mo.App) -> None:
        self._app = app
        self._data = {}

    @final
    @property
    def data(self) -> FrozenDict:
        """Return a dictionary of data available to the user.
        Return `None` if it's intended to output no data.
        """
        return FrozenDict(**self._data)

    @final
    @data.setter
    def data(self, value: Any) -> None:
        raise RuntimeError("Can't set value on `.data`. Attribute is read-only.")

    @final
    def _display_(self) -> str:
        """Prints a readable string to the marimo cell."""
        return "Use `await` before the `widget` instance or call `await widget.display()` to render it."

    async def _update(self) -> mo.Html:
        """This internal method allows you to assign data to the state to return it via `data`"""
        result = await self._app.embed()
        self._data = _filter_defs(result.defs)
        return result.output

    @final
    async def display(self) -> mo.Html:
        """Renders the widget and outputs renderable marimo HTML.

        This is the public interface that calls the `._update()` method.
        Override `._update()` for custom widget behaviors.
        """
        return await self._update()

    @final
    def __await__(self):
        """Use `await _MoWidget()` to render it."""
        return (yield from self.display().__await__())

    @final
    def _ipython_key_completions_(self) -> list[str]:
        """Use IPython key completion system to provide suggestions to `__getitem__()`

        This is supported by marimo.
        """
        return list(self.data.keys())

    @final
    def __getitem__(self, key: str) -> Any:
        """Key access to the `.data` directly on the widget instance.

        For example, those two expressions are equivalent
        ```python
        w = MoWidget()
        w.data["foo"] == w["foo"]
        ```
        """
        return self.data[key]


class MoWidget(_MoWidgetBase):
    """Basic widget implementation. Provides data access."""


class DisplayMoWidget(_MoWidgetBase):
    """Read-only widget implementation. No data is stored on the widget."""

    @property
    def _data(self) -> dict:
        """Always returns an empty directory"""
        return {}

    @_data.setter
    def _data(self, value: Any) -> None:
        """Setter prevents setting value to the internal `._data`"""
        pass

    async def _update(self) -> mo.Html:
        """Update doesn't store anything on `._data`"""
        result = await self._app.embed()
        return result.output


class FrozenDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frozen = True

    def __setitem__(self, key, value):
        if getattr(self, '_frozen', False):
            raise RuntimeError("`FrozenDict` is read-only. Can only set values at `__init__`.")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if getattr(self, '_frozen', False):
            raise RuntimeError("`FrozenDict` is read-only. Can only delete values at `__init__`.")
        super().__delitem__(key)


def _filter_defs(defs: Mapping[str, Any]) -> dict[str, Any]:
    """Filter output data from the widget's `marimo.App`.
    Excludes Python modules and marimo UI elements.
    """
    data = {}
    for k in defs:
        try:
            value = defs[k]
        except Exception:
            continue

        if isinstance(value, (ModuleType, UIElement)):
            continue

        data[k] = value

    return data


def app_is_top_level_notebook_import(app: mo.App) -> bool:
    import __main__

    for v in vars(__main__).values():
        if app is v:
            return True

    return False


def widgetize(app: mo.App, *, data_access: bool = False) -> _MoWidgetBase:
    """Create a reusable `MoWidget` from a `marimo.App` instance. To properly
    refresh, the `marimo.App` variable needs to be imported in the context of
    the main notebook.

    For example:
        ```python
        # %% cell 1
        import mowidgets
        from my_project.marimo_app import app

        # %% cell 2
        w = mowidgets.widgetize(app)
        await w
        ```
    """
    if isinstance(app, ModuleType):
        # inspect if the module received contains a marimo `App`
        retrieved_app = getattr(app, "app", None)
        if isinstance(retrieved_app, mo.App):
            raise ValueError(
                "Received a Python module containing a `marimo.App`."
                " Start by importing the variable into the notebook via"
                f" `from {app.__name__} import app` and pass this value to `widgetize(app)`."
            )

    if not isinstance(app, mo.App):
        raise ValueError(f"Received `app` of type `{type(app)}`. Expected type `marimo.App`")

    if not app_is_top_level_notebook_import(app):
        raise ValueError(
            "To properly refresh, the `marimo.App` object needs to be imported at the top-level"
            " of the notebook. Import should look like `from my_project.my_marimo_notebook import app`."
        )

    if data_access:
        return MoWidget(app=app)
    else:
        return DisplayMoWidget(app=app)
