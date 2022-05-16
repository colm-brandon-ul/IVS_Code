from website_parser import get_website
from website_parser.information_extraction import information_extraction
import logging
import threading
import time
import requests

def thread_function(href):
    logging.info("Thread: starting", str(href))
    res = requests.get(href)
    logging.info("Thread: finishing",str(href) + " " + str(res.status_code))
    




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    start = time.time()
    url = 'https://www.thebrighterside.news/post/innovation-generates-1-000x-more-voltage-from-solar-cells'
    gW = get_website.Get_Website(url)
    res = gW.get_website()
    iE = information_extraction.Information_Extraction(
        url = res['content']['url'],
        html = res)
    data = iE.extract_information()

    end_extraction = time.time()

    threads = list()
    for lo in data['content']['network_data']['content']['links']:
        if lo['internal'] != True:
            x = threading.Thread(target=thread_function, args=(lo['href'],))
            threads.append(x)
            x.start()
    #time.sleep()
    #for index, thread in enumerate(threads):
    #    logging.info("Main    : before joining thread %d.", index)
    #    thread.join()
    #    logging.info("Main    : thread %d done", index)
    
    print('First Website', end_extraction - start)
    print("END TIME ",time.time() - end_extraction)