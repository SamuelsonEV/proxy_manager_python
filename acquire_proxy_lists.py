# TODO Create constructor or methods to give options like local and anonimity.....
'''
This Module Access Known Proxy lists and return a list of proxy list on the format
[[ip, protocol], [ip, protocol], [ip, protocol], [ip, protocol]....]
'''
import time
import json
import logging
from bs4 import BeautifulSoup
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import requests
from lxml.html import fromstring

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

fileHandler = logging.FileHandler('acquire_proxy_lists.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


class scrappe_proxy_lists():
    '''
Uses requests to Access Known Proxy lists and Return them as list.

The method get_all() return a list of proxy list on the format
[[ip, protocol], [ip, protocol], [ip, protocol], [ip, protocol]....]
  - If its not able to find anyone it will return False
'''
    proxy_list=[]
    def get_all(self):
        while len(self.proxy_list) == 0:
            logger.info("Gettimng Proxy lists")
            # ----------------------------- Grab Proxylists !!! --------------------------------------
            try:
                print("-------------------------------First------------------------------------")
                logger.info("Getting First")
                url="https://proxylist.geonode.com/api/proxy-list?limit=1000&page=1&sort_by=latency&sort_type=asc&country=BR&protocols=http%2Chttps%2Csocks4%2Csocks5" #<<<<< PUT IT BACH
                # url="https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=latency&sort_type=asc&country=ID&protocols=http%2Chttps%2Csocks4%2Csocks5"   #<<<<< SLOW ONE
                response = requests.get(url)
                teamidjson = json.loads(response.text)
                for item in teamidjson['data']:
                    # print(item["ip"]+":"+item["port"]+"-"+item["protocols"][0], end="")
                    self.proxy_list.append([item["ip"]+":"+item["port"],item["protocols"][0]])
                print(len(self.proxy_list))
            except:
                print("Failed")

            try:
                print("-------------------------------Second ------------------------------------")
                url2 = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"
                response = requests.get(url2)
                proxy_list2_raw = response.text.splitlines()
                proxy_list2_raw = proxy_list2_raw[9:]
                proxy_list2_raw = proxy_list2_raw[:-2]
                proxy_list2 = []
                for item in proxy_list2_raw:
                    if item.find("S") == -1:
                        protocol = "http"
                    else:
                        protocol = "https"
                    proxy_list2.append([item[:item.find(" ")],protocol])
                self.proxy_list = self.proxy_list + proxy_list2
                print(len(proxy_list2))
            except:
                print("Failed")

            try:
                print("-------------------------------Third------------------------------------")
                proxy_list3 = []
                for it in ["socks4", "socks5", "http"]:
                    url2 = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/{}.txt".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        proxy_list3.append([item[:item.find(" ")], it])
                self.proxy_list = self.proxy_list + proxy_list3
                print(len(proxy_list3))
            except:
                print("Failed")

            try:
                print("-------------------------------Forth------------------------------------")  # <<<<<<<<<<<<<<<<<< Put it alll !!!!!
                proxy_list4 = []
                for it in ["socks4", "socks5", "http"]:
                    url2 = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/{}.txt".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        proxy_list4.append([item[:item.find("::")], it])
                self.proxy_list = self.proxy_list + proxy_list4
                print(len(proxy_list4))
            except:
                print("Failed")

            try:
                print("-------------------------------Fifth------------------------------------")  # <<<<<<<<<<<<<<<<<< Best because geolocation filter option
                proxy_list5 = []
                for it in ["socks4", "socks5", "http"]:
                    url2 = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/{}.txt".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        if item.find("Brazil") != -1:
                            proxy_list5.append([item[:item.find("::")], it])
                self.proxy_list = self.proxy_list + proxy_list5
                print(len(proxy_list5))
            except:
                print("Failed")

            try:
                print("-------------------------------Sixth------------------------------------")
                proxy_list6 = []
                for it in ["socks4", "socks5", "http","https"]:
                    #     mmpx12/proxy-list/master/http.txt
                    url2 = "https://raw.githubusercontent.com/mmpx12/proxy-list/master/{}.txt".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        proxy_list6.append([item[:item.find("::")], it])
                self.proxy_list = self.proxy_list + proxy_list6
                print(len(proxy_list6))
            except:
                print("Failed")

            try:
                print("-------------------------------Seventh------------------------------------")
                proxy_list7 = []
                for it in ["socks4", "socks5", "http","https"]:
                    #     mmpx12/proxy-list/master/http.txt
                    url2 = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/{}.txt".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        proxy_list7.append([item[:item.find("::")], it])
                self.proxy_list = self.proxy_list + proxy_list7
                print(len(proxy_list7))
            except:
                print("Failed")

            try:
                logger.info("Getting Eighth")
                print("-------------------------------Eighth------------------------------------")
                proxy_list8 = []
                # for it in ["socks4", "socks5", "http","https"]:
                for it in ["socks4"]:
                    #    https://api.proxyscrape.com/v2/?request=getproxies&protocol=http
                    url2 = "https://api.proxyscrape.com/v2/?request=getproxies&protocol={}".format(it)
                    response = requests.get(url2)
                    proxy_list_raw = response.text.splitlines()
                    for item in proxy_list_raw:
                        proxy_list8.append([item[:item.find("::")], it])
                self.proxy_list = self.proxy_list + proxy_list8
                print(len(proxy_list8))
            except:
                print("Failed")

            try:
                logger.info("Getting Ninth")
                print("-------------------------------Ninth------------------------------------")
                proxy_list9 = []
                url2 = "https://www.proxynova.com/proxy-server-list/country-br/"
                response = requests.get(url2)
                soup = BeautifulSoup(response.text, features="html.parser")
                found = soup.find_all("tbody")[0]
                found2 = found.find_all("tr")
                for it in found2:
                    try:
                        raw_ip = str(it.find("script"))
                        ip = raw_ip[raw_ip.find("+")+3:raw_ip.find("')")]
                        port = it.find_all("td")[1].text.replace(" ", "").replace("\n", "")
                        proxy_list9.append([ip + ":" + port, "socks5"])
                    except:
                        pass
                self.proxy_list = self.proxy_list + proxy_list9
                print(len(proxy_list9))
            except:
                print("Failed")

            try:
                logger.info("Getting Tenth")
                print("-------------------------------Tenth------------------------------------")
                proxy_list10 = []
                scrapper = Scrapper(category='ALL', print_err_trace=False)
                data = scrapper.getProxies()
                for item in data.proxies:
                    proxy_list10.append(['{}:{}'.format(item.ip, item.port), "http"])
                self.proxy_list = self.proxy_list + proxy_list10
            except:
                print("Failed")

            try:
                logger.info("Getting Eleventh")
                print("-------------------------------Eleventh------------------------------------")
                proxy_list11 = []
                def get_proxies():
                    url = 'https://free-proxy-list.net/'
                    response = requests.get(url)
                    parser = fromstring(response.text)
                    #   print(response.text)
                    proxies = set()
                    for i in parser.xpath('//tbody/tr'):
                        if i.xpath('.//td[7][contains(text(),"yes")]'):
                            #Grabbing IP and corresponding PORT
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            proxies.add(proxy)
                    return proxies
                test = get_proxies()
                for item in test:
                    proxy_list11.append([item, "http"])
                print(len(proxy_list11))
                self.proxy_list = self.proxy_list + proxy_list11
            except:
                print("Failed")

            print("-------------------------------TOTAL ACQUIRED------------------------------------")
            print("TOTAL FOUND : {}".format(len(self.proxy_list)))
            print("-------------------------------REMOVING REPEATED------------------------------------")
            logger.info("Removing Repeated")
            self.proxy_list = list(list(row) for row in (set(tuple(row) for row in self.proxy_list))) # transform in set than back in list
            print("TOTAL WITHOUT REPEATED : {}".format(len(self.proxy_list)))
            print(" inside len(self.proxy_list) == 0       {}".format(str(len(self.proxy_list) == 0)))
            if len(self.proxy_list) != 0:
                return self.proxy_list
            else:
                time.sleep(2)