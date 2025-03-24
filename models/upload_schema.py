from flask_restx import reqparse, fields

from werkzeug.datastructures import FileStorage

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file',
    type=FileStorage,
    location='files',
    required=True,
    help='PDF document to upload.\nUse Content-Type: multipart/form-data.'
)

upload_responses =  {
    201: 'Successful upload',
    409: 'Duplicate file upload'
}

upload_response_model = {
    'message': fields.String(description='Success message'),
    'id': fields.String(description='Unique ID assigned to the uploaded judgment')
}