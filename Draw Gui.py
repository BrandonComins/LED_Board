import tkinter as tk
from tkinter import colorchooser

class LEDButton:
    def __init__(self, row : int, colunm : int) -> None:
        self.color = "#ffffff"
        self.row = row
        self.colunm = colunm

        self.button = tk.Button(
            window, 
            compound = tk.LEFT,
            bg = self.color,
            command=self.changeColor,
            height= 3,
            width= 1
        )

        self.button.grid(sticky="nswe", row=j, column=i)
        window.columnconfigure(self.colunm, weight=1)
        window.rowconfigure(self.row, weight=1)

    def changeColor(self) -> None:
        global color_code
        self.button.configure(bg = color_code[-1])



def chooseColor() -> tuple:
    global color_code
    color_code = colorchooser.askcolor(title ="Choose color")
    print(color_code)
    return color_code

def makeColorButton() -> None:
    color_chooser = tk.Button(
        window,
        text="RGB",
        command = chooseColor
        )
    
    window.rowconfigure(row + 1, weight=0)
    color_chooser.grid(sticky="nswe", row= row + 2, column=round(column/2))


if __name__== "__main__":
    color_code = ((255, 255, 255), '#ffffff') # White
    row : int = int(input("Row Size: "))
    column : int = int(input("Column Size: "))

    window = tk.Tk()
    window.geometry("300x300+960+540")
    window.attributes('-topmost', 1)
    

    for i in range(row):
        for j in range(column):
            LEDButton(i, j)

    makeColorButton()

    window.mainloop()