import numpy as np
import matplotlib.pyplot as plt

##### Opis abstrakcji programu #####

# przeszkoda okrągła - punkt: o[0] - wspolrzedna horyzontalna, o[1] - wspolrzedna wertykalna, z zadanym na stale promieniem d_0
# przeszkoda prostokątna - traktowana jako ograniczony fragment przestrzeni; wektor: p[0] - ograniczenie z lewej, p[1] - ograniczenie dolne, p[2] - ograniczenie z góry, p[3] - ograniczenie z prawej
# ścieżka - obszar oddalony od prostej zadanej równaniem, y=ax+b, o mniej niż r_path
# punkty - losowane z zadanym prawdopodobieństwem na ścieżce (probability_of_path), prawdopodobieństwo pojawienia się w przeszkodzie (delta), pozostałe punkty rozkładają się na ścieżke i pozostały obszar, delta określa również minimalną odległość między punktami, iterations ilość losowanych punktów

# Działanie skryptu:
# implementacja zakłada wyznaczenie ścieżki na podstawie zadanego wspolczynnika kierunkowego i wyrazu wolnego
# przeszkody okrągłe można wprowadzać ręcznie lub generować losowo na podstawie ich liczby zadawanej w zmiennych globalnych
# przeszkody prostokątne można wprowadzać ręcznie
# punkty generowane są losowo na podstawie list przeszkód oraz ścieżki

##### Zmienne globalne #####

a = 2 #wspolczynnik kierunkowy sciezki
b = 10 #wyraz wolny

x_size = 10
y_size = a*x_size    #rozmiar sceny
if y_size < 2:
    y_size=2

y_start=b
y_end=b+y_size
x_start=0
x_end=x_size

delta = 0.001        #najmniejsza dopuszczalna odległość między punktami

NoOfObstacles = 4   #liczba przeszkód okrągłych

d_0 = 1  # promien przeszkod okraglych
r_path = 1 # połowa szerokości ścieżki

probability_of_path = 0.8

point_iters = 100
iterations = 20000 #liczba generowanych pojedynczych punktow

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
    
def RandomObscaleCirc():
    #tworzy losową przeszkodę znajdującą się w całości na scenie i nie znajdującą się na scenie
    Obs_x=RandomCoordinate_x()
    if Obs_x+d_0 >= x_end:
        Obs_x -= d_0
    if Obs_x-d_0 <= x_start:
        Obs_x += d_0
    Obs_y = RandomCoordinate_y()
    i = 0
    while (Obs_y < (a * Obs_x + b + r_path + d_0)) and (Obs_y > (a * Obs_x + b - r_path - d_0)):
        Obs_y = RandomCoordinate_y()
        i += 1
        if i > point_iters:     #na wszelki wypadek przerywa nieskończoną pętle
            print("Nie udało się wylosować przeszkody w %s iteracjach" % point_iters)
            return (Obs_x, Obs_y)
    return (Obs_x, Obs_y)

def IsInObscaleCirc(q, q_i):
    #funkcja sprawdzająca czy punkt jest w pojedynczej przeszkodzie okrągłej
    d_i = CalculateDistance(q, q_i)
    if (d_i <= d_0):
        return True
    else:
        return False

def IsInObscaleRect(q, q_i):
    #funkcja sprawdzająca czy punkt jest w pojedynczej przeszkodzie prostokątnej
    if (ValueInRange(q_i[0],q[0],q_i[2]) and ValueInRange(q_i[1],q[1],q_i[3])):
        return True
    else:
        return False

def IsInObscales(q, VectorCirc, VectorRect):
    #funkcja sprawdzająca czy punkt jest w jakiejkolwiek przeszkodzie
    for q_i in VectorCirc:
        if (IsInObscaleCirc(q, q_i)):
            return True
    for q_i in VectorRect:
        if(IsInObscaleRect(q, q_i)):
            return True
    return False

def MakePath():
    #funkcja tworząca prostą wokół której jest budowana ścieżka, istotna przy ewentualnym debuggingu
    Path = []
    i=x_start
    while(i<x_end):
        Path.append(CalculatePathsPoints(i))
        i+=delta
    return Path

def MakePointInPath():
    #funckja zwraca punkt na sciezce
    x_point = RandomCoordinate_x()
    delta_point = ReturnRounded(np.random.uniform(-r_path, r_path))
    y_point = a * x_point + b + delta_point
    if (y_point>=y_end or y_point<y_start):
        return MakePointInPath()
    return (x_point, y_point)

def MakePointInObscale(ObstVector, VectorRect):
    #funkcja tworzy punkt wewnatrz przeszkody
    point = (RandomCoordinate_x(), RandomCoordinate_y())
    i = 0
    while(IsInObscales(point, ObstVector, VectorRect) == False):
        point = (RandomCoordinate_x(), RandomCoordinate_y())
        i += 1
        if i>point_iters:
            print("Nie udało się wylosować punktu w %s iteracjach" % point_iters)
            return point
    return point

def MakePointOutOfObscale(ObstVector, VectorRect):
    #funkcja tworzaca punkt poza przeszkoda
    point = (RandomCoordinate_x(), RandomCoordinate_y())
    i = 0
    while (IsInObscales(point, ObstVector, VectorRect) == True):
        point = (RandomCoordinate_x(), RandomCoordinate_y())
        i += 1
        if i > point_iters:
            print("Nie udało się wylosować punktu poza przeszkodą w %s iteracjach" % point_iters)
            return point
    return point

def MakePointByProbability(ObstVector, VectorRect):
    #funkcja generujaca punkt w zadanym miejscu zaleznie od zadanego prawdopodobienstwa
    prob = ReturnRounded(np.random.uniform(0, 1))
    if prob == 1:
        return MakePointInObscale(ObstVector, VectorRect)
    if prob <= probability_of_path:
        return MakePointInPath()
    else:
        return MakePointOutOfObscale(ObstVector, VectorRect)

##### main #####

# tworzenie przeszkod
#okraglych
obst_vect = []
for i in range(0, NoOfObstacles):
    obst_vect.append(RandomObscaleCirc())

#prostokatnych
rect_vect = []
#rect_vect.append((0, 15, 3, 20))

#generowanie punktow
point_vect= []
for i in range(0, iterations):
    point_vect.append(MakePointByProbability(obst_vect, rect_vect))

#tworzenie wykresu
fig = plt.figure(figsize=(x_size, y_size))
ax = fig.add_subplot(111)
ax.set_title('Mapa prawdopodobieństwa')

#opcjonalne wyswietlanie środków przeszkód okraglych
#for obstacle in obst_vect:
    #plt.plot(obstacle[0], obstacle[1], "or", color='black')

#i = 0
#wyswietlanie wygenerowanych punktów, z opcjonalnym wypisywaniem postępu, przydatne przy wiekszych ilościach punktow
for point in point_vect:
    #print((i + 1) / iterations * 100, '%')
    #i+=1
    plt.plot(point[0], point[1], ",", color='black')


plt.grid(True)
plt.show()
