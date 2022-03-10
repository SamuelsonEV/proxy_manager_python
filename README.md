NAME
  Proxy Manager

# proxy_manager_python
Scrape proxy lists from various sources, remove repeated, then ping each one of them.
Keep tabs on the number of working proxies avaliable and updates the untested proxys list when running low.


USAGE 
When object is created, it runs self.load_proxy_list() and load proxys....

object = ProxyManager(minimum_number_of_proxys, probing_rate)

get()   -> Give a proxy to be probed or alredy worked

worked(proxy)  -> Keep tabs on proxy that worked
fail(proxy)  -> Keep tabs on proxy that failed


