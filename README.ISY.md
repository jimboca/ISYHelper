
# ISY Programs to monitor the ISYHelper

These are the programs I have started using to make sure ISYHelper is running.   For
these to work you must have the DateAndTime Helper enabled.

## ISYHelper Pong Watch

This runs and restarts whenever the ISYHelper Pong variable changes.
The Status variable is set to 1 to indicate everything is good, but
if the Wait completes it will set Status to 2.
The Wiat time should be larger then the interval you have specified
in the ISYHelper DateAndTime Module.

```
If
        $s.IH.DateAndTime.Pong >= 0
 
Then
        $s.IH.DateAndTime.Pong.Status  = 1
        Wait  1 minute and 30 seconds
        $s.IH.DateAndTime.Pong.Status  = 2
```


## ISYHelper Problem

This sends a notification any time the Status variable is changed to a value that is not 1.

```
If
        $s.IH.DateAndTime.Pong.Status is not 1
 
Then
        Send Notification to 'Pushover-Default' content 'ISYHelper Problem'
 ``` 

## ISYHelper Prog Watch

This makes sure the Pong Watch program is running.  This can happen if the ISY is restarted and ISYHelper does not reconnect to the ISY.

```
If
        $s.IH.DateAndTime.Pong.Status is 1
    And Time is Last Run Time for 'ISYHelper Pong Watch' +  2 minutes
 
Then
        $s.IH.DateAndTime.Pong.Status  = 3
``` 

## Notification content

The notification content specified in ISYHelper should look like this.  You can create this
in the admin console Configuration -> Emails/Notifications -> Customizations

Subject: ISYHelper Status

Body:
```
Ping=${var.2.139}
Pong=${var.2.137}
Status=${var.2.153}
---Status Key---
0 = Pong check program never run? ISYHelper never run?
1 = Pong OK (normal status)
2 = Pong missed (ISYHelper dead, or can't connect to ISY?)
3 = Pong check program not running
----------------
```





