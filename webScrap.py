import concurrent.futures
import os
import re

from dataflow import File
from proxy import proxy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By



def update_proxy():
    service = Service(os.path.join(os.getcwd(), "web-driver", "geckodriver"))
    opts = Options()
    opts.binary_location = FirefoxBinary(os.path.join("/usr/bin/firefox"))

    profile = next(proxy())
    driver = webdriver.Firefox(options=opts, 
                                    service=service,
                                    firefox_profile=profile)
    return driver



def search_domain(domain):
    service = Service(os.path.join(os.getcwd(), "web-driver", "geckodriver"))
    opts = Options()
    opts.binary_location = FirefoxBinary(os.path.join("/usr/bin/firefox"))
    driver = webdriver.Firefox(options=opts, 
                                    service=service)
    
    driver.get(f"https://www.google.com/search?q=site%3A{domain}")
    result = driver.find_element(By.ID, "result-stats")

    if result.text:
        indexed_count =  int(re.search(r' (\d+,)*\d+ ', result.text).group().replace(",", ""))
        driver.close()
        return indexed_count
    else:
        driver = update_proxy()
        search_domain(domain)

def search_domains(domains):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_url = {executor.submit(search_domain, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            print(f"url {url}")
            try:
                data = future.result()
                print(f"data: {data}")
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))



if __name__ == "__main__":
    data_file = File("domains.xlsx")
    domains = data_file.get_domains()
    results = search_domains(domains)

    print(results)
    data_file.save_results(results, path="results.xlsx")