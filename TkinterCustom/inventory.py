import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
from TkinterCustom.nutritionix import EchoMaker


class InventoryFrame(tk.Frame):
    def __init__(self, father, bg):
        super().__init__(father, bg=bg)
        self.dataBaser = DataBaser()
        self.echoMaker = EchoMaker()
        self.NumColumns = 4
        # Create New Food Label
        self.LabelNewItem = tk.Label(self, text="Nuevo Ítem", bg='#EEEEEE')
        self.LabelNewItem.grid(row=0, column=0, pady=10)
        # Create Food Name Entry
        self.EntryItemName = tk.Entry(self)
        self.EntryItemName.grid(row=0, column=1, pady=10)
        # Create Food Name Entry
        self.EntryItemAmount = tk.Entry(self)
        self.EntryItemAmount.grid(row=0, column=2, pady=10)
        # Create Save Food Button
        self.ButtonSaveItem = tk.Button(self, text='Guardar', command=self.save_new_item)
        self.ButtonSaveItem.grid(row=0, column=3, pady=10)
        # Create Search Result Tree View
        self.FrameTreeView = tk.Frame(self, bg='#EEEEEE')
        self.TreeItem = ttk.Treeview(self.FrameTreeView)
        self.TreeItem["columns"] = ('#1',)
        self.fill_tree(self.dataBaser.get_inventory())
        self.TreeItem.bind("<Double-1>", self.tree_double_click)
        self.TreeItem.pack(side=tk.LEFT, expand=True, fill='x')
        self.FrameTreeView.grid(row=1, column=0, columnspan=self.NumColumns)
        # Add Food Info Label
        self.FrameUpdateItem = tk.Frame(self, bg='#EEEEEE')
        self.LabelUpdateItem = tk.Label(self.FrameUpdateItem, text="Actualizar", bg='#EEEEEE')
        self.LabelUpdateItem.grid(row=0, column=0, sticky=tk.W)
        # Update Food Name
        self.LabelItemDetail = tk.Label(self.FrameUpdateItem, text='', bg='#EEEEEE')
        self.LabelItemDetail.grid(row=0, column=1, sticky=tk.W)
        # Create Price Entry
        self.LabelUpdateItem = tk.Label(self.FrameUpdateItem, text="Cantidad", bg='#EEEEEE')
        self.LabelUpdateItem.grid(row=1, column=0, sticky=tk.W)
        self.EntryQuantity = tk.Entry(self.FrameUpdateItem)
        self.EntryQuantity.insert(0, 'Cantidad')
        self.EntryQuantity.grid(row=1, column=1, sticky=tk.W)
        # Create Save Food Button
        self.ButtonSaveItem = tk.Button(self.FrameUpdateItem, text='Actualizar', command=self.update_item)
        self.ButtonSaveItem.grid(row=2, column=1, sticky=tk.W, pady=10)
        # Create Cancel Food Button
        self.ButtonCancelItem = tk.Button(self, text='Cancelar', command=self.hide_update_item)
        self.ButtonCancelItem.grid(row=3, column=1, sticky=tk.E, pady=10)

    def fill_tree(self, items):
        self.TreeItem.delete(*self.TreeItem.get_children())
        for item in items:
            self.TreeItem.insert('', 'end', text=item['name'], values=(item['amount']))

    def save_new_item(self):
        self.echoMaker.natural_nutrients(self.EntryItemName.get())
        self.dataBaser.save_item(self.EntryItemName.get(), self.EntryItemAmount.get())
        self.fill_tree(self.dataBaser.get_inventory())

    def tree_double_click(self, event):
        itemName = self.TreeItem.item(self.TreeItem.selection()[0], 'text')
        if self.dataBaser.get_item_id_by_name(itemName, 'food'):
            self.FrameUpdateItem.grid(row=1, column=5, sticky=tk.N)
            self.LabelItemDetail.configure(text=itemName)

    def update_item(self):
        self.dataBaser.update_item(self.LabelItemDetail.cget('text'), self.EntryQuantity.get())
        self.hide_update_item()
        self.fill_tree(self.dataBaser.get_inventory())

    def hide_update_item(self):
        self.FrameUpdateItem.grid_forget()
