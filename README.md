# Ludus
Ludus is a gamification framework for Github and Trello. It can also be extended to other version control and project management tools like Gitlab, Jira etc. This application has been configured with 11 events and 15 badges currently. You can design and contribute more events or badges as per your needs.</br> 
The Ludus project was completed as a part of the Summer Internship program at **Red Hat Inc**.

## Motivation

According to TalentLMS Gamification at Work Survey 2018, about 85 % of employees agreed that they would spend more time on the gamified software. Our motivation behind Ludus is to bring a positive transformation in the software industry by the gamification of Version Control and Project Tracking tools.

## Architecture

![architecture](/docs/architecture.png)

## Getting started

These instructions will get you a copy of the project up and running on a live OpenShift Cluster.

### Prerequisites

You need to first setup Open Data Hub on a OpenShift cluster. For more information on the Open Data Hub architecture and installation go [here](https://opendatahub.io/arch.html). You can also opt for seperate deployment of Kafka along with	Elasticsearch, Logstash and Kibana. Refer [this](https://dzone.com/articles/deploying-kafka-with-the-elk-stack) tutorial.

### Deployment

To deploy Event Listener application on an OpenShift cluster use the following command with required parameters:
        
```
oc process -f openshift/ludus.event_listener.deployment.template.yaml -p GITHUB_URL=<github_url> KAFKA_TOPIC=<kafka_topic_name> KAFKA_BOOTSTRAP_SERVER=<kafka_bootstrap_server>| oc apply -f -
```

- `GITHUB_URL`: The url of the forked github repository of ludus. The default is https://github.com/akhil-rane/Ludus.git

- `KAFKA_TOPIC`: The name of the kafka topic where event lister will publish the incoming events. The default is ludus_awarder

- `KAFKA_BOOTSTRAP_SERVER`: The hostname and port of the the kafka bootstrap server. The valid format is hostname:port


To deploy Awarder application on an OpenShift cluster use the following command with required parameters:
        
```
oc process -f openshift/ludus.awarder.deployment.template.yaml -p GITHUB_URL=<github_url> KAFKA_TOPIC=<kafka_topic_name> KAFKA_BOOTSTRAP_SERVER=<kafka_bootstrap_server> AWARDER_NAME=<awarder_name> AWARDER_PORT=<awarder_port> EVENTS_TABLE_NAME=<events_table_name> BADGES_TABLE_NAME=<badges_table_name> | oc apply -f -
```

- `GITHUB_URL`: The url of the forked github repository of ludus. The default is https://github.com/akhil-rane/Ludus.git

- `KAFKA_TOPIC`: The name of the kafka topic where event lister will publish the incoming events. The default is ludus_awarder

- `KAFKA_BOOTSTRAP_SERVER`: The hostname and port of the the kafka bootstrap server. The valid format is hostname:port

- `AWARDER_NAME`: The name of the awarder application. This should be unique per kafka cluster. You can scale it to distribute event processing load

- `AWARDER_PORT`: The port number of the awarder application

- `EVENTS_TABLE_NAME`: The table where events data of the user will be stored by awarder. This should be unique per kafka cluster.
        
- `BADGES_TABLE_NAME`: The table where all previously awarded badges for the user will stored by the awarder.This should be unique per kafka cluster

If Event Listener application is not behind the firewall, the hostname of the 'event-listener-route' Route on the OpenShift Cluster will be the `LUDUS_URL`. This can be used to configure the webhooks 

If Event Listener application is behind the firewall, we need to configure [ultrahook](http://www.ultrahook.com/faq) to receive webhooks behind the firewall. Register and get your `ULTRAHOOK_API_KEY` [here](http://www.ultrahook.com/register). Please remember the `WEBHOOK_NAMESPACE`. This will be unique for your ultrahook account.


To deploy Ultrahook on an OpenShift cluster use the following command with required parameters:
        
```
oc process -f openshift/ludus.ultrahook.deployment.template.yaml -p ULTRAHOOK_API_KEY=`echo -n "<ultrahook_api_key>" | base64` ULTRAHOOK_SUBDOMAIN=<ultrahook_subdomain> ULTRAHOOK_DESTINATION=<event_listener_hostname> | oc apply -f -
```

- `ULTRAHOOK_API_KEY`: The api key unique to each ultrahook account

- `ULTRAHOOK_SUBDOMAIN`: A subdomain of your namespace
- `ULTRAHOOK_DESTINATION`: The hostname of the 'event-listener-route' Route on OpenShift cluster

If you registered your account with the 'ludus.ultrahook.com' as your `WEBHOOK_NAMESPACE` and later deployed the ultrahook with `ULTRAHOOK_SUBDOMAIN` as 'redhat', your `LUDUS_URL`will be 'http://redhat.ludus.ultrahook.com'

### How to configure github and trello webhooks?

To set up a github webhook, go to the settings page of your repository or organization. From there, click Webhooks, then Add webhook. Now enter/configure following details:

- `Payload URL`: `LUDUS_URL`
- `Content type`: application/json
- `Which events would you like to trigger this webhook?`: Send me everything
  
To set up a trello webhook, please follow the instructions given [here](https://developers.trello.com/page/webhooks).

### How to configure a new event?

Before adding new events and badges we need to fork this repository. Once you push newly added events and badges, you can use the URL of the forked repository as the `LUDUS_URL` while deploying your application.

To configure a new event follow the steps given below:

- Create a schema for your new event using [jsonschema](https://pypi.org/project/jsonschema/), put it in a python file and add this file to the 'validators' directory. A sample validator file content for Github Comment event is given below
```
schema = {
    "type" : "object", 
    "properties" : {
        "comment" : {
            "type" : "object",
        }
    },
    "required": ["comment"]
}
```

- Create a [jinja](https://jinja.palletsprojects.com/en/2.10.x/) template for your new event that formats the json event payload. Add this file to the formatters directory. A sample formatter template for Github Comment event is given below
```
{
    "username" : "{{ event['sender']['login'] }}",
    "timestamp" : "{{ timestamp }}",
    "event_source" : "github",
    "event_url" : "{{ event['comment']['html_url'] }}",
    "event_type" : "github_comment",
    "raw_github" : {{ json_event }}
}
```

- Add this new event to event_configuration.py file in configs directory. You have to also add validator's schema object and the name of the formatter template to it. A sample configuration for Github Comment event is given below
```
'github_comment': {
        'validator': github_comment_validator.schema,
        'formatter': 'github_comment_formatter'
    }
```

### How to configure a new Badge?

- Currently you can configure badges with 3 different types of criteria
- `every_event` criteria is used when you want to award a badge on every occurrence of the event associated with the badge. A sample configuration for a badge with this criteria is given below
```
'finisher': {
        'description': 'awarded for moving a card in the completed list',
        'event_type': 'task_completed',
        'criteria': {
            'type': 'every_event'
        },
        'image_file': None
    }
```
 
 `description`: General information about the badge

 `event_type`: Type of the event for which badge will be awarded

 `criteria.type`: Type of the criteria for awarding the badge. Here criteria is to award the badge for every occurrence of `event_type`

 `image_file`: Path of an image associated with the badge. Not supported yet 

- `match` criteria is used when you want to award a badge for certain amount of events, associated with the badge, have occurred. This badge is awarded only once per user. A sample configuration for a badge with this criteria is given below
```
'first-github-comment': {
        'description': 'awarded for first github comment',
        'event_type': 'github_comment',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    }
```
 
 `description`: General information about the badge

 `event_type`: Type of the event for which badge will be awarded

 `criteria.type`: Type of the criteria for awarding the badge. Here criteria is to award badge when count of `event_type` for a particular user reaches `criteria.value`

 `criteria.value`: A count value that satisfies this criteria

 `image_file`: Path of an image associated with the badge. Not supported yet 

- `match` criteria is used when you want to award a badge when certain events occur which are matched on a field in the event's json. This field's name can be different for every event but content is equal. A sample configuration for a homerun badge with this criteria is given below. It is awarded when a user creates an issue on github, creates a pull request for the issue, gets it reviewed and merged. The matching filed here is the issue number
```
'homerun': {
        'description': 'awarded for opening an issue, creating pull request, closing the issue',
        'criteria': {
            'type': 'match',
            'matching_events': [
                {
                    'event_type': 'issue_closed',
                    'field': 'raw_github.issue.number'
                },
                {
                    'event_type': 'pull_request',
                    'field': 'issue_closes'
                },
                {
                    'event_type': 'issue',
                    'field': 'raw_github.issue.number'
                }
            ]
        },
        'image_file': None
    },
```
 
 `description`: General information about the badge

 `criteria.type`: Type of the criteria for awarding the badge. Here criteria is to award badge when certain events occur which are matched on a `field` in the event's json

 `criteria.matching_events.event_type`: Type of the event to be matched

 `criteria.matching_events.field`: The name of the field in the event's json to be matched

 `image_file`: Path of an image associated with the badge. Not supported yet 

- Create a badge with one of the above criteria and put it in badge_configuration.py file in the configs directory

## Sample Kibana Dashboard Screenshots

You need to create your own kibana dashboard using the event and badges data stored in the elasticsearch index. Please refer [this](https://www.elastic.co/guide/en/kibana/6.2/dashboard-getting-started.html) tutorial for the same. Following are the sample layouts for reference.  

![dashboard_screenshot_1](/docs/dashboard_screenshot_1.png)

![dashboard_screenshot_2](/docs/dashboard_screenshot_2.png)

## Built With

* Python - interpreted, high-level, general-purpose programming language
* Flask - web framework written in python 
* Kafka - distributed streaming platform 
* Faust - stream processing library, porting the ideas from Kafka Streams to Python
* Elasticsearch - search engine based on the Lucene library
* Kibana - data visualization plugin for Elasticsearch
* Docker - tool to create, deploy, and run applications by using containers
* OpenShift - kubernates based container orchestration platform

## Credits

* [AICoE](https://github.com/AICoE)
* [Open Data Hub](https://opendatahub.io/)
* [Faust](https://github.com/robinhood/faust)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/akhil-rane/ludus/blob/master/LICENSE) file for details
