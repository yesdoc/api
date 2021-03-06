# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.tokenFields import TokenFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_401
from app.mod_profiles.common.swagger.responses.token import code_200 as code_200_token


class Token(Resource):
    # TODO: Añadir parámetros de autenticación a la documentación Swagger.
    @swagger.operation(
        notes=(u'Retorna un token válido para la autenticación del usuario, '
               'por un período de tiempo acotado. Requiere información de '
               'autenticación, ya sea nombre de usuario y contraseña, o un '
               'token del usuario que no haya expirado.').encode('utf-8'),
        responseClass='TokenFields',
        nickname='token_get',
        responseMessages=[
            code_200_token,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(TokenFields.resource_fields, envelope='resource')
    def get(self):
        token = g.user.generate_auth_token(3600)
        new_token = {'token': token.decode('ascii'), 'duration': 3600}
        return new_token
