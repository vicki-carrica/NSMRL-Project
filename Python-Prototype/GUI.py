import math
from multiprocessing import context
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
matplotlib.use("TkAgg")

root = Tk()
root.title('GUI')
root.geometry('800x480')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

s = ttk.Style()
s.configure('TNotebook.Tab', font=('Fixedsys','15'))
s.configure('Treeview', font=('Fixedsys','10'))
s.configure('Treeview.Heading', font=('Fixedsys','15'))

notebook = ttk.Notebook(root)
notebook.grid(row=0,column=0)
frame1 = Frame(notebook, width=800, height=800)
frame2 = Frame(notebook, width=800, height=480)
frame3 = Frame(notebook, width=800, height=480)

notebook.add(frame1, text="Input")
notebook.add(frame2, text="Graph")
notebook.add(frame3, text="Data")

book2 = ttk.Notebook(frame2)
book2.grid(row=0, column=0)
oFrame = Frame(book2, width=760, height=430)
coFrame = Frame(book2, width=760, height=430)
pFrame = Frame(book2, width=760, height=430)
book2.add(oFrame, text="Oxygen")
book2.add(coFrame, text="Carbon Dioxide")
book2.add(pFrame, text="Pressure")

data = ttk.Treeview(frame3)


def oxSurvTime(fit, unfit, cand, percentFlood, oxConc, temp):
    oxygenConcentration = oxConc/100.0
    temperature = temp + 459.67
    survivors = fit + unfit
    volumeCompt = (100-percentFlood)*62800/100
    candleSCF = cand * 115
    tOCandles = candleSCF/survivors
    numerator = (1.0/.7302)*volumeCompt*(oxygenConcentration-0.13)*(1.0/temperature)
    denominator = (survivors*.0838)/32
    tOThirteen = numerator/denominator
    OSurvivalTime = tOCandles + tOThirteen
    return OSurvivalTime

def coSurvTime(fit, unfit, cani, percentFlood, coConc, temp):
    coConcentration = coConc/100.0
    temperature = temp + 459.67
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    tLiOH = (cani*73)/survivors
    numerator = (1/.7302)*volumeCompt*(.06 - coConcentration)*(1/temperature)
    denominator = (survivors * 0.1)/44
    tCO = numerator/denominator
    coSurvivalTime = tLiOH + tCO
    return coSurvivalTime

def hourBreathing(fit, unfit):
    survivors = fit + unfit
    w = fit/2.0
    escapeCycles = round(w)
    escaperHr = escapeCycles*.25*(fit - (2*(escapeCycles + 1)/2))
    nonEscaperHr = (survivors-fit)*fit/(1/.25 * 2)
    g = escaperHr + nonEscaperHr
    return g

def calcVBreath(percentFlooded, fit, pressure):
    vCompt = (100-percentFlooded)* pressure* 62800/100
    vBreath = vCompt - 214 - (fit*53.5)
    return vBreath

def fswToATA(pressure):
    ata = (pressure+33)/33
    return ata

def oStartEscapeTime(cand, fit, unfit, percentFlood, oConc, volumeBreath, temp, breathingHr):
    concInt = oConc/100.0
    temperature = temp + 459.67
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    tCandles = (cand*115.0 - breathingHr)/survivors
    numerator1 = ((concInt*volumeCompt)-(.13*volumeBreath))*(1/.7302)*(1/temperature)
    numerator2 = breathingHr*.0838*(1/32.0)
    numerator = numerator1-numerator2
    denominator = survivors*.0838*(1/32.0)
    oWaitTime = numerator/denominator
    oSET = oWaitTime+tCandles
    return oSET

def coStartEscapeTime(cani, fit, unfit, percentFlood, coConc, volumeBreath, temp, breathingHr):
    concInt = coConc/100.0
    temperature = temp + 459.67
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    tLiOH = (cani*73)/survivors
    numerator = ((.06*volumeBreath)-(concInt*volumeCompt))*(1/.7302)*(1/temperature)-breathingHr*.1*(1/44.0)
    denominator = survivors*.1*(1.0/44.0)
    coWaitingTime = numerator/denominator
    coSET = coWaitingTime + tLiOH
    return coSET

def eabStartEscapeTime(fit, unfit, pFinal, volumeBreath, breathingHr):
    survivors = fit + unfit
    numerator = (1.697 - pFinal)*volumeBreath-(breathingHr*20.0)
    denominator = survivors*20.0
    eabStartTime = numerator/denominator
    return eabStartTime

def pFinal(percentFlood, pressure, volumeBreath):
    volumeCompt = (100-percentFlood)*62800/100
    airAddedByEscapes = 8*pressure*(144+3.33)
    pFinal = ((volumeCompt)*pressure+airAddedByEscapes)/volumeBreath
    return pFinal


oxY = []
oxX = []
coY = []
coX = []
pY = []
pX = []
start = time.time()
counter = 0
fitLabel = Label(frame1, text="Fit survivors: ")
fitLabel.grid(row=1, column=0)
fitLabel.config(font=('Fixedsys',15))
fitEnter = Entry(frame1, width=10)
fitEnter.grid(row=1, column=1, ipady=10, pady=3)
fitEnter.config(font=('Fixedsys', 10))
unfitLabel = Label(frame1, text="Unfit survivors: ")
unfitLabel.grid(row=2, column=0)
unfitLabel.config(font=('Fixedsys', 15))
unfitEnter = Entry(frame1, width=10)
unfitEnter.grid(row=2, column=1, ipady=10, pady=3)
unfitEnter.config(font=('Fixedsys', 10))
candLabel = Label(frame1, text="Chlorate candles: ")
candLabel.grid(row=3, column=0)
candLabel.config(font=('Fixedsys', 15))
candEnter = Entry(frame1, width=10)
candEnter.grid(row=3, column=1, ipady=10, pady=3)
candEnter.config(font=('Fixedsys', 10))
caniLabel = Label(frame1, text="ExtendAir kits: ")
caniLabel.grid(row=4, column=0)
caniLabel.config(font=('Fixedsys', 15))
caniEnter = Entry(frame1, width=10)
caniEnter.grid(row=4, column=1, ipady=10, pady=3)
caniEnter.config(font=('Fixedsys', 10))
pressLabel = Label(frame1, text="Pressure (fsw): ")
pressLabel.grid(row=5, column=0)
pressLabel.config(font=('Fixedsys', 15))
pressEnter = Entry(frame1, width=10)
pressEnter.grid(row=5, column=1, ipady=10, pady=3)
pressEnter.config(font=('Fixedsys', 10))
floodLabel = Label(frame1, text="Percent Flooded: ")
floodLabel.grid(row=1, column=2)
floodLabel.config(font=('Fixedsys', 15))
floodEnter = Entry(frame1, width=10)
floodEnter.grid(row=1, column=3, ipady=10, pady=3)
floodEnter.config(font=('Fixedsys', 10))
tempLabel = Label(frame1, text="Temperature: ")
tempLabel.grid(row=2, column=2)
tempLabel.config(font=('Fixedsys', 15))
tempEnter = Entry(frame1, width=10)
tempEnter.grid(row=2, column=3, ipady=10, pady=3)
tempEnter.config(font=('Fixedsys', 10))
oxLabel = Label(frame1, text="Oxygen (%SEV): ")
oxLabel.grid(row=3, column=2)
oxLabel.config(font=('Fixedsys', 15))
oxEnter = Entry(frame1, width=10)
oxEnter.grid(row=3, column=3, ipady=10, pady=3)
oxEnter.config(font=('Fixedsys', 10))
coLabel = Label(frame1, text="Carbon dioxide (%SEV): ")
coLabel.grid(row=4, column=2)
coLabel.config(font=('Fixedsys', 15))
coEnter = Entry(frame1, width=10)
coEnter.grid(row=4, column=3, ipady=10, pady=3)
coEnter.config(font=('Fixedsys', 10))
eabsEnter = Entry(frame1, width=10)
eabsEnter.grid(row=5, column=3, ipady=10, pady=3)
eabsEnter.config(font=('Fixedsys', 10))
eabsLabel = Label(frame1, text="Survivors with EABs: ")
eabsLabel.grid(row=5, column=2)
eabsLabel.config(font=('Fixedsys', 15))
oSTLabel = Label(frame1, text=" ")
oSTLabel.grid(row=7, column=0, columnspan=2)
oSTLabel.config(font=('Fixedsys', 12))
coSTLabel = Label(frame1, text=" ")
coSTLabel.config(font=('Fixedsys', 12))
coSTLabel.grid(row=8, column=0, columnspan=2)
oSETLabel = Label(frame1, text=" ")
oSETLabel.grid(row=9, column=0, columnspan=2)
oSETLabel.config(font=('Fixedsys', 12))
coSETLabel = Label(frame1, text=" ")
coSETLabel.grid(row=7, column=2, columnspan=2)
coSETLabel.config(font=('Fixedsys', 12))
eabSETLabel = Label(frame1, text=" ")
eabSETLabel.grid(row=8, column=2, columnspan=2, pady=10)
eabSETLabel.config(font=('Fixedsys', 12))
fO = Figure(figsize=(9,4.5), dpi=80) 
fCO = Figure(figsize=(9,4.5), dpi=80) 
fP = Figure(figsize=(9,4.5), dpi=80) 
o = fO.add_subplot(111)
o.set_ylim([13, 25])
c = fCO.add_subplot(111)
c.set_ylim([0, 6])
p = fP.add_subplot(111)
p.set_ylim([0, 25])



canvas = FigureCanvasTkAgg(fO, oFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, oFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

canvas = FigureCanvasTkAgg(fCO, coFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, coFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

canvas = FigureCanvasTkAgg(fP, pFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, pFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

data['columns'] = ("Time", "Oxygen %SEV", "Carbon Dioxide %SEV", "Pressure FSW")
data.column("#0", width=0, stretch=NO)
data.column("Time", anchor=W, width=25, minwidth=10)
data.column("Oxygen %SEV", anchor=W, width=50, minwidth=25)
data.column("Carbon Dioxide %SEV", anchor=W, width=100, minwidth=50)
data.column("Pressure FSW", anchor=W, width=50, minwidth=25)
data.heading("Time", text="Time (s)", anchor=W)
data.heading("Oxygen %SEV", text="Oxygen (%SEV)", anchor=W)
data.heading("Carbon Dioxide %SEV", text="Carbon Dioxide (%SEV)", anchor=W)
data.heading("Pressure FSW", text="Pressure (FSW)", anchor=W)

data.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def enterClick():
    try:
        fitSurv = int(fitEnter.get())
        unfitSurv = int(unfitEnter.get())
        candles = int(candEnter.get())
        canisters = int(caniEnter.get())
        pressure = float(pressEnter.get())
        flood = int(floodEnter.get())
        temp = float(tempEnter.get())
        oConc = float(oxEnter.get())
        coConc = float(coEnter.get())
        eabs = int(eabsEnter.get())

        oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp)
        oSTDay = math.floor(oSurvTime/24)
        oSTHr = math.floor(oSurvTime-24*oSTDay)
        coST = coSurvTime(fitSurv, unfitSurv, canisters, flood, coConc, temp)
        coSTDay = math.floor(coST/24)
        coSTHr = math.floor(coST-24*coSTDay)
        remainingHr = hourBreathing(fitSurv, unfitSurv)
        presATA = fswToATA(pressure)
        vBreath = calcVBreath(flood, fitSurv, presATA)
        finalP = pFinal(flood, presATA, vBreath)
        oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr)
        oSETDay = math.floor(oSET/24)
        oSETHr = math.floor(oSET-24*oSETDay)
        coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr)
        coSETDay = math.floor(coSET/24)
        coSETHr = math.floor(coSET-24*coSETDay)

        oSTLabel.config(text="Oxygen survival time:\n " + str(oSTDay) + " day " + str(oSTHr) + " hr")
        coSTLabel.config(text="Carbon dioxide survival time:\n " + str(coSTDay) + " day " + str(coSTHr) + " hr")
        oSETLabel.config(text="Oxygen start escape time:\n " + str(oSETDay) + " day " + str(oSETHr) + " hr")
        coSETLabel.config(text="Carbon dioxide start escape time:\n " + str(coSETDay) + " day " + str(coSETHr) + " hr")
        if eabs==(fitSurv+unfitSurv):
            eabSET = eabStartEscapeTime(fitSurv, unfitSurv, finalP, vBreath, remainingHr)
            eabSETDay = math.floor(eabSET/24)
            eabSETHr = math.floor(eabSET-24*eabSETDay)
            eabSETLabel.config(text="EABs start escape time:\n " + str(eabSETDay) + " day " + str(eabSETHr) + " hr")
        else:
            eabSET="NA"
            eabSETLabel.config(eabSETLabel.config(text="EABs start escape time:\n N/A"))
    except ValueError:
        messagebox.showwarning("VALUE ERROR","Invalid Inputs\nPlease do not leave blank boxes")
    

def helpClick():
    helpWindow = Toplevel(root)
    helpWindow.title("Help")
    helpWindow.geometry("750x430")
    helpTab = ttk.Notebook(helpWindow)
    helpTab.grid(row=0,column=0)
    h1 = Frame(helpTab, width=800, height=800)
    h2 = Frame(helpTab, width=800, height=480)
    h3 = Frame(helpTab, width=800, height=480)
    helpTab.add(h1, text="Input Information")
    helpTab.add(h2, text="Instructions")
    helpTab.add(h3, text="Spreadsheet Information")

    fitLabel = Label(h1, text="Fit survivors:", anchor=W)
    fitLabel.grid(row=0, column=0)
    fitLabel.config(font=('Fixedsys', 15))
    fitInfo = Label(h1, text="Sailors that have full use of both arms and can stand upright in a flooding escape trunk")
    fitInfo.grid(row=1, column=0)
    fitInfo.config(font=('Fixedsys', 10))

    unfitLabel = Label(h1, text="Unfit survivors:", anchor=W)
    unfitLabel.grid(row=2, column=0)
    unfitLabel.config(font=('Fixedsys', 15))
    unfitInfo = Label(h1, text="Sailors that are unable to escape but still intake oxygen and exhale carbon dioxide")
    unfitInfo.grid(row=3, column=0)
    unfitInfo.config(font=('Fixedsys', 10))

    candleLabel = Label(h1, text="Chlorate candles:", anchor=W)
    candleLabel.grid(row=4, column=0)
    candleLabel.config(font=('Fixedsys', 15))
    candleInfo = Label(h1, text="Candles that release oxygen into the atmosphere")
    candleInfo.grid(row=5, column=0)
    candleInfo.config(font=('Fixedsys', 10))

    extendAirLabel = Label(h1, text="ExtendAir Kits:", anchor=W)
    extendAirLabel.grid(row=6, column=0)
    extendAirLabel.config(font=('Fixedsys', 15))
    extendAirInfo = Label(h1, text="Intake carbon dioxide from the atmosphere through a reaction with lithium hydroxide")
    extendAirInfo.grid(row=7, column=0)
    extendAirInfo.config(font=('Fixedsys', 10))

    pressureLabel = Label(h1, text="Pressure:", anchor=W)
    pressureLabel.grid(row=8, column=0)
    pressureLabel.config(font=('Fixedsys', 15))
    pressureInfo = Label(h1, text="Measurement (in FSW) found on submarine")
    pressureInfo.grid(row=9, column=0)
    pressureInfo.config(font=('Fixedsys', 10))

    floodLabel = Label(h1, text="Percent Flooded:", anchor=W)
    floodLabel.grid(row=8, column=0)
    floodLabel.config(font=('Fixedsys', 15))
    floodInfo = Label(h1, text="Percentage of the compartment that is flooded, measurement found on submarine")
    floodInfo.grid(row=9, column=0)
    floodInfo.config(font=('Fixedsys', 10))

    tempLabel = Label(h1, text="Temperature:", anchor=W)
    tempLabel.grid(row=10, column=0)
    tempLabel.config(font=('Fixedsys', 15))
    tempInfo = Label(h1, text="Measurement (in Fahrenheit) found on submarine")
    tempInfo.grid(row=11, column=0)
    tempInfo.config(font=('Fixedsys', 10))

    concLabel = Label(h1, text="Oxygen and Carbon Dioxide Concentration:", anchor=W)
    concLabel.grid(row=12, column=0)
    concLabel.config(font=('Fixedsys', 15))
    concInfo = Label(h1, text="Measurements (in %SEV) found on submarine")
    concInfo.grid(row=13, column=0)
    concInfo.config(font=('Fixedsys', 10))

    eabLabel = Label(h1, text="Survivors with EABs:", anchor=W)
    eabLabel.grid(row=14, column=0)
    eabLabel.config(font=('Fixedsys', 15))
    eabInfo = Label(h1, text="Number of sailors who are wearing EABs")
    eabInfo.grid(row=15, column=0)
    eabInfo.config(font=('Fixedsys', 10))

    instructionLabel = Label(h2, text="Instructions:")
    instructionLabel.grid(row=0, column=0)
    instructionLabel.config(font=('Fixedsys', 20))
    instr = "-Input atmospheric data found on the submarine in the corresponding slots.\n-Press enter to calculate the survival and start escape times.\n-The shortest start escape time is the true time to start escape.\n-Press plot data to record and graph the atmospheric data.\n-Oxygen, carbon dioxide, and pressure data will be plotted and recorded in\n the 'Data' Tab. Data points can be deleted in the same 'Data' tab.\n-The 'Graph' tab has plots of atmospheric data."
    instructions = Label(h2, text=instr)
    instructions.grid(row=1, column=0)
    instructions.config(font=('Fixedsys', 15))


def plotClick():
    global counter
    global start
    counter=counter+1
    if counter==1:
        start = time.time()
    oxY.append(float(oxEnter.get()))
    coY.append(float(coEnter.get()))
    pY.append(float(pressEnter.get()))
    current = time.time()
    t = current - start
    oxX.append(t)
    coX.append(t)
    pX.append(t)
    o.plot(oxX, oxY)
    c.plot(coX, coY)
    p.plot(pX, pY)
    ti = math.floor(t)
    data.insert(parent='', index='end', iid=(counter-1), values=(ti, oxEnter.get(), coEnter.get(), pressEnter.get()))

def deleteClick():
    selected_item = data.selection()[0]
    print(selected_item)
    try:
        del oxY[int(selected_item)]
        del coY[int(selected_item)]
        del pY[int(selected_item)]
        del oxX[int(selected_item)]
        del coX[int(selected_item)]
        del pX[int(selected_item)]
        data.delete(selected_item)
        o.cla()
        c.cla()
        p.cla()
        o.plot(oxX, oxY)
        c.plot(coX, coY)
        p.plot(pX, pY)
        o.set_ylim([13, 25])
        c.set_ylim([0, 6])
        p.set_ylim([0, 25])
    except IndexError:
        messagebox.showwarning("TYPE ERROR","No data selected")




enterButt = Button(frame1, text="Enter", fg="purple", command=enterClick, padx=20, pady=10)
enterButt.grid(row=6, column=1, pady=10)
enterButt.config(font=('Fixedsys', 10), bg='white')
plotDataButt = Button(frame1, text="Plot Data", fg="purple", command = plotClick, padx=20, pady=10)
plotDataButt.grid(row=6, column=3)
plotDataButt.config(font=('Fixedsys', 10), bg='white')
helpButt = Button(frame1, text="Help", fg="purple", command=helpClick, padx=20, pady=10)
helpButt.grid(row=1, column=5, padx=10, pady=10)
helpButt.config(font=('Fixedsys', 10), bg='white')
deleteButt = Button(frame3, text="Delete", fg="purple", command= deleteClick, padx =10, pady=10)
deleteButt.config(font=('Fixedsys', 10), bg='white')
deleteButt.pack()

root.mainloop()
