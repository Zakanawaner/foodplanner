import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
from TkinterCustom.nutritionix import EchoMaker


# TODO haremos la conversión al paquete que toque dentro de cada mercado
class GroceryFrame(tk.Frame):
    def __init__(self, father, bg):
        super().__init__(father, bg=bg)
        self.dataBaser = DataBaser()
        self.echoMaker = EchoMaker()
        self.NumColumns = 3
        # Create New Food Label
        self.LabelNewFood = tk.Label(self, text="Próxima Compra", bg='#EEEEEE')
        self.LabelNewFood.grid(row=0, column=1, pady=10)
        # Create Search Result Tree View
        self.FrameTreeView = tk.Frame(self, bg='#EEEEEE')
        self.TreeFood = ttk.Treeview(self.FrameTreeView)
        self.TreeFood["columns"] = ('#1', '#2', '#3')
        self.fill_tree()
        self.TreeFood.pack(side=tk.LEFT, expand=True, fill='x')
        self.FrameTreeView.grid(row=1, column=0, columnspan=self.NumColumns)
        # Create calculate button
        self.ButtonNewDiet = tk.Button(self, text='Recalcular', command=self.fill_tree)
        self.ButtonNewDiet.grid(row=2, column=1, pady=10)

    def fill_tree(self):
        groceries = self.calculate_grocery()
        self.TreeFood.delete(*self.TreeFood.get_children())
        total = 0
        for grocery in groceries:
            self.TreeFood.insert('', 'end', text=grocery['name'], values=(grocery['amount'],
                                                                          grocery['market'],
                                                                          str(grocery['price']) +
                                                                          ' €' if grocery['price'] > 0 else ''))
            total += grocery['price']
        self.LabelNewFood['text'] = "Próxima Compra (" + str(total) + ' €)'

    def calculate_grocery(self):
        inventory = self.dataBaser.get_inventory()
        recipes = self.dataBaser.get_recipes(self.dataBaser.get_current_diet()[0:-1])
        necessities = []
        for recipe in recipes:
            for ingredient in recipe['ingredients']:
                exists = False
                index = -1
                for i, product in enumerate(necessities):
                    if product['name'] == ingredient['name']:
                        exists = True
                        index = i
                        break
                if exists:
                    necessities[index]['amount'] += ingredient['quantity']
                else:
                    necessity = {'name': ingredient['name'], 'amount': ingredient['quantity']}
                    necessities.append(necessity)
        groceries = []
        for necessity in necessities:
            exists = False
            index = -1
            for i, item in enumerate(inventory):
                if item['name'] == necessity['name']:
                    exists = True
                    index = i
                    break
            if exists:
                if inventory[index]['amount'] < necessity['amount']:
                    groceries.append({'name': necessity['name'],
                                      'amount': necessity['amount'] - inventory[index]['amount']})
            else:
                groceries.append({'name': necessity['name'],
                                  'amount': necessity['amount']})
        for grocery in groceries:
            options = self.dataBaser.get_food_markets(grocery['name'])
            if options:
                i = [o[2] for o in options].index(min([o[2] for o in options]))
                grocery['market'] = self.dataBaser.get_store_by_id(options[i][0])
                grocery['price'] = options[i][2]
            else:
                grocery['market'] = "No hay información de mercado"
                grocery['price'] = 0
        return groceries
