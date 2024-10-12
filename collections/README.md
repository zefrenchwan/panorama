# Collections 

Code to deal with data collections. 

## Workflow

1. A server is up and periodicaly receives a wake-up call
2. Said server finds tasks to run and starts them 
3. Tasks run at their own pace and push data to a storage system for a further analysis

## Collection 

* `stdcollector` is default collection system: it reads the whole site. If keywords are specified, then only pages with that keywords are transmitted (but all pages are read to find that content)
* `searchcollector` uses a web search engine to collect keywords results. By definition, no keyword makes no sense. 