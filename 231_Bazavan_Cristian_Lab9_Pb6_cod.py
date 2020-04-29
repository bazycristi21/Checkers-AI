import time
import pygame



class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_LINII = 8
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = '#'
    pierzator = None

    def __init__(self, tabla=None):
        self.matr = tabla or [['#', 'a', '#', 'a', '#', 'a', '#', 'a'],   # tabla initiala de joc
                              ['a', '#', 'a', '#', 'a', '#', 'a', '#'],
                              ['#', 'a', '#', 'a', '#', 'a', '#', 'a'],
                              ['#', '#', '#', '#', '#', '#', '#', '#'],
                              ['#', '#', '#', '#', '#', '#', '#', '#'],
                              ['n', '#', 'n', '#', 'n', '#', 'n', '#'],
                              ['#', 'n', '#', 'n', '#', 'n', '#', 'n'],
                              ['n', '#', 'n', '#', 'n', '#', 'n', '#']]

    def final(self):
        rez = fara_piese(self.matr)   # finalul jocului este atins daca un jucator ramane fara piese
        if rez:
            return rez
        rez = (mai_poate_muta(Joc.JMAX,self.matr) == False)  # sau daca nu mai poate muta nici o piesa
        if rez == True:
            return Joc.JMAX
        rez = (mai_poate_muta(Joc.JMIN, self.matr) == False)
        if rez == True:
            return Joc.JMIN
        return False

    def mutari_joc(self, jucator):   # genereaza mutarile calculatorului
        # mutarile vor fi ordonate astfel incat MAX sa aleaga la fiecare pas mutarea cea mai favorabila. acest lucru i se datoreaza functiei de calculare a scorului.
        l_mutari = []
        jucatorOpus = self.JMAX if jucator == self.JMIN else self.JMIN

        if jucator == 'a':
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.matr[i][j] in [jucator,jucator.upper()]:
                        x = i
                        y = j
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]   # se face o copie a tablei de joc
                        if i < 7 and j < 7 and self.matr[i + 1][j + 1] == '#':  # daca se poate realiza mutarea
                            matr_noua[i + 1][j + 1] = matr_noua[i][j]    # se plaseaza piesa pe pozitia noua
                            matr_noua[i][j] = '#'   # se plaseaza loc gol pe pozitia veche
                            joc = Joc(matr_noua)   # se creaza obiect de tip joc nou
                            if joc not in l_mutari:
                                l_mutari.append(joc)   # se adauga in lista de mutari
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i < 7 and j > 0 and self.matr[i + 1][j - 1] == '#':
                            matr_noua[i + 1][j - 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'
                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i > 0 and j < 7 and self.matr[i - 1][j + 1] == '#' and self.matr[i][j] == jucator.upper():  # in acest caz ( adica piesa a ajuns la capatul opus si a devenit rege) poate muta si inapoi
                            matr_noua[i - 1][j + 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'

                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i > 0 and j > 0 and self.matr[i - 1][j - 1] == '#' and self.matr[i][j] == jucator.upper():
                            matr_noua[i - 1][j - 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'

                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        verifica_mutare(matr_noua, x, y, jucator, jucatorOpus, l_mutari,False,1)   # verifica recursiv cat timp poate captura o piesa calculatorul
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.matr[i][j] in [jucator,jucator.upper()]:
                        x = i
                        y = j
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i > 0 and j < 7 and self.matr[i - 1][j + 1] == '#':
                            matr_noua[i - 1][j + 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'
                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i > 0 and j > 0 and self.matr[i - 1][j - 1] == '#':
                            matr_noua[i - 1][j - 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'
                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i < 7 and j < 7 and self.matr[i + 1][j + 1] == '#' and self.matr[i][j] == jucator.upper():
                            matr_noua[i + 1][j + 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'

                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        if i < 7 and j > 0 and self.matr[i + 1][j - 1] == '#' and self.matr[i][j] == jucator.upper():
                            matr_noua[i + 1][j - 1] = matr_noua[i][j]
                            matr_noua[i][j] = '#'
                            joc = Joc(matr_noua)
                            if joc not in l_mutari:
                                l_mutari.append(joc)
                        matr_noua = [[self.matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
                        verifica_mutare(matr_noua, x, y, jucator, jucatorOpus, l_mutari,False,1)
        return l_mutari

    def calculeaza_scor(self):  # calculeaza scorul calculatorului
        scor = 0
        piesa_inamic = False
        for i in range(0,8):
            for j in range(0,8):
                if self.matr[i][j] == Joc.JMAX: # pentru fiecare piesa a calculatorului adauga 1
                    scor += 4
                elif self.matr[i][j] == Joc.JMIN: # pentru fiecare piesa a jucatorului scade 1
                    piesa_inamic = True
                    scor -= 4
                elif self.matr[i][j] == Joc.JMAX.upper():  # pentru fiecare piesa speciala a calculatorului adauga 2
                    scor += 5
                elif self.matr[i][j] == Joc.JMIN.upper(): # pentru fiecare piesa speciala a jucatorului scade 2
                    piesa_inamic = True
                    scor -= 5
        if piesa_inamic == False:
            scor += 10000
        return scor

        # o alta varianta de estimare a scorului ar fi numarul de piese capturate / nr de mutari efectuate

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (99 + adancime)
        elif t_final == Joc.JMIN:
            return (-99 - adancime)
        else:
            return self.calculeaza_scor()

    def __str__(self):
        sir = (" ".join([str(self.matr[0][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[1][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[2][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[3][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[4][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[5][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[6][i]) for i in range(0,8)]) + "\n" +
               " ".join([str(self.matr[7][i]) for i in range(0,8)]) + "\n" +
                "-----------------------")
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
        self.j_curent = j_curent  # simbolul jucatorului curent

        # adancimea in arborele de stari
        #	(scade cu cate o unitate din „tata” in „fiu”)
        self.adancime = adancime

        # scorul starii (daca e finala, adica frunza a arborelui)
        # sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []  # lista va contine obiecte de tip Stare

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari_stare(self):
        l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
        juc_opus = self.jucator_opus()

        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir



def fara_piese(matr):
    j1 = False
    j2 = False
    for i in range(0,8):
        for j in range(0,8):     # verificam daca jucatorii mai au cel putin o piesa fiecare
            if matr[i][j] in ['a', 'A']:
                j1 = True
            if matr[i][j] in ['n','N']:
                j2 = True
    if j1 == False:   # returnam numele jucatorului care nu mai are piese sau false
        return 'n'
    if j2 == False:
        return 'a'
    return False

def verifica_mutare(matr,x,y,jucator,jucatorOpus,l_mutari, ok,mod_returnare):
    val_x = -1
    val_y = -1
    if jucator == 'a':
        matr_noua = [[matr[i][j] for j in range(0,8)] for i in range(0,8)]
        if  x > 1 and y < 6:
            if matr_noua[x - 1][y + 1] in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x - 2][y + 2] == '#' and matr_noua[x][y] == jucator.upper():  # verifica daca poate face o mutare + capturarea unei piese a adversarului
                ok = True
                matr_noua[x - 2][y + 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'       # updatam tabla de joc
                matr_noua[x - 1][y + 1] = '#'

                val_x = x - 2  # retinem valorile pentru care am facut o mutare
                val_y = y + 2
                verifica_mutare(matr_noua,x-2,y+2,jucator,jucatorOpus,l_mutari,ok,mod_returnare)   # apeleaza recursiv cu matricea updatata
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)] # copiem apoi matricea data ca parametru la inceput pentru a incerca in alta directie
        if x > 1 and y > 1:
            if matr_noua[x - 1][y - 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x - 2][y - 2] == '#' and matr_noua[x][y] == jucator.upper():
                ok = True
                matr_noua[x - 2][y - 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x - 1][y - 1] = '#'

                val_x = x - 2
                val_y = y - 2
                verifica_mutare(matr_noua,x-2,y-2,jucator,jucatorOpus,l_mutari,ok,mod_returnare)
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if  x < 6 and y > 1:
            if matr_noua[x + 1][y - 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x + 2][y - 2] == '#' :
                ok = True
                matr_noua[x + 2][y - 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x + 1][y - 1] = '#'

                val_x = x + 2
                val_y = y - 2
                verifica_mutare(matr_noua,x+2,y-2,jucator,jucatorOpus,l_mutari,ok,mod_returnare)
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if x < 6 and y < 6:
            if matr_noua[x + 1][y + 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x + 2][y + 2] == '#':
                ok = True
                matr_noua[x + 2][y + 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x + 1][y + 1] = '#'

                val_x = x + 2
                val_y = y + 2
                verifica_mutare(matr_noua,x+2,y+2,jucator,jucatorOpus,l_mutari,ok,mod_returnare)
    else :
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if x < 6 and y < 6:
            if matr_noua[x + 1][y + 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x + 2][y + 2] == '#' and matr_noua[x][
                y] == jucator.upper():
                ok = True
                matr_noua[x + 2][y + 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x + 1][y + 1] = '#'

                val_x = x + 2
                val_y = y + 2
                verifica_mutare(matr_noua, x + 2, y + 2, jucator, jucatorOpus, l_mutari, ok,mod_returnare)
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if x < 6 and y > 1:
            if matr_noua[x + 1][y - 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x + 2][y - 2] == '#' and matr_noua[x][
                y] == jucator.upper():
                ok = True
                matr_noua[x + 2][y - 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x + 1][y - 1] = '#'

                val_x = x + 2
                val_y = y - 2
                verifica_mutare(matr_noua, x + 2, y - 2, jucator, jucatorOpus, l_mutari, ok,mod_returnare)
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if x > 1 and y > 1:
            if matr_noua[x - 1][y - 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x - 2][y - 2] == '#':
                ok = True
                matr_noua[x - 2][y - 2] = matr[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x - 1][y - 1] = '#'


                val_x = x - 2
                val_y = y - 2
                verifica_mutare(matr_noua, x - 2, y - 2, jucator, jucatorOpus, l_mutari, ok,mod_returnare)
        matr_noua = [[matr[i][j] for j in range(0, 8)] for i in range(0, 8)]
        if x > 1 and y < 6:
            if matr_noua[x - 1][y + 1]  in [jucatorOpus,jucatorOpus.upper()] and matr_noua[x - 2][y + 2] == '#':
                ok = True
                matr_noua[x - 2][y + 2] = matr_noua[x][y]
                matr_noua[x][y] = '#'
                matr_noua[x - 1][y + 1] = '#'

                val_x = x - 2
                val_y = y + 2
                verifica_mutare(matr_noua, x - 2, y + 2, jucator, jucatorOpus, l_mutari, ok,mod_returnare)
    if ok == True:
        if mod_returnare == 1:  # daca mod returnare este 1,
            joc = Joc(matr_noua)   #
            l_mutari.append(joc)
        else:
            if val_x != -1 and val_y != -1:
                l_mutari.append((val_x *100 + 52,val_y* 100 + 52,1))

""" Algoritmul MinMax """

def min_max(stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or mai_poate_muta(stare.j_curent,stare.tabla_joc.matr) == False :
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Altfel, calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari_stare()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]
    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor
    return stare

def alpha_beta(alpha, beta, stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Conditia de retezare:
    if alpha >= beta:
        return stare  # este intr-un interval invalid, deci nu o mai procesez

    # Calculez toate mutarile posibile din starea curenta (toti „fiii”)
    stare.mutari_posibile = stare.mutari_stare()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

        # pentru fiecare „fiu” de tip MIN:
        for mutare in stare.mutari_posibile:
            # calculeaza scorul fiului curent
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (cresc) scorul si alfa
            # „tatalui” de tip MAX, folosind scorul fiului curent
            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MIN


    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')  # scorul „tatalui” de tip MIN

        # pentru fiecare „fiu” de tip MAX:
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (scad) scorul si beta
            # „tatalui” de tip MIN, folosind scorul fiului curent
            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        print("A castigat " + final)
        print("Scor calculator:",Joc.estimeaza_scor(stare_curenta.adancime))
        return True
    return False

class Background(pygame.sprite.Sprite):   # clasa care incarca imaginea de fundal a interfetei
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Piesa():   # clasa pentru piesele ( pt modul interfata)
    def __init__(self,image,available,pressed,king,x,y):
        self.image_path = image
        self.image = pygame.image.load(str(image) + ".png")
        self.pressed_image = str(image) + "-pressed.png"
        self.available = available
        self.pressed = pressed
        self.x = x
        self.y = y
        self.king = king
    def verif_collision(self,mousex,mousey):  # verifica daca mouseul este apasat peste o piesa
        if (mousex - self.x ) < 90 and (mousex - self.x ) > 0 and (mousey - self.y) < 90 and ( mousey - self.y) > 0:
            return True
        return False

    def verif_pressed(self):
        if self.pressed == True:
            self.image = pygame.image.load(self.pressed_image)  # in functie daca piesa este apasata sau nu incarcam imaginea corespunzatoare
        else:
            self.image = pygame.image.load(self.image_path +".png")

def text_objects(text,font):
    textSurface = font.render(text,True,(0,0,0))   # creaza suprafata si rectangleul textului si le returneaza
    return textSurface, textSurface.get_rect()

def displayInfo(jucator,timp,gameDisplay): # functie pentru afisarea timpului si randul jucatorului
    jucator = 'Red' if jucator == 'a' else 'Blue'
    text = "Turn: " + jucator
    largeText = pygame.font.Font('freesansbold.ttf',32)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = (1150,200)
    gameDisplay.blit(TextSurf,TextRect)
    text2 = "Last move time: " + str(timp) +" ms"
    largeText = pygame.font.Font('freesansbold.ttf', 32)
    TextSurf, TextRect = text_objects(text2, largeText)
    TextRect.center = (1150, 400)
    gameDisplay.blit(TextSurf, TextRect)

def verif_mutare(i,j,matr,jucator,doar_capturi):   # functie care returneaza mutarile posibile ale jucatorului pentru modul matrice.
                                                    # apoi vom verifica daca jucatorul incearca sa faca o mutare care se regaseste in aceasta lista de mutari posibile
    mutari_posibile = []
    jucatorOpus = 'n' if jucator == 'a' else 'a'
    if matr[i][j] == jucator or matr[i][j] == jucator.upper():
        if jucator == 'a':
            if not doar_capturi:
                if i < 7 and j < 7 and matr[i + 1][j + 1] == '#':
                    mutari_posibile.append(( 52 + 100 * (i+1),52 + 100 * (j+1) , 0))

                if i < 7 and j > 0 and matr[i + 1][j - 1] == '#':
                    mutari_posibile.append(( 52 + 100 * (i+1),52 + 100 * (j-1),0))

                if i > 0 and j < 7 and matr[i - 1][j + 1] == '#' and matr[i][j] == jucator.upper():
                    mutari_posibile.append(( 52 + 100 * (i-1),52 + 100 * (j+1),0))
                if i > 0 and j > 0 and matr[i - 1][j - 1] == '#' and matr[i][j] == jucator.upper():   # se aplica aceleasi reguli ca la mutarile calculatorului
                    mutari_posibile.append(( 52 + 100 * (i-1),52 + 100 * (j-1),0))
            if i < 6 and j < 6 and matr[i+1][j+1] in [jucatorOpus, jucatorOpus.upper()] and matr[i+2][j+2] == '#':
                mutari_posibile.append((52+100 * (i+2),52+ 100* (j+2),1))
            if i < 6 and j > 1 and matr[i + 1][j - 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i + 2][j - 2] == '#':
                mutari_posibile.append((52 + 100 * (i + 2), 52 + 100 * (j - 2), 1))
            if i > 0 and j < 6 and matr[i - 1][j + 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i - 2][j + 2] == '#' and matr[i][j] == jucator.upper():
                mutari_posibile.append((52 + 100 * (i - 2), 52 + 100 * (j + 2), 1))
            if i > 0 and j > 1 and matr[i - 1][j - 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i - 2][j - 2] == '#'  and matr[i][j] == jucator.upper():
                mutari_posibile.append((52 + 100 * (i - 2), 52 + 100 * (j - 2), 1))

        else:
            if not doar_capturi:
                if i > 0 and j < 7 and matr[i - 1][j + 1] == '#':
                    mutari_posibile.append((52 + 100 * (i - 1), 52 + 100 * (j + 1),0))

                if i > 0 and j > 0 and matr[i - 1][j - 1] == '#':
                    mutari_posibile.append((52 + 100 * (i - 1), 52 + 100 * (j - 1),0))

                if i < 7 and j < 7 and matr[i + 1][j + 1] == '#' and matr[i][j] == jucator.upper():
                    mutari_posibile.append((52 + 100 * (i + 1), 52 + 100 * (j + 1),0))
                if i < 7 and j > 0 and matr[i + 1][j - 1] == '#' and matr[i][j] == jucator.upper():
                    mutari_posibile.append((52 + 100 * (i + 1),52 + 100 * (j-1),0))
            if i > 1 and j < 6 and matr[i - 1][j + 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i - 2][j + 2] == '#':
                mutari_posibile.append((52 + 100 * (i - 2), 52 + 100 * (j + 2), 1))
            if i > 1 and j > 1 and matr[i - 1][j - 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i - 2][j - 2] == '#':
                mutari_posibile.append((52 + 100 * (i - 2), 52 + 100 * (j - 2), 1))
            if i < 6 and j < 6 and matr[i + 1][j + 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i + 2][j + 2] == '#'  and matr[i][j] == jucator.upper():
                mutari_posibile.append((52 + 100 * (i + 2), 52 + 100 * (j + 2), 1))
            if i < 6 and j > 1 and matr[i + 1][j - 1] in [jucatorOpus, jucatorOpus.upper()] and matr[i + 2][j - 2] == '#'  and matr[i][j] == jucator.upper():
                mutari_posibile.append((52 + 100 * (i + 2), 52 + 100 * (j - 2), 1))



    else:
        print("Nu este jucator")

    return mutari_posibile
def verif_piesa_speciala(stare):
    for i in range(0,8):
        if stare.tabla_joc.matr[0][i] == 'n':   # verificam daca una din piese a ajuns in capatul opus si in caz afirmativ o transformam in piesa speciala (rege)
            stare.tabla_joc.matr[0][i] = 'N'
        if stare.tabla_joc.matr[7][i] == 'a':
            stare.tabla_joc.matr[7][i] = 'A'

def coord_to_index(x):
    return round((x-52) / 100)   # functie care preia coordonata unei piese si returneaza indexul in matricea de joc

def index_to_coord(x):     # functie inversa celei anterioare
    return x * 100 + 52



def button(text,x,y,width,height,color,hover_color,gameDisplay,mouse):  # functie care defineste un buton

    if x + width > mouse[0] > x and y + height> mouse[1] > y:
        pygame.draw.rect(gameDisplay, color, (x, y, width, height))
    else:
        pygame.draw.rect(gameDisplay, hover_color, (x, y, width, height))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ( (x + (width / 2)), (y + (height / 2)))
    gameDisplay.blit(textSurf,textRect)

def mai_poate_muta(jucator,matr):   # functie care verifica daca jucatorul mai are mutari posibile
    for i in range(0,8):
        for j in range(0,8):
            if matr[i][j] in [jucator, jucator.upper()]:
                if len(verif_mutare(i,j,matr,jucator,False)) > 0:
                    return True
    return False

def main():
    raspuns_valid = False
    while not raspuns_valid:
        tip_joc = input("Modul de rulare? (raspundeti cu 1 sau 2) \n 1. In consola\n 2. In interfata\n")
        if tip_joc in ['1', '2']:
            raspuns_valid = True

    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")



    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))
    mutari_calculator = 0
    mutari_jucator = 0
    t_inceput = int(round(time.time() * 1000))

    if tip_joc == '1':   # in cazul in care s-a ales tipul de joc 1 ( in consola):

        # initializare ADANCIME_MAX
        raspuns_valid = False
        while not raspuns_valid:
            n = input("Adancime maxima a arborelui: ")
            if n.isdigit():
                Stare.ADANCIME_MAX = int(n)
                raspuns_valid = True
            else:
                print("Trebuie sa introduceti un numar natural nenul.")

        # creare stare initiala
        stare_curenta = Stare(tabla_curenta, 'n', Stare.ADANCIME_MAX)

        # initializare jucatori
        raspuns_valid = False
        while not raspuns_valid:
            Joc.JMIN = input("Doriti sa jucati cu n sau cu a? ").lower()
            if (Joc.JMIN in ['n', 'a']):
                raspuns_valid = True
            else:
                print("Raspunsul trebuie sa fie n sau a.")
        Joc.JMAX = 'n' if Joc.JMIN == 'a' else 'a'

        while True:
            verif_piesa_speciala(stare_curenta)
            if (stare_curenta.j_curent == Joc.JMIN):
                # muta jucatorul
                raspuns_valid = False

                while not raspuns_valid:
                    linie = int(input("linia piesei (0-7) = "))
                    coloana = int(input("coloana piesei (0-7) ="))
                    if (linie in range(0, 8) and coloana in range(0, 8)):
                        if stare_curenta.tabla_joc.matr[linie][coloana] in [Joc.JMIN, Joc.JMIN.upper()] and len(verif_mutare(linie,coloana,stare_curenta.tabla_joc.matr,Joc.JMIN,False)) > 0:
                            raspuns_valid = True
                        else:
                            print("Mutare invalida")
                    else:
                        print("Mutare invalida")
                # dupa acest while stim sigur ca avem valorile linie si coloana valide
                # citim valorile mutarii
                raspuns_valid = False
                while not raspuns_valid:
                    linie_mutare = int(input("linia mutarii (0-7) ="))
                    coloana_mutare = int(input("coloana mutarii (0-7) ="))
                    if linie_mutare in range(0,8) and coloana_mutare in range(0,8):
                        mutari = verif_mutare(linie,coloana,stare_curenta.tabla_joc.matr,Joc.JMIN,False)
                        for mutare in mutari:
                            if coord_to_index(mutare[0]) == linie_mutare and coord_to_index(mutare[1]) == coloana_mutare:
                                raspuns_valid = True
                                if mutare[2] == 0:   # daca este mutare normala:
                                    stare_curenta.tabla_joc.matr[linie_mutare][coloana_mutare] = stare_curenta.tabla_joc.matr[linie][coloana]
                                    stare_curenta.tabla_joc.matr[linie][coloana] = '#'
                                else:  # daca este mutare cu capturat piesa a adversarului
                                    stare_curenta.tabla_joc.matr[linie_mutare][coloana_mutare] = stare_curenta.tabla_joc.matr[linie][coloana]
                                    stare_curenta.tabla_joc.matr[linie][coloana] = '#'
                                    stare_curenta.tabla_joc.matr[int((linie + linie_mutare)/2)][int((coloana+coloana_mutare)/2)] = '#'
                                break
                    else:
                        print("Mutarea este invalida")
                    if raspuns_valid == False:
                        print("Mutarea este invalida")

                # afisarea starii jocului in urma mutarii utilizatorului
                print("\nTabla dupa mutarea jucatorului")
                print(str(stare_curenta))

                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                if (afis_daca_final(stare_curenta)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()

            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator

                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)

                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()

    if tip_joc == '2':  # daca s-a ales modul de joc 2 (in interfata)

        pygame.init()
        gameWidth = 1400   # dimensiunile interfatei
        gameHeight = 900

        pygame.mouse.set_visible(1)

        BackGround = Background('./background.png', [0, 0])     # afisam backgroundul
        gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))
        pygame.display.set_caption('Dame')
        clock = pygame.time.Clock()
        Final = False
        piesa_apasata = None
        durata = 0
        a_mutat = False
        piesa_locked = (-1,-1)
        lock_piesa = False     # initializam variabilele
        index_apasata = (-1,-1)

        pierzator = None
        intro = True
        while intro:   # ecranul de start
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 600 + 200 > mouse[0] > 600 and 300 + 50 > mouse[1] > 300:
                        intro =  False
                    if 615 + 170 > mouse[0] > 615 and 650 + 50 > mouse[1] > 650:
                        pygame.quit()


            gameDisplay.fill((255, 255, 255))
            text = "Dame"
            largeText = pygame.font.Font('freesansbold.ttf', 50)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700,100)
            gameDisplay.blit(TextSurf, TextRect)
            text = "Menu"
            largeText = pygame.font.Font('freesansbold.ttf', 35)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700, 200)
            gameDisplay.blit(TextSurf, TextRect)
            mouse = pygame.mouse.get_pos()
            button("Start", 600, 300, 200, 50, (0, 230, 0), (0, 250, 0), gameDisplay, mouse)
            button("Exit", 615, 650, 170, 50, (230, 0, 0), (255, 0, 0), gameDisplay, mouse)
            pygame.display.update()
            clock.tick(15)

        dificulty = True
        while dificulty:  # ecranul de setare a dificultatii
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # verificam daca userul apasa pe unul din butoane
                    if 400 + 120 > mouse[0] > 400 and 500 + 50 > mouse[1] > 500:
                        Stare.ADANCIME_MAX = int(1)
                        dificulty = False
                    if 600 + 200 > mouse[0] > 600 and 500 + 50 > mouse[1] > 500:
                        Stare.ADANCIME_MAX = int(2)
                        dificulty = False
                    if 850 + 170 > mouse[0] > 400 and 500 + 50 > mouse[1] > 500:
                        Stare.ADANCIME_MAX = int(3)
                        dificulty = False
            gameDisplay.fill((255, 255, 255))
            text = "Dame"
            largeText = pygame.font.Font('freesansbold.ttf', 60)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700, 100)
            gameDisplay.blit(TextSurf, TextRect)
            text = "Choose dificulty"
            largeText = pygame.font.Font('freesansbold.ttf', 35)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700, 300)
            gameDisplay.blit(TextSurf, TextRect)
            mouse = pygame.mouse.get_pos()
            button("Easy", 400, 500, 120, 50, (0, 230, 0), (0, 250, 0), gameDisplay, mouse)
            button("Intermediate", 600, 500, 200, 50, (0, 0, 230), (0, 0, 255), gameDisplay, mouse)
            button("Expert", 850, 500, 170, 50, (230, 0, 0), (255, 0, 0), gameDisplay, mouse)
            pygame.display.update()
            clock.tick(15)

        alege_jucator = True
        while alege_jucator: # ecranul de alegere a jucatorului

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 400 + 120 > mouse[0] > 400 and 500 + 50 > mouse[1] > 500:
                        Joc.JMIN = 'a'
                        Joc.JMAX = 'n'
                        alege_jucator = False
                    if 850 + 170 > mouse[0] > 850 and 500 + 50 > mouse[1] > 500:
                        Joc.JMIN = 'n'
                        Joc.JMAX = 'a'
                        alege_jucator = False

            gameDisplay.fill((255, 255, 255))
            text = "Dame"
            largeText = pygame.font.Font('freesansbold.ttf', 60)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700,100)
            gameDisplay.blit(TextSurf, TextRect)
            text = "Choose player"
            largeText = pygame.font.Font('freesansbold.ttf', 35)
            TextSurf, TextRect = text_objects(text, largeText)
            TextRect.center = (700, 300)
            gameDisplay.blit(TextSurf, TextRect)
            mouse = pygame.mouse.get_pos()
            button("Red", 400, 500, 120, 50, (230,0, 0), (255, 0, 0), gameDisplay, mouse)
            button("Blue", 850, 500, 170, 50, (0, 0, 230), (0, 0, 255), gameDisplay, mouse)
            pygame.display.update()
            clock.tick(15)



        stare_curenta = Stare(tabla_curenta, 'n', Stare.ADANCIME_MAX)
        gameDisplay.blit(BackGround.image, BackGround.rect)
        t_inainte = int(round(time.time() * 1000))
        while not Final:  # ecranul de joc
            verif_piesa_speciala(stare_curenta)
            gameDisplay.blit(BackGround.image, BackGround.rect)
            piese1 = []
            piese2 = []
            for i in range(0, 8):
                for j in range(0, 8):
                    if stare_curenta.tabla_joc.matr[i][j] == 'a':  # randam piesele in functie de cum s-a updatat matricea de joc la ultima iteratie
                        piesa = Piesa('piesa1', True, False, False, 52 + 100 * (j), 52 + 100 * (i))
                        if i == index_apasata[0] and j == index_apasata[1]:
                            piesa.pressed = True
                        piese1.append(piesa)
                    elif stare_curenta.tabla_joc.matr[i][j] == 'n':
                        piesa = Piesa('piesa2', True, False, False, 52 + 100 * (j), 52 + 100 * (i))
                        if i == index_apasata[0] and j == index_apasata[1]:
                            piesa.pressed = True
                        piese2.append(piesa)
                    elif stare_curenta.tabla_joc.matr[i][j] == 'A':
                        piesa = Piesa('piesa1-king', True, False, True, 52 + 100 * (j), 52 + 100 * (i))
                        if i == index_apasata[0] and j == index_apasata[1]:
                            piesa.pressed = True
                        piese1.append(piesa)
                    elif stare_curenta.tabla_joc.matr[i][j] == 'N':
                        piesa = Piesa('piesa2-king', True, False, True, 52 + 100 * (j), 52 + 100 * (i))
                        if i == index_apasata[0] and j == index_apasata[1]:
                            piesa.pressed = True
                        piese2.append(piesa)

            for i in piese1:
                if i.available:
                    i.verif_pressed()  # verificam daca este una din piese apasata
                    gameDisplay.blit(i.image, (i.x,i.y))
            for i in piese2:
                if i.available:
                    i.verif_pressed()
                    gameDisplay.blit(i.image, (i.x,i.y))

            # creare stare initiala

            displayInfo(stare_curenta.j_curent,durata, gameDisplay)

            # highlight piesa apasata
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Final = True
                if stare_curenta.j_curent == Joc.JMIN:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        if stare_curenta.j_curent == 'a':
                            for i in piese1:
                                if i.verif_collision(x, y) :
                                    if i.pressed == False:
                                        i.pressed = True
                                        piesa_apasata = i
                                        index_apasata = (coord_to_index(piesa_apasata.y),coord_to_index(piesa_apasata.x))   # retinem atunci cand apasa userul pe o piesa
                                        for j in piese1:
                                            if i != j:
                                                j.pressed = False
                                    else:
                                            i.pressed = False
                                            piesa_apasata = None
                                            index_apasata = (-1,-1)

                        else:
                            for i in piese2:
                                if i.verif_collision(x, y) :
                                    if i.pressed == False:
                                        i.pressed = True
                                        piesa_apasata = i
                                        index_apasata = (coord_to_index(piesa_apasata.y), coord_to_index(piesa_apasata.x))
                                        for j in piese2:
                                            if i != j:
                                                j.pressed = False
                                    else:
                                        i.pressed = False
                                        piesa_apasata = None
                                        index_apasata = (-1,-1)



                        if piesa_apasata != None:
                            mutari = verif_mutare(coord_to_index(piesa_apasata.y),coord_to_index(piesa_apasata.x), stare_curenta.tabla_joc.matr,stare_curenta.j_curent,False)  # generam mutarile posibile pentru jucator
                            mutari_captura = verif_mutare(coord_to_index(piesa_apasata.y),coord_to_index(piesa_apasata.x), stare_curenta.tabla_joc.matr,
                                                          stare_curenta.j_curent, True)
                            if len(mutari_captura) == 0 and lock_piesa == True:   # daca deja a facut o mutare si a capturat o piesa, piesa respectiva ramane blocata apasata cat timp mai poate face mutari cu captura
                                lock_piesa = False
                                piesa_locked = (-1, -1)
                                stare_curenta.j_curent = stare_curenta.jucator_opus()
                                piesa_apasata = None
                                index_apasata = (-1, -1)  # reinitializam variabilele
                            for mutare in mutari:
                                if mutare[2] == 0 and lock_piesa == False:    # daca este mutare obisnuita

                                    if - mutare[0] + event.pos[1] < 100 and  - mutare[0] + event.pos[1] >= 0 and - mutare[1] + event.pos[0] < 100 and - mutare[1] + event.pos[0] >= 0: # verificam daca mouseul este apasat pe patratul corespunzator uneia
                                        # dintre mutarile posibile
                                        stare_curenta.tabla_joc.matr[coord_to_index(mutare[0])][coord_to_index(mutare[1])] = stare_curenta.tabla_joc.matr[coord_to_index(piesa_apasata.y)][coord_to_index(piesa_apasata.x)]
                                        stare_curenta.tabla_joc.matr[coord_to_index(piesa_apasata.y)][coord_to_index(piesa_apasata.x)] = '#'  # updatam matricea
                                        stare_curenta.j_curent = stare_curenta.jucator_opus()
                                        piesa_apasata = None
                                        index_apasata = (-1, -1)
                                        mutari_jucator += 1
                                else:
                                    if y - mutare[0]  < 100 and y - mutare[0]  >= 0 and x - mutare[1]  < 100 and x - mutare[1] >= 0 :   # altfel fac mutarea, updatez matricea si blochez piesa mutata cat timp poate sa mai captureze alte piese inamice
                                            lock_piesa = True
                                            piesa_locked = (coord_to_index(mutare[0]),coord_to_index(mutare[1]))
                                            stare_curenta.tabla_joc.matr[coord_to_index(mutare[0])][
                                                coord_to_index(mutare[1])] = stare_curenta.tabla_joc.matr[coord_to_index(piesa_apasata.y)][coord_to_index(piesa_apasata.x)]
                                            stare_curenta.tabla_joc.matr[coord_to_index(piesa_apasata.y)][coord_to_index(piesa_apasata.x)] = '#'
                                            stare_curenta.tabla_joc.matr[coord_to_index((piesa_apasata.y + mutare[0])/2)][coord_to_index((piesa_apasata.x + mutare[1])/2)] = '#'

                                            piesa_apasata.y = mutare[0]
                                            piesa_apasata.x = mutare[1]
                                            index_apasata = (
                                            coord_to_index(piesa_apasata.y), coord_to_index(piesa_apasata.x))
                                            mutari_captura = verif_mutare(coord_to_index(piesa_apasata.y),coord_to_index(piesa_apasata.x), stare_curenta.tabla_joc.matr,
                                                                          stare_curenta.j_curent, True)
                                            if len(mutari_captura) == 0 and lock_piesa == True:   # daca nu mai poate face mutari, resetez variabilele
                                                lock_piesa = False
                                                piesa_locked = (-1, -1)
                                                stare_curenta.j_curent = stare_curenta.jucator_opus()
                                                piesa_apasata = None
                                                index_apasata = (-1, -1)
                                                mutari_jucator += 1



            if stare_curenta.j_curent == Joc.JMAX:
                mutari_calculator += 1
                # preiau timpul in milisecunde de dupa mutarea jucatorului si randare
                t_dupa = int(round(time.time() * 1000))
                durata = str(t_dupa - t_inainte)
                verif_piesa_speciala(stare_curenta)
                gameDisplay.blit(BackGround.image, BackGround.rect)
                displayInfo(stare_curenta.j_curent, durata, gameDisplay)
                # preiau timpul in milisecunde de dinainte de mutarea calculatorului si randare
                t_inainte = int(round(time.time() * 1000))
                piese1 = []
                piese2 = []
                for i in range(0, 8):
                    for j in range(0, 8):
                        if stare_curenta.tabla_joc.matr[i][j] == 'a':
                            piesa = Piesa('piesa1', True, False, False, 52 + 100 * (j), 52 + 100 * (i))
                            if i == index_apasata[0] and j == index_apasata[1]:
                                piesa.pressed = True
                            piese1.append(piesa)
                        elif stare_curenta.tabla_joc.matr[i][j] == 'n':
                            piesa = Piesa('piesa2', True, False, False, 52 + 100 * (j), 52 + 100 * (i))
                            if i == index_apasata[0] and j == index_apasata[1]:
                                piesa.pressed = True
                            piese2.append(piesa)
                        elif stare_curenta.tabla_joc.matr[i][j] == 'A':
                            piesa = Piesa('piesa1-king', True, False, True, 52 + 100 * (j), 52 + 100 * (i))
                            if i == index_apasata[0] and j == index_apasata[1]:
                                piesa.pressed = True
                            piese1.append(piesa)
                        elif stare_curenta.tabla_joc.matr[i][j] == 'N':
                            piesa = Piesa('piesa2-king', True, False, True, 52 + 100 * (j), 52 + 100 * (i))
                            if i == index_apasata[0] and j == index_apasata[1]:
                                piesa.pressed = True
                            piese2.append(piesa)

                for i in piese1:
                    if i.available:
                        i.verif_pressed()
                        gameDisplay.blit(i.image, (i.x, i.y))
                for i in piese2:
                    if i.available:
                        i.verif_pressed()
                        gameDisplay.blit(i.image, (i.x, i.y))
                pygame.display.update()

                # Mutare calculator
                if mai_poate_muta(Joc.JMAX,stare_curenta.tabla_joc.matr) == False:
                    print("Nu mai poate muta")
                    Final =  True
                    pierzator = Joc.JMAX
                    break
                else:
                    if tip_algoritm == '1':
                        stare_actualizata = min_max(stare_curenta)

                    else:  # tip_algoritm==2
                        stare_actualizata = alpha_beta(-500, 500, stare_curenta)

                    stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                    if stare_actualizata == None or fara_piese(stare_curenta.tabla_joc.matr):
                        Final = True
                        pierzator = Joc.JMAX
                    print("Tabla dupa mutarea calculatorului")
                    print(str(stare_curenta))

                    # preiau timpul in milisecunde de dupa mutare
                    t_dupa = int(round(time.time() * 1000))
                    durata = str(t_dupa - t_inainte)
                    print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                    stare_curenta.j_curent = stare_curenta.jucator_opus()
                    t_inainte = int(round(time.time() * 1000))  # preiau timpul de la finalul mutarii calculatorului adica inainte de randare si mutarea jucatorului
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Final = True

            clock.tick(30)

        final_screen = True
        while final_screen: # ecranul final (game over)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    final_screen = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 650 + 120 > mouse[0] > 650 and 700 + 50 > mouse[1] > 700:
                        final_screen = False
                        pygame.quit()
            if final_screen == True:
                if pierzator != None:
                    castigator = 'Red' if pierzator == 'n' else 'Blue'
                gameDisplay.fill((255, 255, 255))
                text = "Dame"
                largeText = pygame.font.Font('freesansbold.ttf', 60)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = (680, 100)
                gameDisplay.blit(TextSurf, TextRect)
                text = "Game over"
                largeText = pygame.font.Font('freesansbold.ttf', 35)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = (730, 300)
                gameDisplay.blit(TextSurf, TextRect)
                if pierzator != None:
                    text = "Winner: " + castigator
                else:
                    text = "No winner. Game interrupted."
                largeText = pygame.font.Font('freesansbold.ttf', 40)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = (700, 500)
                gameDisplay.blit(TextSurf, TextRect)
                mouse = pygame.mouse.get_pos()
                button("Exit", 650, 700, 170, 50, (230, 0, 0), (255, 0, 0), gameDisplay, mouse)
                pygame.display.update()
                clock.tick(15)




        pygame.quit()

    t_sfarsit = int(round(time.time() * 1000))
    print("Mutari calculator: ", mutari_calculator)
    print("Mutari jucator: ", mutari_jucator)
    print("Timp total:", t_sfarsit - t_inceput)
    scor_calculator = 0
    scor_jucator = 0
    for i in range(0,8):
        for j in range(0,8):
            if stare_curenta.tabla_joc.matr[i][j] == Joc.JMIN:
                scor_jucator += 1
            if stare_curenta.tabla_joc.matr[i][j] == Joc.JMIN.upper():
                scor_jucator += 2
            if stare_curenta.tabla_joc.matr[i][j] == Joc.JMAX:
                scor_calculator += 1
            if stare_curenta.tabla_joc.matr[i][j] == Joc.JMAX.upper():
                scor_calculator += 2

    print("Scor jucator: ",scor_jucator)
    print("Scor calculator: ", scor_calculator)

if __name__ == "__main__":
    main()