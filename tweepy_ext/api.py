import tweepy
from tweepy_ext.binder import bind_api


class BRTweepyAPI(tweepy.API):

    @property
    def search_30day(self):
        """ :reference: https://dev.twitter.com/rest/reference/get/search/tweets
                    :allowed_param:'q', 'lang', 'locale', 'since_id', 'geocode',
                     'max_id', 'since', 'until', 'result_type', 'count',
                      'include_entities', 'from', 'to', 'source'
                """
        return bind_api(
            api=self,
            path='/tweets/search/30day/brsentimentdev.json',
            # path='/tweets/search/fullarchive/brsentimentfulldev.json',
            method='POST',
            payload_type='search_results',
            allowed_param=['q', 'lang', 'locale', 'since_id', 'geocode',
                           'max_id', 'since', 'until', 'result_type',
                           'count', 'include_entities', 'from',
                           'to', 'source', 'fromDate', 'toDate']
        )

    @property
    def search_fullarchive(self):
        """ :reference: https://dev.twitter.com/rest/reference/get/search/tweets
                    :allowed_param:'q', 'lang', 'locale', 'since_id', 'geocode',
                     'max_id', 'since', 'until', 'result_type', 'count',
                      'include_entities', 'from', 'to', 'source'
                """
        return bind_api(
            api=self,
            # path='/tweets/search/30day/brsentimentdev.json',
            path='/tweets/search/fullarchive/brsentimentfulldev.json',
            method='POST',
            payload_type='search_results',
            allowed_param=['q', 'lang', 'locale', 'since_id', 'geocode',
                           'max_id', 'since', 'until', 'result_type',
                           'count', 'include_entities', 'from',
                           'to', 'source', 'fromDate', 'toDate']
        )