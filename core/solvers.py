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


class SolverTemplate:

    title = "No solver title"

    def __init__(self, solver_input: dict):
        self.solver_input = solver_input

    def validate_input(self):
        pass

    def parse_input(self):
        pass

    def solver_setup(self):
        self.validate_input()
        self.parse_input()

    def get_header(self) -> str:
        raise NotImplementedError("`get_header()` must be implemented.")

    def get_solver_header(self) -> dict:
        return {
            "title": self.title,
            "header": self.get_header(),
        }

    def get_summary(self) -> str:
        raise NotImplementedError("`get_summary()` must be implemented.")

    def get_solver_summary(self) -> str:
        return self.get_summary()


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

    def __init__(self, solver_input: dict):
        if not hasattr(self, self.section_timeout):
            self.section_timeout = self.default_section_timeout
        super().__init__(solver_input)

    def set_selenium_driver(self, driver):
        self.driver = driver

    def get_result(self, query ,pos, sleep_time=5):
        """ 
        Get a result from the wolfram app 

        query: a wolfram query object
        pos: wolfram give us a list of the results, pos indicate what result use.
        sleep_time: after retrieving the results section, how much time wait to get the result indicated
        """
        self.driver.get(query.get_url())
        time.sleep(sleep_time)
        self.driver.execute_script(self.MOUSE_OVER_SCRIPT.format(pos=pos))
        try:
            result_section = self.get_results_section()
            a_element = result_section.find_element_by_css_selector(
                f"{self.RESULT_CONTAINER_SELECTOR} a")
            res = a_element.get_attribute("title")
        except NoSuchElementException:
            imgs = result_section.find_elements_by_class_name(
                self.RESULTS_IMAGE_SELECTOR)
            res = imgs[pos].get_attribute("alt").replace(" ", "")
            res = res[res.find("=") + 1:]
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