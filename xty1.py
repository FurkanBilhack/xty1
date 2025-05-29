import threading
import time
import random
import win32gui
import win32api
import win32con
import tkinter as tk

running = False
stop_thread = False

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

def send_z1():
    global running, stop_thread
    while not stop_thread:
        if running and "Knight Online" in get_active_window_title():
            for char in "z1":
                win32api.keybd_event(ord(char.upper()), 0, 0, 0)
                win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.05)
            time.sleep(random.uniform(0.8, 1.4))
        else:
            time.sleep(0.2)

def toggle():
    global running
    running = not running
    status_var.set("Aktif" if running else "Pasif")

def listen_mouse():
    global stop_thread
    while not stop_thread:
        if win32api.GetAsyncKeyState(0x05):  # XButton1 (mouse yan düğmesi)
            toggle()
            time.sleep(0.3)
        time.sleep(0.05)

def on_close():
    global stop_thread
    stop_thread = True
    root.destroy()

root = tk.Tk()
root.title("xty1 - KO Makro")
root.geometry("300x100")
root.resizable(False, False)

status_var = tk.StringVar(value="Pasif")
label = tk.Label(root, text="Durum:")
label.pack(pady=5)
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack()

threading.Thread(target=send_z1, daemon=True).start()
threading.Thread(target=listen_mouse, daemon=True).start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
