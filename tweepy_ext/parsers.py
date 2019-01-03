from tweepy.parsers import JSONParser
from tweepy_ext.models import BRSearchResults


class BRModelParser(JSONParser):

    def __init__(self, model_factory=None):
        JSONParser.__init__(self)
        # self.model_factory = model_factory or ModelFactory

    def parse(self, method, payload):
        try:
            if method.payload_type is None:
                return
            model = BRSearchResults
        except Exception as e:
            print(e)

        json = JSONParser.parse(self, method, payload)
        if isinstance(json, tuple):
            json, cursors = json
        else:
            cursors = None

        if method.payload_list:
            result = model.parse_list(method.api, json)
        else:
            result = model.parse(method.api, json)

        if cursors:
            return result, cursors
        else:
            return result