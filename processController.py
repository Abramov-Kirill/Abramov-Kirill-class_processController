import time
import threading
from threading import Thread
from multiprocessing import Process


class ProcessController:
    def __init__(self, max_proc=1):
        self.max_proc = max_proc
        self.semaphore = threading.BoundedSemaphore(self.max_proc)
        self.all_thread = []
        self.active_process = 0
        self.loc = threading.Lock()

    def set_max_proc(self, max_proc):
        self.max_proc = max_proc
        self.semaphore = threading.BoundedSemaphore(self.max_proc)

    def run_process(self, func, args, max_exec_time):
        """
        Данная функция создает процесс для выполнения фунций из tasks и ведет подсчет времени работы данного процесса.
        """
        with self.semaphore:  #Ограничение на кол-во запущенных потоков (а в данном случае и процессов)
            with self.loc:  #Подсчет активных в данный момент потоков
                self.active_process += 1
            pr = Process(target=func, args=args)
            pr.start()
            start_time = time.time()
            while time.time() < max_exec_time + start_time and pr.is_alive():  #Таймер работы процесса
                time.sleep(0.0001)
            with self.loc:  #Подсчет активных в данный момент потоков/процессов
                self.active_process -= 1
                self.all_thread.remove(threading.current_thread())
            if pr.is_alive():  #Блокировка процесса и выброс исключения, времени работы превышающем max_exec_time
                pr.terminate()
                raise Exception(f'The process {pr.name} has exceeded the waiting time\n '
                                f'The function being performed: {func.__name__}\n '
                                f'Passed arguments: {args}')

    def start(self, tasks, max_exec_time=10):
        """
        Данная функция создает несколько потоков, которые в свою очередь создают процессы для выполнения фунций из tasks.
        Также данные потоки предназначены для подчета времени работы процессов.
        """
        for func, args in tasks:
            th = Thread(target=self.run_process, args=(func, args, max_exec_time))
            self.all_thread.append(th)
            th.start()

    def get_max_proc(self):
        return self.max_proc

    def wait(self):
        """
        Блокировка основного потока работы пока не закончится работа других потоков/процессов.
        """
        while sum([th.is_alive() for th in self.all_thread]) > 0:
            time.sleep(0.001)

    def wait_count(self):
        """
        Возвращает число еще не запущенных заданий.
        """
        return sum([th.is_alive() for th in self.all_thread]) - self.active_process

    def alive_count(self):
        """
        Возвращает число выполняемых в данный момент заданий.
        """
        return self.active_process
