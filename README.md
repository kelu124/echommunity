## Objective: providing the echOmmunity with a clear mapping of the mapping

### Data

Possible data per user:

* Country
* City
* Keywords
    * Keywords could be separated into 2 categories : roles in echOpen / skills
    * Keywords must be chosen from a pre-defined list
* Nick on slack
* Channels on slack
* People mentionned by user on slack
* Mentions of user by other people on slack
* Nick on basecamp
* Github account
* Programming skills (languages, databases, ...)

#### Origin of the data

* Former CSVs
* Questionnaires through a bot asking people with private messages on Slack
* Bot crawling slack to see mentions of people by others
* Bot crawling, seeing who is following what (github, slack channel)

Channels of capture: slack, github, ...?

### Deliverables

#### Graphs

##### How ?

1. Bots crawling slack / forms --> store as .csv files
2. Python+neo4j --> update graph database 
3. Python+neo4j --> queries for personnalized suggestions --> results stored as .csv files
4. Delivery : 
    * Slack bot sending private message to user
    * Webpage for "global" informations about the community 

##### What ?

* Mapping people by geography
* Mapping by interest
* Connecting

#### Recommendation:

Have an algo recommend you:

* to connect with the 3 most similar profiles
* to subscribe to the three most interesting channels on slack
    * Query of type : " Most popular channels among people who have your skills/interests..."
* to connect with slack members
    * Query of type : "People who have your skills/interest also interact with..."
* to follow on github the three most interesting projects for you 
    * Query of type : "People who have your skills/interests contribute to..."


### Doing..

Slack:

* `data[channel][userid]` to list user id
* `data[channel][userid][posts]` 
* `data[channel][userid][links]` 
* `data[channel][userid][mention]`: pairs of id mentionned / # of mention 
* `data[channel][userid][category]`: int of terms used in each category (see below)


Categories:

* Hardware: pcb, electronic, fpga, cpld, stm32, arduino, power, pulser, kicad, 
* Software: code, android, java, 
* Legal: patent, agreement, cla, 
* Medical: doctor, patient,
* Design: design, user, 
* Community: graph, community, communication, event, contribution, contributor, wiki

### Todo

* Include reactions to link two users
* 
