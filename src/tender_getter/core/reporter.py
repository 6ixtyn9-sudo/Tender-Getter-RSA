"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.reporter`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..reporter import *  # noqa: F401,F403
