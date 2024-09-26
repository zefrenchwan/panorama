# Webscraping

Requesting the web may be:
* random walks from search engines, looking for data based on keywords (the usual google use case)
* random walks from search engines, looking for what said engine would recommend (google news for instance)
* specific website reading, looking for data based on keywords (looking for information about a topic from wikipedia, for instance )
* specific website reading, looking for what is new from that website (looking for what tiktok suggests, for instance)

A collector (something that collects data) is an abstract data collection tool. 
General contract is simple:
* A scheduler activates a collector so it starts to load data. 
* Collector defines its own collecting strategy
* It stores collected documents for a later asynchronous processing 


## Useful links 
* [How to use selenium and chrome with docker](https://stackoverflow.com/questions/53657215/how-to-run-headless-chrome-with-selenium-in-python)