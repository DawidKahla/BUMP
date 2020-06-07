import numpy as np
import matplotlib.pyplot as plt

##### Funkcje #####

Accuracy = int(np.log10(1 / delta))  # do funkcji ReturnRounded

def ReturnRounded(SingleCoord):
    return round(SingleCoord, Accuracy) #zaokrągla koordy na podstawie delty

def RandomCoordinate_x():
    return ReturnRounded(np.random.uniform(x_start, x_end)) #generuje odpowiednio zokrąglony losowy koord

def RandomCoordinate_y():
    return ReturnRounded(np.random.uniform(y_start, y_end))

def CalculateDistance(q1, q2):
    return np.sqrt((q1[0] - q2[0]) ** 2 + (q1[1] - q2[1]) ** 2) #liczy dystans między dwoma punktami na płaszczyźnie

def CalculatePathsPoints(x_func):
    y_func=a*x_func+b
    return (x_func, y_func) #liczy punkty znajdujace sie na prostej opisujacej sciezke

def ValueInRange(Min, Value, Max):
    if Min <= Value and Value <= Max:
        return True
    else:
        return False
