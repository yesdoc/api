# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.common.fields.analysisFields import AnalysisFields
from app.mod_profiles.common.parsers.analysis import parser_post_auth
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_201_created, code_401, \
    code_404
from app.mod_profiles.models import Analysis


class MyAnalysisList(Resource):
    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de análisis, '
               'asociadas al perfil del usuario autenticado, ordenadas por '
               'fecha y hora del análisis.').encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='myAnalysisList_get',
        responseMessages=[
            code_200_found,
            code_401,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil.
        profile = g.user.profile

        # Obtiene todos los análisis asociados al perfil, y los ordena por
        # fecha y hora.
        analyses = profile.analyses.order_by(Analysis.datetime).all()
        return analyses

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Crea una nueva instancia de análisis asociada al perfil del '
               'usuario autenticado, y la retorna.').encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='myAnalysisList_post',
        parameters=[
            {
              "name": "datetime",
              "description": u'Fecha y hora del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "datetime",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_201_created,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post_auth.parse_args()
        new_analysis = Analysis(args['datetime'],
                                args['description'],
                                g.user.profile.id)
        db.session.add(new_analysis)
        db.session.commit()
        return new_analysis, 201
