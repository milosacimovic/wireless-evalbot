import socket
import threading
import time

##
def forward():
    print("Forward")
    senderSocket.send('w'.encode())

##
def backward():
    print("Backward")
    senderSocket.send('s'.encode())

##
def turn_left():
    print("Turn left")
    senderSocket.send('a'.encode())

##
def turn_right():
    print("Turn right")
    senderSocket.send('d'.encode())

##
def rotate_left():
    print("Rotate left")
    senderSocket.send('A'.encode())

##
def rotate_right():
    print("Rotate right")
    senderSocket.send('D'.encode())

##
def increase_speed():
    print("Increase speed")
    senderSocket.send('+'.encode())
    senderSocket.send('+'.encode())
    senderSocket.send('x'.encode())

##
def decrease_speed():
    print("Decrease speed")
    senderSocket.send('-'.encode())
    senderSocket.send('-'.encode())
    senderSocket.send('x'.encode())

##
def stop():
    print("Stop")
    senderSocket.send('x'.encode())

##

'''
def workingThread(message):
    instruction[str(message)]()
    print("Message : ", str(message))
'''


instruction = {
    "_forward_": forward,
    "_backward_": backward,
    "_turn_left_": turn_left,
    "_turn_right_": turn_right,
    "_rotate_left_": rotate_left,
    "_rotate_right_": rotate_right,
    "_increase_speed_": increase_speed,
    "_decrease_speed_": decrease_speed,
    "_stop_": stop,
    'w':forward,
    's':backward,
    'a':turn_left,
    'd':turn_right,
    'A':rotate_left,
    'D':rotate_right,
    '+':increase_speed,
    '-':decrease_speed,
    'x':stop
}

receiverSocket = socket.socket()
receiverSocket.bind(("192.168.1.33", 4001))
receiverSocket.listen(50)

while True:
    conn, addr = receiverSocket.accept()
    global senderSocket
    senderSocket = socket.socket()
    senderSocket.connect(("169.254.152.245", 23))
    print("Connection established with : ", str(addr))
    while True:
        message = conn.recv(1024).decode()
        '''
        if (message != "_end_" and 
                    message != "_forward_" and
                    message != "_backward_" and
                    message != "_turn_left_" and
                    message != "_turn_right_" and
                    message != "_rotate_left_" and
                    message != "_rotate_right_" and
                    message != "_increase_speed_" and
                    message != "_decrease_speed_" and
                    message != 'w' and
                    message != 's' and
                    message != 'a' and
                    message != 'd' and
                    message != 'A' and
                    message != 'D' and
                    message != 'x' and
                    message != '+' and
                    message != '-'):
            continue
        '''
        if  message == '':
            print("End of transmission")
            break
        if  message == "_end_":
            print("End of transmission")
            break
        else:
            if message in instruction.keys():
                instruction[str(message)]()
                print("Message : ", str(message))

    conn.close()
    senderSocket.close()
receiverSocket.close()

