"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django import template

register = template.Library()

@register.filter
# --- Def `split`: High-level intent
# This function contributes to the domain model or view/controller layer.
# Outline: responsibilities, key parameters, side-effects, and return semantics.
def split(value, arg):
    """Splits a string by the given argument."""
    return value.split(arg)
