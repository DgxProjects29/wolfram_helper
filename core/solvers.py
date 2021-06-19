import re
from typing import List
import inspect
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class InvalidInputException(Exception):
    """ invalid input provided by the user """
    pass

class WolframSolverException(Exception):
    """ an exception raise if something goes wrong in a wolfram solver """
    pass


class UserStopException(Exception):
    """ an exception raise if the user doesn't want to continue """
    pass


class SolverTemplate:

    title = "No solver title"

    def __init__(self, solver_input: dict, cli=False):
        self.solver_input = solver_input
        self.cli = cli
        self.step_descriptions = []

    def validate_input(self):
        pass

    def parse_input(self):
        pass
    
    def solver_setup(self):
        """ initialize the input names for this solver, then execute, validate_input and parse_input respectively """
        
        if not hasattr(self, 'input_names'):
            raise NotImplementedError("`input_names` must be implemented.")
        else:
            for input_name in self.input_names:
                try:
                    setattr(self, input_name, self.solver_input[input_name])
                except:
                    raise KeyError(
                        f"not all input were provided, the inputs for this solver are {self.input_names}"
                    )

        self.validate_input()
        self.parse_input()

    def start_solver(self):

        def filter_func(member):
            if (inspect.ismethod(member)):
                if hasattr(member, '__name__'):
                    match = re.match(r"step(\d+)", member.__name__) 
                    return bool(match)
                else:
                    return False
            else:
                return False
        
        step_methods = inspect.getmembers(self, filter_func)
        step_methods.sort(key=lambda t: int(t[0][4:]))

        for step in step_methods:
            
            name = step[0]
            function_to_execute = step[1]
            self.step_descriptions.append(name)
            function_to_execute()

            if self.cli:
                continue_process = input("CONTINUE PROCESS [y/n]:  ")
                if continue_process == 'n':
                    raise UserStopException("stop program by the user")


    def get_header(self) -> List[str]:
        raise NotImplementedError("`get_header()` must be implemented.")

    def get_summary(self) -> List[str]:
        raise NotImplementedError("`get_summary()` must be implemented.")

    def get_solver_result(self):
        solver_result = {
            'title': self.title,
            'header': self.get_header(),
            'step_descriptions': self.step_descriptions,
            'summary': self.get_summary(),
        }
        return solver_result
        


class WolframSolver(SolverTemplate):

    # this script is executed to simulate a hover effect, 
    # and retrieve the answer
    MOUSE_OVER_SCRIPT = """

    event = document.createEvent("HTMLEvents");
    event.initEvent("mouseover", true, true);
    event.eventName = "mouseover";
    document.querySelectorAll("._8J16o")[{pos}].dispatchEvent(event)

    """

    RESULTS_SECTION_SELECTOR = "._2GT4c"
    RESULT_CONTAINER_SELECTOR = "._8J16o"
    RESULTS_IMAGE_SELECTOR = "_3vyrn"

    # The default timeout for the results section
    default_section_timeout = 15

    def __init__(self, solver_input: dict, cli = False):
        if not hasattr(self, 'section_timeout'):
            self.section_timeout = self.default_section_timeout
        super().__init__(solver_input, cli=cli)

    def set_selenium_driver(self, driver):
        self.driver = driver

    def get_result(self, query, pos, sleep_time=5):
        """ 
        Get a result from the wolfram app 

        query: a wolfram query object
        pos: wolfram give us a list of the results, pos indicate what result to use.
        sleep_time: after retrieving the results section, how long to wait for the indicated result
        """
        self.driver.get(query.get_url())
        time.sleep(sleep_time)
        try:
            self.driver.execute_script(self.MOUSE_OVER_SCRIPT.format(pos=pos))
            result_section = self.get_results_section()
            a_element = result_section.find_element_by_css_selector(
                f"{self.RESULT_CONTAINER_SELECTOR} a")
            res = a_element.get_attribute("title")
        except NoSuchElementException:
            imgs = result_section.find_elements_by_class_name(
                self.RESULTS_IMAGE_SELECTOR)
            res = imgs[pos].get_attribute("alt").replace(" ", "")
            res = res[res.find("=") + 1:]
        except Exception as e:
            raise WolframSolverException(str(e))
        return res

    def get_results_section(self):
        """  
        Get a selenium web element of the results section from wolfram
        """
        results_section = WebDriverWait(
            self.driver, self.section_timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.RESULTS_SECTION_SELECTOR)))
        return results_section