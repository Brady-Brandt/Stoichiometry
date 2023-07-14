from chempy import chemistry
from chempy.util import periodic 
from chempy.util import parsing



subscripts = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}

def format_subscripts(string):
    new_string = ""
    for char in string:
        if char.isdigit():
            new_string += subscripts[char]
        else:
            new_string += char

    return new_string


def get_elements_from_comp(comp):
    parsed_compound = parsing.formula_to_composition(comp)
    new_dict = {}
    for atomic_num in parsed_compound:
        if atomic_num != 0:
            new_dict[parsing.symbols[atomic_num - 1]] = parsed_compound[atomic_num]
    return new_dict

def parse_equation(eq):
    eq = eq.rstrip().replace(" ", "")
    eq= eq.split('=')
    # check for reactants and products
    if len(eq) == 2:
        reactants = eq[0].split('+')
        products = eq[1].split('+')     
        return ChemicalEquation(reactants, products)
    return None

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
            

def calculate_molar_mass(comp):
    parsed_compound = parsing.formula_to_composition(comp)
    return round(periodic.mass_from_composition(parsed_compound), 4)

def percent_error(observed, accepted):
    return abs((observed - accepted) / observed) * 100

    
class ChemicalEquation:
    def __init__(self, reactants, prod):
        self.formula = reactants + prod
        self.reactants = dict.fromkeys(reactants)
        self.products = dict.fromkeys(prod)
        self.bal_react = {}
        self.bal_prod = {}
      
        try:
            self.bal_react, self.bal_prod = chemistry.balance_stoichiometry(self.reactants, self.products)
        except Exception as e:
            print(e) 
            self.bal_react = {}
            self.bal_prod = {}
            self.reactants = {}
            self.products = {}


    def get_reactants(self):
        return self.reactants
    def get_products(self):
        return self.products

    def is_correct_coeff(self, coeff, compound):
        if compound in self.bal_react:
            return self.bal_react[compound] == coeff
        if compound in self.bal_prod:
            return self.bal_prod[compound]  == coeff
        return False

    def get_correct_coeff(self, compound):
        if compound in self.bal_react:
            return self.bal_react[compound]    
        if compound in self.bal_prod:
            return self.bal_prod[compound] 
        return -1


    def as_string(self):
        formula = ""
        for react in self.reactants:
            formula += react + " + "

        formula = formula[:-3]
        formula += " -> "
        for prod in self.products:
            formula += prod + " + "

        formula = formula[:-3]
        return format_subscripts(formula)

                
    def get_formula(self):
        return self.formula.copy()

    def get_molar_ratio(self, comp1, comp2):
        coeff_one = 1
        coeff_two = 1
        if comp1 in self.bal_react:
            coeff_one = self.bal_react[comp1]
        elif comp1 in self.bal_prod:
            coeff_one = self.bal_prod[comp1]

        if comp2 in self.bal_react:
            coeff_two  = self.bal_react[comp2]
        elif comp2 in self.bal_prod:
            coeff_two = self.bal_prod[comp2]

        return (coeff_one, coeff_two)
    

