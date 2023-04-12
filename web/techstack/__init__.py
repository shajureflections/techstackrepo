import os
import sys

from .hello_world import hello_world_test
from .todoapi import todo_app

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "common",
    )
)


def techstack_init(app):
    app.register_blueprint(hello_world_test, url_prefix="/user")
    app.register_blueprint(todo_app, url_prefix="/task")
