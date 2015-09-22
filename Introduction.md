# Introduction #
## Overview ##
ConnectTheDots is put together to demonstrate the power of Azure IoT and its use of data from various devices.  It's built off the assumption that the sensors get the raw data and format it into a JSON string.  That string is then shuttled off to the Azure Event Hub, where it gathers the data and displays it as a chart.  Optional other functions of the Azure cloud include sending alerts and averages, however this is not required.

The JSON string is sent to the Event Hub one of two ways: packaged into an AMQP message or in a REST packet.  This can be done via a Gateway, which is how the [Getting Started](GettingStarted.md) sample does it, or through a device that is directly connected to the Event Hub, if the device is capable.  More details on each of those options are below.


## Device basics ##
The current project is built on the premise that data from sensors is sent to an Azure Event Hub in a prescribed JSON format. The minimum structure, with required attribute names, is 

    {
	"guid" 			:	"string",
	"organization"	:	"string",
	"displayname"	:	"string",
	"location"		:	"string",
	"measurename"	:	"string",
	"unitofmeasure"	:	"string",
	"value" 		:	double/float/integer,
	"timecreated"   :   "string"
	}
	
This should all be sent as one string message to the Event Hub, for example as the following strings: 
Note that timecreated field is in UTC ordinal formatting.

     {"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"Microsoft Singapore DX Team","timecreated":"2015-09-22T13:39:06.6400000Z","displayname":"Arduino + Raspiberry Pi 2 on Windows","location":"SG MIC","measurename":"humidity","unitofmeasure":"%","value":52.00}
   

Furthermore, the project is built upon the premise that the *sensors* create and format this JSON string. For example, if using a sensor attached to an Arduino, the code running on the Arduino would send successive JSON strings, CRLF ended, out the serial port to a gateway such as a Raspberry Pi or Windows Tablet. The gateway does nothing other than receive the JSON string, package that into an AMQP message, and send it to Azure. In the case of a directly connected device, the latest needs to send the JSON package to the event hub whether encapsulating the JSON message in an AMQP message or sending the JSON message in a REST packet.

All the device code included in this project, or submitted for inclusion, must conform to the JSON format requirement above. 

### Devices and Gateway ###
ConnectTheDots provides a Gateways in different language implementation to collect data from devices that can and cannot target the cloud directly. The Gateway Projects are named appended with "sender" in the folder name and is a simple sending service to eventhub. 

## Software prerequisites ##
In order to reproduce one of the project scenarios, you will need the following:

Common Stack

	1. Microsoft Azure subscription ([free trial subscription](http://azure.microsoft.com/en-us/pricing/free-trial/) is sufficient)
	2. Python 2.7.x for your CPU Architecture [Windows x86 and x64](https://www.python.org/downloads/) or [MacOS] (https://www.python.org/downloads/mac-osx/)
		a. Do remember to set your environment variable for your installed folder containing Python.exe 
	3. Node 0.10.40 [Windows x64](https://nodejs.org/dist/v0.10.40/x64/node-v0.10.40-x64.msi) or [MacOS] (https://nodejs.org/dist/v0.10.40/node-v0.10.40.pkg)
		a. a. Do remember to set your environment variable for your installed folder containing node.exe 
	4. Visual Studio Code https://code.visualstudio.com/

Microsoft Specific Stack 

	1. Visual Studio 2015 Recommended – [Community Edition](http://www.visualstudio.com/downloads/download-visual-studio-vs) is sufficient
	2. Node JS Tools for Visual Studio 2015 https://www.visualstudio.com/en-us/features/node-js-vs.aspx
	3. Azure SDK for Visual Studio [Select the latest version here](http://azure.microsoft.com/en-us/downloads/)
	4. Python Tools for Visual Studio https://www.visualstudio.com/en-us/features/python-vs.aspx


## Where to start ##
If this is you're first time with the project, we suggest you head over to the [Getting Started project](GettingStarted.md) to learn the basics.  If you'd like to create your own solution with Azure IoT, check out the [supported devices](SupportedDevices.md).



