import threading
import queue

import thread1
import thread2

class Threadtwee(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting ")
        print("Exiting ")

class Threadeen(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting ")
        print("Exiting ")

thread2 = Threadtwee(1)
thread = Threadeen(1)


thread.start()
