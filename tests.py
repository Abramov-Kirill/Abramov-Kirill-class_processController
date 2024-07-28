import random
from processController import ProcessController
import time
import multiprocessing


def write_to_file(file_name, start_time=None, finish_time=None, result=None):
    """
    Вспомогательная функция для записи резельтатов работы процесса в файл
    Пример результата выполнения можно посмотреть в result_test/max_proc_test/
    """
    result_file = open(file_name, 'w+')
    result_file.write(f'The process {multiprocessing.current_process()}:\n'
                      f'started working at {start_time}\n'
                      f'finished its work at {finish_time}\n'
                      f'The result of the process: {result}')
    result_file.close()


def helper_test_max_proc(a, b, result_file_name=None):
    """
    Данная функция после завершения основного кода делает небольшую задержку,
    это позволяет увидеть, что новый процесс не запустится, пока для него не освободится место.
    Также для примера здесь запускается функция write_to_file
    """
    start_time = time.time()
    pr_name = multiprocessing.current_process()
    print(f'The process {pr_name} started working at {start_time}')

    result = a + b
    time.sleep(2)

    finish_time = time.time()
    print(f'The process {pr_name} finished its work at {finish_time}')

    if not (result_file_name is None):
        write_to_file(result_file_name, start_time, finish_time, result)


def helper_test_max_exec_time(a, b):
    """
    Данная функция после завершения основного кода делает случайную задержку, которая может превышать max_exec_time.
    В таком случае ProcessController выведет в консоль Exception с сообщением о достигнутом лимите времени,
    выполняемой функции и параметрами выполняемой функции.
    """
    start_time = time.time()
    pr_name = multiprocessing.current_process()
    print(f'The process {pr_name} started working at {start_time}')

    result = a + b
    #print(result)
    time.sleep(random.randint(1, 5))

    finish_time = time.time()
    print(f'The process {pr_name} finished its work at {finish_time}')


def helper_test_wait(a, b):
    pr_name = multiprocessing.current_process()

    result = a + b
    time.sleep(random.randint(1, 5))

    finish_time = time.time()
    print(f'The process {pr_name} finish working at {finish_time}')


def helper_test_wait_count(a, b):
    result = a + b
    time.sleep(0.5)


def helper_test_alive_count(a, b):
    result = a + b
    time.sleep(1)

def helper_test_multiple_starts(a, b):
    result = a + b
    print(result)
    time.sleep(1)



def test_max_proc():
    pc = ProcessController()
    assert pc.max_proc == 1
    pc.set_max_proc(2)
    assert pc.max_proc == 2

    result_file_name = 'result_test/max_proc_test/'
    tasks = [(helper_test_max_proc, (1, 2, result_file_name+str(i)+'.txt')) for i in range(3)]
    pc.start(tasks, 10)


def test_max_exec_time():
    pc = ProcessController(3)
    tasks = [(helper_test_max_exec_time, (i, 2)) for i in range(5)]
    pc.start(tasks, 3)


def test_wait():
    """
    В данной функции продемонстрирована работа метода wait().
    Сообщение: 'All processes are completed' выведется лишь после того как отработают все процессы запущенные ProcessController-ом
    """
    pc = ProcessController(3)
    tasks = [(helper_test_wait, (i, 2)) for i in range(5)]
    pc.start(tasks, 10)
    pc.wait()
    print('All processes are completed')


def test_wait_count():
    """
    Данная функция запускает функцию helper_test_wait_count,
    после чего в основном потоке проверяет, сколько задач находится в очереди.
    При общем кол-ве задач равном 20 и max_proc равном 3,  функция выводит в консоль 17 14 11 8 5 2
    """
    pc = ProcessController(3)
    tasks = [(helper_test_wait_count, (i, 2)) for i in range(20)]
    pc.start(tasks, 10)
    while pc.wait_count() > 0:
        print(pc.wait_count())
        time.sleep(0.5)


def test_alive_count():
    """
    Данная функция запускает процессов менбше чем значение max_proc, для того чтобы оценить корректность работы alive_count()
    """
    pc = ProcessController(5)
    tasks = [(helper_test_alive_count, (i, 2)) for i in range(3)]
    pc.start(tasks, 10)
    while pc.alive_count() > 0:
        print(pc.alive_count())
        time.sleep(0.7)


def test_multiple_starts():
    """
    Данная функция тестирует добавление задач в очередь
    """
    pc = ProcessController(5)
    tasks = [(helper_test_multiple_starts, (i, 2)) for i in range(10)]
    pc.start(tasks, 10)
    tasks_2 = [(helper_test_multiple_starts, (15, 5)) for i in range(10)]
    pc.start(tasks_2, 10)