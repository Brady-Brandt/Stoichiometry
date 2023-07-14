from chempy import chemistry
from chempy.util import periodic 
from chempy.util import parsing


equations = """
N2O3 + H2O = HNO2
HAsO3 = As2O5 + H2O
HIO3 = I2O5 + H2O
Fe2O3 + SiO2 = Fe2Si2O7
Na2O + H2O = NaOH
NH4NO3 = N2O + H2O
Mg(OH)2 = (MgOH)2O + H2O
HAsO3 = As2O5 + H2O
KHSO4 = K2S2O7 + H2O
H3PO4 = H4P2O7 + H2O
Ca(OH)2 + CO2 = Ca(HCO3)2
CaSO4 = CaS + O2
Mg + N2 = Mg3N2
K2O + H2O = KOH
N2O5 + H2O = HNO3
CaS + H2O = Ca(OH)2 + H2S
Li2O + H2O = LiOH
Na2HPO4 = Na4P2O7 + H2O
H4As2O7 = As2O5 + H2O
Al(OH)3 + NaOH = NaAlO2 + H2O
(CuOH)2CO3 = CuO + CO2 + H2O
"""


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
        print(reactants, products, sep=", ")
        return ChemicalEquation(reactants, products)
    return None

#parses the string at the top of the file for chemical equations
#return an array of chemical equations
def parse_equations():
    chemical_equations_arr = []
    for equation in equations.splitlines():
        eq = parse_equation(equation)             
        if eq != None:
            chemical_equations_arr.append(eq)
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

        # balanced products and reactants 
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
    

