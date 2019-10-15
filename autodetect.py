import re
import subprocess

def autodetect():
    proc = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
    lines = re.split('[\n]', str(proc.stdout, 'utf-8'))

    running = []

    flag = False
    for line in lines:
        if 'GPU' in line and 'PID' in line and 'Type' in line and 'Process name' in line:
            flag = True
            continue

        if flag:
            if 'MiB' in line: # process line
                words = re.split('[ |\n]', line)
                words = [word for word in words if word != '']
                running.append(int(words[0]))
    running = set(running)
    return running

def occupy(n_gpus, running, exe):
    if len(running) == n_gpus:
        return

    command = [exe]
    for i in range(n_gpus):
        if not i in running:
            command += str(i)

    proc = subprocess.run(command, stdout=subprocess.PIPE)

def detect_occupy(n_gpus, exe):
    running = autodetect()
    occupy(n_gpus, running, exe)

def kill(exe):
    #command = ["kill", "-9", "$(ps -aux | grep " + exe + " | awk '{print $2}')"]
    command = "kill -9 $(ps -aux | grep " + exe + " | awk '{print $2}')"
    proc = subprocess.run(command, stdout=subprocess.PIPE, shell=True)

if __name__ == '__main__':
    running = autodetect()
    print(running)
    occupy(3, running, '/home/an/Projects/OccupyGPU/run')
