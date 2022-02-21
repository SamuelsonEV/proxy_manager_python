# TODO Create some sort of loading bar

'''
This Module receives Proxy lists on the format [[ip, protocol], [ip, protocol], [ip, protocol], [ip, protocol]....]
Uses it to ping it alll and returns the ones that had responded before timeout, it returns on the format:
[[ip, protocol, delay], [ip, protocol, delay], [ip, protocol, delay], [ip, protocol, delay]....]
'''

from ping3 import ping
import threading
import time
from datetime import datetime
from operator import itemgetter
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

fileHandler = logging.FileHandler('ping_proxys.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


class ping_proxy_list:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        logger.info("Setting Vars")

        # Ping Config
        self.timeout_of_ping = 1.2 # Its in seconds !!!!!!
        self.number_of_threads = 50
        self.threads = [] # Just to initialize
        self.wait_before_launch_new_thread = 0.03
        self.maximum_delay_in_ms = 320 # Maximum delay of the response(if more will not be added)
        self.print_refresh_rate = 0.3   # Print on screen
        if proxy_list is None:
            raise ValueError('Ping Proxy Received a None proxy_list')
        self.len_original_proxy_list = len(proxy_list)
        self.result = []
        self.thread_output_list = []


    def test_proxy(self, thread_number, list_of_proxys, timeout_of_ping):
        logger.info("Tread {} started with {} proxys to test".format(str(thread_number), str(len(list_of_proxys))))
        string_size_proxy_list = str(len(list_of_proxys))
        size_proxy_list = float(len(list_of_proxys))
        self.thread_output_list[thread_number] = 0.0
        number_of_checked_proxys_from_list = 0
        local_reesult = []

        # Ping each Proxy to find out which ones are working <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        for item in list_of_proxys:
            delay = ping(item[0][:item[0].find(":")], unit='ms', timeout=timeout_of_ping)

            # Try access some site using the Proxy <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            if delay is not None:
                if delay < self.maximum_delay_in_ms:
                    proxy_used_in_this_round = item[0]
                    local_reesult.append([item[0], item[1], delay])
            number_of_checked_proxys_from_list += 1

            b = number_of_checked_proxys_from_list/size_proxy_list
            self.thread_output_list[thread_number] = b
        # Add Local Result to Global
        self.result = self.result + local_reesult
        b = number_of_checked_proxys_from_list/size_proxy_list
        self.thread_output_list[thread_number] = b


    def chunk(self, list_to_be_splited_equally,num):
        logger.info("Separating the list of {} proxys in equal chunks of {}".format(str(len(list_to_be_splited_equally)),
                                                                                    str(num)))
        avg =len(list_to_be_splited_equally) / float(num)
        out = []
        last = 0.0
        while last < len(list_to_be_splited_equally):
            out.append(list_to_be_splited_equally[int(last):int(last+avg)])
            last += avg
        return out

    # def printing_thread(self, interval):
    #     first_time_before_open_first_thread = True # When it starts there is no thread Running ....
    #     one_alive = True
    #     while one_alive or first_time_before_open_first_thread:
    #         one_alive = False
    #         for t in self.threads:
    #             if t.is_alive():
    #                 one_alive = True
    #                 first_time_before_open_first_thread = False
    #         # os.system('cls' if os.name == 'nt' else 'clear')
    #         percentage = 0
    #         sum = 0
    #         for item in self.thread_output_list:
    #             sum += item
    #             # print(str(item))
    #         percentage = sum/self.number_of_threads
    #         print("------>>>>>>>>>>>" + str(percentage))
    #         time.sleep(interval)

    def start(self):
        start = time.time()
        # Dividing the proxy_list in chuncks equal to the number of threads
        self.proxy_list = self.chunk(self.proxy_list, self.number_of_threads)
        # # Create Thread Responsible for printing updates on the screen
        # thr = threading.Thread(target=self.printing_thread, args=(self.print_refresh_rate,))
        # thr.start()  # Start Thread

        # Start test_proxy THREADS !!!!!!
        for item in range(self.number_of_threads):    # Strart test_proxy THREADS !!!!!!
            logger.info("Starting {} threads".format(str(self.number_of_threads)))
            t = threading.Thread(target=self.test_proxy, args=(item, self.proxy_list[item], self.timeout_of_ping))
            self.thread_output_list.append(" ")
            t.start()
            self.threads.append(t)
            time.sleep(self.wait_before_launch_new_thread)
        # Join test_proxy THREADS !!!!!!
        for t in self.threads:
            t.join()

        logger.info("Sorting the results by the delay")
        # Sort the list
        result = sorted(self.result, key=itemgetter(2))

        end = time.time()
        logger.info("Checked !!!! {} proxys in {} seconds resulting in {}".format(str(self.len_original_proxy_list),
                                                                                     str(end - start), str(len(result))))
        return result