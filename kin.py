import math


class KinematicsSolver:
    def __init__(self):
        self.v0 = None  # initial velocity (m/s)
        self.vf = None  # final velocity (m/s)
        self.t = None  # time (s)
        self.a = None  # acceleration (m/s²)
        self.d = None  # displacement (m)
        self.target = None
        self.list = {}
        self.p_eq = []

        self.equations = {
            1: {
                'name': 'Find final velocity (v = v0 + at)',
                'equation': 'vf = v0+a*t',
                'requires': ['v0', 'a', 't'],
                'solves': 'vf'
            },
            2: {
                'name': 'Find displacement (d = v0t + 1/2at²)',
                'equation': 'd = (v0*t) +(.5)*(a)*t*t',
                'requires': ['v0', 'a', 't'],
                'solves': 'd'
            },
            3: {
                'name': 'Find final velocity (vf² = v0² + 2ad)',
                'equation': 'vf = math.sqrt(v0*v0+ (2*a*d))',
                'requires': ['v0', 'a', 'd'],
                'solves': 'vf'
            },
            4: {
                'name': 'Find displacement (d = ((v0 + v)/2)t)',
                'equation': '(d=((v0+vf)/2) *t',
                'requires': ['v0', 'vf', 't'],
                'solves': 'd'
            },
            5: {
                'name': 'Find the acceleration from the first kinematic ((v -v0)/t = a)',
                'equation': 'a = ((vf-v0)/t)',
                'requires': ['v0', 'vf', 't'],
                'solves': 'a'
            },
            6: {
                'name': 'Find the time from the first kinematic',
                'equation': 't = ((vf-v0)/a)',
                'requires': ['v0', 'vf', 'a'],
                'solves': 't'
            },
            7: {
                'name': 'Find acceleration from displacement equation',
                'equation': 'a = (2*(d-v0*t))/(t*t)',
                'requires': ['d', 'v0', 't'],
                'solves': 'a'
            },
            8: {
                'name': 'Find initial velocity from displacement equation',
                'equation': 'v0 = (d-(0.5*a*t*t))/t',
                'requires': ['d', 'a', 't'],
                'solves': 'v0'
            },
            9: {
                'name': 'Find acceleration using vf² = v0² + 2ad',
                'equation': 'a = (vf*vf-v0*v0)/(2*d)',
                'requires': ['vf', 'v0', 'd'],
                'solves': 'a'
            }
        }

    def get_user_input(self):
        print("Welcome to Physics 106 Kinematics Solver")
        self.target = input("List the varaible that you want as you target:v0,vf,d,t, or a")
        print(
            "Please list whether you have each varaible. If you do, give the value, otherwise, say None in that same casing")
        self.vf = input('What is you final velocity ')
        if (self.vf != "None"):
            self.list["vf"] = self.vf
        self.v0 = input("What is your initial velocity ")
        if (self.v0 != "None"):
            self.list["v0"] = self.v0
        self.a = input("What is you acceleration ")
        if (self.a != "None"):
            self.list["a"] = self.a
        self.d = input("What is the displacement value given ")
        if (self.d != "None"):
            self.list["d"] = self.d
        self.t = input("What is the time value given ")
        if (self.t != "None"):
            self.list["t"] = self.t
        return self.list

    def find_Equation(self):
        list = self.get_user_input() if not self.list else self.list
        for x, y in self.equations.items():
            requirements = self.equations[x]['requires']
            requirements_met = True
            for i in requirements:
                if i not in list.keys():
                    requirements_met = False
                    break
            if requirements_met:
                self.p_eq.append(self.equations[x]['equation'])
        return self.p_eq

    def calculate_vals(self):
        eq = self.find_Equation()
        values = self.list
        target = self.target
        for key in values:
            values[key] = float(values[key])
        possible_solutions = []
        for e in eq:
            left_side = e.split('=')[0].strip()
            if target in left_side:
                e = e.replace(' ', '')
                solved_eq = e
                for var, val in values.items():
                    solved_eq = solved_eq.replace(var, str(val))
                try:
                    right_side = e.split('=')[1]
                    if 'math.sqrt' in right_side:
                        before_sqrt = right_side[:right_side.find('math.sqrt')].strip()
                        start_pos = right_side.find('(')
                        end_pos = right_side.rfind(')')
                        inner_expr = right_side[start_pos + 1:end_pos]
                        after_sqrt = right_side[end_pos + 1:].strip()
                        eval_ready_inner = inner_expr
                        eval_ready_before = before_sqrt
                        eval_ready_after = after_sqrt
                        for var, val in values.items():
                            eval_ready_inner = eval_ready_inner.replace(var, str(val))
                            eval_ready_before = eval_ready_before.replace(var, str(val))
                            eval_ready_after = eval_ready_after.replace(var, str(val))
                        sqrt_val = math.sqrt(eval(eval_ready_inner))
                        full_expr = right_side.replace(f'math.sqrt({inner_expr})', str(sqrt_val))
                        for var, val in values.items():
                            full_expr = full_expr.replace(var, str(val))
                        result = eval(full_expr)
                    else:
                        eval_ready = right_side
                        for var, val in values.items():
                            eval_ready = eval_ready.replace(var, str(val))
                        result = eval(eval_ready)
                    possible_solutions.append(result)
                    print(f"Using equation: {e}")
                    print(f"Result: {target} = {result:.3f}")
                except Exception as err:
                    print(f"Could not solve equation: {e}")
                    print(f"Error: {err}")
                    print(f"Current state of variables: {values}")
        if possible_solutions:
            return possible_solutions[0]
        else:
            return None

    def run_simple_tests(self):
        # Test 1: Find final velocity using v = v0 + at
        print("\nTest 1: Final velocity using v = v0 + at")
        self.list = {"v0": "5", "a": "2", "t": "3"}
        self.target = "vf"
        # In run_simple_tests():
        result = self.calculate_vals()
        if result is None:
            print(f"Expected: 11.000, Got: No solution found")
        else:
            print(f"Expected: 11.000, Got: {result:.3f}")

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 2: Find displacement using d = v0t + 1/2at²
        print("\nTest 2: Displacement using d = v0t + 1/2at²")
        self.list = {"v0": "2", "a": "3", "t": "4"}
        self.target = "d"
        result = self.calculate_vals()
        if result is None:
            print("No solution found")
        else:
            print(f"Expected: 32.000, Got: {result:.3f}")  # 2*4 + 0.5*3*4*4 = 32

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 3: Find final velocity using vf² = v0² + 2ad
        print("\nTest 3: Final velocity using vf² = v0² + 2ad")
        self.list = {"v0": "3", "a": "2", "d": "6"}
        self.target = "vf"
        result = self.calculate_vals()
        if result is None:
            print("No solution found")
        else:
            print(f"Expected: 5.000, Got: {result:.3f}")  # sqrt(3² + 2*2*6) = 5

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 4: Find acceleration using (vf - v0)/t
        print("\nTest 4: Acceleration using (vf - v0)/t")
        self.list = {"vf": "10", "v0": "5", "t": "2.5"}
        self.target = "a"
        result = self.calculate_vals()
        if result is None:
            print("No solution found")
        else:
            print(f"Expected: 2.000, Got: {result:.3f}")  # (10 - 5)/2.5 = 2

        # Clear equations for next test
        self.p_eq = []
        self.list = {}
        print("\nTest 5: Find displacement using average velocity")
        self.list = {"v0": "4", "vf": "8", "t": "3"}
        self.target = "d"
        result = self.calculate_vals()
        if result is None:
            print("No solution found")
        else:
            print(f"Expected: 18.000, Got: {result:.3f}")


        # Test 6: Find initial velocity from displacement
        self.p_eq = []
        self.list = {}
        print("\nTest 6: Initial velocity from displacement")
        self.list = {"d": "20", "a": "2", "t": "4"}
        self.target = "v0"
        result = self.calculate_vals()
        if result is None:
            print("No solution found")
        else:
            print(f"Expected: 1.000, Got: {result:.3f}")  # (20 - 0.5*2*4*4)/4 = 1





        self.p_eq = []
        self.list = {}
        #Test CASe 7 HOMEWORK 2 QUestino 9 A
        print("\nTest 1: Ball speed 1 second after being thrown")
        self.list = {"v0": "22", "a": "-9.81", "t": "1"}
        self.target = "vf"
        result = self.calculate_vals()
        if result is None:
            print(f"Expected: 12.19, Got: No solution found")
        else:
            print(f"Expected: 12.19, Got: {result:.2f}")


if __name__ == '__main__':
    print("Enter 1 for calculator, 2 for tests:")
    choice = input()
    Km = KinematicsSolver()
    if choice == "1":
        Km.calculate_vals()
        result =  Km.calculate_vals()
        if result is not None:
            print(f"the result is {result}.3f")
    else:
        Km.run_simple_tests()