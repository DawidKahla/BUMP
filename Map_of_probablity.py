import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

##### Zmienne globalne #####
x_size = y_size = 10    #rozmiar sceny

delta = 0.01        #odległośc między kolejnymi punktami pojedynczej drogi
NoOfObstacles = 7   #liczba przeszkód

k_p = 5  # wpolczynnik sily przyciagania mety
k_o = 100  # wspolczynnik sily odpychajacej od przeszkod
d_0 = 5  # promien przeszkod

iterations = 100 #liczba generowanych pojedynczych drog

F_rep_MaxValue = 4 * k_p * 10 * np.sqrt(2) #ogarniczona sila odpychania przez przeszkode, by nie osiagala astronomicznych wartosci, bo zasadniczo dazy do nieskonczonosci

PathLength = 15000  #maksymalna liczba punktow w pojedynczej drodze

# do wyswietlania kolorowego
DisplayForce = "N"  # przyciaganie(attraction) "A"; odpychanie(repulsion) "R"; wypadkowa(net) "N"

##### Funkcje #####

Accuracy = int(np.log10(1 / delta))  # do funkcji ReturnRounded


def ReturnRounded(SingleCoord):
    return round(SingleCoord, Accuracy) #zaokrągla koordy na podstawie delty


def RandomCoordinate():
    return ReturnRounded(np.random.uniform(-x_size, x_size)) #generuje odpowiednio zokrąglony losowy koord


def CalculateDistance(q1, q2):
    return np.sqrt((q1[0] - q2[0]) ** 2 + (q1[1] - q2[1]) ** 2) #liczy dystans między dwoma punktami na płaszczyźnie
