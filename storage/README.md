# Storage

There are two main databases: 
1. One to store what to collect and how to perform data collection
2. One to store collected data 

## Selectors model

Selectors define what to collect. 
For our use case, it means:
* the system to connect to
* the keywords to look for 
* launching frequency

Then, tasks run to look for selections. 
Each task is launched by a processor. 
For instance, a processor may deal with all google searches, another with all bing searches, etc. 
Given a processor, each task performs a series of loads. 
For instance, when scraping a given website: 
* task is the website data collection 
* each load is a page to inspect and collect