import tkinter as tk
from equation import *
from practice import *


class Root:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.menu_widgets = []
        
        self.practice_session = Practice(self.screen, self.WIDTH, self.HEIGHT)
        self.GRAMS = "grams"
        self.MOLES = "moles"
    def show_main_menu(self):
        #main menu 
        title = tk.Label(text = "Stoichiometry Interactive Guide")
        title.config(font =('Helvetica bold', 25))

        stoich_practice_button = tk.Button(screen, text="Stoichiometry Practice", width =20, height=3)
        stoich_problem_button = tk.Button(screen, text="Stoichiometry Problem Help", width=20,height=3)

        title.place(x = WIDTH / 2 - 200, y = 200)
        stoich_practice_button.place(x=self.WIDTH / 2 - 100, y=self.HEIGHT / 2)
        stoich_problem_button.place(x=self.WIDTH / 2 - 100, y=self.HEIGHT / 2 + 100)
        

        self.menu_widgets = [title, stoich_practice_button, stoich_problem_button]
        stoich_practice_button.config(command = self.start_practice) 

    def start_practice(self):
        for widget in self.menu_widgets:
            widget.place_forget()

        self.practice_session.setup_problem()
        





WIDTH = 800
HEIGHT = 800
screen = tk.Tk()
screen.geometry("800x800")
screen.title("Stoichiometry")
screen["bg"] = "white"
root = Root(screen, WIDTH, HEIGHT)
root.show_main_menu()




screen.mainloop()


