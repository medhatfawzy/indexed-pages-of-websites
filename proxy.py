from selenium import webdriver

def proxy():
    PROXY_LIST = [
                ["https://130.41.55.190",  8080],
                ["http://139.59.1.14", 8080],
                ["http://110.238.74.184",  8080],
                ["http://169.57.1.85", 8123],
                ["http://82.165.105.48",  80],
                ["http://3.111.155.124",  80]
                ]
    
    for i in range(len(PROXY_LIST)):
        host = PROXY_LIST[i][0]
        port = PROXY_LIST[i][1]

        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", host) 
        profile.set_preference("network.proxy.http_port", port) 
        profile.set_preference("network.proxy.ssl", host) 
        profile.set_preference("network.proxy.ssl_port", port)
        yield profile