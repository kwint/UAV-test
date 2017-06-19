import thread1


def process():
    while True:
        if thread1.flag == 2:
            print("got move: ", thread1.move)
            thread1.flag = 1