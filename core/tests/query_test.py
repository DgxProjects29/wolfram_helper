import unittest
from core import queries 


def print_info_from_query(query):
    print()
    print(query.get_query())
    print(query.get_verbose_query())


class TestQueryMixins(unittest.TestCase):

    def simple_query_test_generator(self, test_query_pair):
        for test_pair in test_query_pair:
            query, result = test_pair
            self.assertEqual(query.get_query(), result)
            print_info_from_query(query)

class TestDerivativeQuery(TestQueryMixins):

    def test_simple_derivative_cases(self):
        test_query_pair = [
            (queries.DerivativeQuery('2x^2'), 'D[2x^2,x]'),
            (queries.DerivativeQuery('x^2', order=2), 'D[x^2,x,x]'),
        ]

        self.simple_query_test_generator(test_query_pair)


    def test_partial_derivative_cases(self):

        test_query_pair = [
            (queries.PartialDerivativeQuery('yx^2', ['x', 'y']), 'D[yx^2,x,y]'),
            (queries.PartialDerivativeQuery(
                'sqrt(y)*x^2', ['y', 'y']), 
                'D[sqrt(y)*x^2,y,y]'
            ),
        ]
        
        self.simple_query_test_generator(test_query_pair)

 
class TestIntegralQuery(TestQueryMixins):

    def test_indefinite_integral_cases(self):

        test_query_pair = [
            (queries.IndefiniteIntegralQuery('2x^2'), 'Integrate[2x^2,x]'),
            (queries.IndefiniteIntegralQuery(
                'y^2', variable='y'), 
                'Integrate[y^2,y]'
            ),
        ]

        self.simple_query_test_generator(test_query_pair)

    def test_definite_integral_cases(self):

        test_query_pair = [
            (queries.DefiniteIntegralQuery(
                '2x^2', 2, 5), 
                'Integrate[2x^2,{x,2,5}]'
            ),
            (queries.DefiniteIntegralQuery(
                'y^2', 0, 'x', variable='y'), 
                'Integrate[y^2,{y,0,x}]'
            ),
        ]

        self.simple_query_test_generator(test_query_pair)

class TestVectorQuery(TestQueryMixins):

    def test_indefinite_integral_cases(self):

        test_query_pair = [
            (
                queries.DotProductQuery(
                    queries.VectorQuery([1, 2]).get_query(),
                    queries.VectorQuery([5, 6]).get_query()
                ),
                'Dot[{1,2},{5,6}]'
            ),
            (
                queries.DotProductQuery(
                    queries.VectorQuery(['x^2', 'x']).get_query(),
                    queries.VectorQuery(['y', 'sqrt(x)']).get_query()
                ),
                'Dot[{x^2,x},{y,sqrt(x)}]'
            )

        ]

        self.simple_query_test_generator(test_query_pair)

if __name__ == '__main__':
    unittest.main()