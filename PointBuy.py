import tkinter as tk
from functools import partial
import names
import re

PADX = 20
PADY = 10
TOTAL_POINTS = 50
DESCRIPTORS = [
    "detrimental",
    "impractical",
    "weak",
    "less than average",
    "average",
    "above average",
    "exceptional",
    "extraordinary",
    "excessive",
    "over-encumbering"
]

SKILLS = [
    "Strength",
    "Agility",
    "Constitution",
    "Edge",
    "Intelligence",
    "Focus",
    "Special",
    "Equipment",
    "Connection",
    "Experience"
]

LIST_LENGTH = len(SKILLS)


def updateTotal(var, index, mode):
    temp = 0
    for i in range(LIST_LENGTH):
        if str.isdigit(entries[i].get()) or entries[i].get() == 0:
            temp += int(entries[i].get())
            if int(entries[i].get()) < 1:
                row = 0
            elif int(entries[i].get()) >= 10:
                row = 9
            else:
                row = int(entries[i].get()) - 1
            caps[i].config(text=DESCRIPTORS[row])
    pointsLabel.config(text="Total Points: {}".format(str(temp)))


def save():
    text = ""
    for i in range(LIST_LENGTH):
        text += "{}: {} ({})\n".format(SKILLS[i],
                                       entries[i].get(), DESCRIPTORS[i])
    maxLen = len(max(re.findall(r"^\S+", text, re.M), key=len))
    result = re.sub(r"(\S+)[^\S\r\n]+", lambda m: m.group(1) +
                    ((maxLen + 1) - len(m.group(1))) * " ", text)
    final = "{}\n\n".format(name.get()) + result
    file = open("{}.txt".format(name.get()), "w")
    file.write(final)
    file.close()


def reset():
    master.destroy()
    _start()


def _start():
    global master
    master = tk.Tk()
    master.title("Point Buy")
    master.geometry("750x600")

    global nameVar
    nameVar = tk.IntVar(master)
    nameVar.set(names.get_full_name())
    global name
    name = tk.Entry(master, textvariable=nameVar)
    name.grid(row=0, column=0, padx=PADX, pady=PADY)
    name.config(text=names.get_full_name())

    global pointsLabel
    pointsLabel = tk.Label(master, text="Total Points: 50")
    pointsLabel.grid(row=6, column=20, padx=PADX, pady=PADY)

    tk.Label(master, text="Skill").grid(row=1, column=0, padx=PADX, pady=PADY)
    tk.Label(master, text="Capability").grid(
        row=1, column=12, padx=PADX, pady=PADY)
    tk.Label(master, text="Points").grid(row=1, column=4, padx=PADX, pady=PADY)

    global entries
    global caps
    global entryVars
    entries = []
    caps = []
    entryVars = []

    for i in range(LIST_LENGTH):
        tk.Label(master, text=SKILLS[i]).grid(
            row=i+2, column=0, padx=PADX, pady=PADY)

    for i in range(LIST_LENGTH):
        caps.append(tk.Label(master, text=DESCRIPTORS[4]))
        caps[-1].grid(row=i+2, column=12)

    for i in range(LIST_LENGTH):
        entryVars.append(tk.IntVar(master))
        entryVars[-1].set("5")
        entryVars[-1].trace_add("write", partial(updateTotal))
        ent = tk.Entry(master, textvariable=entryVars[-1])
        ent.grid(row=i+2, column=4, padx=PADX, pady=PADY)
        entries.append(ent)
        i += 1

    saveButton = tk.Button(master, text="Save File", command=save)
    saveButton.grid(row=16, column=0, padx=PADX, pady=PADY)

    resetButton = tk.Button(master, text="Reset", command=reset)
    resetButton.grid(row=16, column=1, padx=PADX, pady=PADY)

    master.mainloop()


if __name__ == '__main__':
    _start()
