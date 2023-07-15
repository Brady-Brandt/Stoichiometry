import tkinter as tk 
from chempy.util.periodic import names, symbols, relative_atomic_masses


class Element:
    def __init__(self,window, atomic_num) -> None:
        self.screen = window 
        self.color = 'orange'
        self.frame_size = 60
        self.atomic = atomic_num
        self.element = names[atomic_num - 1]
        self.symbol = symbols[atomic_num - 1]
        self.mass = round(relative_atomic_masses[atomic_num-1], 4)
        self.frame = tk.Frame(window, bg=self.color, highlightbackground='black', highlightthickness=0.5,  width=self.frame_size, height=self.frame_size, pady=0, padx=0)

        self.symbol_lb = tk.Label(self.frame, bg=self.color, text=f"{self.symbol}", font=('Helvetica', 13))
        self.atomic_lb = tk.Label(self.frame, bg=self.color, text=str(self.atomic), font=('Helvetica', 8))
        self.mass_lb = tk.Label(self.frame, bg=self.color, text=str(self.mass), font=('Helvetica', 8))

        self.atomic_lb.pack_propagate(False)
        self.symbol_lb.pack_propagate(False)
        self.atomic_lb.pack(side='top', anchor="nw", padx=0, pady=0, ipadx=0, ipady=0)
        self.symbol_lb.pack(padx=0, pady=0, ipadx=0, ipady=0)
        self.mass_lb.pack()

    # allows us to place the element and set its color at the same time
    def place(self, x, y, color='orange'):
        self.frame.pack_propagate(False)
        self.frame.configure(bg=color)
        self.atomic_lb.configure(bg=color)
        self.mass_lb.configure(bg=color)
        self.symbol_lb.configure(bg=color)
        
        self.frame.place(x=x, y=y)

class PeriodicTable:
    def __init__(self, screen):
        self.window = tk.Toplevel(screen)
        self.window.title("Periodic Table")
        self.window.geometry("1080x600")
        self.window.resizable(False, False) 
        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
        self.window.withdraw()


        self.window_width = 1080
        self.window_height = 600

        self.elements = []
        # size of each box on the periodic table 
        self.frame_size = 60
        for atomic_number in range(1,119):
            self.elements.append(Element(self.window, atomic_number))

    def draw_nonmetals(self):
        #draws Hydrogen, Boron, Carbon, Nitrogen, Oxygen
        # Silicon, Phosphorous, Sulfur, Arscenic, Se, Te 
        nonmetal_color = "#FF7377" 
        self.elements[0].place(0,0,nonmetal_color) #Hydrogen
        boron_x_pos = self.frame_size * 11
        index = 4
        #draws Boron, Carbon, Nitrogen, Oxygen
        for i in range(1,5):
            self.elements[index].place(boron_x_pos + i * self.frame_size,self.frame_size, nonmetal_color)
            index += 1

        silicon_x_pos = self.frame_size * 12 

        index = 13
        #draws silicon, Phosphorous, Sulfur 
        for i in range(1,4):
            self.elements[index].place(silicon_x_pos + i * self.frame_size,self.frame_size * 2, nonmetal_color)
            index += 1

        self.elements[32].place(self.frame_size * 14,self.frame_size * 3,nonmetal_color) #Arscenic
        self.elements[33].place(self.frame_size * 15,self.frame_size * 3 ,nonmetal_color) #Se 
        self.elements[51].place(self.frame_size * 15,self.frame_size * 4,nonmetal_color) #Te 
        
    def draw_alkali_metals(self):
        alkali_metals_atomic_nums = [3,11,19,37,55,87]
        alkali_metal_color = "#FFD69A"
        x_offset = 1
        for atomic_num in alkali_metals_atomic_nums:
            # subtract one because of 0 based indexing 
            self.elements[atomic_num - 1].place(0,self.frame_size * x_offset, alkali_metal_color)
            x_offset += 1


    def draw_alkaline_earth_metals(self):
        alkaline_earth_metals_atomic_nums = [4,12,20,38,56,88]
        alkaline_earth_metals_color = "#AB7E4C"
        y_offset = 1
        for atomic_num in alkaline_earth_metals_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size, self.frame_size * y_offset, alkaline_earth_metals_color)
            y_offset += 1

    def draw_lanthaniod(self):
        lanthanoid_color = "#A1DF50"
        self.elements[56].place(self.frame_size * 2,self.frame_size * 5, lanthanoid_color)
        atomic_num = 57 
        x_offset = 2
        for i in range(atomic_num, 71):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 7 + 30, lanthanoid_color)
            x_offset += 1

    def draw_actinoid(self):
        actinoid_color = "#87CEEB"
        self.elements[88].place(self.frame_size * 2,self.frame_size * 6, actinoid_color) #Ac
        atomic_num = 89 
        x_offset = 2
        for i in range(atomic_num, 103):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 8 + 30, actinoid_color)
            x_offset += 1

    def draw_transition_metals(self):
        transition_metal_color = "#9966CB"
        #draw first row
        # Sc - Zn 
        x_offset = 2 
        for i in range(20, 30):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 3, transition_metal_color)
            x_offset += 1

        #draw second row 
        x_offset = 2 
        for i in range(38, 48):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 4, transition_metal_color)
            x_offset += 1

        #draw third row 
        x_offset = 3 
        for i in range(71, 80):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 5, transition_metal_color)
            x_offset += 1

        #draw fourth row 
        x_offset = 3 
        for i in range(103, 112):
            self.elements[i].place(self.frame_size * x_offset,self.frame_size * 6, transition_metal_color)
            x_offset += 1

    def draw_halogens(self):
        halogen_atomic_nums = [9,17,35,53,85,117]
        halogen_color = "#3DED97"
        y_offset = 1 
        for atomic_num in halogen_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size * 16, self.frame_size * y_offset, halogen_color)
            y_offset += 1

    def draw_noble_gases(self):
        noble_gas_atomic_nums = [2,10,18,36,54,86,118]
        noble_gas_color = "#FF69B4"
        y_offset = 0
        for atomic_num in noble_gas_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size * 17, self.frame_size * y_offset, noble_gas_color)
            y_offset += 1

    def draw_metals(self):
        metal_color = "Yellow"
        col_thirteen_atomic_nums = [13,31,49,81,113]
        y_offset = 2 
        for atomic_num in col_thirteen_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size * 12, self.frame_size * y_offset, metal_color)
            y_offset += 1

        y_offset = 3
        col_fourteen_atomic_nums = [32,50,82,114]
        for atomic_num in col_fourteen_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size * 13, self.frame_size * y_offset, metal_color)
            y_offset += 1

        col_fifteen_atomic_nums = [51,83,115]
        y_offset = 4 
        for atomic_num in col_fifteen_atomic_nums:
            self.elements[atomic_num - 1].place(self.frame_size * 14, self.frame_size * y_offset, metal_color)
            y_offset += 1

        # Po and Lv 
        self.elements[83].place(self.frame_size * 15, self.frame_size * 5, metal_color)
        self.elements[115].place(self.frame_size * 15, self.frame_size * 6, metal_color)


    def show_periodic_table(self):
        self.window.wm_deiconify()
        self.draw_nonmetals()
        self.draw_alkali_metals()
        self.draw_alkaline_earth_metals()
        self.draw_lanthaniod()
        self.draw_actinoid()
        self.draw_transition_metals()
        self.draw_halogens()
        self.draw_noble_gases()
        self.draw_metals()


