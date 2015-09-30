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
using System.Collections.ObjectModel;

namespace connectthedotsservice
{
    class Program
    {
        //connection string stored in app.config
        static String connectionString = ConfigurationSettings.AppSettings["Microsoft.ServiceBus.ConnectionString"];
        static string eventHubName = ConfigurationSettings.AppSettings["Microsoft.ServiceBus.EventHubName"];
        static EventHubClient eventHubClient = EventHubClient.CreateFromConnectionString(connectionString, eventHubName);

        private static StringBuilder tempStringbuilder = new StringBuilder();
        public static void Main(string[] args)
        {

            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "c:\\python27\\python.exe";//cmd is full path to python.exe
            start.Arguments = "pyscripts\\tz_cms50.py --port 8";//args is path to .py file and any cmd line args
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;



            readString( start);
        }

        public async static void readString(ProcessStartInfo start)
        {




            Process p = new Process();
            p.StartInfo = start;
            p.EnableRaisingEvents = true;
            p.Exited += new EventHandler(OnProcessExit);
            p.Start();
            StreamReader q = p.StandardOutput;
            int count = 0;
            Collection<EventData> e = new Collection<EventData>();
            while (!p.HasExited) {
                count++;
                string x = q.ReadLine();
               

                if (true) //bulksend
                {
                    if (count >= 100)
                    {
                      
                        SendingBulkMessage(e);
                        count = 0;
                        e.Clear();
                    }
                    else
                    {
                        if (count % 2 == 0)
                        {
                            e.Add(new EventData(Encoding.UTF8.GetBytes(x)));
                            Console.WriteLine(count);
                        }
                       
                    }
                }
                else {
                    if (count % 5 == 0)
                    {
                        SendingMessage(q);
                        Console.WriteLine(count);
                    }
                  
                }


                //GC.Collect();
            }
            Console.ReadKey();
            //p.BeginErrorReadLine();
        }

        private static void OnProcessExit(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }



       
        static async Task SendingMessage(StreamReader q)
        {
            try
            {
                String x = q.ReadLine();
                //Console.WriteLine("{0} > Sending message: {1}", DateTime.Now, message);
                Console.Write("Sending");
                await eventHubClient.SendAsync(new EventData(Encoding.UTF8.GetBytes(x)));
            }
            catch (Exception exception)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("{0} > Exception: {1}", DateTime.Now, exception.Message);
                Console.ResetColor();
            }


        }
        static async Task SendingBulkMessage(IEnumerable<EventData> eventDataList)
        {
            try
            {
               
                //Console.WriteLine("{0} > Sending message: {1}", DateTime.Now, message);
                Console.Write("Sending");
                await eventHubClient.SendBatchAsync(eventDataList);
            }
            catch (Exception exception)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("{0} > Exception: {1}", DateTime.Now, exception.Message);
                Console.ResetColor();
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


