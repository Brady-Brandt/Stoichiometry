import tkinter as tk 
from chempy.util.periodic import names, symbols, relative_atomic_masses

element_boxes = []

win_width = 1080
win_height = 600
element_width = 60

#draws Hydrogen, Boron, Carbon, Nitrogen, Oxygen
# Silicon, Phosphorous, Sulfur, Arscenic, Se, Te 
def draw_nonmetals():
    nonmetal_color = "#FF7377" 

    element_boxes[0].place(0,0,nonmetal_color) #Hydrogen
    boron_x_pos = element_width * 11
    index = 4
    #draws Boron, Carbon, Nitrogen, Oxygen
    for i in range(1,5):
        element_boxes[index].place(boron_x_pos + i * element_width,element_width, nonmetal_color)
        index += 1

    silicon_x_pos = element_width * 12 

    index = 13
    #draws silicon, Phosphorous, Sulfur 
    for i in range(1,4):
        element_boxes[index].place(silicon_x_pos + i * element_width,element_width * 2, nonmetal_color)
        index += 1

    element_boxes[32].place(element_width * 14,element_width * 3,nonmetal_color) #Arscenic
    element_boxes[33].place(element_width * 15,element_width * 3 ,nonmetal_color) #Se 
    element_boxes[51].place(element_width * 15,element_width * 4,nonmetal_color) #Te 

def draw_alkali_metals():
    alkali_metals_atomic_nums = [3,11,19,37,55,87]
    alkali_metal_color = "#FFD69A"
    x_offset = 1
    for atomic_num in alkali_metals_atomic_nums:
        # subtract one because of 0 based indexing 
        element_boxes[atomic_num - 1].place(0,element_width * x_offset, alkali_metal_color)
        x_offset += 1

def draw_alkaline_earth_metals():
    alkaline_earth_metals_atomic_nums = [4,12,20,38,56,88]
    alkaline_earth_metals_color = "#AB7E4C"
    y_offset = 1
    for atomic_num in alkaline_earth_metals_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width, element_width * y_offset, alkaline_earth_metals_color)
        y_offset += 1

def draw_lanthaniod():
    lanthanoid_color = "#A1DF50"
    element_boxes[56].place(element_width * 2,element_width * 5, lanthanoid_color)
    atomic_num = 57 
    x_offset = 2
    for i in range(atomic_num, 71):
        element_boxes[i].place(element_width * x_offset,element_width * 7 + 30, lanthanoid_color)
        x_offset += 1

def draw_actinoid():
    actinoid_color = "#87CEEB"
    element_boxes[88].place(element_width * 2,element_width * 6, actinoid_color) #Ac
    atomic_num = 89 
    x_offset = 2
    for i in range(atomic_num, 103):
        element_boxes[i].place(element_width * x_offset,element_width * 8 + 30, actinoid_color)
        x_offset += 1

def draw_transition_metals():
    transition_metal_color = "#9966CB"
    #draw first row
    # Sc - Zn 
    x_offset = 2 
    for i in range(20, 30):
        element_boxes[i].place(element_width * x_offset,element_width * 3, transition_metal_color)
        x_offset += 1

    #draw second row 
    x_offset = 2 
    for i in range(38, 48):
        element_boxes[i].place(element_width * x_offset,element_width * 4, transition_metal_color)
        x_offset += 1

    #draw third row 
    x_offset = 3 
    for i in range(71, 80):
        element_boxes[i].place(element_width * x_offset,element_width * 5, transition_metal_color)
        x_offset += 1

    #draw fourth row 
    x_offset = 3 
    for i in range(103, 112):
        element_boxes[i].place(element_width * x_offset,element_width * 6, transition_metal_color)
        x_offset += 1

def draw_halogens():
    halogen_atomic_nums = [9,17,35,53,85,117]
    halogen_color = "#3DED97"
    y_offset = 1 
    for atomic_num in halogen_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width * 16, element_width * y_offset, halogen_color)
        y_offset += 1

def draw_noble_gases():
    noble_gas_atomic_nums = [2,10,18,36,54,86,118]
    noble_gas_color = "#FF69B4"
    y_offset = 0
    for atomic_num in noble_gas_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width * 17, element_width * y_offset, noble_gas_color)
        y_offset += 1

def draw_metals():
    metal_color = "Yellow"
    col_thirteen_atomic_nums = [13,31,49,81,113]
    y_offset = 2 
    for atomic_num in col_thirteen_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width * 12, element_width * y_offset, metal_color)
        y_offset += 1

    y_offset = 3
    col_fourteen_atomic_nums = [32,50,82,114]
    for atomic_num in col_fourteen_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width * 13, element_width * y_offset, metal_color)
        y_offset += 1

    col_fifteen_atomic_nums = [51,83,115]
    y_offset = 4 
    for atomic_num in col_fifteen_atomic_nums:
        element_boxes[atomic_num - 1].place(element_width * 14, element_width * y_offset, metal_color)
        y_offset += 1

    # Po and Lv 
    element_boxes[83].place(element_width * 15, element_width * 5, metal_color)
    element_boxes[115].place(element_width * 15, element_width * 6, metal_color)





class ElementBox:
    def __init__(self,window, atomic_num) -> None:
        self.screen = window 
        self.color = 'orange'
        self.atomic = atomic_num
        self.element = names[atomic_num - 1]
        self.symbol = symbols[atomic_num - 1]
        self.mass = round(relative_atomic_masses[atomic_num-1], 4)
        self.frame = tk.Frame(window, bg=self.color, highlightbackground='black', highlightthickness=0.5,  width=element_width, height=element_width, pady=0, padx=0)

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


def place_elements(screen):
    window = tk.Toplevel(screen)
    window.title("Periodic Table")
    window.geometry("1080x600")
    window.resizable(False, False)

    for i in range(1,119):
        element_boxes.append(ElementBox(window, i))

    draw_nonmetals()
    draw_alkali_metals()
    draw_alkaline_earth_metals()
    draw_lanthaniod()
    draw_actinoid()
    draw_transition_metals()
    draw_halogens()
    draw_noble_gases()
    draw_metals()
