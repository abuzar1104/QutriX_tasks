import tkinter as tk
from tkinter import messagebox

# --- Style Constants for Easy Customization ---
STYLE = {
    "BACKGROUND": "#1e1e1e",
    "DISPLAY_BG": "#2d2d2d",
    "BUTTON_BG": "#505050",
    "OPERATOR_BG": "#ff9500",
    "SPECIAL_BG": "#d4d4d2",
    "TEXT_COLOR": "#ffffff",
    "SPECIAL_TEXT_COLOR": "#000000",
    "HOVER_COLOR": "#6a6a6a",
    "OPERATOR_HOVER": "#ffab3d",
    "EQUAL_COLOUR": "#69ec5f",  # Your light green color
    "EQUAL_HOVER": "#83f27b",  # A slightly lighter green for the hover effect
    "FONT_MAIN": ("Segoe UI", 16),
    "FONT_DISPLAY": ("Segoe UI", 28, "bold"),
    "FONT_COPYRIGHT": ("Segoe UI", 9),
}


# -----------------------------
# Functions
# -----------------------------
def click(event):
    """Handles button click events."""
    global expression
    text = event.widget.cget("text")

    if text == "=":
        if not expression:
            return
        try:
            eval_expression = expression.replace("x", "*").replace("÷", "/")
            result = str(eval(eval_expression))
            screen_var.set(result)
            expression = result
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            expression = ""
            screen_var.set("")
    elif text == "C":
        expression = ""
        screen_var.set("")
    elif text == "⌫":  # Backspace character
        expression = expression[:-1]
        screen_var.set(expression)
    else:
        expression += text
        screen_var.set(expression)


def on_enter(event):
    """Changes button color on hover."""
    button = event.widget
    text = button.cget("text")
    if text == "=":
        button.config(bg=STYLE["EQUAL_HOVER"])
    elif text in "÷X-+":
        button.config(bg=STYLE["OPERATOR_HOVER"])
    else:
        button.config(bg=STYLE["HOVER_COLOR"])


def on_leave(event):
    """Restores button color when mouse leaves."""
    button = event.widget
    text = button.cget("text")
    if text == "=":
        button.config(bg=STYLE["EQUAL_COLOUR"])
    elif text in "÷x-+":
        button.config(bg=STYLE["OPERATOR_BG"])
    elif text in "C⌫%":
        button.config(bg=STYLE["SPECIAL_BG"])
    else:
        button.config(bg=STYLE["BUTTON_BG"])


# -----------------------------
# Main Window and Display
# -----------------------------
root = tk.Tk()
root.title("Modern Calculator")
root.geometry("350x500")
root.resizable(False, False)
root.configure(bg=STYLE["BACKGROUND"])

expression = ""
screen_var = tk.StringVar()

display_frame = tk.Frame(root, bg=STYLE["BACKGROUND"])
display_frame.pack(fill="x", padx=10, pady=15)

screen = tk.Entry(
    display_frame,
    textvariable=screen_var,
    font=STYLE["FONT_DISPLAY"],
    bg=STYLE["DISPLAY_BG"],
    fg=STYLE["TEXT_COLOR"],
    bd=0,
    relief="flat",
    justify="right",
)
screen.pack(fill="x", ipady=15)

# -----------------------------
# Buttons Frame and Creation
# -----------------------------
btns_frame = tk.Frame(root, bg=STYLE["BACKGROUND"])
btns_frame.pack(expand=True, fill="both", padx=10, pady=10)

buttons = [
    ("C", 0, 0, 1, 1),
    ("⌫", 0, 1, 1, 1),
    ("%", 0, 2, 1, 1),
    ("÷", 0, 3, 1, 1),
    ("7", 1, 0, 1, 1),
    ("8", 1, 1, 1, 1),
    ("9", 1, 2, 1, 1),
    ("x", 1, 3, 1, 1),
    ("4", 2, 0, 1, 1),
    ("5", 2, 1, 1, 1),
    ("6", 2, 2, 1, 1),
    ("-", 2, 3, 1, 1),
    ("1", 3, 0, 1, 1),
    ("2", 3, 1, 1, 1),
    ("3", 3, 2, 1, 1),
    ("+", 3, 3, 1, 1),
    ("0", 4, 0, 1, 2),
    (".", 4, 2, 1, 1),
    ("=", 4, 3, 1, 1),
]

for text, row, col, rowspan, columnspan in buttons:
    # --- THIS SECTION SETS THE INITIAL COLOR ---
    if text in "0123456789.":
        bg_color, fg_color = STYLE["BUTTON_BG"], STYLE["TEXT_COLOR"]
    elif text in "C⌫%":
        bg_color, fg_color = STYLE["SPECIAL_BG"], STYLE["SPECIAL_TEXT_COLOR"]
    elif text == "=":  # Specifically sets the '=' button to green
        bg_color, fg_color = STYLE["EQUAL_COLOUR"], STYLE["TEXT_COLOR"]
    else:  # Operators
        bg_color, fg_color = STYLE["OPERATOR_BG"], STYLE["TEXT_COLOR"]

    btn = tk.Button(
        btns_frame,
        text=text,
        font=STYLE["FONT_MAIN"],
        bg=bg_color,
        fg=fg_color,
        bd=0,
        relief="flat",
        activebackground=bg_color,
        activeforeground=fg_color,
    )
    btn.grid(
        row=row,
        column=col,
        rowspan=rowspan,
        columnspan=columnspan,
        sticky="nsew",
        padx=2,
        pady=2,
    )
    btn.bind("<Button-1>", click)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Make grid cells expand
for i in range(5):
    btns_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    btns_frame.grid_columnconfigure(i, weight=1)

# -----------------------------
# Copyright Footer
# -----------------------------
copyright_label = tk.Label(
    root,
    text="Copyright © 2025 Abuzar Ansari. All rights reserved.",
    font=STYLE["FONT_COPYRIGHT"],
    bg=STYLE["BACKGROUND"],
    fg="#a4b0be",
)
copyright_label.pack(side="bottom", fill="x", pady=5)

root.mainloop()
