import tkinter as tk
import pyautogui as gui
import serial
from tkinter import colorchooser
from tkinter import filedialog


class LEDButton:
    def __init__(self, row : int, colunm : int) -> None:
        self.color : str = "#ffffff"
        self.row : int = row
        self.colunm : int = colunm

        self.button = tk.Button(
            window, 
            compound = tk.LEFT,
            bg = self.color,
            command=self.setColor,
            height= 5,
            width= 5
        )

        self.button.grid(sticky="nswe", row=j, column=i)
        window.columnconfigure(self.colunm, weight=1)
        window.rowconfigure(self.row, weight=1)

    def setColor(self) -> None:
        global color_code
        self.button.configure(bg = color_code)
        
        if serialObj != None:
            serialObj.write(b'%d, %d, %s' % (self.row, self.colunm, Hex_RGB(color_code)))
        
    
    def resetColor(self) -> None:
        self.button.configure(bg = '#ffffff')
        
        if serialObj != None:
            serialObj.write(b'%d, %d, #ffffff' % (self.row, self.colunm))

    def getColor(self) -> str:
        return self.button.cget('bg')


def chooseColor() -> tuple:
    global color_code
    color_code = colorchooser.askcolor(title ="Choose color")[-1]
    return color_code

def clearCanvas() -> None:
    for i in range(row):
        for j in range(column):
            colorButtonList[i][j].resetColor()

def saveImage() -> None:
    def saveText(event=None) -> None:
        if(event == None): # For save box
            text : str = 'Saves/' + inputText.get("1.0","end-1c") + '.txt'
        else: # For Enter Key
            text : str = 'Saves/' + inputText.get("1.0","end-2c") + '.txt'
        
        questionBox.destroy()
        
        file = open(text, "w")
        for i in range(row):
            for j in range(column):
                file.write(colorButtonList[i][j].getColor())
                if(not (i == row - 1 and j == column - 1)):
                    file.write(', ')
            file.write('\n')
    
    questionBox = tk.Toplevel(window)
    questionBox.title("Save Image")
    questionBox.geometry(str(("500x50+%d+%d" % (int(screenWidth/2.5), int(screenHeight/3)))))
    questionBox.attributes('-topmost',True)
    questionBox.bind('<Return>', saveText)

    inputText = tk.Text(questionBox, height = 1,
                width = 25,
                bg = "light yellow")
    
    inputText.pack(side= 'left', pady = 10, padx = 10)

    tk.Label(questionBox, text=".txt").pack(side = 'left', pady = 10, padx = 10)
    
    saveButton = tk.Button(questionBox, height = 2,
                 width = 10,
                 text ="save",
                 command = saveText)
    saveButton.pack(pady=1)

def loadImage() -> None:
    global color_code

    file =  filedialog.askopenfilename(
        initialdir="/Saves" ,
        filetypes=[("Text files", "*.txt")]
    )
    
    try:
        file = open(file, "r")
        
        for i, line in enumerate(file):
            temp = line.split(", ")[:-1]
            for j, color in enumerate(temp):
                color_code = color
                colorButtonList[i][j].setColor()
    except FileNotFoundError:
        pass

def makeColorButton() -> None:
    color_chooser = tk.Button(
        window,
        text="RGB",
        command = chooseColor
    )

    window.rowconfigure(row + 1, weight=0)
    color_chooser.grid(sticky="nswe", row= row + 2, column=round(column/2))


def makeClearButton() -> None:
    clear = tk.Button(
        window,
        text="Clear",
        command=clearCanvas
    )
    
    window.rowconfigure(row + 1, weight=0)
    clear.grid(sticky="nswe", row= row + 2, column=column-3)

def makeLoadButton() -> None:
    load = tk.Button(
        window,
        text="Load",
        command=loadImage
    )
    
    window.rowconfigure(row + 1, weight=0)
    load.grid(sticky="nswe", row= row + 2, column=0)

def makeSaveButton() -> None:
    save = tk.Button(
        window,
        text="Save",
        command=saveImage
    )
    
    window.rowconfigure(row + 1, weight=0)
    save.grid(sticky="nswe", row= row + 2, column=column-1)

def serialBegin(comPort : str) -> serial.Serial:
    try:
        serialObj = serial.Serial(comPort)
        serialObj.baudrate = 9600
        serialObj.bytesize = 8
        serialObj.parity = 'N'
        serialObj.stopbits = '1'
    except serial.SerialException:
        print("Could not open", comPort)
        return None

    return serialObj

def Hex_RGB(hex : str) -> tuple:
    return tuple(int(hex.lstrip('#')[i:i+2],16) for i in (0, 2, 4))

if __name__== "__main__":
    # serialObj = serialBegin('COM' + input("Serial Number: "))
    serialObj = serialBegin("COM24")

    color_code = '#ffffff' # White
    # row : int = int(input("Row Size: ")) 
    # column : int = int(input("Column Size: "))
    row : int = 10 
    column : int = 10

    screenWidth, screenHeight = gui.size()
    window = tk.Tk()
    window.geometry(str(("500x500+%d+%d" % (int(screenWidth/2.5), int(screenHeight/3)))))
    window.attributes('-topmost', 1)
    window.title("Color Grid")
    
    colorButtonList = []
    for i in range(row):
        colorButtonList.append([])
        for j in range(column):
            Button = LEDButton(i, j)
            colorButtonList[i].append(Button)
    
    makeColorButton()
    makeClearButton()
    makeSaveButton()
    makeLoadButton()

    window.mainloop()