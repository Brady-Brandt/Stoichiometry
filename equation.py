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

    
#takes in a string of a compound
#takes in an float amount of grams
#returns amount of moles 
def grams_to_moles(comp, grams):
    return grams / calculate_molar_mass(comp)

def moles_to_grams(comp, moles):
    return calculate_molar_mass(comp) * moles

class ChemicalEquation:
    def __init__(self, reactants, prod):
        self.formula = reactants + prod
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
    

