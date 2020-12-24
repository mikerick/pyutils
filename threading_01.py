import threading
import queue

logger_lock = threading.Lock()


def __log(note: str):
    """
    This is your log function
    Args:
        note: a note to log
    """
    logger_lock.acquire()
    try:
        with open("trash/logfile_01.txt", 'a') as lf:
            lf.write(note + '\n')
    except Exception:
        print("Some error with logging")
    finally:
        logger_lock.release()


def log_all(q: queue.Queue):
    """
    A function to fetch new data from a queue and call a log function
    """
    while not FULL_STOP or q.qsize() > 0:
        note = q.get()
        __log(note)


FULL_STOP = False


def stop_execution():
    """
    A special function to stop all threads
    (Of course, those of threads that check FULL_STOP variable)
    """
    global FULL_STOP
    FULL_STOP = True


if __name__ == '__main__':
    logger_queue = queue.Queue()
    lt = threading.Thread(target=log_all, name="logger_thread", args=(logger_queue,))
    lt.start()
    logger_queue.put("note 1")
    logger_queue.put("note 2")
    logger_queue.put("note 3")
    logger_queue.put("note 4")
    stop_execution()
    lt.join()
    print("Ok!")
