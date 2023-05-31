import tkinter as tk
from functools import partial
import names
import re

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


class PointBuyApp:
    def __init__(self, totalPoints, capabilities, attributes):
        self.padX = 20
        self.padY = 10

        self.totalPoints = totalPoints
        self.capabilities = capabilities
        self.attributes = attributes

        self.window = None
        self.nameEntry = None

        self.attrEntries = []
        self.capLabels = []

        self.setupWindow()
        self.setupAttributes()
        self.setupPointEntries()
        self.setupCapabilities()

    def setupWindow(self):
        self.window = tk.Tk()
        self.window.title("Point Buy")

        nameVar = tk.IntVar(self.window)
        nameVar.set(names.get_full_name())
        self.nameEntry = tk.Entry(self.window, textvariable=nameVar)
        self.nameEntry.grid(row=0, column=0, padx=self.padX, pady=self.padY)
        self.nameEntry.config(text=names.get_full_name())

        self.pointsLabel = tk.Label(self.window, text="Total Points: 50")
        self.pointsLabel.grid(row=6, column=20, padx=self.padX, pady=self.padY)

        saveButton = tk.Button(
            self.window, text="Save File", command=self.save)
        saveButton.grid(row=0, column=1, padx=self.padX, pady=self.padY)

        resetButton = tk.Button(self.window, text="Reset", command=self.reset)
        resetButton.grid(row=0, column=2, padx=self.padX, pady=self.padY)

    def setupAttributes(self):
        tk.Label(self.window, text="Attributes").grid(
            row=1, column=0, padx=self.padX, pady=self.padY)

        for i in range(len(self.attributes)):
            tk.Label(self.window, text=self.attributes[i]).grid(
                row=i+2, column=0, padx=self.padX, pady=self.padY)

    def setupPointEntries(self):
        tk.Label(self.window, text="Points").grid(
            row=1, column=1, padx=self.padX, pady=self.padY)

        for i in range(len(self.attributes)):
            entry = {}

            strVar = tk.StringVar(self.window)
            strVar.set("5")
            strVar.trace_add("write", partial(self.updateTotal))

            entryObj = tk.Entry(
                self.window, textvariable=strVar)
            entryObj.grid(row=i+2, column=1, padx=self.padX, pady=self.padY)

            entry["strVar"] = strVar
            entry["obj"] = entryObj
            self.attrEntries.append(entry)

    def setupCapabilities(self):
        tk.Label(self.window, text="Capability").grid(
            row=1, column=2, padx=self.padX, pady=self.padY)

        for i in range(len(self.capabilities)):
            self.capLabels.append(
                tk.Label(self.window, text=self.capabilities[4]))
            self.capLabels[-1].grid(row=i+2, column=2)

    def updateTotal(self, var, index, mode):
        currentTotal = 0
        for i in range(len(self.attributes)):
            if str.isdigit(self.attrEntries[i]["obj"].get()) or self.attrEntries[i]["obj"].get() == 0:
                currentTotal += int(self.attrEntries[i]["obj"].get())
                if int(self.attrEntries[i]["obj"].get()) < 1:
                    row = 0
                elif int(self.attrEntries[i]["obj"].get()) >= 10:
                    row = 9
                else:
                    row = int(self.attrEntries[i]["obj"].get()) - 1
                self.capLabels[i].config(text=self.capabilities[row])
        self.pointsLabel.config(
            text="Total Points: {}".format(str(currentTotal)))

    def save(self):
        text = ""
        for i in range(len(self.attributes)):
            text += "{}: {} ({})\n".format(self.attributes[i],
                                           self.attrEntries[i].get(), self.capabilities[i])

        maxLen = len(max(re.findall(r"^\S+", text, re.M), key=len))
        formatted = re.sub(r"(\S+)[^\S\r\n]+", lambda m: m.group(1) +
                           ((maxLen + 1) - len(m.group(1))) * " ", text)
        output = "{}\n\n".format(self.nameEntry.get()) + formatted

        file = open("{}.txt".format(self.nameEntry.get()), "w")
        file.write(output)
        file.close()

    def reset(self):
        self.window.destroy()
        self.setupWindow()
        self.setupAttributes()
        self.setupCapabilities()
        self.setupPointEntries()
        self.run()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = PointBuyApp(50, DESCRIPTORS, SKILLS)
    app.run()
