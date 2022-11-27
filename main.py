import pygame, sys
from win10toast import ToastNotifier

class Timer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Countdown Timer')
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

        self.fontSize = 100
        self.font = pygame.font.SysFont('Ubuntu-M.ttf', self.fontSize)
        self.font2 = pygame.font.SysFont('Ubuntu-M.ttf', 50)
        self.clock = pygame.time.Clock()
        self.width = 800
        self.height = 400

        self.screen = pygame.display.set_mode([self.width, self.height])
        self.screen.fill((26, 43, 66))

        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.isTimerActive = False
        self.isTimeUp = False

        self.draw_buttons()

        self.refresh_img=pygame.image.load('refresh.png')
        self.screen.blit(self.refresh_img,(self.width-50,20))

    def logicLoop(self):
        while True:
            self.draw_text(self.hours, self.minutes, self.seconds)
            self.mouse = pygame.mouse.get_pos()
            self.process_action()

            if self.isTimerActive:
                self.start_timer()

            pygame.display.flip()
            self.clock.tick(60)

    def notification(self):
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

    def draw_text(self, i, j, k):
        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.width / 2 - 200, self.height / 2 - 50, 400, 100))
        text = f"{i:02d} : {j:02d} : {k:02d}"
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (self.width / 2 - 180, self.height / 2 - 35))
        pygame.display.update()

    def draw_buttons(self):
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

        if self.isTimeUp:
            self.screen.blit(label5, (self.width / 2 - 90, self.height / 2 - 175))
        else:
            pygame.draw.rect(self.screen, (26, 43, 66),pygame.Rect(self.width / 2 - 100, self.height / 2 - 175, 200, 50))

        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.width / 2 - 100, self.height / 2 + 100, 200, 50), 0, 4)

        if not self.isTimerActive:
            self.screen.blit(label3, (self.width / 2 - 35, self.height / 2 + 105))
        else:
            self.screen.blit(label4, (self.width / 2 - 50, self.height / 2 + 105))

        pygame.display.update()

    def start_timer(self):
        stopTimer = False
        for i in range(self.hours, -1, -1):
            for j in range(self.minutes, -1, -1):
                for k in range(self.seconds, -1, -1):
                    self.process_action()
                    if(not self.isTimerActive):
                        stopTimer = True
                        self.seconds = k
                        self.minutes = j
                        self.hours = i
                        break
                    self.draw_text(i, j, k)
                    pygame.time.delay(1000)

                if(stopTimer):
                    break
                self.seconds = 59
            if(stopTimer):
                break
            self.minutes = 59

        self.isTimerActive = False

        if (not stopTimer):
            self.isTimeUp = True
            self.notification()
            self.minutes = 0
            self.seconds = 0

        self.draw_buttons()


    def process_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 240 <= self.mouse[0] <= 275 and 100 <= self.mouse[1] <= 135:
                    self.hours += 1
                    self.isTimeUp = False
                elif 380 <= self.mouse[0] <= 415 and 100 <= self.mouse[1] <= 135:
                    self.minutes += 1
                    self.isTimeUp = False
                    if self.minutes == 60:
                        self.hours += 1
                        self.minutes = 0
                elif 520 <= self.mouse[0] <= 555 and 100 <= self.mouse[1] <= 135:
                    self.seconds += 1
                    self.isTimeUp = False
                    if self.seconds == 60:
                        self.minutes += 1
                        self.seconds = 0
                elif 240 <= self.mouse[0] <= 275 and 255 <= self.mouse[1] <= 280:
                    self.hours -= 1
                    self.isTimeUp = False
                    if self.hours < 0:
                        self.hours = 0
                elif 380 <= self.mouse[0] <= 415 and 255 <= self.mouse[1] <= 280:
                    self.minutes-= 1
                    self.isTimeUp = False
                    if self.minutes < 0:
                        self.minutes = 0
                elif 520 <= self.mouse[0] <= 555 and 255 <= self.mouse[1] <= 280:
                    self.seconds -= 1
                    self.isTimeUp = False
                    if self.seconds < 0:
                        self.seconds = 0
                elif 750 <= self.mouse[0] <= 780 and 15 <= self.mouse[1] <= 50:
                    self.hours = 0
                    self.minutes = 0
                    self.seconds = 0
                    self.isTimeUp = False
                elif 300 <= self.mouse[0] <= 500 and 300 <= self.mouse[1] <= 350:
                    if self.seconds != 0 or self.minutes != 0 or self.hours != 0:
                        self.isTimerActive = not self.isTimerActive
                        self.isTimeUp = False
                self.draw_buttons()


if __name__ == "__main__":
    timer = Timer()
    timer.logicLoop()
