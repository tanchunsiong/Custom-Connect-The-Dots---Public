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
        static String connectionString = ConfigurationSettings.AppSettings["Microsoft.ServiceBus.ConnectionString"];
        static string eventHubName = ConfigurationSettings.AppSettings["Microsoft.ServiceBus.EventHubName"];
        static String guid = Guid.NewGuid().ToString();


        private static StringBuilder tempStringbuilder = new StringBuilder();
        public static void Main(string[] args)
        {
          
                sendRandomString();
                //currentfork++;
                //Console.WriteLine(currentfork);
                //ProcessStartInfo start = new ProcessStartInfo();
                //start.FileName = System.Reflection.Assembly.GetExecutingAssembly().Location;//cmd is full path to python.exe
                //start.Arguments = currentfork.ToString();//args is path to .py file and any cmd line args

                //Process p = new Process();
                //p.StartInfo = start;
                //p.EnableRaisingEvents = true;
                //p.Start();
      


        }


        static async Task sendRandomString()
        {
            Random ran = new Random();
            int tempbase = ran.Next(25, 35);
            int humdbase = ran.Next(0, 100);
            int lightbase = ran.Next(0, 100);
            int serial = ran.Next(0, 1000);

            while (true)
            {

                StringBuilder sb = new StringBuilder();
                sb.Append("{");
                sb.Append("\"guid\":\"");
                sb.Append(guid);
                sb.Append("\",\"organization\":\"Microsoft\",\"timecreated\":\"");
                sb.Append(DateTime.Now.ToString("o"));
                sb.Append("\",\"displayname\":\"DX Singapore " + serial + "\",\"location\":\"SGMIC\",\"measurename\":\"temperature\",\"unitofmeasure\":\"C\",\"value\":");
                sb.Append(tempbase + ran.Next(-3, +3));
                sb.Append("}");
                StringBuilder sb2 = new StringBuilder();
                sb2.Append("{");
                sb2.Append("\"guid\":\"");
                sb2.Append(guid);
                sb2.Append("\",\"organization\":\"Microsoft\",\"timecreated\":\"");
                sb2.Append(DateTime.Now.ToString("o"));
                sb2.Append("\",\"displayname\":\"DX Singapore " + serial + "\",\"location\":\"SGMIC\",\"measurename\":\"humidity\",\"unitofmeasure\":\"%\",\"value\":");
                sb2.Append(humdbase + ran.Next(-5, 5));
                sb2.Append("}");

                StringBuilder sb3 = new StringBuilder();
                sb3.Append("{");
                sb3.Append("\"guid\":\"");
                sb3.Append(guid);
                sb3.Append("\",\"organization\":\"Microsoft\",\"timecreated\":\"");
                sb3.Append(DateTime.Now.ToString("o"));
                sb3.Append("\",\"displayname\":\"DX Singapore " + serial + "\",\"location\":\"SGMIC\",\"measurename\":\"light\",\"unitofmeasure\":\"lumen\",\"value\":");
                sb3.Append(lightbase + ran.Next(-10, +10));
                sb3.Append("}");

                StringBuilder sb4 = new StringBuilder();
                sb4.Append("{");
                sb4.Append("\"guid\":\"");
                sb4.Append(guid);
                sb4.Append("\",\"organization\":\"Microsoft\",\"timecreated\":\"");
                sb4.Append(DateTime.Now.ToString("o"));
                sb4.Append("\",\"displayname\":\"DX Singapore "+ serial + "\",\"location\":\"SGMIC\",\"measurename\":\"motion\",\"unitofmeasure\":\"binary\",\"value\":");
                sb4.Append(ran.Next(0, 2));
                sb4.Append("}");

                var eventHubClient = EventHubClient.CreateFromConnectionString(connectionString, eventHubName);

                try
                {

                    Console.WriteLine("{0} > Sending message: {1}", DateTime.Now, "");
                  eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(sb.ToString())));
                   eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(sb2.ToString())));
                   eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(sb3.ToString())));
                   eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(sb4.ToString())));
                    Thread.Sleep(1000);
                }
                catch (Exception exception)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("{0} > Exception: {1}", DateTime.Now, exception.Message);
                    Console.ResetColor();
                }

            }
        }

        static void savetotext(String message)
        {


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
            else
            {

                using (StreamWriter sw = new StreamWriter(path + @"\sample.txt", true))
                {
                    Console.WriteLine("{0} > Saving message: {1}", DateTime.Now, message);
                    sw.WriteLine(message);
                }
            }

        }
    }
}

