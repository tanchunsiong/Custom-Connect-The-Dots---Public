# Gateway for Windows Based OS  #
The basic premise of this project is that data from sensing devices can be sent upstream in a prescribed JSON format. This might be achieved by programming the devices themselves (e.g. compiling and uploading a Wiring script to an Arduino UNO), or by reading the data from the device and formatting it accordingly (e.g. using a Python script on a Raspberry Pi to read USB output from a commercial Sound Level Meter). 

## Connect The Dots getting started project ##
For this project, follow the instructions.

1. Find out the port of the connected Arduino device via Device Manager or Arduino IDE
2. Make sure that the drivers are installed, else the Arduino device will not show up as a COM port device.
3. Replace the SerialPort and BaudRate in "program.cs" based on your own settings

			SerialPort mySerialPort = new SerialPort("COM3");

            mySerialPort.BaudRate = 115200;
            mySerialPort.Parity = Parity.None;
            mySerialPort.StopBits = StopBits.One;
            mySerialPort.DataBits = 8;
            mySerialPort.Handshake = Handshake.None;

4. Replace "App.config" with your eventhub name and key

 <appSettings>
    <!-- Service Bus specific app setings for messaging connections -->
    <add key="Microsoft.ServiceBus.ConnectionString" value="Endpoint=sb://cspi1-ns.servicebus.windows.net/;SharedAccessKeyName=D1;SharedAccessKey=Ck7zXkmQXSM1ocrf+2WxugAl5BA7VTgQVAYAEIX72SY=" />
    <add key="Microsoft.ServiceBus.EventHubName" value="ehdevices" />
    <add key="ClientSettingsProvider.ServiceUri" value="" />
  </appSettings> 

5. Rebuild, run and you will on your way to sending your data your eventhub.