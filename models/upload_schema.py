from flask_restx import reqparse
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