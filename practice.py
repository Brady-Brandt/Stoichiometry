import tkinter as tk
from equation import *
from fractions import Fraction
import time
import random


equations = parse_equations()

class Practice:
    def __init__(self, screen, width, height, scrollbar, frame):
        self.screen = screen
        self.width = width
        self.heigh = height
        
        self.scrollbar = scrollbar
        self.frame = frame
        self.frame.pack() 
   
        #holds all the entry widgets to enter
        # for balanced equations
        self.balance_entries = {}
        self.molar_ratio_entries = [0,0]
        #holds the element or ion as the key and its entry as the value
        self.molar_mass_entries = {}
        #holds the element or ion as the key and its entry as the value
        self.molar_mass_multiply_entries = {}
        self.total_molar_mass_entry = None
        self.mole_entry = None
        self.mole_convert_entry = None
        self.equation_entry = None

        self.equation_entry_button = None
        self.help_button = None


        self.equation = None
        # used for displaying equation
        self.col = 0

        self.font25 = ('Helvetica', 25)


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
        self.grams = 0
        self.molar_ratio = 0
        # holds a dictionary  of elements for a certain compound
        self.elements = {}
        # holds a dictionary of elements and the molar mass the user has inputted
        self.user_inputted_mass = {}
        self.user_inputted_multiply_mass = {}

    def check_mass(self, args):
        for element in self.molar_mass_entries:
            entry = self.molar_mass_entries[element]
            inputted_molar_mass = entry.get()
            if inputted_molar_mass != "":
                molar_mass = float(inputted_molar_mass)
                # checks if the molar mass inputted is correct
                if percent_error(molar_mass, calculate_molar_mass(element)):
                    self.user_inputted_mass[element] = molar_mass
                    #check if the user has already inputted a correct value 
                    # if so we don't want to re enable the entry
                    if self.molar_mass_multiply_entries[element]["bg"] == 'green':
                        continue
                    else:
                        self.molar_mass_multiply_entries[element].configure(state='normal') 
                    entry.configure(state='disabled')
                else:
                    entry.configure(bg='red')

    def check_multiply_mass(self, args):
        count = 0
        for element in self.molar_mass_multiply_entries:
            entry = self.molar_mass_multiply_entries[element]
            inputted_total_mass = entry.get()
            if inputted_total_mass != "":
                product = float(inputted_total_mass)
                # get the molar mass inputted by user times the number of particles  
                expected_prod = self.elements[element] * self.user_inputted_mass[element]
                if percent_error(product, expected_prod) < 2:
                    self.user_inputted_multiply_mass[element] = product
                    # set the bg to blue to check if it has been disabled by the 
                    # user inputting a correct value
                    entry.configure(state='disabled', bg='green')
                    count += 1
                else:
                    entry.configure(bg='red')
        if count == len(self.molar_mass_entries) - 1:
            self.total_molar_mass_entry.configure(state='normal')

    
    def check_moles(self, args):
        moles = self.mole_entry.get()
        if moles != "":
            moles = float(moles)
            if percent_error(moles, self.grams / self.molar_mass) < 2:
                self.mole_entry.configure(state='disabled')
                self.moles = moles
                self.show_molar_ratio()
            else:
                self.mole_entry.configure(bg='red')


    def show_grams_to_moles(self, compound):
        gram_to_mole_frame = tk.Frame(self.frame, bg='white')
        format_comp = format_subscripts(compound)
        directions_lb = tk.Label(self.frame, bg='white', text=f"Get the moles of {format_comp} by taking grams / molar mass", font=self.font25)
        formula_lb = tk.Label(gram_to_mole_frame, bg='white', text=f"{self.grams}/{self.molar_mass} = ", font=self.font25)
        units_lb = tk.Label(gram_to_mole_frame, bg='white', text=f"moles of {format_comp}", font=self.font25)
        self.mole_entry = tk.Entry(gram_to_mole_frame, bg='white', font=self.font25, width=8)

        self.mole_entry.bind("<Return>", self.check_moles)

        directions_lb.pack()
        formula_lb.grid(row=1)
        self.mole_entry.grid(row=1,column=1)
        units_lb.grid(row=1, column=2)
        gram_to_mole_frame.pack()
               

    def check_grams(self, args):
        if self.gram_entry.get() != "":
            grams = float(self.gram_entry.get())
            if percent_error(grams, self.moles * self.molar_mass) < 2:
                self.gram_entry.configure(state='disabled')
                self.result = grams
                self.display_answer()
            else:
                self.gram_entry.configure(bg='red')

    def show_moles_to_grams(self):
        format_comp = format_subscripts(self.first_compound)
        mole_to_gram_frame = tk.Frame(self.frame, bg='white')
        directions_lb = tk.Label(self.frame, bg='white', text=f"Get the grams of {format_comp} by taking moles X molar mass", font=self.font25)
        formula_lb = tk.Label(mole_to_gram_frame, bg='white', text=f"{self.moles} X {self.molar_mass}=", font=self.font25)
        units_lb = tk.Label(mole_to_gram_frame, bg='white', text=f"grams of {format_comp}", font=self.font25)
        self.gram_entry = tk.Entry(mole_to_gram_frame, bg='white', font=self.font25, width=8)
        self.gram_entry.bind("<Return>", self.check_grams)

        directions_lb.pack()
        formula_lb.grid(row=1)
        self.gram_entry.grid(row=1, column=1)
        units_lb.grid(row=1, column=2)

        mole_to_gram_frame.pack()


    def display_answer(self):
        answer_lb = tk.Label(self.frame, bg='white', text=f"So the answer is {self.result} {self.first_unit} :)", font=self.font25)
        answer_lb.pack()

    
    def check_mole_conversion(self, args):
        if self.mole_convert_entry.get() != "":
            moles = float(self.mole_convert_entry.get())
            if percent_error(moles, self.moles * self.molar_ratio) < 2:
                self.moles = moles
                self.mole_convert_entry.configure(state='disabled')
                if self.first_unit == "moles":
                    self.result = moles
                    self.display_answer()
                else:
                    self.show_molar_mass(self.first_compound)

            else:
                self.mole_convert_entry.configure(bg='red')


    def show_moles_to_moles(self):
        mole_to_mole_frame = tk.Frame(self.frame, bg='white')
        format_first_comp = format_subscripts(self.first_compound)
        format_second_comp = format_subscripts(self.second_compound)

        directions_lb = tk.Label(self.frame, bg='white', text=f"Get the moles of {format_first_comp} by taking the moles of {format_second_comp} X molar ratio ", font=('Helvetica', 20))

        formula_lb = tk.Label(mole_to_mole_frame, bg='white', text=f"{self.moles} X {self.molar_ratio} = ", font=self.font25)
        self.mole_convert_entry = tk.Entry(mole_to_mole_frame, bg='white', font=self.font25, width=4)
        units_lb = tk.Label(mole_to_mole_frame, bg='white', text=f" Moles of {self.second_compound}", font=self.font25)

        self.mole_convert_entry.bind("<Return>", self.check_mole_conversion)
        directions_lb.pack()
        formula_lb.grid(row=1)
        self.mole_convert_entry.grid(row=1, column=1)
        units_lb.grid(row=1, column=2)
        mole_to_mole_frame.pack()

         



    def check_total_molar_mass(self, args):
        if self.total_molar_mass_entry.get() != "":
            total_mass = float(self.total_molar_mass_entry.get())
            expected_mass = 0
            for element in self.user_inputted_multiply_mass:
                expected_mass += self.user_inputted_multiply_mass[element]
            if percent_error(total_mass, expected_mass) < 2:
                self.molar_mass = total_mass
                self.total_molar_mass_entry.configure(state='disabled')

                if self.grams != 0:
                    self.show_grams_to_moles(self.second_compound)
                else:
                    self.show_moles_to_grams()
                
            else:
                self.total_molar_mass_entry.configure(bg='red')
                

    def show_molar_mass(self, comp):
        molar_mass_frame = tk.Frame(self.frame, bg='white') 
        format_comp = format_subscripts(comp)
        molar_mass_dir_lb = tk.Label(self.frame, bg='white', text=f"Calculate the Molar Mass of {format_comp}", font=self.font25)
        molar_mass_tip_lb = tk.Label(self.frame, bg='white', text="Look at a periodic table to find the atomic mass of each of the following elements. \n Multiply the atomic mass by the subscript that follows that element \n Add each of the products together to get the total molar mass", font=('Helvetica', 15))

        
        total_molar_mass_label = tk.Label(molar_mass_frame, bg='white', text="Molar Mass:", font=self.font25)
        self.total_molar_mass_entry = tk.Entry(molar_mass_frame, bg='white', state='disabled', width=8, font=self.font25)
        unit_label = tk.Label(molar_mass_frame, bg='white', text="g/Mol", font=self.font25)

        molar_mass_dir_lb.pack()
        molar_mass_tip_lb.pack()
        row = 0
        #setup labels and entries for calculating molar mass
        self.elements = get_elements_from_comp(comp)
        for elem in self.elements:
            entry = tk.Entry(molar_mass_frame,width=8, bg='white',  font=self.font25)
            label = tk.Label(molar_mass_frame, bg='white', text=elem, font=self.font25)
            sub_label = tk.Label(molar_mass_frame, bg='white', text=f" X {self.elements[elem]} = ", font=self.font25)

            #holds the molar mass times the amount of particles of that element
            # disabled until the user inputs the correct molar mass for that particle
            multiply_entry = tk.Entry(molar_mass_frame, state='disabled', width=8, bg='white', font=self.font25)
            label.grid(row=row, column=0)
            entry.grid(row=row, column=1)
            sub_label.grid(row=row, column=2)
            multiply_entry.grid(row=row, column=3)

            row += 1
            multiply_entry.focus()
            entry.focus()
            self.molar_mass_multiply_entries[elem] = multiply_entry
            self.molar_mass_entries[elem] = entry
            multiply_entry.bind("<Return>", self.check_multiply_mass)
            entry.bind("<Return>", self.check_mass)
        
        total_molar_mass_label.grid(row=row, column=2)
        self.total_molar_mass_entry.grid(row=row, column=3)
        self.total_molar_mass_entry.bind("<Return>", self.check_total_molar_mass)
        unit_label.grid(row=row, column=4)

        molar_mass_frame.pack()

    def check_molar_ratio(self, args):
        # gets a tuple of the ratio
        ratio = self.equation.get_molar_ratio(self.second_compound, self.first_compound)
        count = 0
        for index, entry in enumerate(self.molar_ratio_entries):
            inputted_coeff = entry.get()
            if inputted_coeff != "":
                coeff = int(inputted_coeff)
                if coeff == ratio[index]:
                    entry.configure(state='disabled')
                    count += 1
                else: 
                    entry.configure(bg='red')

        if count == 2:
            self.molar_ratio = ratio[0] / ratio[1]
            molar_ratio = Fraction(ratio[0], ratio[1])
            mr_num = molar_ratio.numerator
            mr_den = molar_ratio.denominator
            molar_ratio_lb = tk.Label(self.frame, bg='white', text=f"Molar Ratio: {mr_num}/{mr_den}", font=('Helvetica', 20))
            molar_ratio_lb.pack()
            self.show_moles_to_moles() 


        


    def show_molar_ratio(self):
        molar_ratio_frame = tk.Frame(self.frame, bg='white') 
        molar_ratio_step_lb = tk.Label(self.frame, bg='white', font=self.font25, text="Find the Molar Ratio")
        molar_ratio_dir_label = tk.Label(self.frame, wraplength=600, justify='center', bg='white', text=f"Get the coefficient of {self.format_first_comp} and divide it by the coefficient of {self.format_second_comp}", font=('Helvetica', 18))
        first_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_second_comp} Coeff:")
        first_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20))

        second_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_first_comp} Coeff:")
        second_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20))


        self.molar_ratio_entries[0] = second_compound_entry
        self.molar_ratio_entries[1] = first_compound_entry
        second_compound_entry.bind("<Return>", self.check_molar_ratio)
        first_compound_entry.bind("<Return>", self.check_molar_ratio)

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
        if self.second_unit == "grams":
            self.show_molar_mass(self.second_compound)
        else:
            self.show_molar_ratio()



    def check_balance(self,args):
        count = 0
        for compound in self.balance_entries:
            entry = self.balance_entries[compound]
            inputted_coeff = entry.get()
            if inputted_coeff != "":
                coeff = int(inputted_coeff)
                if self.equation.is_correct_coeff(coeff, compound):
                    entry.configure(state='disabled')
                    count += 1
                else:
                    entry.configure(bg='red')
        if count == len(self.balance_entries):
            self.check_next_step()

    # called if user can't balance the equation themselves
    def balance_equation(self):
        for compound in self.balance_entries:
            entry = self.balance_entries[compound]
            current_val = entry.get()
            entry.delete(0,len(current_val))
            entry.insert(0,str(self.equation.get_correct_coeff(compound)))
            entry.configure(state='disabled')

        self.help_button.configure(state='disabled')
        self.check_next_step()



    # compounds is either reactants or products
    #side is a char containing a p or r 
    def show_equation_balance(self,frame, compounds, side):
        for index, comp in enumerate(compounds):
            entry_box = tk.Entry(frame, width=2, bg='white', font=('Helvetica', 20))
            self.balance_entries[comp] = entry_box
            entry_box.bind("<Return>", self.check_balance)
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

            entry_box.grid(row=0,column=self.col)
            self.col += 1
            compound_str.grid(row=0, column=self.col)
            self.col += 1
        if side == 'p':
           self.help_button = tk.Button(frame, height=2, bg='white', text="Help Me", command=self.balance_equation) 
           self.help_button.grid(row=0, column=self.col)


    def setup_problem(self):
        random.seed(time.time())
        self.equation = equations[random.randrange(0,48)]
        self.formula = self.equation.get_formula()

        self.first_unit = random.choice(["grams", "moles"]) 
        self.first_compound = self.formula.pop(random.randrange(len(self.formula)))
        self.format_first_comp = format_subscripts(self.first_compound)

        self.second_unit = random.choice(["grams", "moles"]) 
        self.second_compound = self.formula.pop(random.randrange(len(self.formula)))
        self.format_second_comp = format_subscripts(self.second_compound)

        molar_mass = calculate_molar_mass(self.second_compound)
        self.amount = round(random.uniform(1,molar_mass * 3),3)

        if self.second_unit == "moles":
            self.moles = self.amount
        else:
            self.grams = self.amount

        problem_str = f"How many {self.first_unit} of {self.format_first_comp} do I need to produce {self.amount} {self.second_unit} of {self.format_second_comp}"
        self.show_practice_widgets(problem_str,self.equation)

    def set_problem(self):
        if self.equation_entry.get() != 0:
            self.equation = parse_equation(self.equation_entry.get())
            self.formula = self.equation.get_formula()
            self.equation_entry_button.configure(state='disabled')


    def setup_help(self):
        dir_label = tk.Label(self.frame,bg='white', text="Enter a chemical reaction in the form: Mg(OH)2 = (MgOH)2O + H20", font=self.font25)
        self.equation_entry = tk.Entry(self.frame, bg='white', width=50, font=('Helvetica', 20))
        self.equation_entry_button = tk.Button(self.frame, height=3, text="Enter", command = self.set_problem)

        dir_label.pack()
        self.equation_entry.pack()
        self.equation_entry_button.pack()

    def show_practice_widgets(self, problem_str, eq):
        problem_lb = tk.Label(self.frame, bg='white', text=problem_str, anchor='center')
        problem_lb.configure(font=('Helvetica', 18), height=1)
        step_one_lb = tk.Label(self.frame, bg='white', text="Balance the Equation", anchor='center')
        step_one_lb.configure(font=self.font25)
        problem_lb.pack(pady=20)
        step_one_lb.pack(pady=10)

        balancing_frame = tk.Frame(self.frame, bg='white') 
        self.show_equation_balance(balancing_frame, eq.get_reactants(), 'r')
        self.show_equation_balance(balancing_frame, eq.get_products(), 'p')
        balancing_frame.pack()

