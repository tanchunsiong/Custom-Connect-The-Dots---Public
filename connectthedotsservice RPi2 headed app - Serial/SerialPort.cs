using Microsoft.Maker.RemoteWiring;
using Microsoft.Maker.Serial;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TemperatureMeasurement
{
    class SerialPort
    {

        public UsbSerial usb;
        public RemoteDevice arduino;
        public SerialPort()
        {

            Start();
        }

        public async void Start()
        {

            var aqs = Windows.Devices.SerialCommunication.SerialDevice.GetDeviceSelector();
            var devices = await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(aqs);



            try {
                var device = devices.Where(x => x.Id.Contains("VID_1A86&PID_7523") || x.Id.Contains("VID_2341&PID_0043")).FirstOrDefault();
                Debug.WriteLine("Arduino found: " + device.Name);
                Debug.WriteLine("Arduino found: " + device.Id);

                usb = new UsbSerial(device);
                //arduino = new RemoteDevice(usb);

                usb.ConnectionEstablished += Usb_ConnectionEstablished;
                usb.ConnectionFailed += Usb_ConnectionFailed;
                usb.ConnectionLost += Usb_ConnectionLost;

                Debug.WriteLine("Begin USB connection");
                usb.begin(9600, SerialConfig.SERIAL_8N1);
            }
            catch (Exception ex) {
              

            }





        }



        private void Usb_ConnectionLost(string message)
        {
            Debug.WriteLine("USB Connection lost");
        }

        private void Usb_ConnectionFailed(string message)
        {
            Debug.WriteLine("USB Connection failed");
        }

        private void Usb_ConnectionEstablished()
        {
            Debug.WriteLine("USB Connection established");



        }
        public ushort ReadLine()
        {

            return usb.read();
        }

    }
}
