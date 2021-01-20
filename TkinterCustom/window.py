import tkinter as tk
from tkinter import ttk
from TkinterCustom.food import FoodFrame
from TkinterCustom.recipe import RecipeFrame
from TkinterCustom.diet import DietFrame
from TkinterCustom.inventory import InventoryFrame
from TkinterCustom.groceries import GroceryFrame


# TODO arreglar un poco la organización de los widgets en general, pero una vez esté hecho todo
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Main window configuration
        self.title("OneThousandFoods")
        self.resizable(width=1, height=1)
        # Tabs Configuration
        self.Notebook = ttk.Notebook(self)
        self.Notebook.pack(fill='both', expand='yes')
        # Food tab
        self.TabFood = FoodFrame(self.Notebook, bg='#EEEEEE')
        # Recipe tab
        self.TabRecipes = RecipeFrame(self.Notebook, bg='#EEEEEE')
        # Diet Tab
        self.TabDiet = DietFrame(self.Notebook, bg='#EEEEEE')
        # Inventory tab
        self.TabInventory = InventoryFrame(self.Notebook, bg='#EEEEEE')
        # Grocery tab
        self.TabLogGrocery = GroceryFrame(self.Notebook, bg='#EEEEEE')
        # Apply Tabs
        self.Notebook.add(self.TabFood, text='Alimentos')
        self.Notebook.add(self.TabRecipes, text='Recetas')
        self.Notebook.add(self.TabDiet, text='Dieta')
        self.Notebook.add(self.TabInventory, text='Inventario')
        self.Notebook.add(self.TabLogGrocery, text='Compras')
        # Add Click event of every tab
        self.Notebook.bind("<<NotebookTabChanged>>", self.manage_tab_change)
        # Launch
        self.mainloop()

    def manage_tab_change(self, event):
        pass
