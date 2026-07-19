"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.parser`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..parser import *  # noqa: F401,F403
