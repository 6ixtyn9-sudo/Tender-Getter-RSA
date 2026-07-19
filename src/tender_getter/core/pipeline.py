"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.pipeline`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..pipeline import *  # noqa: F401,F403
