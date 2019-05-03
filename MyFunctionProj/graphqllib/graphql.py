import graphene
import json
from datetime import datetime, timezone
from ..cosmosdb.cosmosdb import DatabaseConnection, getItem, getReplacedItem
from logging import getLogger
logger = getLogger(__name__)

# type DBItem
class DbItem(graphene.ObjectType):
    id = graphene.String(required=True)
    partitionKey = graphene.ID(required=True)
    message = graphene.String()
    addition = graphene.String()
    rid = graphene.String() # comosdb column name _rid
    link = graphene.String() # comosdb column name _self
    etag = graphene.String() # comosdb column name _etag
    attachments = graphene.String() # comosdb column name _attachments
    ts = graphene.Int() # comosdb column name _ts
    datetime = graphene.types.datetime.DateTime()  

    def resolve_rid(self, info):
        return self._rid
    def resolve_link(self, info):
        return self._self
    def resolve_etag(self, info):
        return self._etag
    def resolve_attachments(self, info):
        return self._attachments
    def resolve_ts(self, info):
        return self._ts
    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self._ts, timezone.utc)

# type Query
class Query(graphene.ObjectType):
    printName = graphene.String()
    hello = graphene.String(argument=graphene.String(default_value="world."))
    getSampleItem = graphene.Field(DbItem)
    readItem = graphene.Field(DbItem, argument=graphene.String())
    readItems = graphene.List(DbItem)

    def resolve_printName(self, info):
        return info.context.get('name') + '\n'

    def resolve_hello(self, info, argument):
        return 'Hello ' + argument + '\n'

    def resolve_getSampleItem(self, info):
        item = DbItem(id="1", partitionKey=1,
            message="SampleMessage", addition="SampleAddtionMessage")
        return item

    def resolve_readItem(self, info, argument):
        results = DatabaseConnection().read_item(argument)
        if results.__len__() > 0:
            item = DbItem.__new__(DbItem)
            item.__dict__.update(results[0])
            return item
        else:
            return {}

    def resolve_readItems(self, info):
        results = []
        for item in DatabaseConnection().read_items():
            i = DbItem.__new__(DbItem)
            i.__dict__.update(item)
            results.append(i)
        return results

class GraphQL:
    def __init__(self):
        self.schema = graphene.Schema(
            query=Query,
        )

    def query(self, query):
        results = self.schema.execute(query)
        return json.dumps(results.data)

    def queryWithContext(self, query, context):
        results = self.schema.execute(query, context=context)
        return results


# class Mutation(graphene.Mutation):
