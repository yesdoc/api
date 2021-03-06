# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementUnit
from app.mod_profiles.common.fields.measurementUnitFields import MeasurementUnitFields
from app.mod_profiles.common.parsers.measurementUnit import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class MeasurementUnitView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de unidad de medición.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
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
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def get(self, id):
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        return measurement_unit

    @swagger.operation(
        notes=u'Actualiza una instancia específica de unidad de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "name",
              "description": u'Nombre de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "symbol",
              "description": u'Símbolo de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "suffix",
              "description": (u'Variable booleana que indica si el símbolo de '
                              'la unidad de medición es un sufijo (verdadero) '
                              'o un prefijo (falso) del valor de la medición.').encode('utf-8'),
              "required": False,
              "dataType": "boolean",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def put(self, id):
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['name'] is not None and
              measurement_unit.name != args['name']):
            measurement_unit.name = args['name']
        # Actualiza el símbolo de la unidad de medida, en caso de que haya sido
        # modificado.
        if (args['symbol'] is not None and
              measurement_unit.symbol != args['symbol']):
            measurement_unit.symbol = args['symbol']
        # Actualiza el estado del sufijo, en caso de que haya sido modificado.
        if (args['suffix'] is not None and
              measurement_unit.suffix != args['suffix']):
            measurement_unit.suffix = args['suffix']

        db.session.commit()
        return measurement_unit, 200
