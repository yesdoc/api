# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import Gender
from app.mod_profiles.common.fields.genderFields import GenderFields
from app.mod_profiles.common.parsers.gender import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class GenderView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de género.'.encode('utf-8'),
        responseClass='GenderFields',
        nickname='genderView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del género.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(GenderFields.resource_fields, envelope='resource')
    def get(self, id):
        gender = Gender.query.get_or_404(id)
        return gender

    @swagger.operation(
        notes=u'Actualiza una instancia específica de género, y la retorna.'.encode('utf-8'),
        responseClass='GenderFields',
        nickname='genderView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del género.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "name",
              "description": u'Nombre del género.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del género.'.encode('utf-8'),
              "required": False,
              "dataType": "string",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(GenderFields.resource_fields, envelope='resource')
    def put(self, id):
        gender = Gender.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['name'] is not None and
              gender.name != args['name']):
            gender.name = args['name']
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (args['description'] is not None and
              gender.description != args['description']):
            gender.description = args['description']

        db.session.commit()
        return gender, 200
