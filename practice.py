import tkinter as tk
from equation import *
import time
import random


class Practice:
    def __init__(self,screen, width, height):
        self.screen = screen
        self.width = width
        self.heigh = height

        self.equations = parse_equations()
        #holds all the entry widgets to enter
        # for balanced equations
        self.balance_entries = []
        self.is_balanced = False
        self.equation = None
        # used for displaying equation
        self.col = 0

        self.GRAMS = "grams"
        self.MOLES = "moles"

    def check_balance(self,args):
        count = 0
        for block in self.balance_entries:
            if block[0].get() != "":
                coeff = int(block[0].get())
                if self.equation.is_correct_coeff(coeff, block[1]):
                    block[0].configure(fg='green')
                    count += 1
                else:
                    block[0].configure(fg='red')
        if count == len(self.balance_entries):
            self.is_balanced = True

    # compounds is either reactants or products
    #side is a char containing a p or r 
    def show_equation_balance(self,frame, compounds, side):
        for index, comp in enumerate(compounds):
            entry_box = tk.Entry(frame, width=2, bg='white')
            self.balance_entries.append([entry_box, comp])

            format_comp = format_subscripts(comp)
            if index == len(compounds) - 1:
                if side == 'r':
                    format_comp +=  " ->"
                else:
                    format_comp += " "
            else:
                format_comp +=  "+"
            
            compound_str = tk.Label(frame, height=2, bg='white', text=format_comp)
            compound_str.config(font=('Helvetica', 35))
            entry_box.grid(row=0,column=self.col)
            self.col += 1
            compound_str.grid(row=0, column=self.col)
            self.col += 1

    def setup_problem(self):
        random.seed(time.time())
        self.is_balanced = False
        eq = self.equations[random.randrange(0,50)]
        self.equation = eq
        formula = eq.get_formula()

        first_unit = random.choice([self.GRAMS, self.MOLES]) 
        first_compound = formula.pop(random.randrange(len(formula)))
        format_first_comp = format_subscripts(first_compound)
        amount = round(random.uniform(1,50),4)

        second_unit = random.choice([self.GRAMS, self.MOLES]) 
        second_compound = formula.pop(random.randrange(len(formula)))
        format_second_comp = format_subscripts(second_compound)
        problem_str = f"How many {first_unit} of {format_first_comp} do I need to produce {amount} {second_unit} of {format_second_comp}"

        self.show_practice_widgets(problem_str,eq)

        if first_unit == self.GRAMS:
            first_comp_mass = calculate_molar_mass(first_compound)
            amount /= first_comp_mass 
        
        molar_ratio = eq.get_molar_ratio(first_compound, second_compound)
        amount *= molar_ratio
        if second_unit == self.GRAMS:
            second_comp_mass = calculate_molar_mass(second_compound)
            amount *= second_comp_mass



    def show_practice_widgets(self, problem_str, eq):
        eq_lb = tk.Label(self.screen, bg='white', text=eq.as_string(), anchor='center')
        eq_lb.configure(font=('Helvetica', 40), height=2)
        problem_lb = tk.Label(self.screen, bg='white', text=problem_str, anchor='center')
        problem_lb.configure(font=('Helvetica', 18), height=1)
        step_one_lb = tk.Label(self.screen, bg='white', text="1. Balance the Equation", anchor='center')
        step_one_lb.configure(font=('Helvetica', 25))
        eq_lb.pack(pady=20)
        problem_lb.pack()
        step_one_lb.pack(pady=10)


        balancing_frame = tk.Frame(self.screen, bg='white') 
        self.show_equation_balance(balancing_frame, eq.get_reactants(), 'r')
        self.show_equation_balance(balancing_frame, eq.get_products(), 'p')
        # 0 is the entry
        # 1 is the compound assoicated with that entry
        for block in self.balance_entries:
            block[0].bind("<Return>", self.check_balance)
        balancing_frame.pack()


