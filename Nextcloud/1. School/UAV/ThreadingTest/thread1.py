import thread2
import threading

class threadtwee(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting ")
        thread2.process()
        print("Exiting ")

thread = threadtwee(1)
thread.start()

while True:
    print("Henkie")