# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.groupMembershipFields import GroupMembershipFields
from app.mod_profiles.common.parsers.profileGroupMembership import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_401, code_404


class MyGroupMembershipList(Resource):
    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de membresías de, '
               'grupo, del usuario autenticado.').encode('utf-8'),
        responseClass='GroupMembershipFields',
        nickname='myGroupMembershipList_get',
        parameters=[
            {
                "name": "group",
                "description": (u'Identificador único del grupo. Permite '
                                'filtrar las membresías, para sólo obtener '
                                'las asociadas al grupo especificado.').encode('utf-8'),
                "required": False,
                "dataType": "int",
                "paramType": "query"
            },
        ],
        responseMessages=[
            code_200_found,
            code_401,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupMembershipFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil.
        profile = g.user.profile

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        group_id = args['group']

        # Obtiene todas las membresías de grupo asociadas al perfil.
        profile_memberships = profile.memberships

        # Filtra las membresías por grupo.
        if group_id is not None:
            profile_memberships = profile_memberships.filter_by(group_id=group_id)

        profile_memberships = profile_memberships.all()
        return profile_memberships
