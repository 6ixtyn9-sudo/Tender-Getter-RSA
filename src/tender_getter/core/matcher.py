"""Deprecated compatibility facade.

Canonical implementation: :mod:`tender_getter.matcher`.  This module deliberately
re-exports it so legacy imports cannot diverge from the running implementation.
"""
from ..matcher import *  # noqa: F401,F403
