import tkinter as tk
import names
import re

CAPABILITIES = [
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
    def __init__(self, attributes, capabilities):
        self.padX = 20
        self.padY = 10
        self.defaultPoints = "5"

        self.capabilities = capabilities
        self.attributes = attributes

        self.window = None
        self.nameEntry = None
        self.pointsLabel = None

        self.attrEntries = []
        self.capLabels = []

        self.setupWindow()
        self.setupAttributes()
        self.setupCapabilities()
        self.setupPointEntries()

    def setupWindow(self):
        self.window = tk.Tk()
        self.window.title("Point Buy")

        self.nameEntry = tk.Entry(self.window, width=30)
        self.nameEntry.grid(row=0, column=0, padx=self.padX, pady=self.padY)
        self.nameEntry.insert(0, names.get_full_name())

        self.pointsLabel = tk.Label(self.window, text="Total Points: 50")
        self.pointsLabel.grid(row=6, column=3, padx=self.padX, pady=self.padY)

        saveButton = tk.Button(
            self.window, text="Save File", command=self.save)
        saveButton.grid(row=0, column=1, padx=self.padX, pady=self.padY)

        resetButton = tk.Button(self.window, text="Reset", command=self.reset)
        resetButton.grid(row=0, column=2, padx=self.padX, pady=self.padY)

        newCharButton = tk.Button(
            self.window, text="New Character", command=self.newCharacter)
        newCharButton.grid(row=0, column=3, padx=self.padX, pady=self.padY)

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
            strVar.set(self.defaultPoints)
            strVar.trace_add("write", self.updateTotal)

            entryObj = tk.Entry(
                self.window, textvariable=strVar)
            entryObj.grid(row=i+2, column=1, padx=self.padX, pady=self.padY)

            entry["strVar"] = strVar
            entry["obj"] = entryObj
            self.attrEntries.append(entry)
        self.updateTotal()

    def setupCapabilities(self):
        tk.Label(self.window, text="Capability").grid(
            row=1, column=2, padx=self.padX, pady=self.padY)

        for i in range(len(self.capabilities)):
            self.capLabels.append(
                tk.Label(self.window, text=self.capabilities[4]))
            self.capLabels[-1].grid(row=i+2, column=2)

    def updateTotal(self, var=None, index=None, mode=None):
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
                                           self.attrEntries[i]["obj"].get(), self.capLabels[i].cget("text"))

        maxLen = len(max(re.findall(r"^\S+", text, re.M), key=len))
        formatted = re.sub(r"(\S+)[^\S\r\n]+", lambda m: m.group(1) +
                           ((maxLen + 1) - len(m.group(1))) * " ", text)
        output = "{}\n\n".format(self.nameEntry.get()) + formatted

        file = open("{}.txt".format(self.nameEntry.get()), "w")
        file.write(output)
        file.close()

    def reset(self):
        for entry in self.attrEntries:
            entry["strVar"].set(self.defaultPoints)

    def newCharacter(self):
        self.reset()
        self.nameEntry.delete(0, 'end')
        self.nameEntry.insert(0, names.get_full_name())

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = PointBuyApp(SKILLS, CAPABILITIES)
    app.run()
