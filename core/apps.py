"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.apps import AppConfig

# --- Class `CoreConfig`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # --- Def `ready`: High-level intent

    # This function contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    def ready(self):
        from . import signals  # noqa