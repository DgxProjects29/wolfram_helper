from core.queries import DefiniteIntegralQuery, DerivativeQuery, DotProductQuery
from core.solvers import WolframSolver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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