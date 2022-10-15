import pandas as pd
from googleapiclient.discovery import build
import multiprocessing
import time

API_KEY = "AIzaSyAg2BK_1PW1UaVbVkcxRYErA4lye8tCCp4"
CSE_ID = "e3809d7dad3914c1d"
SERVICE = build("customsearch", "v1", developerKey=API_KEY)
ENGINE = SERVICE.cse()


def search(domain):
    result = ENGINE.list(q=" ", cx=CSE_ID, siteSearch=f"{domain}", num=1).execute()
    return result["queries"]["request"][0]["totalResults"]

def search_concurrenct(domains):
    with multiprocessing.Pool as pool:
        return pool.map(search, domains)

if __name__ == "__main__":
    df = pd.read_excel("domains.xlsx")
    domains = df["domains"]

    start_time = time.time()
    results = search_concurrenct(domains)
    duration = time.time() - start_time

    print(f"Downloaded {len(domains)} in {duration} seconds")

    df["indexed_pages"] = pd.Series(results)
    df.to_excel("domains.xlsx")