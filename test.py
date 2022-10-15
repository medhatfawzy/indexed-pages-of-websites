import pandas as pd
from googleapiclient.discovery import build
import multiprocessing
import time

API_KEY = "AIzaSyDUHTaHf2thcw5prhMnszrKXWnahmGWoJg"
CSE_ID = "9444c97a6a5064662"
SERVICE = build("customsearch", "v1", developerKey=API_KEY)
ENGINE = SERVICE.cse()


def download_site(domain):
    response =  ENGINE.list(q=" ", cx=CSE_ID, siteSearch=f"{domain}", num=1).execute()
    return response["queries"]["request"][0]["totalResults"]

def download_all_sites(domains):
    with multiprocessing.Pool() as pool:
        return pool.map(download_site, domains)

if __name__ == "__main__":
    df = pd.read_excel("domains.xlsx")
    domains = df["domains"]
    
    start_time = time.time()
    results = download_all_sites(domains)
    duration = time.time() - start_time

    print(f"Downloaded {len(domains)} in {duration} seconds")
    
    df["indexed_pages"] = pd.Series(results)
    df.to_excel("domains.xlsx")