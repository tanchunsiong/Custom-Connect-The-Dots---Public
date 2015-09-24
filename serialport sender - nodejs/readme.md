# Gateway for Windows, Linux and Mac Based OS  #
The basic premise of this project is that data from sensing devices can be sent upstream in a prescribed JSON format. This might be achieved by programming the devices themselves (e.g. compiling and uploading a Wiring script to an Arduino UNO), or by reading the data from the device and formatting it accordingly (e.g. using a Python script on a Raspberry Pi to read USB output from a commercial Sound Level Meter). 
This implementation is based on NodeJS 0.10.40.

## Connect The Dots getting started project ##
For this project, follow the instructions.

1. Find out the port of the connected Arduino device
	a. Windows via Device Manager or Arduino IDE
	b. Linux via command "dmesg" when device is unplugged and plugged
	c. MacOS via ls /dev/tty.* or ls /dev/cu.* command
2. Make sure that the drivers are installed, else the Arduino device will not show up as a COM or /dev/*** port device.
3. Replace the SerialPort and BaudRate in "serialreader.js" based on your own settings

		//this is for windows based systems
		var sp = new SerialPort("COM3", {
		baudrate: 9600
		});
		//this is for linux and macos based systems
		//var sp = new SerialPort("/dev/tty.usbmodem1421");


4. Replace the settings within "serialreader.js" with your eventhub name and key



	// Set up variables, this is for sending to eventhub
	var serviceBus2 = 'cspi1-ns',
		eventHubName2 = 'ehdevices',
		sasKeyName2 = 'D1', // A SAS Key Name for the Event Hub, with Receive privilege
		sasKey2 = 'Ck7zXkmQXSM1ocrf+2WxugAl5BA7VTgQVAYAEIX72SY=', // The key value
		consumerGroup2 = 'nodejsconsumergroup',
		numPartitions2 = 8;
	var uriappend2 = "ConsumerGroups/" + consumerGroup + "/Partitions/";


5. You would now need to nagivate to the folder directory of this project in either command prompt on Windows or prefered shell on Mac, and resolve all dependencies by typing "npm install"

6. Extract sbus-amqp10.zip into node_modules directory

To start the application, type in "node serialreader.js" in the same folder directory. The command prompt should start reading JSON objects and send to eventhub.
