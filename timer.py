import pygame
import sys
from win10toast import ToastNotifier


class Timer:

    def __init__(self):

        pygame.init()  # initializarea ferestrei
        pygame.display.set_caption('Countdown Timer')
        pygame.event.set_blocked(None)  # sunt atribuite permisiuni pentru toate evenimentele
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])  # sunt permise evenimentele de tip QUIT (inchiderea ferestrei la apasarea butonuului *X* si MOUSEBUTTONDOWN pentru orice altfel de click cu mouse-ul

        # initializarea fonturilor utilizate, marimea lor si marimea ferestrei
        self.fontSize = 100
        self.font = pygame.font.SysFont('Ubuntu-M.ttf', self.fontSize)
        self.font2 = pygame.font.SysFont('Ubuntu-M.ttf', 50)
        self.clock = pygame.time.Clock()  # initializez ceasul pentru stabilirea fps
        self.width = 800
        self.height = 400

        self.screen = pygame.display.set_mode([self.width, self.height])  # crearea unei variabile pentru ecran
        self.screen.fill((26, 43, 66))  # colorarea ecranului

        self.hours = 0
        self.minutes = 0
        self.seconds = 5

        self.isTimerActive = False  # monitorizez starea de pauza/activitate
        self.isTimeUp = False  # mentine starea pentru afisarea mesajului "Time is Up!" la scurgerea timpului

        self.draw_buttons()  # se apeleaza functia de afisare a butoanelor

        # este incarcata imaginea de refresh si "lipita" peste ecran
        self.refresh_img = pygame.image.load('refresh.png')
        self.screen.blit(self.refresh_img, (self.width - 50, 20))

    def fiveSeconds(self):
        stopTimer = False
        for k in range(self.seconds, -1, -1):
            self.process_action()  # daca s-a facut vreo actiune pe ecran (play, pause, + , -)
            if not self.isTimerActive:  # daca suntem in stare de pausa, h:m:s primesc valorile pe care le au in momentul apasarii butonului de pause
                stopTimer = True
                self.seconds = k
                break
            self.draw_text(self.hours, self.minutes, k)  # altfel, se afiseaza h:m:s cu un de[lay de 1 secunda
            pygame.time.delay(1000)
        if not stopTimer:  # daca s-a scurs timpul, pornim notificarea si m:s devin 0
            self.isTimeUp = True
            self.notification()
            self.seconds = 5
            self.fiveSeconds()

    def logicLoop(self):  # apelarea tuturor functiilor pentru functionalitate

        while True:
            self.draw_text(self.hours, self.minutes, self.seconds)  # afisarea textului (ore:minute:secunde)
            self.mouse = pygame.mouse.get_pos()  # preluarea pozitiei mouse-ului
            self.process_action()  # apel functie de procesare a evenimentelor la un anumit click

            if self.isTimerActive:  # verifica daca timer-ul nu este in stare de pauza si apeleaza functia de start
                # self.start_timer() # timp normal
                self.fiveSeconds() # timp 5 secunde
            pygame.display.flip()  # face refresh la anumite sectiuni selectate de pe ecran
            self.clock.tick(60)  # stabilirea de 60fps

    def notification(self):  # functie pentru afisarea notificarii vizual si auditiv

        toast = ToastNotifier()
        toast.show_toast(
            "Countdown Timer",
            "Time is up!",
            duration=10,
            icon_path="clock.ico",
            threaded=True
        )
        pygame.mixer.music.load('_alarm.wav')
        pygame.mixer.music.play()
        print("Time is up")

    def draw_text(self, i, j, k):  # afisarea textului din timer (ore:minute:secunde)

        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.width / 2 - 200, self.height / 2 - 50, 400, 100))
        text = f"{i:02d} : {j:02d} : {k:02d}"  # formatarea textului astfel incat in cazul afisarii a unei singuure cifre, in fata ei sa fie afisat un 0
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (self.width / 2 - 180, self.height / 2 - 35))
        pygame.display.update()

    def draw_buttons(self):  # afisarea butoanelor pe ecran

        text = "+"
        text2 = "-"
        text3 = "Play"
        text4 = "Pause"
        text5 = "Time is up!"
        label = self.font.render(text, True, (92, 197, 158))
        label2 = self.font.render(text2, True, (92, 197, 158))
        label3 = self.font2.render(text3, True, (92, 197, 158))
        label4 = self.font2.render(text4, True, (92, 197, 158))
        label5 = self.font2.render(text5, True, (255, 255, 255))
        self.screen.blit(label, (self.width / 2 - 160, self.height / 2 - 120))
        self.screen.blit(label, (self.width / 2 - 20, self.height / 2 - 120))
        self.screen.blit(label, (self.width / 2 + 120, self.height / 2 - 120))
        self.screen.blit(label2, (self.width / 2 - 150, self.height / 2 + 30))
        self.screen.blit(label2, (self.width / 2 - 10, self.height / 2 + 30))
        self.screen.blit(label2, (self.width / 2 + 130, self.height / 2 + 30))

        if self.isTimeUp:  # daca s-a scurs timpul, afisam mesajul "time is up!"
            self.screen.blit(label5, (self.width / 2 - 90, self.height / 2 - 175))
        else:  # altfel "astupam" mesajul cu un dreptunghi de culoarea fundalului
            pygame.draw.rect(self.screen, (26, 43, 66),
                             pygame.Rect(self.width / 2 - 100, self.height / 2 - 175, 200, 50))

        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.width / 2 - 100, self.height / 2 + 100, 200, 50),
                         0, 4)  # afisarea butonului de Play/Pause

        if not self.isTimerActive:  # daca nu suntem in stare de pauza afisam buonul Play, altfel Puase
            self.screen.blit(label3, (self.width / 2 - 35, self.height / 2 + 105))
        else:
            self.screen.blit(label4, (self.width / 2 - 50, self.height / 2 + 105))

        pygame.display.update()

    def start_timer(self):
        stopTimer = False
        # pentru fiecare h:m:s, se verifica de la valoarea initiala pana la -1, cu pasul -1:
        for i in range(self.hours, -1, -1):
            for j in range(self.minutes, -1, -1):
                for k in range(self.seconds, -1, -1):
                    self.process_action()  # daca s-a facut vreo actiune pe ecran (play, pause, + , -)
                    if not self.isTimerActive:  # daca suntem in stare de pausa, h:m:s primesc valorile pe care le au in momentul apasarii butonului de pause
                        stopTimer = True
                        self.seconds = k
                        self.minutes = j
                        self.hours = i
                        break
                    self.draw_text(i, j, k)  # altfel, se afiseaza h:m:s cu un delay de 1 secunda
                    pygame.time.delay(1000)

                if stopTimer:  # daca e pauza, iesim din for
                    break
                self.seconds = 59  # daca val minutelor este decrementata cu 1, secundele devin 59
            if stopTimer:
                break
            self.minutes = 59

        self.isTimerActive = False

        if not stopTimer:  # daca s-a scurs timpul, pornim notificarea si m:s devin 0
            self.isTimeUp = True
            self.notification()
            self.minutes = 0
            self.seconds = 0

        self.draw_buttons()

    def process_action(self):  # verfica ce se intampla iin momentul apasarii anumitor coordonate de pe ecran

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # inchide fereastra
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 240 <= self.mouse[0] <= 275 and 100 <= self.mouse[1] <= 135:  # incrementeaza orele cu 1
                    self.hours += 1
                    self.isTimeUp = False
                elif 380 <= self.mouse[0] <= 415 and 100 <= self.mouse[1] <= 135:  # incrementeaza minutele cu 1, iar in momentul in care m ajung la 60,h este incremnetat cu 1
                    self.minutes += 1
                    self.isTimeUp = False
                    if self.minutes == 60:
                        self.hours += 1
                        self.minutes = 0
                elif 520 <= self.mouse[0] <= 555 and 100 <= self.mouse[1] <= 135:  # incrementeaza secunde cu 1, iar in momentul in care s ajung la 60,m este incrementat cu 1
                    self.seconds += 1
                    self.isTimeUp = False
                    if self.seconds == 60:
                        self.minutes += 1
                        self.seconds = 0
                elif 240 <= self.mouse[0] <= 275 and 255 <= self.mouse[1] <= 280:  # decrementeaza orele
                    self.hours -= 1
                    self.isTimeUp = False
                    if self.hours < 0:
                        self.hours = 0
                elif 380 <= self.mouse[0] <= 415 and 255 <= self.mouse[1] <= 280:  # decrementeaza minutele
                    self.minutes -= 1
                    self.isTimeUp = False
                    if self.minutes < 0:
                        self.minutes = 0
                elif 520 <= self.mouse[0] <= 555 and 255 <= self.mouse[1] <= 280:  # decremneteaza secundele
                    self.seconds -= 1
                    self.isTimeUp = False
                    if self.seconds < 0:
                        self.seconds = 0
                elif 750 <= self.mouse[0] <= 780 and 15 <= self.mouse[1] <= 50:  # este apasat butonul de refresh, vslorile deviin 0
                    self.hours = 0
                    self.minutes = 0
                    self.seconds = 0
                    self.isTimeUp = False
                elif 300 <= self.mouse[0] <= 500 and 300 <= self.mouse[1] <= 350:  # apasarea butonului de Play/Pause
                    if self.seconds != 0 or self.minutes != 0 or self.hours != 0:  # verifica ca valorile h:m:s nu sunt pe 0 inainte sa se apese pe play
                        self.isTimerActive = not self.isTimerActive  #din pauza in play sau invers
                        self.isTimeUp = False
                self.draw_buttons()
