'''
TODO figure out the logic to put minimum_lef_to_probe_before_load_more and minimum_working_proxys on the script
         without breaking it...right now it let`s get to zero before reloading the needed probing proxy`s
'''

'''
This module manage all proxy related problems like acquiring receiving get requests and probing rate of the proxys
that will be given.

USAGE 
When object is created, it runs self.load_proxy_list() and load proxys....
object = ProxyManager(minimum_number_of_proxys, probing_rate)

get()   -> Give a proxy to be probed or alredy worked

worked(proxy)  -> Receive a proxy that worked
fail(proxy)  -> Receive a proxy that failed
'''


from acquire_proxy_lists import scrappe_proxy_lists
from ping_proxys import ping_proxy_list
import random
import logging
import pandas as pd
import time
import threading

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler=logging.StreamHandler( )
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

fileHandler=logging.FileHandler('proxy_manager.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


class ProxyManager:
    def __init__(self, minimum_number_of_proxys, probing_rate):
        logger.info("Instancing minimum_number_of_proxys: {}   probing_rate: {}".format(str(minimum_number_of_proxys),
                                                                                        str(probing_rate)))
        self.minimum_working_proxys = minimum_number_of_proxys
        self.max_consecultive_failures = 4  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< maybe change to receive on instanciation
        self.minimum_lef_to_probe_before_load_more = 32 #  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< maybe change to receive on instanciation
        self.probing_to_working_rate = probing_rate
        self.proxy_list = []
        self.needs_probing = []
        self.worked_before_df=pd.DataFrame(columns = ['Adress', 'Protocol', 'sum_Delays', 'Cons_Failures', 'Attemps'])  # Create empty DF
        self.worked_before = []
        self.worked_before_last_failures = []
        self.how_many_times_probed = 0
        self.probing_new_proxy_was_successful = 0
        self.how_many_times_gave_already_working = 0
        self.thread_load_proxy_list = threading.Thread(target=self.load_proxy_list)
        self.load_proxy_list()

    def load_proxy_list(self):
        logger.info("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV Starting Method: reload_proxy_list(self):")
        start = time.time()
        self.proxy_list = []
        obb = scrappe_proxy_lists()
        proxy_list_raw = obb.get_all()
        logger.info("Finished proxy_list_raw = scrappe_proxy_lists.get_all(scrappe_proxy_lists)")
        print()
        pingged_proxy_list = ping_proxy_list(proxy_list_raw)
        self.proxy_list = pingged_proxy_list.start()
        print("Tested and working proxys: {}".format(len(self.proxy_list)))
        if len(self.worked_before_df) > 0:
            proxy_list_df = pd.DataFrame(self.proxy_list, columns = ['Adress', 'Protocol', 'Delay'])
            # Subrtacting the worked_berofe_df from the proxy_list_df
            proxy_list_df = pd.concat([proxy_list_df,self.worked_before_df, self.worked_before_df]).drop_duplicates(
                subset = ['Adress', 'Protocol'], keep = False)
            proxy_list_df = proxy_list_df.reset_index(drop=True)
            self.needs_probing = proxy_list_df[['Adress', 'Protocol']].values.tolist()
        else:
            self.needs_probing = self.proxy_list  #  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        end = time.time()
        logger.info("-------------------------------------- Method reload_proxy_list() took {} seconds".format(str(end - start)))


    def get(self):
        logger.info("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV Starting Method: get(self):")
        logger.info(" {} Proxys Worked Before while the minimum working proxys required are {}  and there is {} left to probe".format(str(len(self.worked_before)), str(self.minimum_working_proxys), str(len(self.needs_probing))))
        start = time.time()
        # Add Those Later !!!!  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # self.minimum_lef_to_probe_before_load_more
        # self.minimum_working_proxys
        if (len(self.needs_probing) > self.minimum_lef_to_probe_before_load_more ):
            if (len(self.worked_before) > self.minimum_working_proxys):
                # case -> len(probe) > 0  & len(worked) > 0
                if self.how_many_times_gave_already_working == 0:                                        # Repeated code to avoid the case in the first time when how_many_times_gave_already_working == 0
                    log_string = "The  (How_many_probed/how_many_times_gave_already_working) ratio is tending to infinite since how_many_times_gave_already_working == 0 "
                    logger.info(
                        log_string + "giving one that worked Before ")
                    self.how_many_times_gave_already_working += 1
                    end = time.time()
                    logger.info("-------------------------------------- >>>>>>Method get() took {} seconds".format(str(end - start)))
                    return random.choice(self.worked_before)
                # case -> len(probe) > 0  & len(worked) > 0
                if (self.how_many_times_probed / self.how_many_times_gave_already_working) >= self.probing_to_working_rate:
                    log_string = "The  (How_many_probed/how_many_times_gave_already_working) ratio is {} BIGGER than {} probring rate..."
                    logger.info(
                        log_string.format(str(self.how_many_times_probed / self.how_many_times_gave_already_working),
                                          str(self.probing_to_working_rate))+"giving one that worked Before ")
                    self.how_many_times_gave_already_working += 1
                    end = time.time()
                    logger.info("-------------------------------------- >>>>>>Method get() took {} seconds".format(str(end - start)))
                    return random.choice(self.worked_before)
                else:
                    log_string = "The  (How_many_probed/how_many_times_gave_already_working) ratio is {} SMALLER than {} probring rate..."
                    logger.info(
                        log_string.format(str(self.how_many_times_probed / self.how_many_times_gave_already_working),
                                          str(self.probing_to_working_rate))+"giving one to probe ")
                    use_this_proxy = self.needs_probing[0]
                    self.needs_probing.pop(0)
                    self.how_many_times_probed += 1
                    end = time.time()
                    logger.info("-------------------------------------- >>>>>>Method get() took {} seconds".format(str(end - start)))
                    return [use_this_proxy[0], use_this_proxy[1]]
            else:
                # case -> len(probe) > 0  & len(worked) == 0
                logger.info(" {} Proxys Worked Before while the minimum working proxys required are {}  and there is {} left to probe".format(str(len(self.worked_before)), str(self.minimum_working_proxys), str(len(self.needs_probing))))
                use_this_proxy = self.needs_probing[0]
                self.needs_probing.pop(0)
                self.how_many_times_probed += 1
                end = time.time()
                logger.info("-------------------------------------- >>>>>>Method get() took {} seconds".format(str(end - start)))
                return use_this_proxy
        else:
            # case -> len(probe) == 0 & len(worked) > 0
            logger.info("xxxxxxxxxxxxxx Running LOW on probing PROXYS !!!!!!! TO PROSPECT {} left to probe, and the minimum is: {}".format(len(self.needs_probing), str(self.minimum_lef_to_probe_before_load_more)))
            if not self.thread_load_proxy_list.is_alive():
                print("Beforeeee Started THREADDD !!!!!!!: {}".format(str(self.thread_load_proxy_list.is_alive())))
                self.thread_load_proxy_list = threading.Thread(target=self.load_proxy_list)
                self.thread_load_proxy_list.start()
                print("After Started THREADDD !!!!!!! IS IT RUNNING: {}".format(str(self.thread_load_proxy_list.is_alive())))
            if len(self.worked_before) > 0:
                return random.choice(self.worked_before)

        print()
        logger.info("Getting a proxy !!!!  {} left to probe, and the minimum is: {}".format(len(self.needs_probing), str(self.minimum_lef_to_probe_before_load_more)))
        while (len(self.needs_probing) == 0) & (len(self.worked_before) == 0):     #  ------------------------------------ Can only be tested when run reload proxy as thread
            # case -> len(probe) == 0 & len(worked) == 0                           #  --------------------------------------- If thread already running, just join and wait...
            logger.info("Run out !!!!!!! Proxis to probe:{}        and Working Proxys:{}".format(len(self.needs_probing), len(self.worked_before)))
            print("Run out !!!!!!! Proxis to probe:{}        and Working Proxys:{}".format(len(self.needs_probing), len(self.worked_before)))
            print("Trying to acquire more")
            print("THREADDD !!!!!!! IS IT STILL RUNNING: {}".format(str(self.thread_load_proxy_list.is_alive())))
            if not self.thread_load_proxy_list.is_alive():
                print("Beforeeee Started THREADDD !!!!!!!: {}".format(str(self.thread_load_proxy_list.is_alive())))
                self.thread_load_proxy_list = threading.Thread(target=self.load_proxy_list)
                self.thread_load_proxy_list.start()
                print("After Started THREADDD !!!!!!!: {}".format(str(self.thread_load_proxy_list.is_alive())))
                self.thread_load_proxy_list.join()
                print("After joined THREADDD !!!!!!!: {}".format(str(self.thread_load_proxy_list.is_alive())))
                print()
            else:
                self.thread_load_proxy_list.join()
                print("It was already started ...After joined THREADDD !!!!!!!: {}".format(str(self.thread_load_proxy_list.is_alive())))
                print()

        if len(self.needs_probing) > 0:  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                             ERASE AFTER MAKING load_proxy_list a Thread !!!!!!
            use_this_proxy = self.needs_probing[0]
            self.needs_probing.pop(0)
            self.how_many_times_probed += 1
            end = time.time()
            logger.info("-------------------------------------- >>>>>>Method get() took {} seconds".format(str(end - start)))
            return use_this_proxy

    def worked(self, proxy):
        logger.info("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV Starting Method: worked(self, {}):".format(str(proxy)))
        start = time.time()
        logger.info("Receiving proxy that worked:  {}".format(str(proxy)))
        if (self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1])]).empty:  # Check if its able to find that row !!!!!
            print("Nao Achoooouu, Adicionandooooo ")
            dic = {'Adress': proxy[0], 'Protocol': proxy[1], 'sum_Delays': proxy[2], 'Cons_Failures': 0, 'Attemps': 1}
            self.worked_before_df = self.worked_before_df.append(dic, ignore_index = True)
            self.probing_new_proxy_was_successful += 1
            logger.info("probing_new_proxy_was_successful:  {}   |  how_many_times_probed:  {}".format(str(self.probing_new_proxy_was_successful), str(self.how_many_times_probed)))
            logger.info("round(self.how_many_times_probed/self.probing_new_proxy_was_successful) = ratio_of_probings_ending_successfully:  {}".format(str(round(self.how_many_times_probed/self.probing_new_proxy_was_successful))))
        else:  # If it already exists it will modify the A Column
            print("     Achoooouu, modificando existente")
            # dic = {'Adress': proxy[0], 'Protocol': proxy[1], 'sum_Delays': proxy[2], 'Cons_Failures': 0, 'Attemps': 1}
            self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'Cons_Failures'] = 0
            self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'sum_Delays'] += proxy[2]
            self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'Attemps'] += 1
        print(self.worked_before)
        self.worked_before_df = self.worked_before_df.reset_index(drop=True)
        self.worked_before = self.worked_before_df[['Adress', 'Protocol']].values.tolist()
        print(self.worked_before)
        end = time.time()
        logger.info("-------------------------------------- >>>>>>Method worked() took {} seconds".format(str(end - start)))

    def fail(self, proxy):
        logger.info("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV Starting Method: fail(self, {})):".format(str(proxy)))
        start = time.time()
        print(proxy)
        logger.info("Receiving proxy that FAILED:  {}".format(str(proxy)))
        print(self.worked_before)
        if (self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1])]).empty:  # Check if its able to find that row !!!!!
            print("Nao Achoooouu Na lista de WORKED BEFORE... no need to do anything remove")
        else:  # If it already exists it will modify the A Column >>>>>>>>>>>>>>>>>>>>>>>> IF IT had X consecutive FAILURES .... DELETE IT >>>>>>>>>>>>>>>>>>>>> IMPLEMENT SOMETHING IF IT FALIED TO MUCH
            print("     Achoooouu a Que falhou, Anotando a Falha, ou removendo ....!!!!!")
            self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'Attemps'] += 1
            if self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'Cons_Failures'].values[0] < (self.max_consecultive_failures - 1):
                print("Failed Less than max consecultive failures {}  {}".format(proxy[0], proxy[1]))
                self.worked_before_df.loc[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]), 'Cons_Failures'] += 1
                print("")
            else:
                print(self.worked_before_df)
                print("REMOVING {}  {}".format(proxy[0], proxy[1]))
                self.worked_before_df = self.worked_before_df.drop(self.worked_before_df.index[(self.worked_before_df['Adress'] == proxy[0]) & (self.worked_before_df['Protocol'] == proxy[1]) ]).reset_index(drop=True)
                print(self.worked_before_df)
        print(self.worked_before)
        self.worked_before_df = self.worked_before_df.reset_index(drop=True)
        self.worked_before = self.worked_before_df[['Adress', 'Protocol']].values.tolist()
        print(self.worked_before)
        end = time.time()
        logger.info("-------------------------------------- >>>>>>Method Fail() took {} seconds".format(str(end - start)))
