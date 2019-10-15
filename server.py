import time
import socket
import subprocess

from multiprocessing import Process, Queue

from autodetect import detect_occupy, kill


port = 12134
ip = '127.0.0.1'
n_gpus =  # total number of gpus
exe = 'OccupyGPU/run'
interval =  # check every x seconds


msg_q = Queue()
def server(ip, port):
    s = socket.socket()
    s.bind((ip, port))
    s.listen()
    
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(4096)
            msg_q.put(data)
            if data == b'stop':
                break

    s.close()


p_server = Process(target=server, args=(ip, port), daemon=True)
p_server.start()

while True:
    stop = False
    p_occupy = Process(target=detect_occupy, args=(n_gpus, exe), daemon=True)
    p_occupy.start()
    print('occupied')

    start = time.time()
    while True:
        if time.time() - start > interval: # re-check
            kill(exe)
            p_occupy.join()
            print('to re-check')
            break
        if msg_q.empty():
            continue

        msg = msg_q.get()
        if msg == b'reset':
            kill(exe)
            p_occupy.join()
            start = time.time() # reset check time
            print('to suspend for a while')
        elif msg == b'stop':
            kill(exe)
            p_occupy.join()
            stop = True
            print('to stop')
            break
    if stop:
        break

p_server.join()
