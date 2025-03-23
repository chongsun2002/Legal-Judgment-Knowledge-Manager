from flask import Blueprint
from flask_restx import Api
from controllers.judgments_controller import judgments_ns
from controllers.upload_controller import upload_ns
from controllers.search_controller import search_ns

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_namespace(judgments_ns, path='/judgments')
api.add_namespace(upload_ns, path='/upload')
api.add_namespace(search_ns, path='/search')