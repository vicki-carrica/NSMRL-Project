# Vicki Carrica and Ronan Allison, Naval Submarine Medical Research Lab, 2022

# This is the python file that creates the Graphic User Interface (GUI) for the SET Calculator, a calculation device that calculates start escape time and visualizes
# Trends in atmospheric data. For more information, refer to the README on the NSMRL-Project Github repository owned by vicki-carrica ().

# Contact: 
# vickicarrica@yahoo.com
# roal1878@gmail.com


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
import numpy as np
matplotlib.use("TkAgg")



#creates a window with a 800 by 480 resolution to match calculator screen resolution: may vary depending on calculator screen size
root = Tk()
root.title('GUI')
root.geometry('800x480')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#styles tkinter ttk attributes with the same font as the rest of the code
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Fixedsys','15'))
s.configure('Treeview', font=('Fixedsys','10'))
s.configure('Treeview.Heading', font=('Fixedsys','15'))

#creates the main notebook for "Input" (main screen where data is entered), "Graph", and "Data" (spreadsheet that tracks inputs) tabs.
notebook = ttk.Notebook(root)
notebook.grid(row=0,column=0)
frame1 = Frame(notebook, width=800, height=480)
frame2 = Frame(notebook, width=800, height=480)
frame3 = Frame(notebook, width=800, height=480)

notebook.add(frame1, text="Input")
notebook.add(frame2, text="Graph")
notebook.add(frame3, text="Data")

#creates the notebook for the "Graph" frame and adds "Oxygen", "Carbon Dioxide", and "Pressure" tabs
book2 = ttk.Notebook(frame2)
book2.grid(row=0, column=0)
oFrame = Frame(book2, width=770, height=430)
coFrame = Frame(book2, width=770, height=430)
pFrame = Frame(book2, width=770, height=430)

book2.add(oFrame, text="Oxygen")
book2.add(coFrame, text="Carbon Dioxide")
book2.add(pFrame, text="Pressure")

#adds a Treeview spreadsheet to frame3 ("Data" tab)
data = ttk.Treeview(frame3)

#The following functions are calculations of survival times, start escape times, and other necessary variables
#A more thorough compilation of formulas, including the units and explanations are on the Guard Book spreadsheet created by Tony Quatroche
#Email vickicarrica@yahoo.com for a reference of this document

def oxSurvTime(fit, unfit, cand, percentFlood, oxConc, temp):
    #This function calculates oxygen survival time based on sailor inputs
    #Survival time is the time left if depth prevents escape
    #Sailors can escape if the depth is less than 600 fsw
    oxygenConcentration = oxConc/100.0
    #converts to temperature from Fahrenheit to Rankine:
    temperature = temp + 459.67
    survivors = fit + unfit
    #62800 is the volume of the compartment- a constant that depends on the submarine but is 62800 on SSN-774 forward compartment:
    volumeCompt = (100-percentFlood)*62800/100 
    candleSCF = cand * 115
    tOCandles = candleSCF/survivors
    numerator = (1.0/.7302)*volumeCompt*(oxygenConcentration-0.13)*(1.0/temperature)
    denominator = (survivors*.0838)/32
    #time until oxygen concentration reaches 13%:
    tOThirteen = numerator/denominator
    OSurvivalTime = tOCandles + tOThirteen
    return OSurvivalTime

def coSurvTime(fit, unfit, cani, percentFlood, coConc, temp):
    #This function calculates carbon dioxide survival time based on sailor inputs
    #Survival time is the time left if depth prevents escape
    #Sailors can escape if the depth is less than 600 fsw
    coConcentration = coConc/100.0
    #converts to temperature from Fahrenheit to Rankine:
    temperature = temp + 459.67
    #62800 is the volume of the compartment- a constant that depends on the submarine but is 62800 on SSN-774 AFT compartment:
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    tLiOH = (cani*73)/survivors
    #Some calculations throughout the code are broken into numerator & denominator calculations to avoid math errors and make it more readable
    numerator = (1/.7302)*volumeCompt*(.06 - coConcentration)*(1/temperature)
    denominator = (survivors * 0.1)/44
    #time until carbon dioxide concentration reaches 6%:
    tCO = numerator/denominator
    coSurvivalTime = tLiOH + tCO
    return coSurvivalTime

def hourBreathing(fit, unfit):
    #This function calculates the number of man-hours of breathing
    #This is for both the fit who are waiting to escape and unfit sailors who will remain
    survivors = fit + unfit
    #w is the number of escape cycles for fit survivors to escape (number of escapers/number of escapers per escape cycle (2)):
    w = fit/2.0
    escapeCycles = round(w) #rounds up if w is a decimal for true escape cycles
    #Hrs of breathing for fit survivors that are escaping:
    escaperHr = escapeCycles*.25*(fit - (2*(escapeCycles + 1)/2)) 
    #Hrs of breathing for unfit survivors that are unable to escape:
    nonEscaperHr = (survivors-fit)*fit/(1/.25 * 2)
    g = escaperHr + nonEscaperHr
    return g

def calcVBreath(percentFlooded, fit, pressure):
    #This function calculates the volume of breathable air in the compartment after flooding
    vCompt = (100-percentFlooded)* pressure* 62800/100
    vBreath = vCompt - 214 - (fit*53.5)
    return vBreath

def fswToATA(pressure):
    #This function converts pressure from fsw (feet sea water) to ATA (atmosphere absolute)
    ata = (pressure+33)/33
    return ata

def oStartEscapeTime(cand, fit, unfit, percentFlood, oConc, volumeBreath, temp, breathingHr):
    #This function calculates the start escape time based on oxygen
    #Start escape time is the amount of time until escapes must begin 
    concInt = oConc/100.0
    #converts to temperature from Fahrenheit to Rankine:
    temperature = temp + 459.67
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    #tCandles is the amount of time added by chlorate candles that release oxygen:
    tCandles = (cand*115.0 - breathingHr)/survivors
    numerator1 = ((concInt*volumeCompt)-(.13*volumeBreath))*(1/.7302)*(1/temperature)
    numerator2 = breathingHr*.0838*(1/32.0)
    numerator = numerator1-numerator2
    denominator = survivors*.0838*(1/32.0)
    oWaitTime = numerator/denominator
    oSET = oWaitTime+tCandles
    return oSET

def coStartEscapeTime(cani, fit, unfit, percentFlood, coConc, volumeBreath, temp, breathingHr):
    #This function calculates the start escape time based on carbon dioxide
    #Start escape time is the amount of time until escapes must begin 
    concInt = coConc/100.0
    #converts to temperature from Fahrenheit to Rankine:
    temperature = temp + 459.67
    volumeCompt = (100-percentFlood)*62800/100
    survivors = fit + unfit
    #tLiOH is the amount of time added by ExtendAir kits that intake carbon dioxide:
    tLiOH = (cani*73)/survivors
    numerator = ((.06*volumeBreath)-(concInt*volumeCompt))*(1/.7302)*(1/temperature)-breathingHr*.1*(1/44.0)
    denominator = survivors*.1*(1.0/44.0)
    coWaitingTime = numerator/denominator
    coSET = coWaitingTime + tLiOH
    return coSET

def eabStartEscapeTime(fit, unfit, pFinal, volumeBreath, breathingHr):
    #This function calculates the start escape time based on pressure
    #Start escape time is the amount of time until escapes must begin 
    survivors = fit + unfit
    numerator = (1.697 - pFinal)*volumeBreath-(breathingHr*20.0)
    denominator = survivors*20.0
    eabStartTime = numerator/denominator
    return eabStartTime

def pFinal(percentFlood, pressure, volumeBreath):
    #This function calculates the final pressure in the submarine after escapes 
    volumeCompt = (100-percentFlood)*62800/100
    airAddedByEscapes = 8*pressure*(144+3.33)
    pFinal = ((volumeCompt)*pressure+airAddedByEscapes)/volumeBreath
    return pFinal

def plotGraphs(oxX, oxY, coX, coY, pX, pY):
    global o
    global c
    global p
    #Gets the slope and intercept of the line of best fit
    oa, ob = np.polyfit(oxX, oxY, 1)
    print(oa)
    
    #Creates new arrays to plot the line of best fit
    newoY = []
    newoX = []

    #clears previous plot
    o.cla()

    x = 0

    #Creates loop to find the time to reach critical levels 
    while True:
        newy = oa*x + ob
        roundeda = math.ceil(oa*1000)
        print("OXYGEN- x: " + str(x) + ", roundeda: " + str(roundeda) + ", newy: " + str(newy))
        #Checks if the line will not reach critical level with slope (i.e. positive slope when level is more negative)
        if ((roundeda>=0) and (x>100)):
            print("breaking")
            break
        #When graph reaches critical point, break from the loop
        elif (newy<13):
            newoX.append(x)
            newoY.append(newy)
            #Adds label to time where level is reached
            setox = (13-ob)/oa #x coordinate where critical level is reached
            setoxtext="Time:\n" + str(math.floor(setox))
            o.scatter(setox, 13, color='red')
            o.text(setox, 13, setoxtext, ha='right', va='top', fontname="Serif")
            break
        newoX.append(x)
        newoY.append(newy)
        x=x+1

    #Scatters points of actual data 
    o.scatter(oxX, oxY, color='darkblue')
    #Plots line of best fit 
    o.plot(newoX, newoY)
    o.set_ylim([11, 25])
    #Adds titles
    o.set_title("Oxygen Readings", fontname="Serif")
    o.set_xlabel("Time (seconds)", fontname="Serif")
    o.set_ylabel("Oxygen Concentration (%SEV)", fontname="Serif")

    #Creates line of best fit for carbon dioxide with same process as oxygen
    coa, cob = np.polyfit(coX, coY, 1)
    newcoY = []
    newcoX = []

    #clears previous plot
    c.cla()

    x = 0

    #Creates loop to find the time to reach critical levels 
    while True:
        newy = coa*x + cob
        roundeda = math.ceil(coa*1000)-1
        print("CO2- x: " + str(x) + ", roundeda: " + str(roundeda) + ", newy: " + str(newy) + ", coa: " + str(coa))
        #Checks if the line will not reach critical level with slope (i.e. positive slope when level is more negative)
        if ((roundeda<=0) and (x>100)):
            break
        #When graph reaches critical point, break from the loop
        elif (newy>6):
            newcoX.append(x)
            newcoY.append(newy)
            #Adds label to time where level is reached
            setcox = (6-cob)/coa #x coordinate where critical level is reached
            setcoxtext="Time:\n" + str(math.floor(setcox))
            c.scatter(setcox, 6, color='red')
            c.text(setcox, 6, setcoxtext, ha='left', va='top', fontname="Serif")
            break
        newcoX.append(x)
        newcoY.append(newy)
        x=x+1

    c.scatter(coX, coY, color='darkblue')
    c.plot(newcoX, newcoY)
    c.set_ylim([0, 7])
    c.set_title("Carbon Dioxide Readings", fontname="Serif")
    c.set_xlabel("Time (seconds)", fontname="Serif")
    c.set_ylabel("Carbon Dioxide Concentration (%SEV)", fontname="Serif")


    #Creates line of best fit for pressure with same process as oxygen
    pa, pb = np.polyfit(pX, pY, 1)
    newpY = []
    newpX = []

    #clears previous plot
    p.cla()

    x = 0

    #Creates loop to find the time to reach critical levels 
    while True:
        newy = pa*x + pb
        roundeda = math.ceil(pa*1000)
        print("PRESSURE- x: " + str(x) + ", roundeda: " + str(roundeda) + ", newy: " + str(newy))
        #Checks if the line will not reach critical level with slope (i.e. positive slope when level is more negative)
        if ((roundeda<=0) and (x>100)):
            break
        #When graph reaches critical point, break from the loop
        elif (newy>23):
            newpX.append(x)
            newpY.append(newy)
            #Adds label to time where level is reached
            setpx = (23-pb)/pa #x coordinate where critical level is reached
            setpxtext="Time:\n" + str(math.floor(setpx))
            p.scatter(setpx, 23, color='red')
            p.text(setpx, 23, setpxtext, ha='left', va='top', fontname="Serif")
            break
        newpX.append(x)
        newpY.append(newy)
        x=x+1
        
    p.scatter(pX, pY, color='darkblue')
    p.plot(newpX, newpY)
    p.set_ylim([0, 25])
    p.set_title("Pressure Readings", fontname="Serif")
    p.set_xlabel("Time (seconds)", fontname="Serif")
    p.set_ylabel("Pressure (fsw)", fontname="Serif")

    #Plots the x (time) and y (data) arrays with points at the data points (o marker) and a dark blue curve color
    o.scatter(oxX, oxY, color='darkblue')
    c.scatter(coX, coY, color='darkblue')
    p.scatter(pX, pY, color='darkblue')


#Declaration of arrays (x and y coordinates for the oxygen, carbon dioxide, and pressure graphs)
oxY = []
oxX = []
coY = []
coX = []
pY = []
pX = []

#Declaration of the start time as the current time (for the x axis of the graphs)
start = time.time()

#counter variables to count the number of times buttons are pressed
counter = 0
count = 0
undoCount = -1

#variables that store the value of previous data points when delete is hit (to be able to undo the action)
storeT = []
storeO = []
storeCO = []
storeP = []
storeIndex = []

#Variables for battery
HOST = "127.0.0.1"
PORT = 8423



#Label and enter box for the variables on the input frame

#Fit survivors:
fitLabel = Label(frame1, text="Fit survivors: ")
fitLabel.grid(row=1, column=0)
fitLabel.config(font=('Fixedsys',15))
fitEnter = Entry(frame1, width=10)
fitEnter.grid(row=1, column=1, ipady=10, pady=3)
fitEnter.config(font=('Fixedsys', 10))

#Unfit survivors:
unfitLabel = Label(frame1, text="Unfit survivors: ")
unfitLabel.grid(row=2, column=0)
unfitLabel.config(font=('Fixedsys', 15))
unfitEnter = Entry(frame1, width=10)
unfitEnter.grid(row=2, column=1, ipady=10, pady=3)
unfitEnter.config(font=('Fixedsys', 10))

#Chlorate candles:
candLabel = Label(frame1, text="Chlorate candles: ")
candLabel.grid(row=3, column=0)
candLabel.config(font=('Fixedsys', 15))
candEnter = Entry(frame1, width=10)
candEnter.grid(row=3, column=1, ipady=10, pady=3)
candEnter.config(font=('Fixedsys', 10))

#ExtendAir kits (canisters):
caniLabel = Label(frame1, text="ExtendAir kits: ")
caniLabel.grid(row=4, column=0)
caniLabel.config(font=('Fixedsys', 15))
caniEnter = Entry(frame1, width=10)
caniEnter.grid(row=4, column=1, ipady=10, pady=3)
caniEnter.config(font=('Fixedsys', 10))

#Pressure:
pressLabel = Label(frame1, text="Pressure (fsw): ")
pressLabel.grid(row=5, column=0)
pressLabel.config(font=('Fixedsys', 15))
pressEnter = Entry(frame1, width=10)
pressEnter.grid(row=5, column=1, ipady=10, pady=3)
pressEnter.config(font=('Fixedsys', 10))

#Percent flooded:
floodLabel = Label(frame1, text="Percent Flooded: ")
floodLabel.grid(row=1, column=2)
floodLabel.config(font=('Fixedsys', 15))
floodEnter = Entry(frame1, width=10)
floodEnter.grid(row=1, column=3, ipady=10, pady=3)
floodEnter.config(font=('Fixedsys', 10))

#Temperature:
tempLabel = Label(frame1, text="Temperature: ")
tempLabel.grid(row=2, column=2)
tempLabel.config(font=('Fixedsys', 15))
tempEnter = Entry(frame1, width=10)
tempEnter.grid(row=2, column=3, ipady=10, pady=3)
tempEnter.config(font=('Fixedsys', 10))

#Oxygen concentration:
oxLabel = Label(frame1, text="Oxygen (%SEV): ")
oxLabel.grid(row=3, column=2)
oxLabel.config(font=('Fixedsys', 15))
oxEnter = Entry(frame1, width=10)
oxEnter.grid(row=3, column=3, ipady=10, pady=3)
oxEnter.config(font=('Fixedsys', 10))

#Carbon dioxide concentration:
coLabel = Label(frame1, text="Carbon dioxide (%SEV): ")
coLabel.grid(row=4, column=2)
coLabel.config(font=('Fixedsys', 15))
coEnter = Entry(frame1, width=10)
coEnter.grid(row=4, column=3, ipady=10, pady=3)
coEnter.config(font=('Fixedsys', 10))

#EABs:
eabsEnter = Entry(frame1, width=10)
eabsEnter.grid(row=5, column=3, ipady=10, pady=3)
eabsEnter.config(font=('Fixedsys', 10))
eabsLabel = Label(frame1, text="Survivors with EABs: ")
eabsLabel.grid(row=5, column=2)
eabsLabel.config(font=('Fixedsys', 15))

#Label that displays oxygen survival time 
oSTLabel = Label(frame1, text=" ")
oSTLabel.grid(row=7, column=0, columnspan=2)
oSTLabel.config(font=('Fixedsys', 12))

#Label that displays carbon dioxide survival time
coSTLabel = Label(frame1, text=" ")
coSTLabel.config(font=('Fixedsys', 12))
coSTLabel.grid(row=8, column=0, columnspan=2)

#Label that displays oxygen start escape time
oSETLabel = Label(frame1, text=" ")
oSETLabel.grid(row=9, column=0, columnspan=2)
oSETLabel.config(font=('Fixedsys', 12))

#Label that displays carbon dioxide start escape time
coSETLabel = Label(frame1, text=" ")
coSETLabel.grid(row=7, column=2, columnspan=2)
coSETLabel.config(font=('Fixedsys', 12))

#Label that displays pressure start escape time
eabSETLabel = Label(frame1, text=" ")
eabSETLabel.grid(row=8, column=2, columnspan=2, pady=10)
eabSETLabel.config(font=('Fixedsys', 12))

#Creates figures to place graphs on
fO = Figure(figsize=(9,4.5), dpi=80) 
fCO = Figure(figsize=(9,4.5), dpi=80) 
fP = Figure(figsize=(9,4.5), dpi=80)

#Adds oxygen plot to the figure with graph titles and y limits to match the Guard Book's axis labels (13%-25%)
o = fO.add_subplot(111)
o.set_ylim([13, 25])
o.set_title("Oxygen Readings", fontname="Serif")
o.set_xlabel("Time (seconds)", fontname="Serif")
o.set_ylabel("Oxygen Concentration (%SEV)", fontname="Serif")

#Adds carbon dioxide plot to the figure with graph titles and y limits to match the Guard Book's axis labels (0%-6%)
c = fCO.add_subplot(111)
c.set_ylim([0, 6])
c.set_title("Carbon Dioxide Readings", fontname="Serif")
c.set_xlabel("Time (seconds)", fontname="Serif")
c.set_ylabel("Carbon Dioxide Concentration (%SEV)", fontname="Serif")

#Adds pressure plot to the figure with graph titles and y limits to match the Guard Book's axis labels (0%-25%)
p = fP.add_subplot(111)
p.set_ylim([0, 25])
p.set_title("Pressure Readings", fontname="Serif")
p.set_xlabel("Time (seconds)", fontname="Serif")
p.set_ylabel("Pressure (fsw)", fontname="Serif")


#Adds the oxygen figure and frame to a canvas and a toolbar to the graph
canvas = FigureCanvasTkAgg(fO, oFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, oFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

#Adds the carbon dioxide figure and frame to a canvas and a toolbar to the graph
canvas = FigureCanvasTkAgg(fCO, coFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, coFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

#Adds the pressure figure and frame to a canvas and a toolbar to the graph
canvas = FigureCanvasTkAgg(fP, pFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, pFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH)

#Adds column titles to the spreadsheet (Treeview)
data['columns'] = ("Time", "Oxygen %SEV", "Carbon Dioxide %SEV", "Pressure FSW")

data.column("#0", width=0, stretch=NO) #Sets column "0" (automatic column) to have no width- essentially deletes the column

#Configures the columns:
data.column("Time", anchor=W, width=25, minwidth=10)
data.column("Oxygen %SEV", anchor=W, width=50, minwidth=25)
data.column("Carbon Dioxide %SEV", anchor=W, width=100, minwidth=50)
data.column("Pressure FSW", anchor=W, width=50, minwidth=25)

#Configures the headings:
data.heading("Time", text="Time (s)", anchor=W)
data.heading("Oxygen %SEV", text="Oxygen (%SEV)", anchor=W)
data.heading("Carbon Dioxide %SEV", text="Carbon Dioxide (%SEV)", anchor=W)
data.heading("Pressure FSW", text="Pressure (FSW)", anchor=W)

#Adds the spreadsheet onto the frame
data.grid(column=0, row=0, ipadx=250, ipady=75, columnspan=2)

def enterClick():
    #This function collects the data from the enter boxes and displays the calculated survival times/start escape times

    #Attemps to collect the numbers from each of the enter boxes. 
    try:
        #Declares the inputs as variables and casts them as ints/floats for calculations
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

        oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp) #stores the oxygen survival time
        #Converts hours (decimal) to days (whole number) and hours (whole number) 
        oSTDay = math.floor(oSurvTime/24)
        oSTHr = math.floor(oSurvTime-24*oSTDay)
        
        coST = coSurvTime(fitSurv, unfitSurv, canisters, flood, coConc, temp) #stores the carbon dioxide survival time
        #Converts hours (decimal) to days (whole number) and hours (whole number) 
        coSTDay = math.floor(coST/24)
        coSTHr = math.floor(coST-24*coSTDay)

        remainingHr = hourBreathing(fitSurv, unfitSurv) #stores the remaining man-hours 

        presATA = fswToATA(pressure) #stores the pressure in ATA

        vBreath = calcVBreath(flood, fitSurv, presATA) #stores the volume of breathable air

        finalP = pFinal(flood, presATA, vBreath) #stores final pressure

        oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr) #stores oxygen start escape time
        #Converts hours (decimal) to days (whole number) and hours (whole number) 
        oSETDay = math.floor(oSET/24)
        oSETHr = math.floor(oSET-24*oSETDay)

        coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr) #stores carbon dioxide start escape time
        #Converts hours (decimal) to days (whole number) and hours (whole number) 
        coSETDay = math.floor(coSET/24)
        coSETHr = math.floor(coSET-24*coSETDay)

        #Displays the survival/start escape times onto the labels 
        oSTLabel.config(text="Oxygen survival time:\n " + str(oSTDay) + " day " + str(oSTHr) + " hr")
        coSTLabel.config(text="Carbon dioxide survival time:\n " + str(coSTDay) + " day " + str(coSTHr) + " hr")
        oSETLabel.config(text="Oxygen start escape time:\n " + str(oSETDay) + " day " + str(oSETHr) + " hr")
        coSETLabel.config(text="Carbon dioxide start escape time:\n " + str(coSETDay) + " day " + str(coSETHr) + " hr")


        #Checks if all survivors are wearing EABs. If not, the pressure start escape time is not calculated 
        if eabs==(fitSurv+unfitSurv):
            eabSET = eabStartEscapeTime(fitSurv, unfitSurv, finalP, vBreath, remainingHr) #stores eab start escape time
            #Converts hours (decimal) to days (whole number) and hours (whole number)
            eabSETDay = math.floor(eabSET/24)
            eabSETHr = math.floor(eabSET-24*eabSETDay)

            #Displays the start escape times onto the label 
            eabSETLabel.config(text="EABs start escape time:\n " + str(eabSETDay) + " day " + str(eabSETHr) + " hr")
        else:
            eabSET="NA"
            eabSETLabel.config(eabSETLabel.config(text="EABs start escape time:\n N/A"))
    #If any of the boxes have invalid inputs (blank or inconsistent with casting), a ValueError will be catched and a warning box will pop up
    except ValueError:
        messagebox.showwarning("VALUE ERROR","Invalid Inputs\n\nPlease do not leave blank boxes.")
    

def helpClick():
    #This function creates a popup "Help" window when the "Help" button is clicked 

    #Declares a new window 
    helpWindow = Toplevel(root)
    helpWindow.title("Help")
    helpWindow.geometry("750x430")

    #Creates tabs on the "Help" window ("Input Information" and "Instructions")
    helpTab = ttk.Notebook(helpWindow)
    helpTab.grid(row=0,column=0)
    h1 = Frame(helpTab, width=800, height=480)
    h2 = Frame(helpTab, width=800, height=480)
    helpTab.add(h1, text="Input Information")
    helpTab.add(h2, text="Instructions")

    #Information about fit survivors:
    fitLabel = Label(h1, text="Fit survivors:", anchor=W)
    fitLabel.grid(row=0, column=0)
    fitLabel.config(font=('Fixedsys', 15))
    fitInfo = Label(h1, text="Sailors that have full use of both arms and can stand upright in a flooding escape trunk")
    fitInfo.grid(row=1, column=0)
    fitInfo.config(font=('Fixedsys', 10))

    #Information about unfit survivors:
    unfitLabel = Label(h1, text="Unfit survivors:", anchor=W)
    unfitLabel.grid(row=2, column=0)
    unfitLabel.config(font=('Fixedsys', 15))
    unfitInfo = Label(h1, text="Sailors that are unable to escape but still intake oxygen and exhale carbon dioxide")
    unfitInfo.grid(row=3, column=0)
    unfitInfo.config(font=('Fixedsys', 10))

    #Information about chlorate candles:
    candleLabel = Label(h1, text="Chlorate candles:", anchor=W)
    candleLabel.grid(row=4, column=0)
    candleLabel.config(font=('Fixedsys', 15))
    candleInfo = Label(h1, text="Candles that release oxygen into the atmosphere")
    candleInfo.grid(row=5, column=0)
    candleInfo.config(font=('Fixedsys', 10))

    #Information about ExtendAir kits:
    extendAirLabel = Label(h1, text="ExtendAir Kits:", anchor=W)
    extendAirLabel.grid(row=6, column=0)
    extendAirLabel.config(font=('Fixedsys', 15))
    extendAirInfo = Label(h1, text="Intake carbon dioxide from the atmosphere through a reaction with lithium hydroxide")
    extendAirInfo.grid(row=7, column=0)
    extendAirInfo.config(font=('Fixedsys', 10))

    #Information about pressure:
    pressureLabel = Label(h1, text="Pressure:", anchor=W)
    pressureLabel.grid(row=8, column=0)
    pressureLabel.config(font=('Fixedsys', 15))
    pressureInfo = Label(h1, text="Measurement (in FSW) found on submarine")
    pressureInfo.grid(row=9, column=0)
    pressureInfo.config(font=('Fixedsys', 10))

    #Information about percentage flooded:
    floodLabel = Label(h1, text="Percent Flooded:", anchor=W)
    floodLabel.grid(row=8, column=0)
    floodLabel.config(font=('Fixedsys', 15))
    floodInfo = Label(h1, text="Percentage of the compartment that is flooded, measurement found on submarine")
    floodInfo.grid(row=9, column=0)
    floodInfo.config(font=('Fixedsys', 10))

    #Information about temperature:
    tempLabel = Label(h1, text="Temperature:", anchor=W)
    tempLabel.grid(row=10, column=0)
    tempLabel.config(font=('Fixedsys', 15))
    tempInfo = Label(h1, text="Measurement (in Fahrenheit) found on submarine")
    tempInfo.grid(row=11, column=0)
    tempInfo.config(font=('Fixedsys', 10))

    #Information about oxygen/carbon dioxide concentrations:
    concLabel = Label(h1, text="Oxygen and Carbon Dioxide Concentration:", anchor=W)
    concLabel.grid(row=12, column=0)
    concLabel.config(font=('Fixedsys', 15))
    concInfo = Label(h1, text="Measurements (in %SEV) found on submarine")
    concInfo.grid(row=13, column=0)
    concInfo.config(font=('Fixedsys', 10))

    #Information about EABs:
    eabLabel = Label(h1, text="Survivors with EABs:", anchor=W)
    eabLabel.grid(row=14, column=0)
    eabLabel.config(font=('Fixedsys', 15))
    eabInfo = Label(h1, text="Number of sailors who are wearing EABs")
    eabInfo.grid(row=15, column=0)
    eabInfo.config(font=('Fixedsys', 10))

    #Instructions (on the second tab):
    instructionLabel = Label(h2, text="Instructions:")
    instructionLabel.grid(row=0, column=0)
    instructionLabel.config(font=('Fixedsys', 20))
    #String that contains instructions:
    instr = "1) Input atmospheric data found on the submarine in the corresponding slots.\n\n2a) Press 'Enter' to calculate the Start Escape Time (SET).\n2b) Press 'Plot Data' to record and graph the atmospheric data.\n\n3) Click the 'Data' tab to view the plotted data.\n   - Click 'Delete' to delete a plotted data point\n   - Click 'Undo' to undo a deletion\n\n4) Plot data periodically (about every 30 minutes unless data changes dramatically)\n\n5) Once there are 2+ plotted data points, click the 'Graph' tab to view atmospheric\n trends and predicted SET.\n   -To update the graph after a change, click the move button (fourth from the right\n on the toolbar) and change the view.\n   - Click the home button (first from the right) to return to the default view.\n\n6) Repeat these steps periodically to have the most accurate and updated SET."
    instructions = Label(h2, text=instr)
    instructions.grid(row=1, column=0, sticky='w')
    instructions.config(font=('Fixedsys', 10))


def plotClick():
    #This functions stores the data in the enter boxes, graphs it, and adds it to the spreadsheet when the "Plot Data" button is clicked

    #counter serves as a way to track the amount of times the button is clicked. On the first click, the start time should begin
    global counter
    global start
    counter=counter+1
    if counter==1:
        start = time.time()
    
    #Adds the data in the enter boxes to the array of Y values
    oxY.append(float(oxEnter.get()))
    coY.append(float(coEnter.get()))
    pY.append(float(pressEnter.get()))

    #sets the time (for the X value) to the current time subtracted by the start time (set on the first click)
    current = time.time()
    t = current - start

    #adds the time (in seconds) to the array of X values
    oxX.append(t)
    coX.append(t)
    pX.append(t)

    #Creates the line of best fit 
    #Will plot the line of best fit only if there is more than one point
    if (counter > 1):
        plotGraphs(oxX, oxY, coX, coY, pX, pY)

    #rounds down the seconds to a whole number:
    ti = math.floor(t)

    #inserts the data point into the spreadsheet
    data.insert(parent='', index='end', iid=(counter-1), values=(ti, oxEnter.get(), coEnter.get(), pressEnter.get()))

def deleteClick():
    #This function deletes the plotted data points from the spreadsheet and the graph 

    #This counter is used to account for the difference in index after item(s) are deleted 
    global count
    global storeIndex
    global storeO
    global storeCO
    global storeP
    global storeT
    global counter
    global undoButt
    global undoCount
    try:
        #returns the integer of the selected row in the Treeview
        selected_item = int(data.selection()[0])-count
        print(selected_item)

        #Stores the value from the deletion 
        storeO.append(oxY[int(selected_item)])
        storeCO.append(coY[int(selected_item)])
        storeP.append(pY[int(selected_item)])
        storeT.append(oxX[int(selected_item)])
        storeIndex.append(selected_item)

        #Deletes index from x and y arrays
        del oxY[int(selected_item)]
        del coY[int(selected_item)]
        del pY[int(selected_item)]
        del oxX[int(selected_item)]
        del coX[int(selected_item)]
        del pX[int(selected_item)]
        print(oxY)

        #Deletes the selected row from the Treeview spreadsheet
        data.delete((selected_item+count))

        if (counter > 1):
            plotGraphs(oxX, oxY, coX, coY, pX, pY)

        #Changes the colors of the undo button so that it activates after a row has been deleted
        undoButt.config(bg="white", fg="purple")

        count = count+1
        undoCount = undoCount+1

    #Checks for no selected row and displays a warning message in that case
    except IndexError:
        messagebox.showwarning("INDEX ERROR","No data selected")

def undoClick():
    #This function undos a deletion on the spreadsheet and graph 
    global storeIndex
    global storeO
    global storeCO
    global storeP
    global storeT
    global count
    global undoCount
    global undoButt
    #Ensures that there is something to undo 
    try:
        
        #Print statements serve for debugging 
        print("hi this is count", count)
        ind = storeIndex[undoCount]
        print("index: ", ind)
        print("time: ", storeT[undoCount])
        print("oxygen: ", storeO[undoCount])
        print("carbon dioxide: ", storeCO[undoCount])
        print("pressure: ", storeP[undoCount])
        
        tr = math.floor(storeT[undoCount]) #Time rounded

        #Inserts stored values back into the spreadsheet
        data.insert(parent='', index=ind, iid=(ind), values=(tr, storeO[undoCount], storeCO[undoCount], storeP[undoCount]))

        #Inserts the stored values into the graphed x and y arrays
        oxY.insert(ind, storeO[undoCount])
        coY.insert(ind, storeCO[undoCount])
        pY.insert(ind, storeP[undoCount])
        oxX.insert(ind, storeT[undoCount])
        coX.insert(ind, storeT[undoCount])
        pX.insert(ind, storeT[undoCount])

        #Deletes the values from the stored values after they are added back into the arrays and spreadsheet
        del storeT[undoCount]
        del storeO[undoCount]
        del storeCO[undoCount]
        del storeP[undoCount]
        del storeIndex[undoCount]

        #clears previous plots
        o.cla()
        c.cla()
        p.cla()

        #plots the graphs with the modified arrays
        if (counter > 1):
            plotGraphs(oxX, oxY, coX, coY, pX, pY)

        #Modifies counters to take into account the addition of the value into the graph/spreadsheet
        undoCount=undoCount-1
        count = count-1

        #Sets the color back to grey if no more values can be undoed
        if undoCount<0:
            undoButt.config(bg='lightgrey', fg="darkgrey")
    except IndexError:
        messagebox.showwarning("INDEX ERROR","Cannot Undo")



#Declares "Enter" button
enterButt = Button(frame1, text="Enter", fg="purple", command=enterClick, padx=20, pady=10)
enterButt.grid(row=6, column=1, pady=10)
enterButt.config(font=('Fixedsys', 10), bg='white')

#Declares "Plot Data" button
plotDataButt = Button(frame1, text="Plot Data", fg="purple", command = plotClick, padx=20, pady=10)
plotDataButt.grid(row=6, column=3)
plotDataButt.config(font=('Fixedsys', 10), bg='white')

#Declares "Help" button
helpButt = Button(frame1, text="Help", fg="purple", command=helpClick, padx=20, pady=10)
helpButt.grid(row=1, column=5, padx=10, pady=10)
helpButt.config(font=('Fixedsys', 10), bg='white')

#Declares "Delete" button
deleteButt = Button(frame3, text="Delete", fg="purple", command= deleteClick, padx =10, pady=10)
deleteButt.config(font=('Fixedsys', 10), bg='white')
deleteButt.grid(column=1, row=1)

#Declares "Undo" button
undoButt = Button(frame3, text="Undo", fg='darkgrey', command=undoClick, padx=10, pady=10)
undoButt.config(font=('Fixedsys', 10), bg='lightgrey')
undoButt.grid(column=0, row=1)


root.mainloop()
