import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import time

# --
# Units
# --
UNITS = [
    "", "K", "M", "B", "T",
    "Qa","Qi","Sx","Sp","Oc","N","Dc",
    "Ud","Dd","Td","Qua","Qui","Sxd","Spd","Ocd","Nod",
    "Vg","UVg","DVg","TVg","QaVg"
]
UNIT_MAP = {abbr: 10**(3*i) for i, abbr in enumerate(UNITS)}

# --
# Number conversion
# --
def to_number(value: str, unit: str):
    try:
        num = float(value)
    except:
        num = 0
    return num * UNIT_MAP.get(unit, 1)

# ---
# Main calculation
# --
def calculate():
    try:
        want = to_number(entry_want.get(), unit_want.get())
        have = to_number(entry_have.get(), unit_have.get())
        per_tick = to_number(entry_tick.get(), unit_tick.get())
        gamepass = gamepass_var.get()

        remaining = want - have
        if remaining <= 0:
            result_label.config(text=lang["already"])
            return

        ticks = remaining / per_tick
        time_seconds = ticks * (0.6 if gamepass == "Yes" else 1.2)

        h = int(time_seconds // 3600)
        m = int((time_seconds % 3600) // 60)
        s = int(time_seconds % 60)

        result_label.config(text=f"{lang['time']}: {h}h {m}m {s}s")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# ---
# Anim
# --
def animate_title():
    t = time.time() * 0.1
    hue = t % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)  # pastel rainbow
    color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

    title_label.config(fg=color)
    root.configure(highlightbackground=color, highlightcolor=color, highlightthickness=4)
    root.after(16, animate_title)

# --
# Language dictionaries
# --
LANG_EN = {
    "want": "Power you want:",
    "have": "Power you have now:",
    "tick": "Power I get per tick:",
    "gamepass": "X2 Gamepass?",
    "calc": "Calculate",
    "time": "Time",
    "already": "You already reached your goal 🎉",
    "credits_btn": "Credits",
    "credits_title": "Credits",
    "credits_message": (
        'App made by "RoWu" AKA "4d5d" in Roblox\n'
        "Also thanks ARK for telling me how much is a tick lol.\n\n"
        "You can post this file wherever you want,\n"
        "but please don't remove the credits :)"
    )
}
LANG_ES = {
    "want": "Poder que quieres:",
    "have": "Poder que tienes ahora:",
    "tick": "Poder que ganas por tick:",
    "gamepass": "¿X2 Gamepass?",
    "calc": "Calcular",
    "time": "Tiempo",
    "already": "Ya alcanzaste tu meta 🎉",
    "credits_btn": "Créditos",
    "credits_title": "Créditos",
    "credits_message": (
        'Aplicación hecha por "RoWu" AKA "4d5d" en Roblox\n'
        "Gracias a ARK por decirme cuánto dura un tick, lol.\n\n"
        "Puedes publicar este archivo donde quieras,\n"
        "pero por favor no quites los créditos :)"
    )
}

current_lang = "ENG"
lang = LANG_EN

# --
# Language toggle
# ----
def toggle_lang():
    global lang, current_lang
    if current_lang == "ENG":
        lang = LANG_ES
        current_lang = "ESP"
        lang_btn.config(text="ENG")
    else:
        lang = LANG_EN
        current_lang = "ENG"
        lang_btn.config(text="ESP")
    credits_btn.config(text=lang["credits_btn"])
    update_labels()

def update_labels():
    lbl_want.config(text=lang["want"])
    lbl_have.config(text=lang["have"])
    lbl_tick.config(text=lang["tick"])
    lbl_gamepass.config(text=lang["gamepass"])
    calc_btn.config(text=lang["calc"])

# ---
# Credits popup
# --
def show_credits():
    messagebox.showinfo(lang["credits_title"], lang["credits_message"])

# --
# Number-only validation
# --
def validate_number(P):
    if P == "" or P.replace(".", "", 1).isdigit():
        return True
    return False

# ---
# Modern button factory (bubble style)
# -
def make_button(parent, text, command, width=12):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg="#2C2C2C",
        fg="white",
        activebackground="#3C3C3C",
        activeforeground="white",
        relief="flat",
        font=("Bahnschrift SemiBold", 11),
        bd=0,
        width=width,
        height=1
    )
    return btn

# --
# UI
# --
root = tk.Tk()
root.title("RoWu's Tool")
root.configure(bg="#121212")
root.geometry("550x500")

vcmd = (root.register(validate_number), "%P")

# Top-left controls
lang_btn = make_button(root, "ESP", toggle_lang, width=5)
lang_btn.place(x=10, y=10)

credits_btn = make_button(root, LANG_EN["credits_btn"], show_credits, width=8)
credits_btn.place(x=70, y=10)

# Title
title_label = tk.Label(
    root,
    text="RoWu's Tool",
    font=("Bahnschrift SemiBold", 30),
    bg="#121212"
)
title_label.pack(pady=30)

# ---- Power you want
frame1 = tk.Frame(root, bg="#121212")
frame1.pack(pady=10)
lbl_want = tk.Label(frame1, text=lang["want"], bg="#121212", fg="white", font=("Segoe UI", 11))
lbl_want.pack(side="left")
entry_want = ttk.Entry(frame1, width=12, validate="key", validatecommand=vcmd)
entry_want.pack(side="left", padx=6)
unit_want = ttk.Combobox(frame1, values=UNITS, width=6, state="readonly")
unit_want.set("B")
unit_want.pack(side="left")

# ---- Power you have
frame2 = tk.Frame(root, bg="#121212")
frame2.pack(pady=10)
lbl_have = tk.Label(frame2, text=lang["have"], bg="#121212", fg="white", font=("Segoe UI", 11))
lbl_have.pack(side="left")
entry_have = ttk.Entry(frame2, width=12, validate="key", validatecommand=vcmd)
entry_have.pack(side="left", padx=6)
unit_have = ttk.Combobox(frame2, values=UNITS, width=6, state="readonly")
unit_have.set("M")
unit_have.pack(side="left")

# ---- Power per tick
frame3 = tk.Frame(root, bg="#121212")
frame3.pack(pady=10)
lbl_tick = tk.Label(frame3, text=lang["tick"], bg="#121212", fg="white", font=("Segoe UI", 11))
lbl_tick.pack(side="left")
entry_tick = ttk.Entry(frame3, width=12, validate="key", validatecommand=vcmd)
entry_tick.pack(side="left", padx=6)
unit_tick = ttk.Combobox(frame3, values=UNITS, width=6, state="readonly")
unit_tick.set("M")
unit_tick.pack(side="left")

# ---- Gamepass
frame4 = tk.Frame(root, bg="#121212")
frame4.pack(pady=15)
lbl_gamepass = tk.Label(frame4, text=lang["gamepass"], bg="#121212", fg="white", font=("Segoe UI", 11))
lbl_gamepass.pack(side="left")
gamepass_var = tk.StringVar(value="No")
gamepass_select = ttk.Combobox(frame4, textvariable=gamepass_var, values=["Yes","No"], width=6, state="readonly")
gamepass_select.pack(side="left")

# ---- Calculate
calc_btn = make_button(root, lang["calc"], calculate)
calc_btn.pack(pady=25)

# ---- Result
result_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Bahnschrift SemiBold", 15))
result_label.pack(pady=10)

# Start animation
animate_title()

root.mainloop()

