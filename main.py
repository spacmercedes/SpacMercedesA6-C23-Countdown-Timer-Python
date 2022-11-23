import time



if __name__ == '__main__':
    n = int(input("Enter the seconds: "))

    for i in range(n, 0, -1):
        time.sleep(1)
        print(i)
    print("Time is up! ")

