# Supported Devices #

Below you'll find a list of supported devices, which can be found under each parent directory.

### Connect The Dots Getting Started project ###
If you are going to deploy the getting started project, you need to procure an Arduino Board, Raspberry Pi, or other compatiable devices as shown in the documentation for those devices in the appropriate folders:

- [Arduino UNO R3 and sensors](https://github.com/tanchunsiong/Custom-Connect-The-Dots---Public/tree/master/connectthedots%20arduino%20sketch)
- [Raspberry Pi](https://github.com/tanchunsiong/Custom-Connect-The-Dots---Public/tree/master/connectthedotsservice%20RPi2%20headed%20app%20-%20Serial)

Once you have these, head over to the [Getting Started project](GettingStarted.md) to get going.

## Additional devices ##
If you decide to connect another device, you can check out the samples provided in the devices sub folder containing .NET, Python and Node.js examples. Other languages examples are coming soon! Additionally, we encourage the community to submit new devices.

The devices currently showcased are the following:

- Directly connected devices:
    - Linux VM sending SSH attack logs via Python over HTTP/REST
    - Raspberry Pi 2 running Windows 10 IoT Core and a Universal Application sending dummy data over HTTP/REST
    - Windows Phone C# application sending a data from a paired Microsoft Band (accelerometer, body temperature, heartbeat)over HTTP/REST
- Gateways:
    - Linux/Windows based OS reading off serial port via Python and sending data over HTTP/REST
	- Linux/Windows based OS reading off serial port via NodeJS and sending data over AMQS
	- Windows based OS reading off serial port via C# and sending data over AMQS
- Gateway connected devices (devices connecting to a gateway to send their data)
    - Arduino connected with multiple sensors

