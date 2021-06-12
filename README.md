# Notifications System

### Description:
This should allow users to send 3 types of notifications which is (Push Notifications, Email, SMS).

### Requirements:
- Notifications should be received as soon as possible
- If the system is under high workload, a light delay is acceptable
- Should be scalable
- Notifications can be triggered to be scheduled (added to queue), or being sent immediately


### Expectations:
Expecting daily notifications equal 10 million mobile push notifications, 1 million SMS messages, and 5 million emails.

## System Architecture:
_**Notification Handlers:**_ A handler should be implemented for each type of notifications, so currently there is 4 below classes:
- `NotificationHandler:` Base abstract class for handlers 
- `Email Handler`
- `SMS Handler`
- `Push Handler`

_Notification handler is determined based on the message `type` attribute sent._

_**Message Queue:**_ Which consists of the following classes:
- `MessageQueue:` Base abstract class for handling publishing / subscribing for message queues
- `RabbitMQ:` which implements `MessageQueue` publish and subscribe methods to handle the rabbitmq message broker
- `GcpPubSub:` to be implemented to handle google cloud pub/sub support as a message broker for the system 

_Message Queue is being injected as a preference for the application which can be configured in the file `dependencies.py`_

`service.py`: the class `NotificationServer` which is responsible for initializing the correct Notification Handler based on the message type and sending through it.  

`main.py`: Responsible for adding two flask REST API in order to allow clients to send notifications through the below endpoints:
1. POST `/syncNotify`: this is for sending a notification immediately by skipping adding it to the queue. 
2. POST `/asyncNotify`: this is for sending a notification by adding it to the message broker:

Both methods request / response are exactly same.

Endpoint: `http://localhost:5000/syncNotify`

**Example request:**
```
{
    "type": "SMS",
    "notifiable": "+201122009002",
    "message": "Message"
}
```

**Success Response:**
```
Body:
{
    "success": true
}

Status Code: 200
```

**Failure Response:**
```
Body: 
{
    "success": false,
    "message": "<Failure Message>"
}

Status Codes:
400: In case of invalid inputs.
500: In case of notification sending failure / server error.
```
## Getting Started:
You can start this by navigating to root project directory and running the following docker command
```docker-compose up```
This should run 3 services:
- _**web:**_ for handling the flask rest APIs
- **_worker:_** running a subscriber / consumer for handling the new notifications added to the broker.
  Note that docker compose file adjusted to run 3 worker nodes.
- **_rabbitmq:_** which we use as our message broker.

### TODO:
1. Add unit / integration tests
2. Add logging for the message being sent, we can use an RDBMS such as MySQL to log the notifications including a flag if it's sent or not yet.
