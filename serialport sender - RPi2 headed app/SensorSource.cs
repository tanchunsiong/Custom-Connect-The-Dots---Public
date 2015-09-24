using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.Devices.Enumeration;
using Windows.Devices.Gpio;
using Windows.Devices.SerialCommunication;
using Windows.Devices.Spi;

namespace TemperatureMeasurement
{
    public class SensorSource : IDisposable
    {
        private bool isDisposed = false;
        private bool isRunning = false;
        private bool isError = false;

        private const double referenceVoltage = 4.58; // Based on the measurement from the board. By right it should be 5.0V, in actual this is not always table and fix.

        SerialPort sp;

        //Helper class to generate the JSON Object, and Sending to Event Hub
        ConnectTheDotsHelper ctdHelper;
        ConnectTheDotsSensor tempsensor, motionsensor, lightsensor;



        public event EventHandler<TemperatureChangedEventArgs> ValueChanged = delegate { };
        public event EventHandler<MotionChangedEventArgs> MotionValueChanged = delegate { };
        public event EventHandler<LightChangedEventArgs> LightValueChanged = delegate { };
        public event EventHandler<StateChangedEventArgs> StateChanged = delegate { };

        /// <summary>
        /// Initializes a new instance of the <see cref="SensorSource"/> class.
        /// </summary>
        public SensorSource()
        {
            List<ConnectTheDotsSensor> sensors = new List<ConnectTheDotsSensor> {
                new ConnectTheDotsSensor("2298f348-13a2-4258-ed52-82a4353531ab", "temperature", "C"),
                new ConnectTheDotsSensor("3213a232-e2f9-4438-ab23-63a7676542fe", "light", "lumen"),
                new ConnectTheDotsSensor("6458a325-63a7-7694-ce23-74a5326453ab", "motion", "binary")
                   };

            //this is the connection to eventhub
            ctdHelper = new ConnectTheDotsHelper(serviceBusNamespace: "cspi1-ns",
            eventHubName: "ehdevices",
            keyName: "raspiberrypisender",
            key: "",
            displayName: "RaspberryPi2Win10",
            organization: "Microsoft Singapore DX Team",
            location: "SG MIC 2",
            sensorList: sensors);

            motionsensor = ctdHelper.sensors.Find(item => item.measurename == "motion");
            tempsensor = ctdHelper.sensors.Find(item => item.measurename == "temperature");
            lightsensor = ctdHelper.sensors.Find(item => item.measurename == "light");
            // Hard coding guid for sensors. Not an issue for this particular application which is meant for testing and demos

            Init();
        }

        /// <summary>
        /// Starts this instance.
        /// </summary>
        public void Start()
        {
            isRunning = true;
            ReadData();
        }

        /// <summary>
        /// Stops this instance.
        /// </summary>
        public void Stop()
        {
            isRunning = false;
            StateChanged(this, new StateChangedEventArgs(false, "STOP"));
            try
            {
                sp.usb.end();
                sp.usb.Dispose();
            }
            catch (Exception ex) { }
        }

        /// <summary>
        /// Initializes this instance.
        /// </summary>
        private async void Init()
        {
            await Task.Run(async () =>
            {

                try
                {
                    sp = new SerialPort();


                    isError = false;
                }
                catch (Exception ex)
                {
                    isError = true;
                    StateChanged(this, new StateChangedEventArgs(false, "INITIALIZE ERROR"));
                    Debug.WriteLine(ex.Message);
                }

            }).ContinueWith((task) => ReadData());
        }

        /// <summary>
        /// Reads the data.
        /// </summary>
        private async void ReadData()
        {
            StringBuilder sb = new StringBuilder();
            await Task.Run(() =>
            {
                while (isRunning)
                {
                    try
                    {

                        //code for reading from Digital Pin 12, Sensor is PIR
                        ushort rawtext = sp.ReadLine();
                        double dblvalue = 0.0;
                        char tempChar = Convert.ToChar(rawtext);
                        if (!tempChar.Equals('￿'))
                        {
                            sb.Append(tempChar);
                        }



                        if (tempChar.Equals('}'))
                        {
                            String textosend = sb.ToString();
                            sb.Clear();
                            ctdHelper.SendRawTextSensorData(textosend);
                            JToken root = JObject.Parse(textosend);
                            var serializer = new JsonSerializer();
                            var obj = serializer.Deserialize<ConnectTheDotsSensor>(root.CreateReader());


                            if (obj.measurename.Equals("motion"))
                            {
                                MotionValueChanged(this, new MotionChangedEventArgs(obj.value.ToString()));
                            }

                            else if (obj.measurename.Equals("light"))
                            {
                                LightValueChanged(this, new LightChangedEventArgs(obj.value.ToString("F03")));
                            }
                            else
                             if (obj.measurename.Equals("temperature"))
                            {
                                ValueChanged(this, new TemperatureChangedEventArgs(obj.value.ToString("F02")));
                            }
                            else
                            {
                            }


                        }
                        ////throw a new change event
                        //MotionValueChanged(this, new MotionChangedEventArgs(value.ToString()));

                        ////assign to variable and send to cloud
                        //motionsensor.value = dblvalue;
                        // ctdHelper.SendSensorData(motionsensor);
                        ////end code for PIR

                        ////code for reading from MCP3208 ADC
                        ////Read Channel 0
                        //device.TransferFullDuplex(writeBufferCh0, readBufferCh0);
                        //int res = ConvertToInt(readBufferCh0);
                        //var light = (1.0 / res * 40) * 0.8;

                        ////assign to variable and send to cloud
                        //lightsensor.value = light;
                        //ctdHelper.SendSensorData(lightsensor);

                        ////Read Channel 1
                        //device.TransferFullDuplex(writeBufferCh1, readBufferCh1);
                        //res = ConvertToInt(readBufferCh1);
                        //var tempC = ((referenceVoltage * 100) * res) / 4096;

                        ////assign to variable and send to cloud
                        //tempsensor.value = tempC;
                        //ctdHelper.SendSensorData(tempsensor);

                        ////throw a new change event
                        //LightValueChanged(this, new LightChangedEventArgs(light.ToString("F03")));
                        //ValueChanged(this, new TemperatureChangedEventArgs(tempC.ToString("F02")));

                        StateChanged(this, new StateChangedEventArgs(true, "OKAY"));

                        // Task.Delay(500).Wait();

                        isError = false;
                    }
                    catch (Exception ex)
                    {
                        isError = true;
                        StateChanged(this, new StateChangedEventArgs(false, "READ ERROR"));
                    }
                }
            });

        }

        /// <summary>
        /// Converts to int.
        /// </summary>
        /// <param name="data">The data.</param>
        public int ConvertToInt(byte[] data)
        {
            int result = data[1] & 0x00F;
            result <<= 8;
            result += data[2];
            return result;
        }

        #region IDisposable Members
        /// <summary>
        /// Releases unmanaged and - optionally - managed resources.
        /// </summary>
        private void Dispose(bool isDisposing)
        {
            if (isDisposing)
            {
                if (!isDisposed)
                {
                    Stop();
                }
            }
        }

        /// <summary>
        /// Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
        /// </summary>
        public void Dispose()
        {
            Dispose(true);
        }
        #endregion
    }

}
