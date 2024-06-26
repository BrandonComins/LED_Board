import tkinter as tk
import pyautogui as gui
import serial
import os
import time
from threading import Thread
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
            bg = color_code,
            command=self.doAction,
            height= 10,
            width= 10
        )

        self.button.grid(sticky="nswe", row=j, column=i)
        window.columnconfigure(self.colunm, weight=1)
        window.rowconfigure(self.row, weight=1)

    def doAction(self):
        global button_mode
        if button_mode == True:
            self.setColor()
        else:
            global color_code
            color_code = self.getColor()
            button_mode = True
            window.config(cursor="arrow")

    def setColor(self) -> None:
        global color_code
        if self.button.cget('background') != color_code:
            self.button.configure(bg = color_code)

            if serialObj != None:
                serialObj.write(('%s, %s' % (
                    (str(self.row) + str(self.colunm)),
                    str(Hex_RGB(color_code)))).replace(')', '').replace('(','').replace(',', '').encode())

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
    global animate
    animate = False

    for i in range(row):
        for j in range(column):
            colorButtonList[i][j].resetColor()

def saveImage() -> None:
    def saveText(event=None) -> None:
        if(event == None): # For save box
            text : str = os.curdir + "/Python/Saves/" + inputText.get("1.0","end-1c") + '.txt'
        else: # For Enter Key
            text : str = os.curdir + "/Python/Saves/" + inputText.get("1.0","end-2c") + '.txt'

        questionBox.destroy()

        file = open(text, 'w')
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

    file_name =  filedialog.askopenfilename(
        initialdir = os.curdir + "/Python/Saves/",
        filetypes = [("Text files", "*.txt")]
    )

    loadImage2(file_name)


def loadImage2(file_name : str) -> None:
    global color_code

    try:
        file = open(file_name, "r")

        for i, line in enumerate(file):
            temp = line.split(", ")[:-1]
            for j, color in enumerate(temp):
                color_code = color
                colorButtonList[i][j].setColor()
    except FileNotFoundError:
        print(file_name + " not found")


def loadMany() -> None:
    global animate
    global color_code

    animate = True
    path_name = filedialog.askdirectory(initialdir=os.curdir + "/Python/Saves/")
    files = os.listdir(path_name)
    print(files)

    i : int = 0
    now : time = time.time()
    while(animate == True):
        if(i == len(files)):
            i = 0

        file_name = files[i]
        loadImage2(path_name+'/'+file_name)

        if(int(time.time() - now) >= 2):
            print(file_name)
            i+=1
            now = time.time()


def eyeDrop() -> None:
    global button_mode
    button_mode = False
    window.config(cursor="plus")

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

def makeLoadManyButton() -> None:
    load = tk.Button(
        window,
        text="Anim",
        command= lambda: Thread(target=loadMany).start()
    )

    window.rowconfigure(row + 1, weight=0)
    load.grid(sticky="nswe", row= row + 2, column=1)

def makeSaveButton() -> None:
    save = tk.Button(
        window,
        text="Save",
        command=saveImage
    )

    window.rowconfigure(row + 1, weight=0)
    save.grid(sticky="nswe", row= row + 2, column=column-1)

def makeColorPickerButton() -> None:
    picker = tk.Button(
        window,
        text="Picker",
        command=eyeDrop
    )

    window.rowconfigure(row + 1, weight=0)
    picker.grid(sticky="nswe", row= row + 2, column= round(column/2) - 1)


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

    button_mode : bool = True
    color_code : str = '#ffffff' # White
    animate : bool = False
    # row : int = int(input("Row Size: "))
    # column : int = int(input("Column Size: "))
    row    : int = 10
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
    makeLoadManyButton()
    makeColorPickerButton()

    window.mainloop()