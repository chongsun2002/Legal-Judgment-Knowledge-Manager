from flask_restx import Namespace, Resource
from flask import request, send_file
from services.search_service import get_judgments_search
from exceptions.storage_exceptions import NoMatchingJudgmentException
from models.search_schema import get_search_parser, search_responses

search_ns = Namespace('search', description="Search judgments")

search_parser = get_search_parser()

@search_ns.route('')
class JudgmentSearch(Resource):
    @search_ns.expect(search_parser, validate=True)
    @search_ns.doc(responses=search_responses)
    def get(self):
        args = search_parser.parse_args()
        query = args.get('query')
        count = args.get('count')

        if count <= 0:
            return {"error": "Count must be a positive integer."}, 400
        
        try:
            zip_file = get_judgments_search(query, count)
            return send_file(zip_file, download_name="search_results.zip", as_attachment=True)
        except NoMatchingJudgmentException as e:
            return {"error": str(e)}, 404