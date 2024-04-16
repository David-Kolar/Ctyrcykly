import numpy

def nacti_hrany():
    V, E = [int(val) for val in input().split()]
    hrany = []
    for i in range(E):
        hrany.append(tuple([int(val) for val in input().split()]))
    return V, hrany

def vyrob_matici(N, hrany):
    A = numpy.zeros((N, N))
    for a, b in hrany:
        A[a][b] = 1
        A[b][a] = 1
    return A

def spocti_nasobenim(K):
    M = K@K
    for i in range(len(M)):
        M[i][i] = 0
    soucet = numpy.sum(M)
    M = M@M
    diagonaly = 0
    for i in range(len(M)):
        diagonaly += M[i][i]
    return (diagonaly - soucet) / 8

def graf_sousednosti(N, hrany):
    graf = [[] for _ in range(N)]
    for a, b in hrany:
        graf[a].append(b)
        graf[b].append(a)

    return graf

def rovinna_metoda(N, hrany):
    graf = graf_sousednosti(N, hrany)
    stupne = [0 for i in range(N)]
    zasobnik = []
    for key, val in enumerate(graf):
        stupne[key] = len(val)
        if (len(val) <= 6):
            zasobnik.append(key)
    kontrola = set()
    for a, b in hrany:
        kontrola.add((a, b))
        kontrola.add((b, a))
    dvojice = set()
    dvojice_ke_zpracovani = [[] for i in range(N)]
    k_odecteni = 0
    while(zasobnik):
        v = zasobnik.pop()
        if (stupne[v] == 0):
            continue
        stupne[v] = 0
        sousede = []
        for s in graf[v]:
            if (stupne[s]>0):
                sousede.append(s)
        for k in dvojice_ke_zpracovani[v]:
            pocitadlo = 0
            for s in sousede:
                if ((s, k) in kontrola) and ((s, v) in kontrola):
                    x = (min(v, k), max(v, k), s)
                    if (x not in dvojice):
                        dvojice.add(x)
                        pocitadlo += 1
            k_odecteni += pocitadlo*(pocitadlo-1)/2
        for i in range(len(sousede)):
            a = sousede[i]
            for j in range(i+1, len(sousede)):
                b = sousede[j]
                dvojice.add((min(a, b), max(a, b), v))
                dvojice_ke_zpracovani[a].append(b)
                dvojice_ke_zpracovani[b].append(a)


        for s in sousede:
            stupne[s] -= 1
            if (stupne[s] <= 6):
                zasobnik.append(s)

    vysledek = 0
    counter = dict()
    for a, b, c in dvojice:
        if ((a, b) not in counter):
            counter[(a, b)] = 0
        counter[(a, b)] += 1
    print(counter)
    for val in counter.values():
        vysledek += val*(val-1)/2
    return vysledek - k_odecteni



N, hrany = nacti_hrany()
M = vyrob_matici(N, hrany)
print(spocti_nasobenim(M))
print(rovinna_metoda(N, hrany))