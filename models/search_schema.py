from flask_restx import reqparse

def get_search_parser():
    search_parser = reqparse.RequestParser()
    search_parser.add_argument('query', type=str, required=True, help='Query parameter is required and should be a string.')
    search_parser.add_argument('count', type=int, default=1, help='Count should be a positive integer.')
    return search_parser

search_responses = {
    200: 'ZIP file containing search results',
    400: 'Invalid input parameters',
    404: 'No matching judgments found'
}