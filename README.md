# proxy_manager_python
Scrape proxy lists from various sources, remove repeated ant then ping each one of them for later use. Keep tabs on the number of working proxies avaliable and updates the list on demand.


This module manage all proxy related problems like acquiring receiving get requests and probing rate of the proxys
that will be given.

USAGE 
When object is created, it runs self.load_proxy_list() and load proxys....
object = ProxyManager(minimum_number_of_proxys, probing_rate)

get()   -> Give a proxy to be probed or alredy worked

worked(proxy)  -> Receive a proxy that worked
fail(proxy)  -> Receive a proxy that failed
