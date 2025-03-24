from flask_restx import Namespace, Resource
from services.upload_service import upload_file
from exceptions.storage_exceptions import DuplicateJudgmentException
from models.upload_schema import upload_parser, upload_responses, upload_response_model


upload_ns = Namespace('upload', description='Upload PDF judgments')

@upload_ns.route('')
class Upload(Resource):
    @upload_ns.expect(upload_parser)
    @upload_ns.doc(responses=upload_responses)
    @upload_ns.marshal_with(upload_ns.model('UploadResponse', upload_response_model), code=201)
    def post(self):
        """Upload a legal judgment PDF"""
        args = upload_parser.parse_args()
        file = args.get('file')

        if not file or not file.filename.lower().endswith('.pdf'):
            return {'error': 'Invalid file. Please upload a PDF.'}, 400

        try:
            id = upload_file(file)
        except DuplicateJudgmentException as e:
            return {'error': str(e)}, 409
        except Exception as e:
            return {'error': str(e)}, 500

        return {
            'message': 'Upload successful',
            'id': id
        }, 201