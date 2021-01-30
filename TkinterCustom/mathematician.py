import tkinter as tk


class Calculator(tk.Frame):
    def __init__(self, father, bg):
        super().__init__(father, bg=bg)
        self.Alu = 0
        self.AluCached = False
        # Create Result Label
        self.LabelResult = tk.Label(self, text="", bg='#FFFFFF', width=15)
        self.LabelResult.grid(row=0, column=0, columnspan=3, pady=10)
        # Create One Button
        self.Button7 = tk.Button(self, text='7', command=lambda: self.num('7'), height=2, width=5)
        self.Button7.grid(row=1, column=0, sticky=tk.W)
        self.Button8 = tk.Button(self, text='8', command=lambda: self.num('8'), height=2, width=5)
        self.Button8.grid(row=1, column=1, sticky=tk.W)
        self.Button9 = tk.Button(self, text='9', command=lambda: self.num('9'), height=2, width=5)
        self.Button9.grid(row=1, column=2, sticky=tk.W)
        self.Button4 = tk.Button(self, text='4', command=lambda: self.num('4'), height=2, width=5)
        self.Button4.grid(row=2, column=0, sticky=tk.W)
        self.Button5 = tk.Button(self, text='5', command=lambda: self.num('5'), height=2, width=5)
        self.Button5.grid(row=2, column=1, sticky=tk.W)
        self.Button6 = tk.Button(self, text='6', command=lambda: self.num('6'), height=2, width=5)
        self.Button6.grid(row=2, column=2, sticky=tk.W)
        self.Button1 = tk.Button(self, text='1', command=lambda: self.num('1'), height=2, width=5)
        self.Button1.grid(row=3, column=0, sticky=tk.W)
        self.Button2 = tk.Button(self, text='2', command=lambda: self.num('2'), height=2, width=5)
        self.Button2.grid(row=3, column=1, sticky=tk.W)
        self.Button3 = tk.Button(self, text='3', command=lambda: self.num('3'), height=2, width=5)
        self.Button3.grid(row=3, column=2, sticky=tk.W)
        self.Button0 = tk.Button(self, text='0', command=lambda: self.num('0'), height=2, width=5)
        self.Button0.grid(row=4, column=1, columnspan=3, sticky=tk.W)
        self.ButtonAdd = tk.Button(self, text='+', command=lambda: self.add(), height=2, width=5)
        self.ButtonAdd.grid(row=1, column=3, sticky=tk.W)
        self.ButtonSubs = tk.Button(self, text='-', command=lambda: self.subs(), height=2, width=5)
        self.ButtonSubs.grid(row=2, column=3, sticky=tk.W)
        self.ButtonMult = tk.Button(self, text='x', command=lambda: self.mult(), height=2, width=5)
        self.ButtonMult.grid(row=3, column=3, sticky=tk.W)
        self.ButtonDiv = tk.Button(self, text='/', command=lambda: self.div(), height=2, width=5)
        self.ButtonDiv.grid(row=4, column=3, sticky=tk.W)
        self.ButtonEquals = tk.Button(self, text='=', command=lambda: self.equals(), height=2, width=5)
        self.ButtonEquals.grid(row=4, column=2, sticky=tk.W)
        self.ButtonC = tk.Button(self, text='C', command=lambda: self.num(), height=2, width=5)
        self.ButtonC.grid(row=4, column=0, sticky=tk.W)
        self.LabelResult['text'] = ''

    def num(self, number):
        self.LabelResult['text'] += number

    def add(self):
        if not self.AluCached:
            self.Alu = float(self.LabelResult['text'])
            self.LabelResult['text'] = ''
            self.AluCached = True
        else:
            aux = float(self.LabelResult['text'])
            self.Alu = float(self.LabelResult['text']) + self.Alu
            self.LabelResult['text'] = str(self.Alu)
            self.AluCached = False

    def subs(self):
        if not self.AluCached:
            self.Alu = float(self.LabelResult['text'])
            self.AluCached = True
        else:
            self.LabelResult['text'] = str(self.Alu - float(self.LabelResult['text']))
            self.Alu = 0
            self.AluCached = False

    def mult(self):
        if not self.AluCached:
            self.Alu = float(self.LabelResult['text'])
            self.AluCached = True
        else:
            self.LabelResult['text'] = str(float(self.LabelResult['text']) * self.Alu)
            self.Alu = 0
            self.AluCached = False

    def div(self):
        if not self.AluCached:
            self.Alu = float(self.LabelResult['text'])
            self.AluCached = True
        else:
            self.LabelResult['text'] = str(self.Alu / float(self.LabelResult['text']))
            self.Alu = 0
            self.AluCached = False

    def erase(self):
        self.Alu = 0
        self.AluCached = False
        self.LabelResult['text'] = ''
