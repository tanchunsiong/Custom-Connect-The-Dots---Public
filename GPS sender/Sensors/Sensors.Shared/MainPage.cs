/*
    Copyright (c) Microsoft Corporation All rights reserved.  
 
    MIT License: 
 
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the  "Software"), to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 
 
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 
 
    THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
    TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Windows.UI;
using Windows.UI.Core;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Media;


using Windows.Devices.Geolocation; //Provides the Geocoordinate class.

namespace Sensors
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    partial class MainPage
    {
        private App viewModel;
        private EventhubHelper ehh;
        //chun siong change to false when running with band
        private bool isTestMode = false;
        private String UserName = "Tan Chun Siong";
        Geolocator myGeolocator;
        protected override void OnNavigatedTo(Windows.UI.Xaml.Navigation.NavigationEventArgs e)
        {




            base.OnNavigatedTo(e);





            usernameTxBlk.Text = UserName;
            lblDate.Text = DateTime.Now.ToString("dddd, d MMM yyyy");
            ehh = new EventhubHelper();
            doWork();

        }
      

        async void doWork()
        {
                bool exception = false;
             myGeolocator = new Geolocator();
            myGeolocator.PositionChanged += MyGeolocator_PositionChanged;
     
       
         
        }
        double count = 1;
        private async void MyGeolocator_PositionChanged(Geolocator sender, PositionChangedEventArgs args)
        {
            Geoposition myGeoposition = await myGeolocator.GetGeopositionAsync();
            Geocoordinate myGeocoordinate = myGeoposition.Coordinate;

            count += 0.01;

            ConnecTheDotsSensor p = new ConnecTheDotsSensor("2298a348-e2f9-4438-ab23-82a3930662ab", "location", "latlong");
            p.value = count;
            p.lat = myGeocoordinate.Latitude;
            p.lng = myGeocoordinate.Longitude;
            p.timecreated = ehh.getFormattedTimeString();
            p.organization = "organization";
            p.location = "location";
            p.displayname = UserName;

            try
            {
                HttpResponseMessage x = await ehh.SendMessageAsync(p.ToJson());
            }
            catch (Exception) { }
        }

    
         protected override void OnNavigatedFrom(Windows.UI.Xaml.Navigation.NavigationEventArgs e)
        {
            base.OnNavigatedFrom(e);

            try
            {
                myGeolocator.PositionChanged -= MyGeolocator_PositionChanged;
               
          
            }
            catch (Exception) { }

          
            }
        

        void Current_Suspending(object sender, Windows.ApplicationModel.SuspendingEventArgs e)
        {

            try
            {
                myGeolocator.PositionChanged -= MyGeolocator_PositionChanged;


            }
            catch (Exception) { }


        }

        void Current_Resuming(object sender, object e)
        {
            doWork();
        }

     

    }
}
