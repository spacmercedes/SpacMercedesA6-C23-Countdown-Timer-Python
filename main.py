import pygame, sys, time, os
from win10toast import ToastNotifier
from playsound import playsound as play

class Game():
    def __init__ (self):
        pygame.init()
        pygame.display.set_caption('Coundown Timer')

        self.fontSize = 100
        self.font = pygame.font.SysFont('Ubuntu-M.ttf', self.fontSize)
        self.font2 = pygame.font.SysFont('Ubuntu-M.ttf', 50)
        self.clock = pygame.time.Clock()
        self.W = 800
        self.H = 400
        self.screen = pygame.display.set_mode([self.W,self.H])

        self.screen.fill((26,43,66))

        self.x = 0

        self.h = 0
        self.m = 0
        self.s = 0

        self.draw_buttons()

        while True:
            self.process_action()

            self.mouse = pygame.mouse.get_pos()

            self.draw_text(self.h,self.m,self.s)

            # print(mouse)
            # start_timer(0,0,3)

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
        audio_file = os.path.dirname(__file__) + '\_alarm.mp3'
        play(audio_file)
        print("Time is up")

    def draw_text(self,i,j,k):
        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.W / 2 - 200, self.H / 2 - 50, 400, 100))
        text = f"{i:02d} : {j:02d} : {k:02d}"
        label = self.font.render(text, True, (255,255,255))
        self.screen.blit(label, (self.W/2-180,self.H/2-35))
        # pygame.time.delay(1000)
        # time.sleep(1)
        pygame.display.update()

    def draw_buttons(self):
        # pygame.draw.rect(screen, (76, 82, 103), pygame.Rect(W / 2 - 200, H / 2 - 50, 400, 100))
        text = "+"
        text2 = "-"
        text3 = "Play"
        text4 = "Pause"
        label = self.font.render(text, True, (92, 197, 158))
        label2 = self.font.render(text2, True, (92, 197, 158))
        label3 = self.font2.render(text3, True, (92, 197, 158))
        label4 = self.font2.render(text4, True, (92, 197, 158))
        self.screen.blit(label, (self.W / 2 - 160, self.H / 2 - 120))
        self.screen.blit(label, (self.W / 2 - 20, self.H / 2 - 120))
        self.screen.blit(label, (self.W / 2 + 120, self.H / 2 - 120))
        self.screen.blit(label2, (self.W / 2 - 150, self.H / 2 + 30))
        self.screen.blit(label2, (self.W / 2 - 10, self.H / 2 + 30))
        self.screen.blit(label2, (self.W / 2 + 130, self.H / 2 + 30))

        pygame.draw.rect(self.screen, (76, 82, 103), pygame.Rect(self.W / 2 - 100, self.H / 2 + 100, 200, 50), 0, 4)

        if self.x % 2 == 0:
            self.screen.blit(label3, (self.W / 2 - 35, self.H / 2 + 105))
        else:
            self.screen.blit(label4, (self.W / 2 - 50, self.H / 2 + 105))

        pygame.display.update()

    def start_timer(self):
        for i in range(self.h, -1, -1):
            for j in range(self.m, -1, -1):
                for k in range(self.s, -1, -1):
                    self.process_action()
                    self.draw_text(i, j, k)
                    pygame.time.delay(1000)
                self.s = 59
            self.m = 59
        self.x=1
        self.draw_buttons()
        self.notification()





    def process_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 <= self.mouse[0] <= 275 and 100 <= self.mouse[1] <= 135:
                    self.h += 1
                if 380 <= self.mouse[0] <= 415 and 100 <= self.mouse[1] <= 135:
                    self.m += 1
                    if self.m == 60:
                        self.h += 1
                        self.m = 0
                if 520 <= self.mouse[0] <= 555 and 100 <= self.mouse[1] <= 135:
                    self.s += 1
                    if self.s == 60:
                        self.m += 1
                        self.s = 0
                if 240 <= self.mouse[0] <= 275 and 255 <= self.mouse[1] <= 280:
                    self.h -= 1
                    if self.h<0:
                        self.h=0
                if 380 <= self.mouse[0] <= 415 and 255 <= self.mouse[1] <= 280:
                    self.m -= 1
                    if self.m < 0:
                        self.m = 0
                if 520 <= self.mouse[0] <= 555 and 255 <= self.mouse[1] <= 280:
                    self.s -= 1
                    if self.s < 0:
                        self.s = 0
                if 300 <= self.mouse[0] <= 500 and 300 <= self.mouse[1] <= 350:
                    self.x += 1
                    self.draw_buttons()
                    if self.x % 2 != 0:
                        self.start_timer()

if __name__ == "__main__":
    timer = Game()