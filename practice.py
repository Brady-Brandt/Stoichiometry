import tkinter as tk
from equation import *
from fractions import Fraction
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
        self.compound_labels = []
        self.molar_mass_entries = []
        self.molar_ratio_entries = []
        self.molar_mass_multiply_entries = []
        self.equation = None
        # used for displaying equation
        self.col = 0


        # all relate to the current problem
        
        self.formula = None
        self.first_unit = "grams"
        self.first_compound = None
        self.format_first_comp = None 
        self.amount = 69 
        self.second_unit = "grams"
        self.second_compound = None
        self.format_second_comp = None 

        self.result = 0
        self.molar_mass = 0
        self.moles = 0
        self.molar_ratio = 0
        self.elements = None

    def check_mass(self, args):
        for block in self.molar_mass_entries:
            if block[0].get() != "":
                molar_mass = float(block[0].get())
                # checks if the molar mass inputted is correct
                if percent_error(molar_mass, calculate_molar_mass(block[1])):
                        block[0].configure(state='disabled')
                else:
                    block[0].configure(bg='red')

    def check_multiply_mass(self, args):
        for block in self.molar_mass_multiply_entries:
            if block[0].get() != "":
                product = float(block[0].get())
                # get the molar mass inputted by user
                expected_prod = self.elements[block[1]]
                if percent_error(product, calculate_molar_mass * expected_prod) < 5:
                        block[0].configure(state='disabled')
                else:
                    block[0].configure(bg='red')



    def show_molar_mass(self, comp):
        molar_mass_frame = tk.Frame(self.screen, bg='white') 
        format_comp = format_subscripts(comp)
        molar_mass_dir_lb = tk.Label(self.screen, bg='white', text=f"Calculate the Molar Mass of {format_comp}", font=('Helvetica', 25))
        molar_mass_tip_lb = tk.Label(self.screen, bg='white', text="Look at a periodic table to find the atomic mass of each of the following elements. \n Multiply the atomic mass by the subscript that follows that element \n Add each of the products together to get the total molar mass", font=('Helvetica', 12))

        molar_mass_dir_lb.pack()
        molar_mass_tip_lb.pack()
        row = 0
        #setup labels and entries for calculating molar mass
        self.elements = get_elements_from_comp(comp)
        for elem in self.elements:
            entry = tk.Entry(molar_mass_frame,width=8, bg='white',  font=('Helvetica', 25))
            label = tk.Label(molar_mass_frame, bg='white', text=elem, font=('Helvetica', 25))
            sub_label = tk.Label(molar_mass_frame, bg='white', text=f" X {self.elements[elem]} = ", font=('Helvetica', 25))
            multiply_entry = tk.Entry(molar_mass_frame, width=8, bg='white', font=('Helvetica', 25))
            label.grid(row=row, column=1)
            entry.grid(row=row, column=2)
            sub_label.grid(row=row, column=3)
            multiply_entry.grid(row=row, column=4)

            row += 1
            multiply_entry.focus()
            entry.focus()
            self.molar_mass_multiply_entries.append([multiply_entry, elem])
            self.molar_mass_entries.append([entry, elem])
            multiply_entry.bind("<Return>", self.check_multiply_mass)
            entry.bind("<Return>", self.check_mass)
           

        molar_mass_frame.pack()

    def check_molar_ratio(self, args):
        # gets a tuple of the ratio
        ratio = self.equation.get_molar_ratio(self.second_compound, self.first_compound)
        count = 0
        if self.molar_ratio_entries[0].get() != "":
            coeff = int(self.molar_ratio_entries[0].get())
            if coeff == ratio[0]:
                self.molar_ratio_entries[0].configure(state='disabled')
                count += 1
            else: 
                self.molar_ratio_entries[0].configure(bg='red')

        if self.molar_ratio_entries[1].get() != "":
            coeff = int(self.molar_ratio_entries[1].get())
            if coeff == ratio[1]:
                self.molar_ratio_entries[1].configure(state='disabled')
                count += 1
            else: 
                self.molar_ratio_entries[1].configure(bg='red')
        if count == 2:
            molar_ratio = Fraction(ratio[0], ratio[1])
            mr_num = molar_ratio.numerator
            mr_den = molar_ratio.denominator
            molar_ratio_lb = tk.Label(self.screen, bg='white', text=f"Molar Ratio: {mr_num}/{mr_den}", font=('Helvetica', 40))
            molar_ratio_lb.pack()


        


    def show_molar_ratio(self):
        molar_ratio_frame = tk.Frame(self.screen, bg='white') 
        molar_ratio_step_lb = tk.Label(self.screen, bg='white', font=('Helvetica', 25), text="Find the Molar Ratio")
        molar_ratio_dir_label = tk.Label(self.screen, wraplength=600, justify='center', bg='white', text=f"Get the coefficient of {self.format_second_comp} and divide it by the coefficient of {self.format_first_comp}", font=('Helvetica', 18))
        first_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_first_comp} Coeff:")
        first_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20))

        second_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_second_comp} Coeff:")
        second_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20))


        self.molar_ratio_entries.append(first_compound_entry)
        self.molar_ratio_entries.append(second_compound_entry)
        for entry in self.molar_ratio_entries:
            entry.bind("<Return>", self.check_molar_ratio)

        molar_ratio_step_lb.pack()
        molar_ratio_dir_label.pack()

        second_compound_lb.grid(row=0,column=0)
        second_compound_entry.grid(row=0,column=1)

        first_compound_lb.grid(row=2,column=0)
        first_compound_entry.grid(row=2,column=1)

        first_compound_entry.focus()
        second_compound_entry.focus()

        molar_ratio_frame.pack()


        
    def check_next_step(self):
        if self.first_unit == "grams":
            self.show_molar_mass(self.first_compound)
            first_comp_mass = calculate_molar_mass(self.first_compound)
            self.result = self.amount / first_comp_mass 
            #molar_ratio = self.equation.get_molar_ratio(self.first_compound, self.second_compound)
            #self.result  *= molar_ratio

        if self.second_unit == "grams":
            second_comp_mass = calculate_molar_mass(self.second_compound)
            self.result  *= second_comp_mass
        if self.first_unit == "moles":
            self.show_molar_ratio()



    def check_balance(self,args):
        count = 0
        for block in self.balance_entries:
            if block[0].get() != "":
                coeff = int(block[0].get())
                if self.equation.is_correct_coeff(coeff, block[1]):
                    block[0].configure(state='disabled')
                    count += 1
                else:
                    block[0].configure(bg='red')
        if count == len(self.balance_entries):
            self.check_next_step()

    # called if user can't balance the equation themselves
    def balance_equation(self):
        for block in self.balance_entries:
            current_val = block[0].get()
            block[0].delete(0,len(current_val))
            block[0].insert(0,str(self.equation.get_correct_coeff(block[1])))

            block[0].configure(state='disabled')
        self.check_next_step()



    # compounds is either reactants or products
    #side is a char containing a p or r 
    def show_equation_balance(self,frame, compounds, side):
        for index, comp in enumerate(compounds):
            entry_box = tk.Entry(frame, width=2, bg='white', font=('Helvetica', 20))
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
            compound_str.config(font=('Helvetica', 30))
            self.compound_labels.append(compound_str)

            entry_box.grid(row=0,column=self.col)
            self.col += 1
            compound_str.grid(row=0, column=self.col)
            self.col += 1
        if side == 'p':
           help_button = tk.Button(frame, height=2, bg='white', text="Help Me", command=self.balance_equation) 
           help_button.grid(row=0, column=self.col)


    def setup_problem(self):
        random.seed(time.time())
        self.equation = self.equations[random.randrange(0,50)]
        self.formula = self.equation.get_formula()

        self.first_unit = random.choice(["grams", "moles"]) 
        self.first_compound = self.formula.pop(random.randrange(len(self.formula)))
        self.format_first_comp = format_subscripts(self.first_compound)
        self.amount = round(random.uniform(1,50),3)

        self.second_unit = random.choice(["grams", "moles"]) 
        self.second_compound = self.formula.pop(random.randrange(len(self.formula)))
        self.format_second_comp = format_subscripts(self.second_compound)
        problem_str = f"How many {self.first_unit} of {self.format_first_comp} do I need to produce {self.amount} {self.second_unit} of {self.format_second_comp}"

        self.show_practice_widgets(problem_str,self.equation)

        

    def show_practice_widgets(self, problem_str, eq):
        problem_lb = tk.Label(self.screen, bg='white', text=problem_str, anchor='center')
        problem_lb.configure(font=('Helvetica', 18), height=1)
        step_one_lb = tk.Label(self.screen, bg='white', text="Balance the Equation", anchor='center')
        step_one_lb.configure(font=('Helvetica', 25))
        problem_lb.pack(pady=20)
        step_one_lb.pack(pady=10)


        balancing_frame = tk.Frame(self.screen, bg='white') 
        self.show_equation_balance(balancing_frame, eq.get_reactants(), 'r')
        self.show_equation_balance(balancing_frame, eq.get_products(), 'p')

        # 0 is the entry
        # 1 is the compound assoicated with that entry
        for block in self.balance_entries:
            block[0].bind("<Return>", self.check_balance)
        balancing_frame.pack()


