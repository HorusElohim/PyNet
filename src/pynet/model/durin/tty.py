from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
import os


class Stdout(Thread):
    active: bool = False

    def __init__(self, stdout: PIPE):
        Thread.__init__(self)
        self.stdout = stdout
        os.set_blocking(self.stdout.fileno(), False)

    def run(self) -> None:
        self.active = True
        print('Stdout started...')
        while self.active:
            if self.stdout:
                try:
                    output = os.read(self.stdout.fileno(), 1024)
                    if output:
                        output = output.decode('utf-8')
                        if output:
                            print(output)
                except OSError:
                    sleep(0.1)

    def stop(self):
        self.active = False


class Stderr(Thread):
    active: bool = False

    def __init__(self, stdout: PIPE):
        Thread.__init__(self)
        self.stdout = stdout
        os.set_blocking(self.stdout.fileno(), False)

    def run(self) -> None:
        self.active = True
        print('Stderr started...')
        while self.active:
            if self.stdout:
                try:
                    output = os.read(self.stdout.fileno(), 1024)
                    if output:
                        output = output.decode('utf-8')
                        if output:
                            print(f'\033[91m{output}\033[0m')
                except OSError:
                    sleep(0.5)

    def stop(self):
        self.active = False


class TTY:
    p: Popen
    th_stdout: Stdout

    def __init__(self):
        self.p = Popen(['python', '-c', 'import pty; pty.spawn("/bin/bash")'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.th_stdout = Stdout(self.p.stdout)
        self.th_stderr = Stderr(self.p.stderr)
        self.th_stdout.start()
        self.th_stderr.start()

    def input(self, cmd: str):
        self.p.stdin.write(f'{cmd}\n'.encode('utf-8'))
        self.p.stdin.flush()

    def terminate(self):
        self.p.terminate()
        self.th_stdout.stop()
