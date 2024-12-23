import math


class Projectile_Motion:
    def __init__(self):
        self.v0 = None
        self.vy0 = None
        self.vx0 = None
        self.g = 9.81
        self.h = None
        self.theta = None
        self.R = None
        self.Thang = None
        self.target = None
        self.list = {}
        self.p_eq = []
        self.equations = {
            2: {
                'name': 'Delta Y (Vertical Position)',
                'equation': 'dy = vy0*t - (1/2)*g*t*t',
                'requires': ['vy0', 't', 'g'],
                'solves': 'dy'
            },
            3: {
                'name': 'Hang Time (using vy0)',
                'equation': 'Thang = 2*vy0/g',
                'requires': ['vy0', 'g'],
                'solves': 'Thang'
            },
            4: {
                'name': 'Hang Time (using initial velocity and angle)',
                'equation': 'Thang = 2*v0*math.sin(theta)/g',
                'requires': ['v0', 'theta', 'g'],
                'solves': 'Thang'
            },
            5: {
                'name': 'Hang Time (using height)',
                'equation': 'Thang = 2*math.sqrt(2*h/g)',
                'requires': ['h', 'g'],
                'solves': 'Thang'
            },
            6: {
                'name': 'Range',
                'equation': 'R = (v0*v0*math.sin(2*theta))/g',
                'requires': ['v0', 'theta', 'g'],
                'solves': 'R'
            },
            7: {
                'name': 'Height from Hang Time',
                'equation': 'h = (0.5)*g*(Thang*Thang/4)',
                'requires': ['g', 'Thang'],
                'solves': 'h'
            },
        }

    def get_user_input(self):
        print("Welcome to Physics 106 Projectile Motion Solver")
        self.target = input("List the variable you want as your target: vy0,vx0,Thang, theta,h, R ")
        print(
            "Please list whether you have each variable. If you do, give the value, otherwise, say None in that same casing")

        self.v0 = input("What is your initial velocity? ")
        if (self.v0 != "None"):
            self.list["v0"] = self.v0

        self.vy0 = input("What is your initial y velocity? ")
        if (self.vy0 != "None"):
            self.list["vy0"] = self.vy0

        self.vx0 = input("What is your initial x velocity? ")
        if (self.vx0 != "None"):
            self.list["vx0"] = self.vx0

        self.Thang = input("What is your hangtime value? ")
        if (self.Thang != "None"):
            self.list["Thang"] = self.Thang

        self.h = input("What is your height value? ")
        if (self.h != "None"):
            self.list["h"] = self.h

        self.theta = input("What is your angle in degrees? ")
        if (self.theta != "None"):
            angle_rad = float(self.theta) * math.pi / 180
            self.list["theta"] = str(angle_rad)

        self.list["g"] = str(self.g)
        return self.list

    def find_Equation(self):
        list = self.get_user_input() if not self.list else self.list
        #print("\nAvailable variables:", list.keys())

        for x, y in self.equations.items():
            requirements = self.equations[x]['requires']
            requirements_met = True
            for i in requirements:
                if i not in list.keys():
                    requirements_met = False
                    break
            if requirements_met:
                #print(f"✓ Found valid equation: {self.equations[x]['equation']}")
                self.p_eq.append(self.equations[x]['equation'])
        #print("\nPossible equations found:", self.p_eq)
        return self.p_eq
    def calculate_vals(self):
        eq = self.find_Equation()
        values = self.list
        target = self.target
        print(f"\nTarget variable: {target}")
        #print(f"Available equations: {eq}")

        for key in values:
            values[key] = float(values[key])

        possible_solutions = []
        for e in eq:
            #print(f"\nTrying equation: {e}")
            left_side = e.split('=')[0].strip()
            #print(f"Left side: {left_side}")
            if target in left_side:
                #print(f"Target {target} found in equation")
                e = e.replace(' ', '')
                solved_eq = e
                for var, val in values.items():
                    solved_eq = solved_eq.replace(var, str(val))
                #print(f"Equation after substitution: {solved_eq}")
                try:
                    right_side = e.split('=')[1]
                    if 'math.sqrt' in right_side:
                        sqrt_parts = right_side.split('math.sqrt')
                        outer_multiplier = sqrt_parts[0].strip() if sqrt_parts[0].strip() else "1"

                        start_pos = right_side.find('(')
                        end_pos = right_side.rfind(')')
                        inner_expr = right_side[start_pos + 1:end_pos]
                        for var, val in values.items():
                            inner_expr = inner_expr.replace(var, str(val))
                            outer_multiplier = outer_multiplier.replace(var, str(val))
                        #print(f"Outer multiplier: {outer_multiplier}")
                        #print(f"Inner expression for sqrt: {inner_expr}")
                        inner_result = eval(inner_expr)
                        sqrt_result = math.sqrt(inner_result)
                        result = eval(f"{outer_multiplier}*{sqrt_result}")
                    else:
                        eval_ready = right_side
                        for var, val in values.items():
                            eval_ready = eval_ready.replace(var, str(val))
                        result = eval(eval_ready)
                    if target == 'theta':
                        result = result * 180 / math.pi
                    possible_solutions.append(result)
                    #print(f"Using equation: {e}")
                    #print(f"Result: {target} = {result:.3f}")
                except Exception as err:
                    print(f"Could not solve equation: {e}")
                    print(f"Error: {err}")
                    print(f"Current state of variables: {values}")
        if possible_solutions:
            return possible_solutions[0]
        else:
            return None
    def run_simple_tests(self):
        # Test 1: Height to Hang Time
        print("\nTest 1: Height to Hang Time")
        self.list = {"h": "6.0", "g": "9.81"}
        self.target = "Thang"
        result = self.calculate_vals()
        print(f"Expected: 2.212, Got: {result:.3f}")

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 2: A simple range calculation
        print("\nTest 2: Simple Range")
        angle_rad = 30 * math.pi / 180  # Convert 30 degrees to radians
        self.list = {"v0": "10", "theta": str(angle_rad), "g": "9.81"}
        self.target = "R"
        result = self.calculate_vals()
        print(f"Expected: 8.839, Got: {result:.3f}")

        # Test 3: Hang Time using initial velocity and angle
        print("\nTest 3: Hang Time using v0 and theta")
        angle_rad = 45 * math.pi / 180  # 45 degree angle
        self.list = {"v0": "15", "theta": str(angle_rad), "g": "9.81"}
        self.target = "Thang"
        result = self.calculate_vals()
        print(f"Expected: 2.163, Got: {result:.3f}")

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 4: Hang Time using initial y velocity
        print("\nTest 4: Hang Time using vy0")
        self.list = {"vy0": "12", "g": "9.81"}
        self.target = "Thang"
        result = self.calculate_vals()
        print(f"Expected: 2.447, Got: {result:.3f}")

        # Clear equations for next test
        self.p_eq = []
        self.list = {}
        # Test 5: Height from Hang Time
        print("\nTest 5: Height from Hang Time")
        self.list = {"Thang": "1.12", "g": "32.2"}
        self.target = "h"
        result = self.calculate_vals()
        print(f"Expected: 5.020, Got: {result:.3f}")

        # Clear equations for next test
        self.p_eq = []
        self.list = {}

        # Test 6: Delta Y calculation
        print("\nTest 6: Delta Y calculation")
        self.list = {"vy0": "10", "t": "1", "g": "9.81"}
        self.target = "dy"
        result = self.calculate_vals()
        print(f"Expected: 5.095, Got: {result:.3f}")

        self.p_eq = []
        self.list = {}
        # Test 8: Height from Hang Time QUestion on Homework4 without cnversion in feet only meters
        print("\nTest 8: Height from Hang Time")
        self.list = {"Thang": "1.12", "g": "9.81"}
        self.target = "h"
        result = self.calculate_vals()
        print(f"Expected: Around 1.52, Got: {result:.3f}")

if __name__ == '__main__':
    print("Enter 1 for calculator, 2 for tests:")
    choice = input()
    pj = Projectile_Motion()
    if choice == "1":
        result = pj.calculate_vals()
        if result is not None:
            print(f"The final result is {result}.3f")

    else:
        pj.run_simple_tests()