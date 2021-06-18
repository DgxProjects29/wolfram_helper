import urllib.parse

WOLFRAM_URL = "https://www.wolframalpha.com/input/?i={expression}"

def get_query_url(expression):
    parsed_exp = urllib.parse.quote(expression)
    return WOLFRAM_URL.format(expression = parsed_exp)


class InvalidQueryException(Exception):
    """ An exception for for invalid queries """
    pass


class WolframQuery:

    def get_url(self):
        """ Get the wolfram url of the given query. """
        return get_query_url(self.get_query())

    def get_query(self):
        """
        Get the raw query 
        
        The query before being transformed into an url, the one that you can type in the wolfram app
        """
        raise NotImplementedError("`get_query() must be implemented`")

    def get_verbose_query(self):
        """ a human readable form of the query """
        raise NotImplementedError("`get_verbose_query() must be implemented`")
    

""" Some basic queries """

class DerivativeQuery(WolframQuery):

    def __init__(self, func, order = 1, variable = 'x'):
        
        if order <= 0:
            raise InvalidQueryException("The order should be greater than 0")
        
        self.func = func
        self.order = order
        self.derivative_respect = f",{variable}"*order
        self.query = f"D[{func}{self.derivative_respect}]"

    def get_query(self):
        return self.query
     
    def get_verbose_query(self):
        order_message = "" if self.order == 1 else f"of order {self.order}"
        return f"compute derivative of {self.func} {order_message}"
    

class PartialDerivativeQuery(WolframQuery):

    def __init__(self, func, order):
            
        self.func = func
        self.order = order
        self.query = f"D[{func},{','.join(self.order)}]"

    def get_query(self):
        return self.query
    
    def get_verbose_query(self):
        dr_human_form = " then ".join(self.order)
        
        return f"compute derivative of {self.func} with respect {dr_human_form}"
    
    
class IndefiniteIntegralQuery(WolframQuery):
    
    def __init__(self, func, variable = 'x'):
        
        self.func = func
        self.variable = variable
        self.query = f"Integrate[{func},{variable}]"

    def get_query(self):
        return self.query
     
    def get_verbose_query(self):
        return f"compute integral of {self.func} with respect {self.variable}"

class DefiniteIntegralQuery(WolframQuery):
    
    def __init__(self, func, a, b, variable = 'x'):
        
        self.func = func
        self.a = a
        self.b = b
        self.variable = variable
        self.query = f"Integrate[{func},{{{variable},{a},{b}}}]"

    def get_query(self):
        return self.query
     
    def get_verbose_query(self):
        return f"compute integral of {self.func} " + \
            f"with respect {self.variable} from {self.a} to {self.b}" 


class VectorQuery(WolframQuery):
    
    def __init__(self, components):
        components = map(str, components)
        self.query = f"{{{','.join(components)}}}"

    def get_query(self):
        return self.query
     
    def get_verbose_query(self):
        return f"Vector {self.query}"


class DotProductQuery(WolframQuery):
    
    def __init__(self, vector1, vector2):
        self.vector1 = vector1
        self.vector2 = vector2
        self.query = f"Dot[{vector1},{vector2}]"

    def get_query(self):
        return self.query
     
    def get_verbose_query(self):
        return f"Dot product of {self.vector1} and {self.vector2}"
