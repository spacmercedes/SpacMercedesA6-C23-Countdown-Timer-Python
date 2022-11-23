import pygame, sys, time, os
from win10toast import ToastNotifier
from playsound import playsound as play

pygame.init()
pygame.display.set_caption('Coundown Timer')

fontSize = 100
font = pygame.font.SysFont('Ubuntu-M.ttf', fontSize)

clock = pygame.time.Clock()
W,H = 800, 400
screen = pygame.display.set_mode([W,H])

boolean = True

def notification():
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

def draw_text(i,j,k):
    text = f"{i:02d} : {j:02d} : {k:02d}"
    label = font.render(text, True, (255,255,255))
    screen.blit(label, (W/2-180,H/2-35))
    # pygame.time.delay(1000)
    time.sleep(1)
    pygame.display.update()


def timer(h,m,s):
    for i in range(h, -1, -1):
        for j in range(m, -1, -1):
            for k in range(s, -1, -1):
                pygame.draw.rect(screen, (76, 82, 103), pygame.Rect(W / 2 - 200, H / 2 - 50, 400, 100))
                draw_text(i, j, k)
            s = 59
        m = 59

    notification()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((26,43,66))

    timer(0,0,3)


    pygame.display.flip()
    clock.tick(100)