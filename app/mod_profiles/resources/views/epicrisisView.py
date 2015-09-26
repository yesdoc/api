# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from app.mod_profiles.models import Epicrisis
from app.config import Config
from app.mod_profiles.resources.fields.epicrisisFields import EpicrisisFields

from flask import Response
from app.mod_shared.models.db import db
import os
#from flaskext.uploads import


class EpicrisisView(Resource):

    @marshal_with(EpicrisisFields.resource_fields, envelope='resource')
    def get(self, id):
        epicrisis = Epicrisis.query.get_or_404(id)
        return epicrisis, 200

    def delete(self, id):
        image = Epicrisis.query.get_or_404(id)
        image_path = Config.uploaded_photos.path(image.image_name)
        os.remove(image_path)
        db.session.delete(image)
        db.session.commit()
        return

