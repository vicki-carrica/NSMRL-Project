# Start Escape Time Calculator
## About
This GitHub repository contains the source code that was used to create a Start Escape Time calculator, used to approximate the amount of time sailors have to escape submarines in dissabled submarine (DISSUB) scenarios. This project was developed as a part of a SEAP internship at the Naval Submarine Medical Research Laboratory (NSMRL). 
</br>
### About Us
**Ronan Allison**
</br>
**Ledyard High School, Class of 2023**
</br>
Builder
</br>
Contact: roal1878@gmail.com


**Vicki Carrica**
</br>
**Old Saybrook High School, Class of 2023**
</br>
Programmer
</br>
Contact: vickicarrica@yahoo.com

### The Problem
Start Escape Time (SET) is the latest possible time that sailors on a DISSUB can commence escape. Sailors would rather be rescued than be forced to escape to a method of calculating SET is critical in these cases. Oxygen SET, carbon dioxide SET, and pressure SET can be calculated and the absolute SET is the lowest of the Start Escape Times.
</br>
The current method is the Guard Book, a lengthy book that includes many steps and complicated equations and tables. The Guard Book is prone to human error and does not have high accuracy. This project was designed to better the method of the Guard Book and create a calculation device that has fewer steps, is less prone to human error, and is quicker.
</br>
Previous interns have created physical calculation devices, but they did not encompass all aspects of SET and were still confusing and prone to human error. 

### Our Solution 
To combat the current issues SET calculation, we created an electronic calculation device that takes inputs from sailors of atmospheric data found on the submarine and automatically calculates SET and survival times. It also plots the data and formats them onto a spreadsheet. 

### Prototypes
This repository contains the source code for both the Java and Python prototypes we developed throughout the project. The Python prototype is far more advanced than the Java prototype and is the most updated version of the calculator. Python was chosen over Java because of the ease to develop Graphical User Interface (GUI) while maintaining the accuracy of the math. 

### Files
**GUI.py**
</br>
This file contains all of the code for the Graphical User Interface and the math. 
</br>
**getBattery.py**
</br>
This file contains the code for obtaining the battery percentage and whether the battery is charging. 
</br>
**batteryGUI.py and battery-info.py**
</br>
These files were used to test obtaining battery information and were not used in the actual calculator. 
</br>
**SETCalculator.py**
</br>
This file contains the calculations for survival time, start escape time, and other formulas found on the Guard Book spreadsheet (contact us for a copy) and was integrated into GUI.py so is not needed for the calculator. 
</br>
**Java files**
</br>
These files have the same function as the Python files but are less developed and are written in Java instead. Python files should be used for future development.
</br>
</br>
GUI.py and getBattery.py were the only files that were ultimately used in the application and are the only files that must be downloaded for the application to function. 

## Getting Started

### Installations

*Python 3*
  - Download the latest version of Python at https://www.python.org/downloads/ 
  - Follow instructions on the executable
  - Add Python to an IDE (we used Visual Studio: see instructions at https://code.visualstudio.com/docs/python/python-tutorial)

*Matplotlib*
```
python -m pip install -U pip
python -m pip install -U matplotlib
```
  - For more information, see https://matplotlib.org/stable/users/installing/index.html


*NumPy*
```
pip install numpy
```
  - For more information, see https://numpy.org/install/

### Add GUI.py and getBattery.py to an IDE

We used Visual Studio Code as the Integrated Development Environment (IDE) but any IDE that supports Python 3 should work as well. 
</br>
For VS Code installation instructions, see https://docs.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2022
</br>
Once you have an IDE, download GUI.py and getBattery.py to your computer and open the files using the ctrl + O shortcut

## Usage

Our SET calculator was designed to replace the tables, calculations, and graphs in the current Guard Book. It features an input tab, a graph tab, and a spreadsheet tab as well as a welcome screen.

### Welcome Screen

Upon opening the SET Calculator, you will see a welcome screen that explains the basics of the application as well as prompts users to input time (military time) and the date. The time and date are input so that SET can be displayed as the time and date that escape must commense. There is an 'Enter and Close' button that records the time and date and closes the Welcome Screen. 

### Input Tab

The default tab is the input tab. This tab features inputs for submarine data, a 'Help' button, an 'Enter' button, a 'Plot Data' button, and the battery percentage. 

**Inputs**
</br>
This tab prompts users to enter the number of fit survivors (sailors that have full use of both arms and can stand upright in the escape trunk), the number of unfit survivors, chlorate candles (that release oxygen), ExtendAir kits (that intake carbon dioxide), pressure in fsw, the percentage of the escape trunk flooded, the temperature in Fahrenheit, the concentration of both oxygen and carbon dioxide in %SEV (Surface Equivalence Value), and the number of survivors that have EABs.
</br>
**Help**
</br>
The 'Help' button causes a pop up to display input information explaining what each input means as well as instructions on how to use the application. 
</br>
**Enter**
</br>
The 'Enter' button accepts or rejects the inputs based on a set of parameters (for examples, the number of survivors cannot be negative and percentages cannot exceed 100) and displays the oxygen, carbon dioxide, and pressure SETs as well as the absolute SET as a date and time (for example, 1-1-2022 1:00). 
</br>
**Plot Data**
</br>
The 'Plot Data' button records the pressure, oxygen concentration, and carbon dioxide concentration and adds the value to an array that is displayed on a spreadsheet (on the 'Data' tab) and is plotted on a graph once 2+ data points have been plotted (on the 'Graph' tab)
</br>
**Battery**
</br>
The battery percentage is displayed directly under the 'Help' button as both a number and a slider. The number text turns green when it the battery and plugged in and charging and black otherwise.
</br>

### Graph Tab
