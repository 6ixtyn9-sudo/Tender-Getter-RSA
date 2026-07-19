"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.schemas`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..schemas import *  # noqa: F401,F403
