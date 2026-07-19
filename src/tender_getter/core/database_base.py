"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.database_base`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..database_base import *  # noqa: F401,F403
