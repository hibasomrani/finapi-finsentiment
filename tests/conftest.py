"""Fixtures partagees entre tests."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


@pytest.fixture
def client():
    """Client Flask de test (pas de vrai serveur)."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()
