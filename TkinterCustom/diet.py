import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
import webbrowser


# TODO calcular informaciones importantes referentes a la dieta
class DietFrame(tk.Frame):
    def __init__(self, notebook, bg):
        super().__init__(notebook, bg=bg)
        self.dataBaser = DataBaser()
        self.ShowingDiets = True
        self.dayList = self.dataBaser.get_all_item_names('day')
        # Frame Diet detail
        self.FrameDietDetail = tk.Frame(self, bg='#EEEEEE')
        self.ButtonShowDiet = tk.Button(self.FrameDietDetail, text='Ver Dietas', command=self.show_diets)
        self.ButtonShowDiet.grid(row=0, column=0, pady=10, padx=10, sticky=tk.N)
        # Create new diet button
        self.ButtonCancelDiet = tk.Button(self.FrameDietDetail, text='Cancelar', command=self.show_diets)
        # Create Days diet
        self.VarNewDietName = tk.StringVar()
        self.EntryNewDietName = tk.Entry(self.FrameDietDetail, textvariable=self.VarNewDietName)
        self.EntryNewDietName.grid(row=0, column=3, pady=10)
        self.ButtonSaveDiet = tk.Button(self.FrameDietDetail, text='Guardar', command=self.save_diet)
        self.LabelSaveResult = tk.Label(self.FrameDietDetail, text='', bg='#EEEEEE')
        # Current Diet
        self.Days = [self.Day(self.FrameDietDetail, bg='#EEEEEE',
                              day=day, dataBase=self.dataBaser) for day in self.dayList]
        # Frame Diets
        self.FrameDiets = tk.Frame(self, bg='#EEEEEE')
        # Create Diets Tree View
        self.FrameDietTree = tk.Frame(self.FrameDiets, bg='#EEEEEE')
        self.TreeDiets = ttk.Treeview(self.FrameDietTree, height=15)
        self.TreeDiets["columns"] = ('#1',)
        self.TreeDiets.bind("<Double-1>", self.diet_actions)
        self.fill_tree(self.dataBaser.get_diets())
        self.TreeDiets.pack(fill=tk.X)
        self.FrameDietTree.grid(row=0, column=0, columnspan=2)
        self.ButtonNewDiet = tk.Button(self.FrameDiets, text='Nueva dieta', command=self.show_new_diet)
        self.ButtonNewDiet.grid(row=1, column=0, sticky=tk.E, padx=10)
        self.ButtonCurrentDiet = tk.Button(self.FrameDiets, text='Dieta actual', command=self.show_current_diet)
        self.ButtonCurrentDiet.grid(row=1, column=1, sticky=tk.W, padx=10)
        # Action buttons
        self.FrameDietActions = tk.Frame(self.FrameDiets, bg='#EEEEEE')
        self.LabelDietName = tk.Label(self.FrameDietActions, text='', bg='#EEEEEE')
        self.LabelDietName.grid(row=0, column=1, padx=10)
        self.ButtonUpdateDiet = tk.Button(self.FrameDietActions, text='Actualizar', command=self.update_diet)
        self.ButtonUpdateDiet.grid(row=1, column=0, padx=10)
        self.ButtonMakeCurrentDiet = tk.Button(self.FrameDietActions, text='Hacer Actual', command=self.make_diet_current)
        self.ButtonMakeCurrentDiet.grid(row=1, column=1, padx=10)
        self.ButtonDietDetail = tk.Button(self.FrameDietActions, text='Detalle', command=self.show_diets)
        self.ButtonDietDetail.grid(row=1, column=2, padx=10)
        self.FrameDiets.grid(row=0, column=1)

    def fill_tree(self, diets):
        self.TreeDiets.delete(*self.TreeDiets.get_children())
        for diet in diets:
            di = self.TreeDiets.insert('',
                                       'end',
                                       text=diet['name'],
                                       values=(('Actual',)[0] if diet['current'] == 1 else ''))
            inf = self.TreeDiets.insert(di, 'end', text='Informaciones')
            for day in diet['days']:
                da = self.TreeDiets.insert(di, 'end', text=day['name'])
                for course in day['courses']:
                    self.TreeDiets.insert(da, 'end', text=course['name'],
                                          values=(course['recipes'][0]['name'] if course['recipes'] else '',))

    def show_diets(self):
        self.ShowingDiets = not self.ShowingDiets
        if self.ShowingDiets:
            self.FrameDietDetail.grid_forget()
            self.ButtonCancelDiet.grid(row=0, column=4, pady=10)
            self.ButtonSaveDiet.grid(row=0, column=2, pady=10)
            self.FrameDiets.grid(row=0, column=0)
        else:
            self.FrameDiets.grid_forget()
            if self.LabelDietName['text']:
                self.get_current_diet(current=False, dietName=self.LabelDietName['text'])
            else:
                self.get_current_diet()
            self.FrameDietDetail.grid(row=0, column=0)

    def diet_actions(self, event):
        self.LabelDietName['text'] = self.TreeDiets.item(self.TreeDiets.selection()[0], 'text')
        self.FrameDietActions.grid(row=0, column=2, sticky=tk.NSEW)
        return event

    def make_diet_current(self):
        self.dataBaser.set_current_diet(self.LabelDietName['text'])
        self.fill_tree(self.dataBaser.get_diets())

    def show_new_diet(self):
        self.show_diets()
        self.ButtonCancelDiet.grid(row=0, column=4, pady=10)
        self.ButtonSaveDiet.grid(row=0, column=2, pady=10)
        self.EntryNewDietName['state'] = 'normal'
        self.EntryNewDietName.delete(0, tk.END)
        for i, day in enumerate(self.Days):
            for food in day.Foods:
                food.EntryRecipeName['state'] = 'normal'
                food.EntryRecipeName.delete(0, tk.END)
                food.EntryRecipeName.unbind("<1>")

    def show_current_diet(self):
        self.show_diets()
        self.get_current_diet()

    def update_diet(self):
        self.show_diets()
        self.ButtonCancelDiet.grid(row=0, column=4, pady=10)
        self.ButtonSaveDiet.grid(row=0, column=2, pady=10)
        self.EntryNewDietName['state'] = 'normal'
        for i, day in enumerate(self.Days):
            for j, food in enumerate(day.Foods):
                food.EntryRecipeName['state'] = 'normal'
                food.FrameTreeView.grid_forget()

    def save_diet(self):
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
        self.show_diets()

    def get_current_diet(self, current=True, dietName=''):
        diet = self.dataBaser.get_current_diet(current=current, dietName=dietName)
        self.EntryNewDietName.delete(0, tk.END)
        self.EntryNewDietName.insert(0, diet[-1])
        self.EntryNewDietName['state'] = 'readonly'
        for i, day in enumerate(self.Days):
            day.grid(row=1, column=i, rowspan=6)
            for j, food in enumerate(day.Foods):
                food.EntryRecipeName.delete(0, tk.END)
                recipe = self.dataBaser.get_recipe(diet[((i*5) + j)])
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
        def __init__(self, father, bg, day, dataBase):
            super().__init__(father, bg=bg)
            self.foodList = dataBase.get_all_item_names('course')
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
                        parent.fill_tree(self.dataBaser.search_item(sv.get(), 'recipe'))
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
                return event
