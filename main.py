import time
from playsound import playsound as play
from win10toast import ToastNotifier


if __name__ == '__main__':
    h = int(input("Enter the hours: "))
    m = int(input("Enter the minutes: "))
    s = int(input("Enter the seconds: "))

    toast = ToastNotifier()



    for i in range(h, -1, -1):
        for j in range(m, -1, -1):
            for k in range(s, -1, -1):
                time.sleep(1)
                print(f"{i:02d}:{j:02d}:{k:02d}")
            s = 59
        m = 59
    print("Time is up! ")
    toast.show_toast(
        "Countdown Timer",
        "Time is up!",
        duration=10,
        icon_path="clock.ico",
        threaded=True
    )
    play('alarm.mp3')

