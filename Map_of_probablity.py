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

def AttractionForce(q, q_k):
    return k_p * CalculateDistance(q, q_k) #zwraca sile przyciagania punktu przez punkt koncowy


def RepulsionForceFromObstacle(q, q_oi):
    #zwraca siłę odpychania od pojedynczej przeszkody
    d_i = CalculateDistance(q, q_oi)                    #odległość od przeszkody
    if (d_i < 0.01):                                    #sytuacja punktu w przeszkodzie
        return F_rep_MaxValue
    if (d_i < d_0):                                     #punkt w polu wpływu przeszkody
        F_oi = k_o* (1/d_i - 1/d_0)/ d_i ** 2           #bazując na prawie Coulomba
        if (F_oi > F_rep_MaxValue):                     #wyliczona siła nie przekroczy zadanego maksa
            return F_rep_MaxValue
    else:                                               #punkt poza polem wpływu przeszkody
        F_oi = 0
    return F_oi


def RepulsionForcesInAPoint(q, ObstVector):
    #zwraca siłę odpychania punktu przez wszystkie przeszkody
    F_rep = 0
    for q_oi in ObstVector:
        F_rep += RepulsionForceFromObstacle(q, q_oi)  #sumujemy siły odpychania dla każdej przeszkody
    return F_rep


def ForcesInAPoint(WhichForce, q, q_k, ObstVector):
    return {
        'N': AttractionForce(q, q_k) + RepulsionForcesInAPoint(q, ObstVector), #net force, czyli siła wypadkowa
        'A': AttractionForce(q, q_k),                                          #siła przyciągania
        'R': RepulsionForcesInAPoint(q, ObstVector)                            #siła odpychania
    }[WhichForce]


def ForceVectorComponents(q, SceneObject, isElementObstacle):

    if isElementObstacle:
        LocalObstacle = (SceneObject[0] - q[0], SceneObject[1] - q[1])
        if LocalObstacle[0] != 0:  # funkcja liniowa
            a1 = LocalObstacle[1] / LocalObstacle[0]  # wspolczynnik funkcji y = a1*x
            ForceSquared = RepulsionForceFromObstacle(q, SceneObject) ** 2
            X_Distance = np.sqrt(ForceSquared / (a1 ** 2 + 1))
            if LocalObstacle[0] < 0:  # na lewo od q
                X_force = X_Distance
            else:  # na prawo od q
                X_force = -X_Distance
            Y_force = a1 * X_force
        else:  # wyjątek x = 0
            X_force = 0
            Y_force = -RepulsionForceFromObstacle(q, SceneObject)

    else:  # nie przeszkoda, czyli meta
        LocalFinish = (SceneObject[0] - q[0], SceneObject[1] - q[1])
        if LocalFinish[0] != 0:  #funkcja liniowa
            a1 = LocalFinish[1] / LocalFinish[0]  # wspolczynnik funkcji y = a1*x
            ForceSquared = AttractionForce(q, SceneObject) ** 2
            X_Distance = np.sqrt(ForceSquared / (a1 ** 2 + 1))
            if LocalFinish[0] < 0:  # na lewo od q
                X_force = - X_Distance
            else:  # na prawo od q
                X_force = X_Distance
            Y_force = a1 * X_force
        else:  # wyjątek x = 0
            X_force = 0
            Y_force = AttractionForce(q, SceneObject)

    return (X_force, Y_force)


def ResultantForceComponents(ListOfVectors):
    #sumuje wektory w jeden
    X_sum = Y_sum = 0
    for SingleVector in ListOfVectors:
        X_sum += SingleVector[0]
        Y_sum += SingleVector[1]
    return (X_sum, Y_sum)


def ValueInRange(Min, Value, Max):
    #czy wartosc zawiera sie w zadanym przedziale (wlacznie z gornym ograniczeniem)
    if Min < Value and Value <= Max:
        return True
    else:
        return False
