from chempy import chemistry

#parse our text file for chemical equations
#return an array of chemical equations
def parse_equations():
    with open("equations.txt") as f:
        chemical_equations_arr = []
        equations_str = [line.rstrip().replace(" ", "") for line in f]
        for eq in equations_str:
           equation = eq.split('=')
           reactants = equation[0].split('+')
           products = equation[1].split('+')
           chemical_equations_arr.append(ChemicalEquation(reactants, products))
        return chemical_equations_arr
            

class ChemicalEquation:
    def __init__(self, reactants, prod):
        self.reactants = dict.fromkeys(prod)
        self.products = dict.fromkeys(reactants)
        
        self.bal_react, self.bal_prod = chemistry.balance_stoichiometry(self.reactants, self.products)

    def print(self):
        print("Equation: ")
        for react in self.reactants:
            print(react, end=" ")

        print("->", end=" ")
        for prod in self.products:
            print(prod, end=" ")
        print("\nBalanced Equation")
        for react in self.bal_react:
            print(str(self.bal_react[react]) + react, end=" ")

        print("->", end=" ")
        for prod in self.bal_prod:
            print(str(self.bal_prod[prod]) + prod, end=" ")

        print("\n")

