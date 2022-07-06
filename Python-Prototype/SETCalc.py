#
# Program that codes for SET Time
#
# Vicki Carrica 2022
#
from math import remainder


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


fitSurv = int(input("Input the number of fit (has use of both arms and can stand upright) survivors in the submarine: "))
unfitSurv = int(input("Input the number of unfit survivors in the submarine: "))
candles = int(input("Input the number of chlorate candles in the submarine: "))
canisters = int(input("Input the number of ExtendAir kits in the submarine: "))
pressure = float(input("Input the pressure (in fsw) in the submarine: "))
flood = int(input("Input the percentage of the submarine compartment that is flooded: "))
temp = float(input("Input the temperature (in F) in the submarine: "))
oConc = float(input("Input the concentration of oxygen (in %SEV) in the submarine: "))
coConc = float(input("Input the concentration of carbon dioxide (in %SEV) in the submarine: "))
oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp)
print("Oxygen survival time:", oSurvTime)
coST = coSurvTime(fitSurv, unfitSurv, canisters, flood, coConc, temp)
print("Carbon dioxide survival time:", coST)
remainingHr = hourBreathing(fitSurv, unfitSurv)
presATA = fswToATA(pressure)
vBreath = calcVBreath(flood, fitSurv, presATA)
finalP = pFinal(flood, presATA, vBreath)
oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr)
print("Oxygen start escape time:", oSET)
coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr)
print("Carbon dioxide start escape time:", coSET)
eabSET = eabStartEscapeTime(fitSurv, unfitSurv, finalP, vBreath, remainingHr)
print("EABs start escape time:", eabSET)
