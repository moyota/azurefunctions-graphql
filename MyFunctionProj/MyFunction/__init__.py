import azure.functions as func
from ..graphqllib.graphql import GraphQL, Query
from logging import getLogger
logger = getLogger(__name__)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

    # results = GraphQL().queryWithContext('query { printName }', {"name": "test"})
    # data = results.data['printName']
    # logger.info(type(data))
    # logger.info(data)

    # results = GraphQL().query('query { hello (argument:"World!") }')
    # data = results.data['hello']
    # logger.info(type(data))
    # logger.info(data)

    # results = GraphQL().query('query { getSampleItem { id partitionKey message addition } }')
    # data = results.data['getSampleItem']
    # logger.info(type(data))
    # logger.info(dict(data))

    # results = GraphQL().query('query { readItem(argument:"id1") { id message } }')
    # data = results.data['readItem']
    # logger.info(type(data))
    # logger.info(data)

    # results = GraphQL().query('query { readItems { id message etag ts} }')
    # data = results.data['readItems']
    # logger.info(type(data))
    # logger.info(data)


    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
            # query = str(req.get_body().decode(encoding='utf-8'))
            logger.info(req_body)
        except ValueError:
            pass
        else:
            query = req_body.get('query')

    try:
        results = GraphQL().query(query)
        logger.info(results.data)
    except Exception as e:
        logger.error(e)
        pass

    if results:
        return func.HttpResponse(f"{results.data}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
