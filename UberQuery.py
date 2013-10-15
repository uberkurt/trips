import urllib2 as urllib
import simplejson, json

class Query:

    def __init__(self, tllat, tllon, brlat, brlon, reqtype):
        # we'll assume the only kind of Uber query is a geo query
        self.tllat = float(tllat)
        self.tllon = float(tllon)
        self.brlat = float(brlat)
        self.brlon = float(brlon)
        self.reqtype = reqtype

    def query_stats(self):
        # form the raw JSON
        query = {
            "query": {
                "filtered": {
                    "query": {
                        "match_all": {}
                        },
                    "filter": {
                        "and": [
                            {
                                "geo_bounding_box": {
                                    "location": {
                                        "top_left": {
                                            "lat": self.tllat,
                                            "lon": self.tllon
                                            },
                                        "bottom_right": {
                                            "lat": self.brlat,
                                            "lon": self.brlon
                                            }
                                        }
                                    }
                                },
                            {
                                "query": {
                                    "query_string": {
                                        "query": self.reqtype
                                        }
                                    }
                                }
                            ]
                        }
                    }
                },
            "facets": {
                "farestat": {
                    "statistical": {
                        "field": "fare"
                        }
                    }
                }
            }

        # make and return the query using urllib
        q = simplejson.dumps(query)
        response = urllib.urlopen('http://uber.kurtado.com:9200/uber/trips/_search', q)
        result = json.loads( response.read() )
        return result
