import pytest
import sys
import os
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
)
from tech_stack_app_init import manageApp



@pytest.fixture
def app():
    flask_app = manageApp()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
