import tkinter as tk
from tkinter import ttk
from BD.dataBaser import DataBaser
from TkinterCustom.nutritionix import EchoMaker


# TODO Hacer el cálculo de lo que tenemos y lo que necesitamos. Para eso, hay que definir una unidad básica,
#  que será el gramo. Un litro son 1000g, y punto. Con eso, calcularemos en una primera instancia los gramos a comprar,
#  y luego haremos la conversión al paquete que toque dentro de cada mercado
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
        self.TreeFood["columns"] = ('#1', '#2')
        self.fill_tree(self.dataBaser.get_last_grocery())
        self.TreeFood.pack(side=tk.LEFT, expand=True, fill='x')
        self.FrameTreeView.grid(row=1, column=0, columnspan=self.NumColumns)

    def fill_tree(self, foods):
        foods = []
        self.TreeFood.delete(*self.TreeFood.get_children())
        for food in foods:
            foo = self.TreeFood.insert('', 'end', text=food['name'], values='100g')
            mac = self.TreeFood.insert(foo, 'end', text='Macros')
            for macro in food['macros']:
                m = self.TreeFood.insert(mac, 'end', text=macro['name'])
                self.TreeFood.insert(m, 'end', text=macro['amount'], values=(macro['unit']))
            mic = self.TreeFood.insert(foo, 'end', text='Micros')
            for micro in food['micros']:
                i = self.TreeFood.insert(mic, 'end', text=micro['name'])
                self.TreeFood.insert(i, 'end', text=micro['amount'], values=(micro['unit']))

    def calculate_grocery(self):
        pass

