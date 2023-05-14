import tkinter as tk
from equation import *
from fractions import Fraction
import time
import random


equations = parse_equations()


class Practice:
    def __init__(self, screen, width, height, canvas, scrollbar):
        self.screen = screen
        self.width = width
        self.heigh = height
       
        self.canvas = canvas
        self.scrollbar = scrollbar
        self.canvas.configure(yscrollcommand = self.scrollbar.set, width=self.screen.winfo_width(), height=self.screen.winfo_height())
        self.scroll_frame = tk.Frame(self.canvas)         
        self.scroll_frame.bind('<Configure>', self.conf_frame)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 

        self.window = self.canvas.create_window((0,0), width=self.canvas["width"], window=self.scroll_frame, anchor='nw')
        self.canvas.pack()


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
        self.option_values = []
        self.amount_entry = None
        self.help_solve_button = None
        self.help_button = None


        self.equation = None
        # used for displaying equation
        self.col = 0

        self.font25 = ('Helvetica', 25)


        # all relate to the current problem 
        self.formula = []
        self.reactants = []
        self.reacants = []

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

        self.vcmd = (self.screen.register(self.validate_digits), '%P')
        
        #hot fix for a bug that shows the answer if you keep hitting enter
        self.has_shown_answer = False

    def conf_frame(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=self.screen.winfo_width(), height=self.screen.winfo_height())

    def configure_canvas(self, event):
        if self.canvas.winfo_width() != self.screen.winfo_width():
            self.canvas["width"] = self.screen.winfo_width()
            self.canvas.itemconfig(self.window, width=self.canvas["width"])
        if self.canvas.winfo_height() != self.screen.winfo_height():
            self.canvas["height"] = self.screen.winfo_height()


    # makes sure user only inputs digits into entry 
    def validate_digits(self, val):
        if val == "" or val == ".":
            return True
        try:
            float(val)
            return True
        except ValueError:
            return False
        return False



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
        gram_to_mole_frame = tk.Frame(self.scroll_frame, bg='white')
        format_comp = format_subscripts(compound)
        directions_lb = tk.Label(self.scroll_frame, bg='white', text=f"Get the moles of {format_comp} by taking grams / molar mass", font=self.font25)
        formula_lb = tk.Label(gram_to_mole_frame, bg='white', text=f"{self.grams}/{self.molar_mass} = ", font=self.font25)
        units_lb = tk.Label(gram_to_mole_frame, bg='white', text=f"moles of {format_comp}", font=self.font25)
        self.mole_entry = tk.Entry(gram_to_mole_frame, bg='white', font=self.font25, width=8, validate='all', validatecommand=self.vcmd)

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
        mole_to_gram_frame = tk.Frame(self.scroll_frame, bg='white')
        directions_lb = tk.Label(self.scroll_frame, bg='white', text=f"Get the grams of {format_comp} by taking moles X molar mass", font=self.font25)
        formula_lb = tk.Label(mole_to_gram_frame, bg='white', text=f"{self.moles} X {self.molar_mass}=", font=self.font25)
        units_lb = tk.Label(mole_to_gram_frame, bg='white', text=f"grams of {format_comp}", font=self.font25)
        self.gram_entry = tk.Entry(mole_to_gram_frame, bg='white', font=self.font25, width=8, validate='all', validatecommand=self.vcmd)
        self.gram_entry.bind("<Return>", self.check_grams)

        directions_lb.pack()
        formula_lb.grid(row=1)
        self.gram_entry.grid(row=1, column=1)
        units_lb.grid(row=1, column=2)

        mole_to_gram_frame.pack()


    def display_answer(self):
        if not self.has_shown_answer:
            answer_lb = tk.Label(self.scroll_frame, bg='white', text=f"So the answer is {self.result} {self.first_unit} :)", font=self.font25)
            answer_lb.pack()
            self.has_shown_answer = True
    
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
        mole_to_mole_frame = tk.Frame(self.scroll_frame, bg='white')
        format_first_comp = format_subscripts(self.first_compound)
        format_second_comp = format_subscripts(self.second_compound)

        directions_lb = tk.Label(self.scroll_frame, bg='white', text=f"Get the moles of {format_first_comp} by taking the moles of {format_second_comp} X molar ratio ", font=('Helvetica', 20))

        formula_lb = tk.Label(mole_to_mole_frame, bg='white', text=f"{self.moles} X {self.molar_ratio} = ", font=self.font25)
        self.mole_convert_entry = tk.Entry(mole_to_mole_frame, bg='white', font=self.font25, width=8, validate='all', validatecommand=self.vcmd)
        units_lb = tk.Label(mole_to_mole_frame, bg='white', text=f" Moles of {self.format_first_comp}", font=self.font25)

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
        molar_mass_frame = tk.Frame(self.scroll_frame, bg='white') 
        format_comp = format_subscripts(comp)
        molar_mass_dir_lb = tk.Label(self.scroll_frame, bg='white', text=f"Calculate the Molar Mass of {format_comp}", font=self.font25)
        molar_mass_tip_lb = tk.Label(self.scroll_frame, bg='white', text="Look at a periodic table to find the atomic mass of each of the following elements. \n Multiply the atomic mass by the subscript that follows that element \n Add each of the products together to get the total molar mass", font=('Helvetica', 15))

        
        total_molar_mass_label = tk.Label(molar_mass_frame, bg='white', text="Molar Mass:", font=self.font25)
        self.total_molar_mass_entry = tk.Entry(molar_mass_frame, bg='white', state='disabled', width=8, font=self.font25, validate='all', validatecommand=self.vcmd)
        unit_label = tk.Label(molar_mass_frame, bg='white', text="g/Mol", font=self.font25)

        molar_mass_dir_lb.pack()
        molar_mass_tip_lb.pack()
        row = 0
        #setup labels and entries for calculating molar mass
        self.elements = get_elements_from_comp(comp)
        self.user_inputted_mass = {}
        self.user_inputted_multiply_mass = {}
        self.molar_mass_multiply_entries = {}
        self.molar_mass_entries = {}

        for elem in self.elements:
            entry = tk.Entry(molar_mass_frame,width=8, bg='white',  font=self.font25, validate='all', validatecommand=self.vcmd)
            label = tk.Label(molar_mass_frame, bg='white', text=elem, font=self.font25)
            sub_label = tk.Label(molar_mass_frame, bg='white', text=f" X {self.elements[elem]} = ", font=self.font25)

            #holds the molar mass times the amount of particles of that element
            # disabled until the user inputs the correct molar mass for that particle
            multiply_entry = tk.Entry(molar_mass_frame, state='disabled', width=8, bg='white', font=self.font25, validate='all', validatecommand=self.vcmd)
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
        ratio = self.equation.get_molar_ratio(self.first_compound, self.second_compound)
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
            molar_ratio_lb = tk.Label(self.scroll_frame, bg='white', text=f"Molar Ratio: {mr_num}/{mr_den}", font=('Helvetica', 20))
            molar_ratio_lb.pack()
            self.show_moles_to_moles() 


        


    def show_molar_ratio(self):
        molar_ratio_frame = tk.Frame(self.scroll_frame, bg='white') 
        molar_ratio_step_lb = tk.Label(self.scroll_frame, bg='white', font=self.font25, text="Find the Molar Ratio")
        molar_ratio_dir_label = tk.Label(self.scroll_frame, wraplength=500, justify='center', bg='white', text=f"Get the coefficient of {self.format_first_comp} and divide it by the coefficient of {self.format_second_comp}", font=('Helvetica', 18))
        first_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_second_comp} Coeff:")
        first_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20), validate='all', validatecommand=self.vcmd)

        second_compound_lb = tk.Label(molar_ratio_frame, bg='white', font=('Helvetica', 20), text=f"{self.format_first_comp} Coeff:")
        second_compound_entry = tk.Entry(molar_ratio_frame, width=2, bg='white', font=('Helvetica', 20), validate='all', validatecommand=self.vcmd)


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
    # input one coeff at a time 
    def balance_equation(self):
        count = 0
        for compound in self.balance_entries:
            entry = self.balance_entries[compound]
            if entry["state"] == 'disabled':
                count += 1
                continue
            else:
                count += 1
                current_val = entry.get()
                entry.delete(0,len(current_val))
                entry.insert(0,str(self.equation.get_correct_coeff(compound)))
                entry.configure(state='disabled')
                break

        if count == len(self.balance_entries):
            self.help_button.configure(state='disabled')
            self.check_next_step()



    # compounds is either reactants or products
    #side is a char containing a p or r 
    def show_equation_balance(self, frame, compounds, side):
        for index, comp in enumerate(compounds):
            entry_box = tk.Entry(frame, width=2, bg='white', font=('Helvetica', 20), validate='all', validatecommand=self.vcmd)
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
        self.equation = equations[random.randrange(0,len(equations)-1)]
        self.formula = self.equation.get_formula()
        self.reactants = list(self.equation.get_reactants().keys())
        self.products= list(self.equation.get_products().keys())

        self.first_unit = random.choice(["grams", "moles"]) 
        self.second_unit = random.choice(["grams", "moles"])

        first_is_react = random.randrange(0,2)
        if first_is_react:
            which_reaction = "do I need to produce"
            self.first_compound = self.reactants.pop(random.randrange(len(self.reactants))) 
            self.second_compound = self.products.pop(random.randrange(len(self.products)))

        else:
            self.first_compound = self.products.pop(random.randrange(len(self.products))) 
            self.second_compound = self.reactants.pop(random.randrange(len(self.reactants)))
            which_reaction = "will I produce if I react"

        self.format_first_comp = format_subscripts(self.first_compound)
        self.format_second_comp = format_subscripts(self.second_compound)
        molar_mass = calculate_molar_mass(self.second_compound)
        self.amount = round(random.uniform(1,molar_mass * 3),3)

        if self.second_unit == "moles":
            self.moles = self.amount
        else:
            self.grams = self.amount

        problem_str = f"How many {self.first_unit} of {self.format_first_comp} {which_reaction} {self.amount} {self.second_unit} of {self.format_second_comp}"
        self.show_practice_widgets(problem_str,self.equation)

    def check_options(self):
        error_frame = tk.Frame(self.scroll_frame)
        failed_to_fill = tk.Label(error_frame, text='Need to fill everything out', fg='red')
        error_lb = tk.Label(error_frame, text="Error: Need to input one product and one reactant", fg='red')

        first_units = self.option_values[0].get() 
        first_comp = self.option_values[1].get()
        second_units = self.option_values[2].get()
        second_comp = self.option_values[3].get()


        if first_units != "Units" and second_units != "Units" and first_comp != "Compound" and second_comp != "Compound":
            if first_comp in self.reactants and second_comp in self.products or first_comp in self.products and second_comp in self.reactants and self.amount_entry.get() != "":
                self.first_unit = first_units
                self.second_unit = second_units
                self.first_compound = first_comp
                self.second_compound = second_comp
                self.amount = float(self.amount_entry.get())
                self.format_first_comp = format_subscripts(self.first_compound)
                self.format_second_comp = format_subscripts(self.second_compound)
                problem_str = f"How many {self.first_unit} of {self.format_first_comp} do I need to produce {self.amount} {self.second_unit} of {self.format_second_comp}"
                self.show_practice_widgets(problem_str,self.equation)


                if self.second_unit == "moles":
                     self.moles = self.amount
                else:
                    self.grams = self.amount

                error_frame.destroy()
                self.help_solve_button.configure(state='disabled')

            else:
                error_frame.pack()
                error_lb.pack()
        else:
            error_frame.pack()
            failed_to_fill.pack()
         
                


    def set_problem(self):
        self.equation_entry.configure(bg='white')
        if self.equation_entry.get() != "":
            self.equation = parse_equation(self.equation_entry.get())
            if self.equation == None or len(self.equation.get_reactants()) == 0 or len(self.equation.get_products()) == 0:
                self.equation_entry.configure(bg='red')
            else:
                self.reactants = list(self.equation.get_reactants().keys())
                self.products= list(self.equation.get_products().keys())

                self.formula = self.equation.get_formula()
                self.equation_entry_button.configure(state='disabled')
                frame = tk.Frame(self.scroll_frame, bg='white')
                opt_font = ('Helvetica', 15)
                start_lb = tk.Label(frame, bg='white', text="How many", font=opt_font)
                first_opt_val = tk.StringVar(frame, "Units")
                first_opt_menu = tk.OptionMenu(frame,first_opt_val, *["grams", "moles"])
               
                
                second_opt_val = tk.StringVar(frame, "Compound")
                second_opt_menu = tk.OptionMenu(frame, second_opt_val,*self.formula) 

                self.amount_entry = tk.Entry(frame, width=8, bg='white', validate='all', validatecommand=self.vcmd, font=opt_font)

                third_opt_val = tk.StringVar(frame, "Units")
                third_opt_menu = tk.OptionMenu(frame,third_opt_val, *["grams", "moles"])
                fourth_opt_val = tk.StringVar(frame, "Compound")
                fourth_opt_menu = tk.OptionMenu(frame, fourth_opt_val,*self.formula)

                self.option_values = [first_opt_val, second_opt_val, third_opt_val, fourth_opt_val]

                frame.pack()
                start_lb.grid(row=0)
                first_opt_menu.grid(row=0, column=1)
                tk.Label(frame, bg='white', text=" of ", font=self.font25).grid(row=0, column=2)
                second_opt_menu.grid(row=0, column=3)
                tk.Label(frame, bg='white', font=('Helvetica', 15),text=" do I need to produce").grid(row=1)
                self.amount_entry.grid(row=1,column=1)
                third_opt_menu.grid(row=1,column=2)
                tk.Label(frame, bg='white', text=" of ", font=self.font25).grid(row=1, column=3)
                fourth_opt_menu.grid(row=1,column=4)
                self.help_solve_button = tk.Button(self.scroll_frame, text='Help me Solve', height=2, command=self.check_options)
                self.help_solve_button.pack()




    def setup_help(self):
        dir_label = tk.Label(self.scroll_frame,bg='white', text="Enter a chemical reaction in the form: Mg(OH)2 = (MgOH)2O + H20\n Do not enter the physical state for example F(s)", font=self.font25)
        self.equation_entry = tk.Entry(self.scroll_frame, bg='white', width=50, font=('Helvetica', 20))
        self.equation_entry_button = tk.Button(self.scroll_frame, height=3, text="Enter", command = self.set_problem)

        dir_label.pack()
        self.equation_entry.pack()
        self.equation_entry_button.pack()

    def show_practice_widgets(self, problem_str, eq):
        problem_lb = tk.Label(self.scroll_frame, bg='white', text=problem_str, anchor='center')
        problem_lb.configure(font=('Helvetica', 18), height=1)
        step_one_lb = tk.Label(self.scroll_frame, bg='white', text="Balance the Equation", anchor='center')
        step_one_lb.configure(font=self.font25)
        problem_lb.pack(pady=20)
        step_one_lb.pack(pady=10)

        balancing_frame = tk.Frame(self.scroll_frame, bg='white') 
        self.show_equation_balance(balancing_frame, eq.get_reactants(), 'r')
        self.show_equation_balance(balancing_frame, eq.get_products(), 'p')
        balancing_frame.pack()

