# MVISION EDR - ACTIVITY FEED [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![build status](https://travis-ci.org/mcafee/mvision-edr-activity-feed.svg?branch=master)](https://travis-ci.org/mcafee/mvision-edr-activity-feed)


## OVERVIEW
- Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python).
- ``mvision-edr-activity-feed`` is a command line tool to consume and subscribe to events from MVISION EDR

## What Activity Feed does?
It pulls BusinessEvents and case-mgmt-events and threatEvents from MVISION EDR. 

case-mgmt-events : If you trigger an Investigation from EDR console the details will be pulled by AF. Type will be case-mgmt-events.
Threat-events : New Threats came into Monitoring UI
Businesss Events: EDR Business events such as EDR.UI - dashboard are operational events that aren’t reported in the EDR Monitoring dashboard. But, they’re published to the EDR Activity feed.

Note: Activity Feed pulls only new Threats and not all Detection for the existing Threat as highligted in https://kcm.trellix.com/corporate/index?page=content&id=KB94730 

### Step by Step usage guide:
## **Prerequisites  **
Make sure you have Python 3.9 or later version installed on the machine. Python needs to be updated into Environment variable. 

Step 1: **Download**
Open https://github.com/mcafee-enterprise/mvision-edr-activity-feed and click on "Code" then click "Download Zip". Once the archive downloaded you can extract it if you are performing the activity in Windows machine or copy the extraced folder into the Linux box.

Step 2: **INSTALL**
Open a command prompt (Windows box) or Shell command (in Linux) and navigate to the extraced folder and install activity feed

    python setup.py install
    
Example:
![1](https://user-images.githubusercontent.com/118408597/217475442-4971524b-b1ca-4300-a6c7-5fb66e940ca1.JPG)

Step 3:** Creating the "Client ID" and "Client Secret"**

## Client Credential Generator

To authenticate against the MVISION EDR API, client credentials need to be generated with the [MVISION EDR Credential Generator](mvision_edr_creds_generator.py) first.

1. Log on to MVISION EPO Console using your credentials
2. Go to "Appliance and Server Registration" page from the menu

   ![1](https://user-images.githubusercontent.com/25227268/165046594-7af12d3c-a6fd-43fc-b88f-0381b08b1b9c.png)
3. Click on "Add" button
4. Choose client type "MVISION Endpoint Detection and Response"
5. Enter number of clients (1)

   ![2](https://user-images.githubusercontent.com/25227268/165046797-2a913460-9f84-480e-a3a5-a9c358467e32.png)
6. Click on the "Save" button
7. Copy the "Token" value from the table under the section "MVISION Endpoint Detection and Response"

   ![3](https://user-images.githubusercontent.com/25227268/165047049-6a40a72e-84fc-42a1-80ae-7bbfff9b56e5.png)
8. Pass the token value as the input parameter to the [mvision_edr_creds_generator.py](mvision_edr_creds_generator.py) script

Say you are getting the Token as "**BDNIzOmY**" from step 7 above, then the command you will need to run:
    **python mvision_edr_creds_generator.py -T BDNIzOmY**
![Capture](https://user-images.githubusercontent.com/118408597/218384835-4fe3ac4f-faca-4a9f-bc0e-cb1817d786af.JPG)

Step 4:** Command to use the Activity Feed for downloading new Threat Information**
Go to https://docs.trellix.com/bundle/mvision-endpoint-detection-and-response-install-guide/page/GUID-FC03A249-0BBA-4DFC-AE5A-AF945515836C.html site and understand which URL you need use depending on your Tenant Region.
US-West data center — https://api.soc.trellix.com/
US-East data center — https://api.soc.us-east-1.trellix.com/
Frankfurt data center — https://api.soc.eu-central-1.trellix.com/
Sydney data center — https://api.soc.ap-southeast-2.trellix.com/
Canada data center — https://api.soc.ca-central-1.trellix.com/
Asia Pacific South data center — https://api.soc.ap-south-1.trellix.com/

**command line will be :**

mvision-edr-activity-feed --url https://api.soc.ap-south-1.trellix.com/ --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --module samples.generic --loglevel=debug
Example:
![Capture1](https://user-images.githubusercontent.com/118408597/218386440-040aa429-e143-4448-ad69-dd555df7c7c1.JPG)

Example on how new Threat will look like:
![Capture3](https://user-images.githubusercontent.com/118408597/218387345-444f5299-df51-43f6-af08-b1cb33886fe3.JPG)

   
## COMMAND LINE USAGE

In order to use the CLI, you need credentials in MVEDR.
The CLI has several parameters (as described with
``mvision-edr-activity-feed  -h``):

::

    usage: mvision-edr-activity-feed [-h] [--version] --url URL
                                     [--username USERNAME] [--password PASSWORD]
                                     [--client_id CLIENT_ID]
                                     [--client_secret CLIENT_SECRET] --module
                                     MODULE [--period PERIOD] [--topic TOPIC]
                                     [--loglevel {critical,error,warning,info,debug,notset}]
                                     [--logfile LOGFILE] [--consumer-reset]
                                     [--consumer-group CONSUMER_GROUP]
                                     [--consumer-timeout CONSUMER_TIMEOUT]
                                     [--cert-bundle CERT_BUNDLE] [--config CONFIG]
                                     [--preprod]

    MVISION EDR Event Dispatcher CLI

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --url URL             Base URL for MVISION EDR (default: None)
      --username USERNAME   MVISION EDR Username (default: None)
      --password PASSWORD   MVISION EDR Password (default: None)
      --client_id CLIENT_ID, -C CLIENT_ID
                            MVISION EDR Client ID (default: None)
      --client_secret CLIENT_SECRET, -S CLIENT_SECRET
                            MVISION EDR Client Secret (default: None)
      --module MODULE       Module to register events (default: None)
      --period PERIOD, --wait PERIOD
                            Time (in seconds) between queries to the event API
                            (default: 5)
      --topic TOPIC         Topic to subscribe to (default: ['case-mgmt-events',
                            'BusinessEvents', 'threatEvents'])
      --loglevel {critical,error,warning,info,debug,notset}
      --logfile LOGFILE
      --consumer-reset, --reset
                            Starts the consumer group from the earliest event
                            available. This only works when initializing the
                            consumer group the first time (default: False)
      --consumer-group CONSUMER_GROUP
                            Name for the consumer group to use (default:
                            mvisionedr_events)
      --consumer-timeout CONSUMER_TIMEOUT
                            Time (in seconds) before the consumer is dropped by
                            the Kafka backend. If event processing takes longer
                            than this, then events might be duplicated. (default:
                            300000)
      --cert-bundle CERT_BUNDLE
                            Path to a CA bundle file containing certificates of
                            trusted CAs. (default: )
      --config CONFIG       Configuration key/value pairs for callbacks (default:
                            None)
      --preprod, -PP        Option to generate the authentication token for the
                            preprod environment. (default: False)

      If the CLIENT_ID or CLIENT_SECRET start with a - use a = to pass the value to the script, example: --client_id=-5-zLBzODnco9hQnHqEZKf1mn



## SUBSCRIPTIONS

You need to provide at least one module with your subscriptions for the
CLI to load. The following is an sample subscription:

.. code:: python

    import logging
    from mvision_edr_activity_feed import subscribe


    @subscribe(entity='case', subtype='creation')
    def case_created(event):
        logging.info("CASE CREATED: %s", event)


    @subscribe(entity='case', subtype='priority-update')
    def case_updated(event):
        logging.info("CASE PRIORITY UPDATED: %s", event)


    @subscribe(entity='case', subtype='status-update')
    def case_status_updated(event):
        logging.info("CASE STATUS UPDATED: %s", event)


    @subscribe("user == 'some_user'")
    def custom_subscription(event):
        logging.info("EVENT FOR USER 'some_user': %s", event)

In the first three examples, we are subscribing to the following events: **Case
creation**, **Case priority updates**, and **Case status updates**. On the
last example we are subscribing to events that have a property ``user`` with a
value of ``some_user`` (as defined by the corresponding `JMESPath <http://jmespath.org/>`_ expression)

Note that there are two ways to subscribe to events:

* **Basic**: This is for events that follow out `Event Specification <EVENT_SPEC.rst>`__

    * **entity**: The entity affected by the event.
    * **subtype**: The event subtype, related to the entity.

* **Advanced**: This is for generic events, and uses a `JMESPath <http://jmespath.org/>`_ expression to determine the subscription


## CONFIGURE RSYSLOG IN CASE OF REMOTE LOGGING

In case of using rsyslog for remote logging please follow the documentation explained here: https://www.tecmint.com/setup-rsyslog-client-to-send-logs-to-rsyslog-server-in-centos-7/

rsyslog.conf that can be used as an example: https://github.com/mcafee/mvision-edr-activity-feed/blob/develop/rsyslog.conf


## PARSING RULE IN CASE OF SIEM

In case of a SIEM of type ESM (syslog_forwarder usage), it's recommended to import the following parsing rule to ASP General Parser in order to see the event categorized as MVDER Suspicious Activity (Displayed in Events View with proper details instead of Unknown event): https://github.com/mcafee/mvision-edr-activity-feed/blob/master/RULE_MVISION_EDR_THREAT.xml  


## RUNNING THE EXAMPLES

There are a couple of simple examples that will log event information to
the console. These are executed as follows:

.. code:: shell

    mvision-edr-activity-feed --url https://api-int-cop.soc.mcafee.com/ --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --module samples.generic --loglevel=debug

.. code:: shell

    mvision-edr-activity-feed --url https://api-int-cop.soc.mcafee.com/ --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --module samples.individual --loglevel=debug

You can also mix several modules in a single call:

.. code:: shell

    mvision-edr-activity-feed --url https://api-int-cop.soc.mcafee.com/ --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --module samples.generic --module samples.individual --loglevel=debug

## PARSING RULE ON McAfee SIEM

For convenience a `Docker` image is provided. For running `MVISION EDR` activity feed client and forward threat events to `McAfee ESM` via `syslog`, follow instructions below.

### BUILDING DOCKER IMAGE

To forward events gather from the cloud, a `rsyslog` daemon will run inside the `Docker` container. To reduce the number of events sent to the `ESM` receiver, a filter is applied to discard all logs that doesn't contain `"Threat Detection Summary"` string. All other events will be forwarded to the `ESM` receiver (see [`Dockerfile`](./Dockerfile#22)). `ESM` reciever IP must be provided when building the `Docker` image and cannot be changed later. That means if you need to change the receiver IP, the `Docker` image must be rebuilt.

```bash
docker build --rm --build-arg esm_ip=<ESM_RECEIVER_IP> -t mvision-edr-activity-feed .
```

If you are behind a proxy, add the following parameter while building the image:

```bash
--build-arg HTTP_PROXY="<PROXY_URL_OR_IP:PROXY_PORT>" \
--build-arg HTTPS_PROXY="<PROXY_URL_OR_IP:PROXY_PORT>" \
--build-arg http_proxy="<PROXY_URL_OR_IP:PROXY_PORT>" \
--build-arg http_proxys="<PROXY_URL_OR_IP:PROXY_PORT>" 
```

### RUNNING DOCKER IMAGE

As mentioned before, the `Docker` container spins it's own `rsyslog` daemon. To access `MVISION EDR` resources on the cloud, `client_id` and `client_secret` must be provided.

*Note*: using a service account is advised.

```
docker run mvision-edr-activity-feed \
    --url https://api.soc.mcafee.com \
    --client_id client_id \
    --client_secret client_secret \
    --module syslog_forwarder \
    --loglevel debug

```

If you are behind a proxy, add the following parameter:

```
--env HTTPS_PROXY="<PROXY_URL_OR_IP:PROXY_PORT>"
```

## Setup ESM Datasource

An `ESM` data source holds the location and connection information of your network's sources of data. It acts as a connector to your source of data. To instruct `ESM` to parse `MVISION EDR` threat events an `Advanced Syslog Parser` rule is provided (see [sample rule](./RULE_MVISION_EDR_THREAT.xml)). More information can be found at [McAfee Knowledge Center](https://kc.mcafee.com/corporate/index?page=content&id=PD26993).

### How to setup ESM for parsing MVISION EDR Threat events

* Go to `Policy Editor`. On the menu bar go to `File`, `Import`, `Rules` and click on `Import Rules`. A pop-up windows will prompt.
* Upload `RULE_MVISION_EDR_THREAT.xml` policy.
* Go back to the `Policy Editor` window, select `Advanced Syslog Parser`, and filter the list to locate the rule uploaded on the previous step (i.e. using `Signature ID` or `Name`). Make sure the rule is enabled.
* Disable aggregation (go to Datasources). Make sure rollout policy.
* Rollout the rule if needed (top right corner).

### Add client data sources

* From the `McAfee ESM` dashboard, click the hamburger menu and select `Configuration`.
* On the system navigation tree, select the Receiver, then click the `Properties` icon (small cog wheel).
* Click `Data Sources`, the `Add`.
* `Data Source Vendor` should be `Generic`, and select `Advanced Syslog Parser` as `Data Source Model`.
* Choose a `Name` and provide the `IP` address from which the client will run.
* Make sure port is `514` (`TLS` can be enabled but the port should be changed on the `Dockerfile` as well).
* Click `OK` and `Write` the data source settings to the receiver.


## BUGS AND FEEDBACK

For bugs, questions and discussions please use the
[GitHub Issues](https://github.com/mcafee/mvision-edr-activity-feed/issues).


## LICENSE

Copyright 2019, McAfee LLC

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

