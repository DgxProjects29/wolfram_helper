# WOLFRAM HELPER

A mini-framework design to solve mathematical problems step-by-step using a solver template class and scraping the results from wolfram alpha.

you can create your own solvers by sub-classing from SolverTemplate or, WolframSolver if you want to get results from wolfram alpha

## Motivation

I created wolfram helper as result of looking for a better way to solve problems in subjects such as differential equations and calculus, I let the mechanical part to the computer and the logical thinking to me

## Dependencies

The only dependency is selenium 3.141.0

```
pip install selenium==3.141.0
```

## Documentation

The structure of a solver is the following

```python
# located in examples/simple_solver.py
class SimpleSolver(SolverTemplate):

    title = "simple solver"

    input_names = (
        'a',
        'b',
    )

    def step1(self):
        self.c = self.a + self.b
        self.step_descriptions.append("after step 1 i'll write this")

    def step2(self):
        self.u = self.c + self.b
        self.step_descriptions.append("after step 2 i'll write this")

    def get_header(self):
        return [
            f"a: {self.a}",
            f"b: {self.b}",
        ]

    def get_summary(self):
        return [
            f"c: {self.c}",
            f"u: {self.u}",
        ]

if __name__ == '__main__':
    
    s = SimpleTestSolver({'a': 12, 'b': 44})
    s.solver_setup()
    s.start_solver()
    print(s.get_solver_result())
```

a solver receive an input, do some calculations through steps and finally output something like this

```python
{
    'title': 'simple solver', 
    'header': [
        'a: 12', 
        'b: 44'
    ], 
    'step_descriptions': [
        'step1', 
        "after step 1 i'll write this", 
        'step2', 
        "after step 2 i'll write this"
    ], 
    'summary': [
        'c: 56', 
        'u: 100'
    ]
}
```

#### Solver attributes:

| name        | type     | description                                                                                                                                        |
|-------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| title       | str      | the solver name, if none is provided the default is "No solver title"                                                                              |
| input_names | iterable | the input names for your solver, these are stored in the dict solver_input, but after the solver initialize, they become attributes of the class |

#### Solver methods

| name           | return | description                                                                              |
|----------------|--------|------------------------------------------------------------------------------------------|
| get_header     | list   | useful for putting information about the solver                                          |
| get_summary    | list   | useful for putting the results found                                                     |
| validate_input | None   | validate solver's input here. if something is wrong, you can rise an InvalidInputException |
| parse_input    | None   | some inputs may be strings, you can parse them in this method  

solver's process is defined in steps methods that follows the pattern step+number

### Wolfram Solver

Essentially a wolfram solver behaves as a simple solver, but with some methods to use wolfram alpha for obtaining results from queries.

this example computes the line integral of a vector field

```python
# located in examples\field_line_integral.py
class FieldLineIntegral(WolframSolver):

    title = "field line integral"

    input_names = (
        'param_function',
        'fxy',
        'integral_range',
    )

    def step1(self):
        self.step_descriptions.append("find F(r(t))")
        
        n = len(self.param_function)
        default_variables = ['x', 'y', 'z',]
        components = self.param_function[1:n - 1].split(',')
        replace_function = self.fxy
        for i, component in enumerate(components):
            replace_function = replace_function.replace(
                default_variables[i], f"({component})"
        )
        self.replaced_function = replace_function

    def step2(self):
        self.step_descriptions.append("find r'(t)")
        query = DerivativeQuery(self.param_function, 1, variable='t')
        self.d_param_function = self.get_result(query, 0)

    def step3(self):
        self.step_descriptions.append(
            "find dot product between F(r(t)) * r'(t)"
        )
        query = DotProductQuery(self.d_param_function, self.replaced_function)
        self.dot_product = self.get_result(query, 1)

    def step4(self):
        a,b = self.integral_range.split(',')
        self.step_descriptions.append("find the integral of F(r(t)) * r'(t)")
        query = DefiniteIntegralQuery(self.dot_product, a, b, variable='t')
        self.integral_result = self.dot_product = self.get_result(query, 0)

    def get_header(self):
        return [
            f'r(t) = {self.param_function}',
            f'F(x,y) = {self.fxy}',
            f'range =  {self.integral_range}',
        ]
    def get_summary(self):
        return [
            f"r'(t) = {self.d_param_function}",               
            f"F(r(t)) * r'(t) = {self.dot_product}",
            f"integral result = {self.integral_result}",
        ]


if __name__ == '__main__':

    PATH = "data/chromedriver.exe"
    CHROME_OPTIONS = Options()
    CHROME_OPTIONS.add_argument("--log-level=3")

    driver = webdriver.Chrome(PATH, options = CHROME_OPTIONS)
    
    s = FieldLineIntegral({
        "param_function": "{-t, t}", 
        "fxy": "{2xy, x^2 - y}", 
        "integral_range":"0,3"
    })
    s.set_selenium_driver(driver)
    s.solver_setup()
    s.start_solver()
    print(s.get_solver_result())
```

To get results from wolfram alpha, use the method get_result, whose positional parameters are query and pos.

query must be a subclass of WolframQuery and pos is the position of the result that you want from the list of results that wolfram alpha offers 


## Disclaimer

Take into account, the program works scraping the results from wolfram alpha, I think, personal use will cause no problem at all.
