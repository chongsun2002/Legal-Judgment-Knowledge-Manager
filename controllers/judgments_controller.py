from flask import request, send_file
from flask_restx import Namespace, Resource
from services.judgment_service import (
    get_judgments,
    get_judgments_id,
    get_judgments_metadata,
)
from exceptions.storage_exceptions import JudgmentNotFoundException, NoMatchingJudgmentException
from exceptions.data_validation_exceptions import InvalidMetadataKeyException
from models.judgments_schema import get_judgments_parser, get_judgments_responses, validate_metadata, get_judgments_id_responses, get_judgments_id_params
import os

judgments_ns = Namespace('judgments', description="Legal judgment retrieval")

# GET /api/judgments
@judgments_ns.route('')
class AllJudgments(Resource):
    @judgments_ns.expect(get_judgments_parser(), validate=True)
    @judgments_ns.doc(responses=get_judgments_responses, produces=['application/zip'])
    def get(self):
        metadata = request.args.get("metadata")

        try:
            if metadata:
                # Metadata is expected as a JSON string
                metadata_dict = request.get_json(force=True) if request.is_json else eval(metadata)
                validate_metadata(metadata_dict)
                zip_file = get_judgments_metadata(metadata_dict)
            else:
                zip_file = get_judgments()

            return send_file(zip_file, download_name="judgments.zip", as_attachment=True)
        except InvalidMetadataKeyException as e:
            return {"error": str(e)}, 400
        except NoMatchingJudgmentException as e:
            return {"error": str(e)}, 404
        except Exception:
            return {"error": "Unable to get judgments. Check your metadata format or try again later!"}



# GET /api/judgments/<id>
@judgments_ns.route('/<string:id>')
class JudgmentById(Resource):
    @judgments_ns.doc(params=get_judgments_id_params,
                      responses=get_judgments_id_responses,
                      produces=["application/pdf"])
    def get(self, id):
        try:
            file_path = get_judgments_id(id)
            return send_file(file_path, download_name=os.path.basename(file_path), as_attachment=True)
        except JudgmentNotFoundException as e:
            return {"error": str(e)}, 404
