# Azure Prep #
The Connect The Dots implementation requires a number of Azure resources and services that need to be created prior to adding devices to the infrastructure, as various configuration parameters for the devices will be depend upon the specific Azure resources created. While these resources can be created manually, in this project we have provided a script that automates this process, described below. It assumes you have all the necessary software and subscriptions and that you cloned or downloaded the ConnectTheDots.io project on your machine.

## Prerequisites ##

## Create Azure resources for IoT infrastructure ##

###Create Event Hubs###

1. Launching http://manage.windowsazure.com
2. Selecting +New, App Service, Service Bus, Event Hub, Custom Create
3. Type in "ehdevices" for eventhub name 
4. Select "Southeast Asia" for region, and enter an unique value for the namespace"
5. Enter "8" for Partition Count, and "7" for Retention

Repeat the steps above, with slight variations

1. Launching http://manage.windowsazure.com
2. Select "Service Bus" in the left hand menu, click on your namespace
3. Click on "Eventhubs", and select "ehdevices". Later repeat step 4 onwards for "ehalerts"
4. Click on Configure	
5. Add new policies based on this table, and save.
	
	Policy Name			 Permissions
	D1						Send
	D2						Send
	D3						Send
	D4						Send
	Website					Manage, Send, Listen
	StreamingAnalytics		Manage, Send, Listen

6. Click on consumer group and add "nodejsconsumergroup". Repeat from step 4 for "ehalerts"


