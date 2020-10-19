import zmq
import time


context = zmq.Context()

#  Socket to talk to server
print("Connecting to Shark server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.16.25:4444")


#  Do 10 requests, waiting each time for a response


def move_shark_left():
    for _ in range(3):
        try:
            socket.send(b"L")
            message = socket.recv()

            print(f"Received reply [ {message} ]")
            break
        except Exception as e:
            print(e)


def move_shark_right():
    for _ in range(3):
        try:
            socket.send(b"R")
            message = socket.recv()

            print(f"Received reply [ {message} ]")
            break
        except Exception as e:
            print(e)
