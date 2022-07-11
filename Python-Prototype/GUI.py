import math
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
matplotlib.use("TkAgg")

root = Tk()
root.title('GUI')
root.geometry('800x480')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

s = ttk.Style()
s.configure('TNotebook.Tab', font=('Fixedsys','15'))

notebook = ttk.Notebook(root)
notebook.grid(row=0,column=0)
frame1 = Frame(notebook, width=800, height=800)
frame2 = Frame(notebook, width=800, height=480)

notebook.add(frame1, text="Data")
notebook.add(frame2, text="Graph")


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

def enterClick():
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

def helpClick():
    message = "Intructions: \n Input the data on the submarine compartment.\n Fit survivors: sailors who have full use of both arms and can stand upright in the flooding escape trunk.\n Unfit survivors: sailors who are unable to complete the task but are still breathing.\n Chlorate candles: release oxygen into the atmosphere.\n ExtendAir kits: intake carbon dioxide from the atmosphere.\n "
    messagebox.showinfo("Help", message)

enterButt = Button(frame1, text="Enter", fg="purple", command=enterClick, padx=20, pady=10)
enterButt.grid(row=6, column=1, pady=10)
enterButt.config(font=('Fixedsys', 10), bg='white')
plotDataButt = Button(frame1, text="Plot Data", fg="purple", padx=20, pady=10)
plotDataButt.grid(row=6, column=3)
plotDataButt.config(font=('Fixedsys', 10), bg='white')
helpButt = Button(frame1, text="Help", fg="purple", command=helpClick, padx=20, pady=10)
helpButt.grid(row=1, column=5, padx=10, pady=10)
helpButt.config(font=('Fixedsys', 10), bg='white')

f = Figure(figsize=(2,2), dpi=70) 
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8])

canvas = FigureCanvasTkAgg(f, frame2)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, frame2)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

root.mainloop()
