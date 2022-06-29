import subprocess
from typing import Callable, Union, Tuple, Optional, Any

from . import Logger


class Process(Logger):
    def __init__(self, func: Union[Callable, None] = None):
        Logger.__init__(self)
        self.func = func
        self.log.debug('DONE')

    def run(self, cmd: str) -> Union[int, Tuple[int, str]]:
        if self.func:
            return self.__run_stream(cmd)
        else:
            return self.__run_single_output(cmd)

    def __run_stream(self, cmd: str):
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        for line in iter(proc.stdout.readline, b''):
            recv = line.decode().strip()
            self.log.debug(recv)
            if self.func:
                self.func(recv)
        proc.wait()
        return_stderr = proc.stderr.read().decode() if proc.stderr else None
        self.log.info(f'Command: {cmd}, Return-code:  {proc.returncode}')
        if proc.returncode != 0:
            self.log.error(f'Command: {cmd}, Return-code:  {proc.returncode}, StdErr: {return_stderr}')
        return proc.returncode

    def __run_single_output(self, cmd: str) -> Tuple[Union[int, Any], Optional[str]]:
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        proc.wait()
        return_code = proc.returncode
        return_stdout = proc.stdout.read().decode() if proc.stdout else None
        return_stderr = proc.stderr.read().decode() if proc.stderr else None
        self.log.info(f'Command: {cmd}, Return-code:  {proc.returncode}')
        self.log.debug(f'Command: {cmd}, Return-code:  {proc.returncode}, StdOut: {return_stdout}')
        if return_code != 0:
            self.log.error(f'Command: {cmd}, Return-code:  {proc.returncode}, StdErr: {return_stderr}')
        return return_code, return_stdout


if __name__ == '__main__':
    # c = Process('cd /data/projects/adcc_developer_pc_profile/; ./adcc_scripts/build/build.sh', print)
    c = Process(print)
    print(c.run('ls ; sleep 1 ; ls ; sleep 1 ; ls '))
    c = Process()
    print(c.run('ls ; sleep 1 ; ls ; sleep 1 ; ls '))
    # Test sudo Run
    sudo_c = Process(print)
