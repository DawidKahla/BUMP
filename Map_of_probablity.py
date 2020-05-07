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

def AssingCell(ResultantForce):
    ForceAngle = np.arctan2(ResultantForce[1], ResultantForce[0])
    ForceAngle = ForceAngle / np.pi  # dla uproszczenia
    if ValueInRange(-1 / 8, ForceAngle, 1 / 8):
        return (delta, 0)  # prawo
    elif ValueInRange(1 / 8, ForceAngle, 3 / 8):
        return (delta, delta)  # prawo góra
    elif ValueInRange(3 / 8, ForceAngle, 5 / 8):
        return (0, delta)  # góra
    elif ValueInRange(5 / 8, ForceAngle, 7 / 8):
        return (-delta, delta)  # lewa góra
    elif ValueInRange(7 / 8, ForceAngle, 1) or ValueInRange(-1, ForceAngle, -7 / 8):  # wyjątek
        return (-delta, 0)  # lewo
    elif ValueInRange(-7 / 8, ForceAngle, -5 / 8):
        return (-delta, -delta)  # lewy dół
    elif ValueInRange(-5 / 8, ForceAngle, -3 / 8):
        return (0, -delta)  # dół
    elif ValueInRange(-3 / 8, ForceAngle, -1 / 8):
        return (delta, -delta)  # prawy dół


def WhichCellNext(q, ObstVector, finish_point):

    SingleVectorsCoords = []

    SingleVectorsCoords.append(ForceVectorComponents(q, finish_point, False))

    for Obst in ObstVector:
        SingleVectorsCoords.append(ForceVectorComponents(q, Obst, True))

    F_res = ResultantForceComponents(SingleVectorsCoords)

    Direction = AssingCell(F_res)
    return Direction


def KeepWithinBorder(coord, sign, border):
    #utrzymuje robota przed określoną granicą
    if sign == "<":
        if coord < border:
            return coord
        else:
            return border
    elif sign == ">":
        if coord > border:
            return coord
        else:
            return border
    else:
        raise ValueError("Incorrect sign. Use: \"<\", \">\"")


def KeepWithinScene(SuggestedPoint):
    #utrzymuje robota w scenie
    SuggestedPoint[0] = KeepWithinBorder(SuggestedPoint[0], "<", x_size)
    SuggestedPoint[0] = KeepWithinBorder(SuggestedPoint[0], ">", -x_size)
    SuggestedPoint[1] = KeepWithinBorder(SuggestedPoint[1], "<", y_size)
    SuggestedPoint[1] = KeepWithinBorder(SuggestedPoint[1], ">", -y_size)

    return SuggestedPoint


def CalculateNextPoint(Path, finish_point, obst_vect):

    Direction = WhichCellNext(Path[-1], obst_vect, finish_point)
    RawPoint = list(map(lambda x, y: x + y, Path[-1], Direction))
    RawPoint = KeepWithinScene(RawPoint)
    RoundedNextPoint = (ReturnRounded(RawPoint[0]), ReturnRounded(RawPoint[1]))
    return RoundedNextPoint

def RandomPoint(Path):
    Rand_X = np.random.choice([-delta, 0, delta])
    Rand_Y = np.random.choice([-delta, 0, delta])
    Direction = (Rand_X, Rand_Y)
    RawPoint = list(map(lambda x, y: x + y, Path[-1], Direction))
    RawPoint = KeepWithinScene(RawPoint)
    RoundedNextPoint = (ReturnRounded(RawPoint[0]), ReturnRounded(RawPoint[1]))
    return RoundedNextPoint

def CreatePath(start_point, finish_point, obst_vect):
    #zwraca liste punktow pojedynczej drogi w postaci krotki (tuple)
    Path = []
    Path.append(start_point)
    i = 0 #liczba iteracji do sprawdzania maksymalnej dlugości pojedynczej drogi

    Path.append(CalculateNextPoint(Path, finish_point, obst_vect))

    while (Path[-1] != finish_point):
        NextPoint = CalculateNextPoint(Path, finish_point, obst_vect)

        if NextPoint == Path[-2]:                                        #jeśli robot przechodzi pomiedzy dwoma punktami, to wykonaj ruch w losowym kierunku
            RP = RandomPoint(Path)
            Path.append(RP)
        else:
            Path.append(NextPoint)

        i += 1
        if i > PathLength:                                               # osiagnieto maksymalna dlugosc pojedynczej drogi
            print("Nie osiągnięto mety w %s iteracjach" % PathLength)
            return Path
    return Path
