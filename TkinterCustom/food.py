import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
from TkinterCustom.nutritionix import EchoMaker


# TODO Pensar en cómo añadir la información de los mercados
class FoodFrame(tk.Frame):
    def __init__(self, father, bg):
        super().__init__(father, bg=bg)
        self.dataBaser = DataBaser()
        self.echoMaker = EchoMaker()
        self.NumColumns = 3
        # Create New Food Label
        self.LabelNewFood = tk.Label(self, text="Nuevo alimento", bg='#EEEEEE')
        self.LabelNewFood.grid(row=0, column=1, pady=10)
        # Create Food Name Entry
        self.EntryFoodName = tk.Entry(self)
        self.EntryFoodName.grid(row=0, column=2, pady=10)
        # Create Save Food Button
        self.ButtonSaveFood = tk.Button(self, text='Guardar', command=self.save_new_food)
        self.ButtonSaveFood.grid(row=0, column=3, pady=10)
        # Create Search Result Tree View
        self.FrameTreeView = tk.Frame(self, bg='#EEEEEE')
        self.TreeFood = ttk.Treeview(self.FrameTreeView)
        self.TreeFood["columns"] = ('#1',)
        self.fill_tree(self.dataBaser.get_foods())
        self.TreeFood.bind("<Double-1>", self.tree_double_click)
        self.TreeFood.pack(side=tk.LEFT, expand=True, fill='x')
        self.FrameTreeView.grid(row=1, column=1, columnspan=self.NumColumns)
        # Add Food Info Label
        self.FrameUpdateFood = tk.Frame(self, bg='#EEEEEE')
        self.LabelUpdateFood = tk.Label(self.FrameUpdateFood, text="Actualizar", bg='#EEEEEE')
        self.LabelUpdateFood.grid(row=0, column=0, sticky=tk.E)
        # Update Food Name
        self.LabelFoodDetail = tk.Label(self.FrameUpdateFood, text='', bg='#EEEEEE')
        self.LabelFoodDetail.grid(row=0, column=1, sticky=tk.W)
        self.LabelFoodMarket = tk.Label(self.FrameUpdateFood, text='Tienda', bg='#EEEEEE')
        self.LabelFoodMarket.grid(row=1, column=0, sticky=tk.E)
        self.LabelFoodPrice = tk.Label(self.FrameUpdateFood, text='Precio (€/Kg)', bg='#EEEEEE')
        self.LabelFoodPrice.grid(row=2, column=0, sticky=tk.E)
        self.LabelFoodQuality = tk.Label(self.FrameUpdateFood, text='Calidad', bg='#EEEEEE')
        self.LabelFoodQuality.grid(row=3, column=0, sticky=tk.E)
        self.LabelFoodAmount = tk.Label(self.FrameUpdateFood, text='Cantidad', bg='#EEEEEE')
        self.LabelFoodAmount.grid(row=4, column=0, sticky=tk.E)
        self.LabelFoodComment = tk.Label(self.FrameUpdateFood, text='Comentarios', bg='#EEEEEE')
        self.LabelFoodComment.grid(row=5, column=0, sticky=tk.E)
        # Add Info Market
        self.StoreList = self.dataBaser.get_store_names()
        self.SelectedStore = tk.StringVar(self.FrameUpdateFood)
        self.SelectedStore.set(self.StoreList[0])
        self.DropdownMarket = tk.OptionMenu(self.FrameUpdateFood,
                                            self.SelectedStore, *self.StoreList,
                                            command=self.change_market_selection)
        self.DropdownMarket.grid(row=1, column=1, sticky=tk.W)
        # Create Price Entry
        self.EntryPrice = tk.Entry(self.FrameUpdateFood)
        self.EntryPrice.grid(row=2, column=1, sticky=tk.W)
        # Add Food Quality
        self.QualityList = ['Lo vomité', 'Malo', 'Meh', 'Bueno', 'Excelente']
        self.SelectedQuality = tk.StringVar(self.FrameUpdateFood)
        self.SelectedQuality.set(self.QualityList[0])
        self.DropdownQuality = tk.OptionMenu(self.FrameUpdateFood, self.SelectedQuality, *self.QualityList)
        self.DropdownQuality.grid(row=3, column=1, sticky=tk.W)
        # Add Store package
        self.EntryAmount = tk.Entry(self.FrameUpdateFood)
        self.EntryAmount.grid(row=4, column=1, sticky=tk.W)
        # Add Store package
        self.EntryComment = tk.Entry(self.FrameUpdateFood)
        self.EntryComment.grid(row=5, column=1, sticky=tk.W)
        # Create Save Food Button
        self.ButtonSaveFood = tk.Button(self.FrameUpdateFood, text='Actualizar', command=self.update_food)
        self.ButtonSaveFood.grid(row=6, column=1, sticky=tk.W)
        # Create Cancel Food Button
        self.ButtonCancelFood = tk.Button(self.FrameUpdateFood, text='Cancelar', command=self.hide_update_food)
        self.ButtonCancelFood.grid(row=6, column=1, sticky=tk.E)

    def fill_tree(self, foods):
        self.TreeFood.delete(*self.TreeFood.get_children())
        for food in foods:
            foo = self.TreeFood.insert('',
                                       'end',
                                       text=food['name'], values='100g')
            mac = self.TreeFood.insert(foo, 'end', text='Macros')
            for macro in food['macros']:
                m = self.TreeFood.insert(mac,
                                         'end',
                                         text=macro['name'])
                self.TreeFood.insert(m, 'end',
                                     text=macro['amount'],
                                     values=(macro['unit']))
            mic = self.TreeFood.insert(foo, 'end', text='Micros')
            for micro in food['micros']:
                i = self.TreeFood.insert(mic,
                                         'end',
                                         text=micro['name'])
                self.TreeFood.insert(i, 'end',
                                     text=micro['amount'],
                                     values=(micro['unit']))

    def save_new_food(self):
        self.echoMaker.natural_nutrients(self.EntryFoodName.get())
        self.fill_tree(self.dataBaser.get_foods())

    def tree_double_click(self, event):
        foodName = self.TreeFood.item(self.TreeFood.selection()[0], 'text')
        if self.dataBaser.get_food(foodName):
            self.FrameUpdateFood.grid(row=1, column=6, padx=10)
            self.LabelFoodDetail.configure(text=foodName)
            self.change_market_selection(self.SelectedStore.get())
        return event

    def update_food(self):
        self.dataBaser.update_food_price(self.LabelFoodDetail.cget('text'),
                                         self.SelectedStore.get(),
                                         float(self.EntryPrice.get()),
                                         self.SelectedQuality.get(),
                                         self.QualityList,
                                         self.EntryAmount.get(),
                                         self.EntryComment.get())
        self.hide_update_food()

    def hide_update_food(self):
        self.SelectedStore.set(self.StoreList[0])
        self.EntryPrice.delete(0, tk.END)
        self.SelectedQuality.set(self.QualityList[0])
        self.EntryAmount.delete(0, tk.END)
        self.EntryComment.delete(0, tk.END)
        self.FrameUpdateFood.grid_forget()

    def change_market_selection(self, event):
        data = self.dataBaser.get_food_markets(self.LabelFoodDetail['text'], event)
        self.EntryPrice.delete(0, tk.END)
        self.SelectedQuality.set(self.QualityList[0])
        self.EntryAmount.delete(0, tk.END)
        self.EntryComment.delete(0, tk.END)
        if data:
            self.EntryPrice.insert(0, data[0][2])
            self.SelectedQuality.set(self.QualityList[int(data[0][3])])
            self.EntryAmount.insert(0, data[0][4])
            self.EntryComment.insert(0, data[0][5])
        return event
