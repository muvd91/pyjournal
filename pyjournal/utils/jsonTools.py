import json
from bson import ObjectId


def json_serialize(obj):
    return json.dumps(obj, cls=ObjEncode)


def json_deserialize(json_obj):
    return json.loads(json_obj)


class ObjEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
