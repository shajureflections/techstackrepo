from flasgger import Swagger


def swagger_init(app):
    app.config["SWAGGER"] = {"title": "Tech Stack API", "uiversion": 3}
    SWAGGER_TEMPLATE = {"securityDefinitions": {"APIKeyHeader": {"type": "apiKey", "name": "x-access-token", "in": "header"}}}
    Swagger(app, template=SWAGGER_TEMPLATE)
