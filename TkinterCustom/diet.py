import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
import webbrowser


# TODO añadir la funcionalidad de modificar dietas. Con el mismo editor de Nueva Dieta
class DietFrame(tk.Frame):
    def __init__(self, notebook, bg):
        super().__init__(notebook, bg=bg)
        self.dataBaser = DataBaser()
        self.ShowingNewRecipe = False
        self.ShowingRecipes = False
        self.dayList = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        # Create diets button
        self.ButtonShowDiet = tk.Button(self, text='Ver Dietas', command=self.show_diets)
        self.ButtonShowDiet.grid(row=0, column=0, pady=10, padx=10, sticky=tk.N)
        # Create new diet button
        self.ButtonNewDiet = tk.Button(self, text='Nueva Dieta', command=self.show_new_recipe)
        self.ButtonNewDiet.grid(row=0, column=2, pady=10)
        # Create Days diet
        self.VarNewDietName = tk.StringVar()
        self.EntryNewDietName = tk.Entry(self, textvariable=self.VarNewDietName)
        self.EntryNewDietName.grid(row=0, column=3, pady=10)
        self.ButtonSaveDiet = tk.Button(self, text='Guardar', command=self.save_recipe)
        self.LabelSaveResult = tk.Label(self, text='', bg='#EEEEEE')
        self.LabelSaveResult.grid(row=0, column=5)
        # Current Diet
        self.Days = [self.Day(self, bg='#EEEEEE', day=day) for day in self.dayList]
        self.get_current_diet()
        # Create Diets Tree View
        self.FrameDietTree = tk.Frame(self, bg='#EEEEEE')
        self.TreeDiets = ttk.Treeview(self.FrameDietTree, height=15)
        self.TreeDiets["columns"] = ('#1',)
        self.TreeDiets.pack(fill=tk.X)

    def fill_tree(self, diets):
        self.TreeDiets.delete(*self.TreeDiets.get_children())
        for diet in diets:
            rec = self.TreeDiets.insert('',
                                          'end',
                                          text=diet['name'])
            foo = self.TreeDiets.insert(rec, 'end', text='Recetas')
            for recipe in diet['recipes']:
                f = self.TreeDiets.insert(foo,
                                            'end',
                                            text=recipe['name'])

    def show_diets(self):
        self.ShowingRecipes = not self.ShowingRecipes
        if self.ShowingRecipes:
            self.ButtonShowDiet['text'] = 'Ocultar Dietas'
            self.fill_tree(self.dataBaser.get_diets())
            self.FrameDietTree.grid(row=0, column=1, columnspan=2)
            self.ButtonSaveDiet.grid_forget()
            self.EntryNewDietName.grid_forget()
            for i, day in enumerate(self.Days):
                day.grid_forget()
        else:
            self.ButtonShowDiet['text'] = 'Ver Dietas'
            self.FrameDietTree.grid_forget()
            self.EntryNewDietName.grid(row=0, column=3, pady=10)
            self.get_current_diet()

    def show_new_recipe(self):
        self.ShowingNewRecipe = not self.ShowingNewRecipe
        if self.ShowingNewRecipe:
            self.ButtonSaveDiet.grid(row=0, column=4, pady=10)
            self.EntryNewDietName['state'] = 'normal'
            self.EntryNewDietName.delete(0, tk.END)
            self.ButtonNewDiet['text'] = 'Cancelar'
            for i, day in enumerate(self.Days):
                for food in day.Foods:
                    food.EntryRecipeName['state'] = 'normal'
                    food.EntryRecipeName.delete(0, tk.END)
                    food.EntryRecipeName.unbind("<1>")
        else:
            self.ButtonNewDiet['text'] = 'Nueva Dieta'
            self.ButtonSaveDiet.grid_forget()
            self.get_current_diet()

    def save_recipe(self):
        Data = []
        good = True
        for day in self.Days:
            data = []
            for food in day.Foods:
                if food.TreeSearch.winfo_viewable() and food.EntryRecipeName.get():
                    good = False
                data.append(food.EntryRecipeName.get())
            Data.append(data)
        if good:
            self.dataBaser.save_diet(Data, self.VarNewDietName.get())
            self.LabelSaveResult['text'] = '¡Dieta Guardada!'
            self.get_current_diet()
        else:
            self.LabelSaveResult['text'] = 'Error'

    def get_current_diet(self):
        diet = self.dataBaser.get_current_diet()
        self.EntryNewDietName.delete(0, tk.END)
        self.EntryNewDietName.insert(0, diet[-1])
        self.EntryNewDietName['state'] = 'readonly'
        for i, day in enumerate(self.Days):
            day.grid(row=1, column=i, rowspan=6)
            for j, food in enumerate(day.Foods):
                food.EntryRecipeName.delete(0, tk.END)
                recipe = self.dataBaser.get_recipe(diet[((i+1)*(j+1))-1])
                if recipe:
                    food.EntryRecipeName.insert(0, recipe[0])
                    food.EntryRecipeName.bind("<1>", lambda event, link=recipe[1]: self.recipe_click(link))
                else:
                    food.EntryRecipeName.insert(0, recipe)
                food.EntryRecipeName['state'] = 'readonly'
                food.FrameTreeView.grid_forget()

    @staticmethod
    def recipe_click(event):
        webbrowser.open(event, new=0)

    class Day(tk.Frame):
        def __init__(self, father, bg, day):
            super().__init__(father, bg=bg)
            self.foodList = ['C1', 'C2', 'C3', 'C4', 'C5']
            self.LabelDay = tk.Label(self, text=day, bg='#EEEEEE')
            self.LabelDay.grid(row=0, column=0)
            self.LabelFoods = []
            self.Foods = []
            i = 1
            for food in self.foodList:
                self.LabelFoods.append(tk.Label(self, text=food, bg='#EEEEEE'))
                self.LabelFoods[-1].grid(row=i, column=0)
                i += 1
                self.Foods.append(self.Food(self, bg='#EEEEEE'))
                self.Foods[-1].grid(row=i, column=0)
                i += 1

        class Food(tk.Frame):
            def __init__(self, father, bg):
                super().__init__(father, bg=bg)
                self.dataBaser = DataBaser()

                def callback(parent, sv):
                    if not parent.TreeSearch.winfo_viewable() and parent.EntryRecipeName.get():
                        parent.FrameTreeView.grid(row=2, column=1)
                    if not parent.EntryRecipeName.get():
                        parent.FrameTreeView.grid_forget()
                    if sv.get():
                        parent.fill_tree(self.dataBaser.search_recipe(sv.get()))
                    else:
                        parent.TreeSearch.delete(*parent.TreeSearch.get_children())

                self.VarRecipeSearch = tk.StringVar()
                self.VarRecipeSearch.trace('w', lambda name, index, mode, sv=self.VarRecipeSearch: callback(self, sv))
                self.EntryRecipeName = tk.Entry(self, textvariable=self.VarRecipeSearch)
                self.EntryRecipeName.grid(row=1, column=1)
                self.FrameTreeView = tk.Frame(self, bg='#EEEEEE')
                self.FrameTreeView.grid(row=2, column=1)
                self.TreeSearch = ttk.Treeview(self.FrameTreeView, height=3)
                self.TreeSearch.bind("<Double-1>", self.tree_double_click)
                self.TreeSearch.pack(fill=tk.X)

            def fill_tree(self, recipes):
                self.TreeSearch.delete(*self.TreeSearch.get_children())
                for recipe in recipes:
                    self.TreeSearch.insert('', 'end', text=recipe[0])

            def tree_double_click(self, event):
                foodName = self.TreeSearch.item(self.TreeSearch.selection()[0], 'text')
                self.EntryRecipeName.delete(0, tk.END)
                self.EntryRecipeName.insert(0, foodName)
                self.FrameTreeView.grid_forget()
