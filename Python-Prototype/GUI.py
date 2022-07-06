from tkinter import *

root = Tk()

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


fitLabel = Label(root, text="Fit survivors: ")
fitLabel.grid(row=0, column=0)
fitEnter = Entry(root)
fitEnter.grid(row=0, column=1)
unfitLabel = Label(root, text="Unfit survivors: ")
unfitLabel.grid(row=1, column=0)
unfitEnter = Entry(root)
unfitEnter.grid(row=1, column=1)
candLabel = Label(root, text="Chlorate candles: ")
candLabel.grid(row=2, column=0)
candEnter = Entry(root)
candEnter.grid(row=2, column=1)
caniLabel = Label(root, text="ExtendAir kits: ")
caniLabel.grid(row=3, column=0)
caniEnter = Entry(root)
caniEnter.grid(row=3, column=1)
pressLabel = Label(root, text="Pressure (fsw): ")
pressLabel.grid(row=4, column=0)
pressEnter = Entry(root)
pressEnter.grid(row=4, column=1)
floodLabel = Label(root, text="Percent Flooded: ")
floodLabel.grid(row=0, column=2)
floodEnter = Entry(root)
floodEnter.grid(row=0, column=3)
tempLabel = Label(root, text="Temperature: ")
tempLabel.grid(row=1, column=2)
tempEnter = Entry(root)
tempEnter.grid(row=1, column=3)
oxLabel = Label(root, text="Oxygen concentration (%SEV): ")
oxLabel.grid(row=2, column=2)
oxEnter = Entry(root)
oxEnter.grid(row=2, column=3)
coLabel = Label(root, text="Carbon dioxide (%SEV): ")
coLabel.grid(row=3, column=2)
coEnter = Entry(root)
coEnter.grid(row=3, column=3)
eabsCheck = Checkbutton(root)
eabsCheck.grid(row=4, column=3)
eabsLabel = Label(root, text="All have EABs: ")
eabsLabel.grid(row=4, column=2)

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
    oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp)
    oSTLabel = Label(root, text="Oxygen survival time: " + str(oSurvTime)).grid(row=6, column=0)
    coST = coSurvTime(fitSurv, unfitSurv, canisters, flood, coConc, temp)
    coSTLabel = Label(root, text="Carbon dioxide survival time: " + str(coST)).grid(row=7, column=0)
    remainingHr = hourBreathing(fitSurv, unfitSurv)
    presATA = fswToATA(pressure)
    vBreath = calcVBreath(flood, fitSurv, presATA)
    finalP = pFinal(flood, presATA, vBreath)
    oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr)
    oSETLabel = Label(root, text="Oxygen start escape time: " + str(oSET)).grid(row=8, column=0)
    coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr)
    coSETLabel = Label(root, text="Carbon dioxide start escape time: " + str(coSET)).grid(row=9, column=0)
    eabSET = eabStartEscapeTime(fitSurv, unfitSurv, finalP, vBreath, remainingHr)
    eabSETLabel = Label(root, text="EABs start escape time: " + str(eabSET)).grid(row=10, column=0)

enterButt = Button(root, text="Enter", fg="purple", command=enterClick)
enterButt.grid(row=5, column=0)
plotDataButt = Button(root, text="Plot Data", fg="purple")
plotDataButt.grid(row=5, column=2)

root.mainloop()
