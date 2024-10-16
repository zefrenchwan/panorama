# panorama
analytics from open source data

MIT License
zefrenchwan, 2024

## Purpose

The purpose of this project is to look for data in the web and agregate them all to display stats.
Data collection, webscraping especially, is a topic per se. 
Some companies deal with this complex issue, and offer solutions to deal with captcha, geoloc, proxies, etc. 
This is a side project, no way to do all of that. 
But defining schedules, analytics, and so on, that, I can do !


General algorithm is to:
1. User defines either websites to read or keywords to find 
2. A scheduler launches data collection based on user requests 
3. Webscraping tasks collect data
4. NLP tasks parse data and try to understand what is going on
5. Data collection and data agregation 
6. User may connect and see what user was looking for

Data may come from many sources (videos, social networks, etc). 
This system should be able to deal with them all, that is to have a plugin system to add new webscrapers. 

## Technical solution 

Panorama is a group of applications: 
1. A end-user web application for users to connect, define their requests see their results
2. A scheduler to launch data collection 
3. Some endpoint apps to collect data and start an asynchronous data flow
4. This data flow passes by text processing, and data agregation 
5. Agregated data is stored and visible by end user

### Auth

Any operation needs to be authenticated and authorized. 
OAuth2 is obvious technical choice. 


### Storage 

There are two main databases: 
1. One for configuration and selectors definition
2. One for analytics (to see results)

Some tactical storages are necessary too:
1. Redis for session management in `interactions`

### Scheduling 

Scheduler will contact a dedicated server to launch the data collection step. 
This server will load database configuration and define collection tasks to run. 

## Installation

1. Define configuration in an `.env` file as descibed below
2. Launch the whole system via a `docker compose up` 

### Security 

**First thing to do: Change file** `interactions/Dockerfile` **to change env values**. 

### The global env file

Create a `.env` file at the same level as `compose.yaml`. 
It will contain all secrets for all subprojects. 

To set configuration database, define in an env file:
* `DBCONF_USER` to define db user 
* `DBCONF_PASS` to define db password 
* `DBCONF_NAME` to define db database name


### Interactions

Both session secret and cookie secret are generated on the fly as random values. 
You may want to use a different security strategy. 