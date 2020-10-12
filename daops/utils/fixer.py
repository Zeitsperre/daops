import json
import os

from elasticsearch import Elasticsearch, exceptions
from pydoc import locate
import hashlib


class FuncChainer(object):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, inputs):
        result = inputs
        for f in self.funcs:
            result = f(result)
        return result


class Fixer(object):
    def __init__(self, ds_id):
        self.ds_id = ds_id
        self.es = Elasticsearch(["elasticsearch.ceda.ac.uk"], use_ssl=True, port=443)
        self._lookup_fix()

    def _convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode("utf-8"))
        return m.hexdigest()

    def _gather_fixes(self, content):
        # if content["hits"]["hits"][-1]["_source"]["fixes"]:
        #     for fix in content["hits"]["hits"][-1]["_source"]["fixes"]:
        if content["_source"]["fixes"]:
            for fix in content["_source"]["fixes"]:

                ref_implementation = fix["reference_implementation"]
                func = locate(ref_implementation)

                if fix["process_type"] == "post_processor":
                    self.post_processors.append([func, fix["operands"]])
                else:
                    self.pre_processors.append(func)

            self.pre_processor = FuncChainer(self.pre_processors)

    def _lookup_fix(self):
        id = self._convert_id(self.ds_id)

        self.pre_processor = None
        self.pre_processors = []
        self.post_processors = []

        try:
            # commented out version work around for the use of multiple indices on one alias
            content = self.es.get(index="roocs-fix", id=id)
            # query_body = {
            #   "query": {
            #     "terms": {
            #       "_id": [f"{id}"]
            #     }
            #   }
            # }
            # content = self.es.search(index="roocs-test", body=query_body)
            self._gather_fixes(content)
        except exceptions.NotFoundError:
            pass
