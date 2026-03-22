import tkinter as tk
import serial
import os
import time
from threading import Thread
from tkinter import colorchooser, filedialog

# Constants
off_color = '#000000'
row_count = 10
col_count = 10

class LEDButton:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.button = tk.Button(
            window,
            bg=off_color,
            command=self.doAction,
            height=2,
            width=4
        )
        self.button.grid(sticky="nswe", row=self.row, column=self.col)
        window.columnconfigure(self.col, weight=1)
        window.rowconfigure(self.row, weight=1)

    def doAction(self):
        global button_mode
        if button_mode:
            self.setColor()
        else:
            global color_code
            color_code = self.getColor()
            button_mode = True
            window.config(cursor="arrow")

    def setColor(self, target_color=None):
        global color_code, brightness, serialObj
        new_color = target_color if target_color else color_code
        
        self.button.configure(bg=new_color)

        if serialObj and serialObj.is_open:
            # --- RESTORED INDEX MATH (Serpentine) ---
            if self.row % 2 == 0:
                target_col = (col_count - 1) - self.col
            else:
                target_col = self.col
            led_index = (self.row * col_count) + target_col

            # --- CONVERT COLOR ---
            r, g, b = Hex_RGB(new_color)
            r_val = int(r * brightness)
            g_val = int(g * brightness)
            b_val = int(b * brightness)

            # --- SEND DATA ---
            payload = f"{int(led_index)} {r_val} {g_val} {b_val}\n"
            serialObj.write(payload.encode('utf-8'))

    def getColor(self):
        return self.button.cget('bg')

# --- Logic Functions ---

def updateBrightness(val):
    global brightness
    brightness = float(val) / 100.0
    
    # This loop refreshes all buttons instantly when you slide the bar
    if serialObj and serialObj.is_open:
        for r in range(row_count):
            for c in range(col_count):
                current_hex = colorButtonList[r][c].getColor()
                colorButtonList[r][c].setColor(current_hex)
            window.update_idletasks() # Keeps the slider smooth

def Hex_RGB(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def chooseColor():
    global color_code
    chosen = colorchooser.askcolor(title="Choose color")[-1]
    if chosen:
        color_code = chosen
    return color_code

def clearCanvas():
    global animate
    animate = False
    print("Clearing Matrix...")
    for r in range(row_count):
        for c in range(col_count):
            colorButtonList[r][c].setColor(off_color)
            time.sleep(0.005) # Slightly faster clear
        window.update() 
    print("Clear Complete.")

def fillCanvas():
    global color_code
    print(f"Filling Matrix with {color_code}...")
    for r in range(row_count):
        for c in range(col_count):
            colorButtonList[r][c].setColor(color_code)
            time.sleep(0.005)
        window.update()
    print("Fill Complete.")

def testRainbow():
    if serialObj and serialObj.is_open:
        serialObj.write(b"T\n")

def saveImage():
    path = os.path.join(os.path.dirname(__file__), "Saves")
    if not os.path.exists(path):
        os.makedirs(path)
        
    f_path = filedialog.asksaveasfilename(initialdir=path, defaultextension=".txt", 
                                         filetypes=[("Text files", "*.txt")])
    if f_path:
        with open(f_path, "w") as f:
            for r_file in range(row_count):
                row_string_list = []
                for c_file in range(col_count):
                    # Fixed rotation: reverse the "Mario flip"
                    gui_row = c_file
                    gui_col = (row_count - 1) - r_file
                    color = colorButtonList[gui_row][gui_col].getColor()
                    row_string_list.append(color)
                
                line = ", ".join(row_string_list) + ", \n"
                f.write(line)
        print(f"Saved: {os.path.basename(f_path)}")

def loadImage():
    path = os.path.join(os.path.dirname(__file__), "Saves")
    f_path = filedialog.askopenfilename(initialdir=path, filetypes=[("Text", "*.txt")])
    if f_path:
        with open(f_path, "r") as f:
            file_data = []
            for line in f:
                if line.strip():
                    colors = [c.strip() for c in line.split(",") if c.strip()]
                    file_data.append(colors)

        for r in range(len(file_data)):
            for c in range(len(file_data[r])):
                hex_val = file_data[r][c]
                target_row = c
                target_col = (col_count - 1) - r
                if 0 <= target_row < row_count and 0 <= target_col < col_count:
                    colorButtonList[target_row][target_col].setColor(hex_val)
                    time.sleep(0.01)
            window.update()

def playAnimation():
    global animate
    selected_path = filedialog.askdirectory(title="Select Animation Folder")
    if not selected_path: return

    files = sorted([f for f in os.listdir(selected_path) if f.endswith('.txt')])
    if not files: return

    animate = True
    while animate:
        for filename in files:
            if not animate: break
            f_path = os.path.join(selected_path, filename)
            try:
                with open(f_path, "r") as f:
                    file_data = [ [c.strip() for c in line.split(",") if c.strip()] for line in f if line.strip() ]

                    for r in range(len(file_data)):
                        for c in range(len(file_data[r])):
                            hex_val = file_data[r][c]
                            target_row = c
                            target_col = (col_count - 1) - r
                            if 0 <= target_row < row_count and 0 <= target_col < col_count:
                                colorButtonList[target_row][target_col].setColor(hex_val)
                                time.sleep(0.005) 
                    window.update()
                    time.sleep(0.15) 
            except Exception as e:
                print(f"Error: {e}")
                
def stopAnimation():
    global animate
    animate = False

def eyeDrop():
    global button_mode
    button_mode = False
    window.config(cursor="plus")

def makeButtons():
    control_frame = tk.Frame(window)
    control_frame.grid(row=row_count, column=0, columnspan=col_count, sticky="we", pady=5)
    
    top_row = tk.Frame(control_frame)
    top_row.pack(side="top", fill="x")
    tk.Label(top_row, text="Bright:").pack(side="left", padx=2)
    b_slider = tk.Scale(top_row, from_=0, to=100, orient="horizontal", command=updateBrightness, length=120)
    b_slider.set(20) 
    b_slider.pack(side="left", padx=5)

    mid_row = tk.Frame(control_frame)
    mid_row.pack(side="top", fill="x", pady=2)
    tk.Button(mid_row, text="Test",  command=testRainbow).pack(side="left", expand=True, fill="x")
    tk.Button(mid_row, text="RGB",   command=chooseColor).pack(side="left", expand=True, fill="x")
    tk.Button(mid_row, text="Pick",  command=eyeDrop).pack(side="left", expand=True, fill="x")
    tk.Button(mid_row, text="Fill",  command=fillCanvas).pack(side="left", expand=True, fill="x")
    tk.Button(mid_row, text="Clear", command=clearCanvas).pack(side="left", expand=True, fill="x")

    bot_row = tk.Frame(control_frame)
    bot_row.pack(side="top", fill="x", pady=2)
    tk.Button(bot_row, text="Save",  command=saveImage).pack(side="left", expand=True, fill="x")
    tk.Button(bot_row, text="Load",  command=loadImage).pack(side="left", expand=True, fill="x")
    tk.Button(bot_row, text="▶ Play", fg="green", command=lambda: Thread(target=playAnimation, daemon=True).start()).pack(side="left", expand=True, fill="x")
    tk.Button(bot_row, text="■ Stop", fg="red", command=stopAnimation).pack(side="left", expand=True, fill="x")

if __name__ == "__main__":
    try:
        serialObj = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        time.sleep(2)
    except Exception as e:
        print(f"Serial Error: {e}")
        serialObj = None

    button_mode = True
    color_code = '#ffffff' 
    brightness = 0.2
    animate = False

    window = tk.Tk()
    window.title("Matrix Master")
    window.geometry("700x850") # Made a bit taller for the buttons

    colorButtonList = [[LEDButton(i, j) for j in range(col_count)] for i in range(row_count)]

    makeButtons()
    window.mainloop()