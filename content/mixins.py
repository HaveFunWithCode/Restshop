import json
from content.models import Category


class LoadShemaMixin(object):
    def load_schema(self,cat_id):
        DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
        with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
            return json.load(jfile)
