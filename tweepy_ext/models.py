from tweepy.models import ResultSet, Status


class BRSearchResults(ResultSet):

    @classmethod
    def parse(cls, api, json):
        results = BRSearchResults()
        results.next = False
        if json.get('next', False):
            results.next = json['next']

        status_model = getattr(api.parser.model_factory, 'status') if api else Status

        for status in json['results']:
            results.append(status_model.parse(api, status))
        return results