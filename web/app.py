"""Pyodide / panel-convert entry. Do not call pn.serve here."""

from main import make_app

make_app().servable()
