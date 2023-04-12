import os
import sys
import json
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import swagger

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common")
)

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "repository"
    )
)
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "middleware"
    )
)
import models


def manageApp():
    """Handles app startup.

    Args:

    Returns:
        app object
    """
    load_dotenv(override=True)

    app = Flask(__name__)

    # Secret Key Integration
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    app.config["SECRET_KEY"] = SECRET_KEY
    import techstack
    import models

    # Swagger Integration
    swaggerapp = swagger.swagger_init(app)

    # app.app_context().push()
    # storing secrete manager cache object to secret_cache

    # configuring log
    

    # database integration
    # Base, engine = database_config()

    models.Base.metadata.create_all(models.engine)
    techstack.techstack_init(app)
    CORS(app, allow_headers="authorization_key,content-type", origins="*")

    return app
