from core.solvers import SolverTemplate

class SimpleTestSolver(SolverTemplate):

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