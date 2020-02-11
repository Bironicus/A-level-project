from tkinter import *
import time
import math

### constants

canvas_width = 680
canvas_height = 700



### input values

mass = 3 #mass in kilogrammes
springConstant = 2 #spring constant in meters
intDispla = 2 #initial displacement

pi = math.pi



### calculated values

timePeriod = (2 * pi) * math.sqrt(springConstant / mass)
frequency = 1 / timePeriod
angularVel = (2 * pi) * frequency

tStat = timePeriod/100
