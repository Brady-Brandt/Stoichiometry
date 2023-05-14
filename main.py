import tkinter as tk
from equation import *
from practice import *


class Root:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        

        self.menu_frame = tk.Frame(self.screen, bg='white')
        self.canvas = tk.Canvas(self.screen, bg='white', highlightthickness=0, borderwidth=0)
        self.menu_button = tk.Button(self.screen, height = 2, text="Main Menu", command = self.show_main_menu)
        self.scrollbar = tk.Scrollbar(self.screen, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack()
        #0 menu
        # 1 practice or help 
        self.which_frame = 0

        self.scrollbar.pack(side='right', fill='y')
    def show_main_menu(self):

        if self.which_frame == 1:
            for widget in self.canvas.winfo_children():
                widget.destroy()
            self.canvas.forget()

        self.menu_button.forget()         
        self.menu_frame.pack()
        #main menu 
        title = tk.Label(self.menu_frame,text = "Stoichiometry Interactive Guide", font=('Helvetica bold', 25), bg='white')
        stoich_practice_button = tk.Button(self.menu_frame, bg='white', text="Stoichiometry Practice", width =20, height=3)
        stoich_problem_button = tk.Button(self.menu_frame, bg='white', text="Stoichiometry Problem Help", width=20,height=3)

        title.pack(pady=100)
        stoich_practice_button.pack(pady=20)
        stoich_problem_button.pack(pady=20)
        

        stoich_problem_button.config(command=self.start_help)
        stoich_practice_button.config(command = self.start_practice) 

    def start_practice(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        
        self.menu_frame.forget()


        self.which_frame = 1
        self.menu_button.pack(side='top', anchor='nw')
        practice_session = Practice(self.screen, self.WIDTH, self.HEIGHT, self.canvas, self.scrollbar)
        practice_session.setup_problem()
        
    def start_help(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        self.menu_frame.forget()
        self.which_frame = 1

        self.menu_button.pack(side='top', anchor='nw')
        help_session = Practice(self.screen, self.WIDTH, self.HEIGHT, self.canvas, self.scrollbar)
        help_session.setup_help()
        




WIDTH = 800
HEIGHT = 800
screen = tk.Tk()
screen.geometry("800x800")
screen.title("Stoichiometry")
screen["bg"] = "white"
root = Root(screen, WIDTH, HEIGHT)
root.show_main_menu()




screen.mainloop()


