from flasgger import Swagger

template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Jogos Gratuitos",
        "description": "Documentação da API com usuários e jogos",
        "version": "1.0.0",
    },
    "basePath": "/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT token - ex: Bearer {seu_token}",
        }
    },
}


def configurar_swagger(app):
    Swagger(app, template=template)
