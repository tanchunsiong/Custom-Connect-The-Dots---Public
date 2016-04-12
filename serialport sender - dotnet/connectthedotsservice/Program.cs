using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using Microsoft.ServiceBus.Messaging;
using System.IO;
using Newtonsoft.Json;
using System.Configuration;

namespace connectthedotsservice
{
    class Program
    {
        //connection string stored in app.config
        static String connectionString =  ConfigurationSettings.AppSettings["Microsoft.ServiceBus.ConnectionString"];
        static string eventHubName = ConfigurationSettings.AppSettings["Microsoft.ServiceBus.EventHubName"];


        private static StringBuilder tempStringbuilder = new StringBuilder();
        static void Main(string[] args)
        {
            SerialPort mySerialPort = new SerialPort("COM3");

            mySerialPort.BaudRate = 9600;
            mySerialPort.Parity = Parity.None;
            mySerialPort.StopBits = StopBits.One;
            mySerialPort.DataBits = 8;
            mySerialPort.Handshake = Handshake.None;

            mySerialPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);

            mySerialPort.Open();

            Console.WriteLine("Press any key to continue...");
            Console.WriteLine();
            Console.ReadKey();
            mySerialPort.Close();

        }

        private static async void DataReceivedHandler(object sender, SerialDataReceivedEventArgs e)
        {
            SerialPort sp = (SerialPort)sender;
            String tempString = sp.ReadExisting();
            tempStringbuilder.Append(tempString);
            
            //assume last string
            if (tempString.Contains("}"))
            {
               
                tempStringbuilder.Replace("timenow", DateTime.UtcNow.ToString("o"));

                //savetotext(tempStringbuilder.ToString());
                 SendingMessage(tempStringbuilder.ToString());

               
                tempStringbuilder.Clear();
                try
                {
                    tempStringbuilder.Append(tempString.Substring(tempString.IndexOf("}\r\n") + 3));
                }
                catch (Exception ex) { }
            }

       

        }
        static async Task SendingMessage(String message)
        {
            var eventHubClient = EventHubClient.CreateFromConnectionString(connectionString, eventHubName);
          
                try
                {
             
                Console.WriteLine("{0} > Sending message: {1}", DateTime.Now, message);
                    await eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(message)));
                }
                catch (Exception exception)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("{0} > Exception: {1}", DateTime.Now, exception.Message);
                    Console.ResetColor();
                }

            
        }

        static void savetotext(String message) {

        
            string path = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            if (!File.Exists(path + @"\sample.txt"))
            {
                Console.WriteLine("{0} > Saving message: {1}", DateTime.Now, message);
                // Create a file to write to.
                using (StreamWriter sw = File.CreateText(path + @"\sample.txt"))
                {
                    sw.WriteLine(message);
                }
            }
            else {

                using (StreamWriter sw = new StreamWriter(path + @"\sample.txt", true))
                {
                    Console.WriteLine("{0} > Saving message: {1}", DateTime.Now, message);
                    sw.WriteLine(message);
                }
            }

        }
    }
}

