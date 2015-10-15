using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Threading.Tasks;

namespace Sensors
{
    class EventhubHelper
    {

        String eventhubname = "ehdevices";
        String deviceID = "D1";
        String serviceNamespace = "cspi2-ns";
        String sas = "SharedAccessSignature sr=https%3a%2f%2fcspi2-ns.servicebus.windows.net%2fehdevices%2fpublishers%2fd1%2fmessages&sig=%2fA8pl9BMAqxv74eORVbh4Dqy2gL9Mv87nvKkEX7gkK4%3d&se=1448426499&skn=D1";

       
        public EventhubHelper()
        {

        }
        public string getFormattedTimeString()
        {
            return DateTime.UtcNow.ToString("o");
        }
        public Task<HttpResponseMessage> SendMessageAsync(String data)
        {
          

            // Namespace info.
            var url = string.Format("{0}/publishers/{1}/messages", eventhubname, deviceID);

            // Create client.
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri(string.Format("https://{0}.servicebus.windows.net/", serviceNamespace))
            };

           
            httpClient.DefaultRequestHeaders.TryAddWithoutValidation("Authorization", sas);

            var content = new StringContent(data, Encoding.UTF8, "application/json");


   
            return httpClient.PostAsync(url, content);
        }
    }
    public class ConnecTheDotsSensor
    {
        public string guid { get; set; }
        public string displayname { get; set; }
        public string organization { get; set; }
        public string location { get; set; }
        public string measurename { get; set; }
        public string unitofmeasure { get; set; }
        public string timecreated { get; set; }
        public double value { get; set; }
        public double lat { get; set; }
        public double lng { get; set; }
        /// <summary>
        /// Default parameterless constructor needed for serialization of the objects of this class
        /// </summary>
        public ConnecTheDotsSensor()
        {
        }

        /// <summary>
        /// Construtor taking parameters guid, measurename and unitofmeasure
        /// </summary>
        /// <param name="guid"></param>
        /// <param name="measurename"></param>
        /// <param name="unitofmeasure"></param>
        public ConnecTheDotsSensor(string guid, string measurename, string unitofmeasure)
        {
            this.guid = guid;
            this.measurename = measurename;
            this.unitofmeasure = unitofmeasure;
        }

        /// <summary>
        /// ToJson function is used to convert sensor data into a JSON string to be sent to Azure Event Hub
        /// </summary>
        /// <returns>JSon String containing all info for sensor data</returns>
        public string ToJson()
        {
            DataContractJsonSerializer ser = new DataContractJsonSerializer(typeof(ConnecTheDotsSensor));
            MemoryStream ms = new MemoryStream();
            ser.WriteObject(ms, this);
            string json = Encoding.UTF8.GetString(ms.ToArray(), 0, (int)ms.Length);

            return json;
        }
    }
}
