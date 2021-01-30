import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser


class RecipeFrame(tk.Frame):
    def __init__(self, notebook, bg):
        super().__init__(notebook, bg=bg)
        self.dataBaser = DataBaser()
        self.NumColumns = 8
        self.ShowingRecipes = False
        self.OnNEwRecipe = False
        self.OnUpdateRecipe = False
        self.Ingredients = []
        # Recipes tree label
        self.LabelRecipes = tk.Label(self, text="Recetas guardadas", bg='#EEEEEE')
        self.LabelRecipes.grid(row=0, column=0, padx=5)
        # Create Recipes Tree View
        self.FrameRecipeTree = tk.Frame(self, bg='#EEEEEE')
        self.TreeRecipes = ttk.Treeview(self.FrameRecipeTree, height=15)
        self.TreeRecipes["columns"] = ('#1',)
        self.TreeRecipes.bind("<Double-1>", self.update_recipe)
        self.fill_tree(self.dataBaser.get_recipes())
        self.TreeRecipes.pack(fill=tk.X)
        self.FrameRecipeTree.grid(row=1, column=0, pady=10)
        # Create New Recipe Button
        self.ButtonNewRecipe = tk.Button(self, text="Nueva receta", command=self.new_recipe)
        self.ButtonNewRecipe.grid(row=0, column=1, pady=10, padx=20, sticky=tk.W)
        # Create Recipe Name Entry
        self.FrameNewRecipe = tk.Frame(self, bg='#EEEEEE')
        self.EntryRecipeName = tk.Entry(self.FrameNewRecipe)
        self.EntryRecipeName.insert(0, 'Nombre')
        self.EntryRecipeName.grid(row=0, column=0, pady=10)
        # Create Recipe Link Entry
        self.EntryRecipeLink = tk.Entry(self.FrameNewRecipe)
        self.EntryRecipeLink.insert(0, 'Link')
        self.EntryRecipeLink.grid(row=0, column=1, pady=10)
        # Add Recipe Servings
        self.ServingList = ['1', '2', '3', '4']
        self.SelectedServing = tk.StringVar(self.FrameNewRecipe)
        self.SelectedServing.set(self.ServingList[0])
        self.DropdownServing = tk.OptionMenu(self.FrameNewRecipe, self.SelectedServing, *self.ServingList)
        self.DropdownServing.grid(row=0, column=2, pady=10)
        # Create Add food Button
        self.ButtonAddFood = tk.Button(self.FrameNewRecipe, text='+', command=self.add_ingredient)
        self.ButtonAddFood.grid(row=0, column=3, pady=10)
        # Create Save recipe button
        self.ButtonSaveFood = tk.Button(self.FrameNewRecipe, text='Guardar receta', command=self.save_recipe)
        self.ButtonSaveFood.grid(row=len(self.Ingredients)+1, column=0, pady=10)

    def new_recipe(self):
        if self.OnUpdateRecipe:
            self.OnUpdateRecipe = False
            self.ButtonNewRecipe['text'] = 'Nueva Receta'
            self.ButtonSaveFood['text'] = 'Guardar'
            for ingredient in self.Ingredients:
                ingredient.grid_forget()
            self.Ingredients = []
            self.EntryRecipeName.delete(0, tk.END)
            self.EntryRecipeLink.delete(0, tk.END)
            self.FrameNewRecipe.grid_forget()
        else:
            self.OnNEwRecipe = not self.OnNEwRecipe
        if self.OnNEwRecipe:
            self.ButtonNewRecipe['text'] = 'Cancelar'
            self.FrameNewRecipe.grid(row=1, column=1, padx=20, sticky=tk.N)
        else:
            self.ButtonNewRecipe['text'] = 'Nueva Receta'
            for ingredient in self.Ingredients:
                ingredient.grid_forget()
            self.FrameNewRecipe.grid_forget()

    def update_recipe(self, event):
        recipeId = self.dataBaser.get_recipe(self.TreeRecipes.item(self.TreeRecipes.selection()[0], 'text'), byId=False)
        recipe = self.dataBaser.get_recipes([recipeId[0]])[0]
        self.OnUpdateRecipe = True
        self.ButtonNewRecipe['text'] = 'Cancelar'
        self.EntryRecipeName.delete(0, tk.END)
        self.EntryRecipeName.insert(0, recipe['name'])
        self.EntryRecipeLink.delete(0, tk.END)
        self.EntryRecipeLink.insert(0, recipe['link'])
        self.SelectedServing.set(self.ServingList[int(recipe['servings'])-1])
        self.ButtonSaveFood['text'] = 'Actualizar'
        for ingredient in self.Ingredients:
            ingredient.destroy()
        self.Ingredients = []
        for i, ingredient in enumerate(recipe['ingredients']):
            self.add_ingredient()
            self.Ingredients[i].EntryFoodSearch.delete(0, tk.END)
            self.Ingredients[i].EntryFoodSearch.insert(0, ingredient['name'])
            self.Ingredients[i].EntryIngredientQuantity.delete(0, tk.END)
            self.Ingredients[i].EntryIngredientQuantity.insert(0, ingredient['quantity'])
            self.Ingredients[i].FrameTreeView.grid_forget()
        self.FrameNewRecipe.grid(row=1, column=1, padx=20, sticky=tk.N)
        return event

    def fill_tree(self, recipes):
        self.TreeRecipes.delete(*self.TreeRecipes.get_children())
        for recipe in recipes:
            rec = self.TreeRecipes.insert('', 'end', text=recipe['name'], values=(str(recipe['servings'])+' personas'))
            foo = self.TreeRecipes.insert(rec, 'end', text='Ingredientes')
            for ingredient in recipe['ingredients']:
                self.TreeRecipes.insert(foo, 'end', text=ingredient['name'], values=(ingredient['quantity']))
            mac = self.TreeRecipes.insert(rec, 'end', text='Macros')
            for macro in recipe['macros']:
                m = self.TreeRecipes.insert(mac, 'end', text=macro['name'])
                self.TreeRecipes.insert(m, 'end', text=macro['amount'], values=(macro['unit']))
            mic = self.TreeRecipes.insert(rec, 'end', text='Micros')
            for micro in recipe['micros']:
                i = self.TreeRecipes.insert(mic, 'end', text=micro['name'])
                self.TreeRecipes.insert(i, 'end', text=micro['amount'], values=(micro['unit']))

    def add_ingredient(self):
        newIngredient = self.Ingredient(self.FrameNewRecipe, bg='#EEEEEE')
        self.Ingredients.append(newIngredient)
        newIngredient.grid(row=len(self.Ingredients), column=0, columnspan=2, pady=5, sticky=tk.W)
        self.ButtonSaveFood.grid(row=len(self.Ingredients)+1, column=1, pady=10)

    def save_recipe(self):
        finalIngredients = [(ingredient.VarIngredientSearch.get(),
                             ingredient.EntryIngredientQuantity.get()) for ingredient in self.Ingredients if ingredient.winfo_exists()]
        saved = self.dataBaser.save_recipe(self.EntryRecipeName.get(),
                                           self.EntryRecipeLink.get(),
                                           self.SelectedServing.get(),
                                           finalIngredients)
        if saved:
            if self.OnUpdateRecipe:
                self.OnUpdateRecipe = False
                self.ButtonNewRecipe['text'] = 'Nueva Receta'
            for ingredient in self.Ingredients:
                ingredient.destroy()
            self.EntryRecipeName.delete(0, tk.END)
            self.EntryRecipeName.insert(0, 'Nombre')
            self.EntryRecipeLink.delete(0, tk.END)
            self.EntryRecipeLink.insert(0, 'Link')
            self.SelectedServing.set(self.ServingList[0])
            self.FrameNewRecipe.grid_forget()

    class Ingredient(tk.Frame):
        def __init__(self, father, bg):
            super().__init__(father, bg=bg)
            self.dataBaser = DataBaser()

            def callback(parent, sv):
                if not parent.TreeSearch.winfo_viewable() and parent.EntryFoodSearch.get():
                    parent.FrameTreeView.grid(row=1, column=1)
                if not parent.EntryFoodSearch.get():
                    parent.FrameTreeView.grid_forget()
                if sv.get():
                    parent.fill_tree(self.dataBaser.search_item(sv.get(), 'food'))
                else:
                    parent.TreeSearch.delete(*parent.TreeSearch.get_children())

            # Ingredient Label
            self.LabelNewIngredient = tk.Label(self, text="Ingrediente", bg='#EEEEEE')
            self.LabelNewIngredient.grid(row=0, column=0, sticky=tk.W)
            # Ingredient search
            self.VarIngredientSearch = tk.StringVar()
            self.VarIngredientSearch.trace('w', lambda name, index, mode, sv=self.VarIngredientSearch: callback(self, sv))
            self.EntryFoodSearch = tk.Entry(self, textvariable=self.VarIngredientSearch)
            self.EntryFoodSearch.grid(row=0, column=1, sticky=tk.W)
            # Create Ingredient Quantity Entry
            self.EntryIngredientQuantity = tk.Entry(self, width=8)
            self.EntryIngredientQuantity.insert(0, 'Cantidad (g)')
            self.EntryIngredientQuantity.grid(row=0, column=2, sticky=tk.W)
            # Create Delete Ingredient Button
            self.ButtonDeleteIngredient = tk.Button(self, text='x', command=self.delete_ingredient)
            self.ButtonDeleteIngredient.grid(row=0, column=3, sticky=tk.W)
            # Create Search Result Tree View
            self.FrameTreeView = tk.Frame(self, bg='#EEEEEE')
            self.TreeSearch = ttk.Treeview(self.FrameTreeView, height=3)
            self.TreeSearch.bind("<Double-1>", self.tree_double_click)
            self.TreeSearch.pack(fill=tk.X)

        def delete_ingredient(self):
            self.destroy()

        def fill_tree(self, foods):
            self.TreeSearch.delete(*self.TreeSearch.get_children())
            for food in foods:
                self.TreeSearch.insert('', 'end', text=food[0])

        def tree_double_click(self, event):
            foodName = self.TreeSearch.item(self.TreeSearch.selection()[0], 'text')
            self.EntryFoodSearch.delete(0, tk.END)
            self.EntryFoodSearch.insert(0, foodName)
            self.FrameTreeView.grid_forget()
            return event
