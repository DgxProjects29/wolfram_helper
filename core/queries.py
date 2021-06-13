import urllib.parse

WOLFRAM_URL = "https://www.wolframalpha.com/input/?i={expression}"

def get_query_url(expression):
    parsed_exp = urllib.parse.quote(expression)
    return WOLFRAM_URL.format(expression = parsed_exp)

class WolframQuery:

    def get_url(self):
        """ Get the wolfram url of the given query. """
        raise get_query_url(self.get_raw_query())

    def get_raw_query(self):
        """
        Get the raw query 
        
        The query before being transformed into an url, the one that you can type in the wolfram app
        """
        raise NotImplementedError("`get_raw_query() must be implemented`")

    def get_verbose_query(self):
        """ a human readable form of the query """
        raise NotImplementedError("`get_verbose_query() must be implemented`")
    

    

    
    
