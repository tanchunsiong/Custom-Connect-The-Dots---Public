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

using Microsoft.Band;
using Microsoft.Band.Sensors;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Windows.UI;
using Windows.UI.Core;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Media;

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
        private String UserName = "Nicholas Soon";
        protected override void OnNavigatedTo(Windows.UI.Xaml.Navigation.NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            usernameTxBlk.Text = UserName;
            lblDate.Text = DateTime.Now.ToString("dddd, d MMM yyyy");
            ehh = new EventhubHelper();
            doWork();

        }
        static IBandClient bandClient;

        async void doWork()
        {
            if (bandClient == null)
            {
                bool exception = false;
                try
                {
                    IBandInfo[] pairedBands = await BandClientManager.Instance.GetBandsAsync();
                    if (pairedBands.Length < 1)
                    {
       
                        lblBand.Text = "Status: band out of range";
                        lblBand.Foreground = new SolidColorBrush(Colors.Red);
                        bandClient = null;
                        if (isTestMode)
                        {
                            startTestMode();
                        }
                        return;
                    }
                    lblBand.Text = "connecting";
                    lblBand.Foreground = new SolidColorBrush(Colors.White);

                    // Connect to Microsoft Band.
                    bandClient = await BandClientManager.Instance.ConnectAsync(pairedBands[0]);
                }
                catch (Exception ex)
                {
                    exception = true;
                    lblBand.Text = "Status: out of range";
                    lblBand.Foreground = new SolidColorBrush(Colors.Red);
                    return;
                }
            }

            #region BandContact
            //bandClient.SensorManager.Contact.SupportedReportingIntervals.GetEnumerator();
            bandClient.SensorManager.Contact.ReadingChanged += Contact_ReadingChanged;

            if (bandClient.SensorManager.Contact.GetCurrentUserConsent() != UserConsent.Granted)
            {
                // user has not consented, request it
                await bandClient.SensorManager.Contact.RequestUserConsentAsync();
            }

            await bandClient.SensorManager.Contact.StartReadingsAsync();
            #endregion
        }

        private async void startTestMode()
        {
            Random rand = new Random();
            while (true) {
              await Task.Delay(TimeSpan.FromSeconds(1));
                int heartRate = rand.Next(50, 120) + 30;

                ConnecTheDotsSensor p = new ConnecTheDotsSensor("2328a348-e2f9-4438-ab23-82a3930122ab", "HeartRate", "BPS");
                p.value = heartRate;
                p.timecreated = ehh.getFormattedTimeString();
                p.organization = "organization";
                p.location = "location";
                p.displayname = UserName;


                HttpResponseMessage x=await  ehh.SendMessageAsync(p.ToJson());


                await Task.Delay(TimeSpan.FromSeconds(1));
                int temp= rand.Next(35, 40) +5;
                
                ConnecTheDotsSensor q = new ConnecTheDotsSensor("41632409-7e93-4e33-9cdd-d99eba60d126", "SkinTemperature", "C");
                q.value = temp;
                q.timecreated = ehh.getFormattedTimeString();
                q.organization = "organization";
                q.location = "location";
                q.displayname = UserName;

                lblHeart.Text = heartRate.ToString() + "BPM";
                lblTemp.Text = temp.ToString() + " °C";

                HttpResponseMessage y = await ehh.SendMessageAsync(q.ToJson()); 
            }
        }

        BandContactState bandState;
        async void Contact_ReadingChanged(object sender, BandSensorReadingEventArgs<IBandContactReading> e)
        {
            bandState = e.SensorReading.State;
            String text = "";
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () =>
            {
                if (bandState == BandContactState.Worn)
                {
                    text = "Status: band connected";
                    lblBand.Text = text;
                    lblBand.Foreground = new SolidColorBrush(Colors.Green);
                }
                else
                {
                    text = "Status: no contact";
                    lblBand.Text = text;
                    lblBand.Foreground = new SolidColorBrush(Colors.Yellow);

                    rectHeartGreen.Visibility = Visibility.Collapsed;
                    rectHeartGrey.Visibility = Visibility.Visible;
                    rectHeartRed.Visibility = Visibility.Collapsed;

                    rectTempGreen.Visibility = Visibility.Collapsed;
                    rectTempGrey.Visibility = Visibility.Visible;
                    rectTempRed.Visibility = Visibility.Collapsed;

                    lblHeart.Text = "-";
                    lblTemp.Text = "-";

                    return;
                }
            }).AsTask();



            if (bandState == BandContactState.Worn)
            {
                //only support 1 minute
                #region bandClient.SensorManager.SkinTemperature
                bandClient.SensorManager.SkinTemperature.ReadingChanged += SkinTemperature_ReadingChanged;
                
                if (bandClient.SensorManager.SkinTemperature.GetCurrentUserConsent() != UserConsent.Granted)
                {
                    // user has not consented, request it
                    await bandClient.SensorManager.SkinTemperature.RequestUserConsentAsync();
                }

                bandClient.SensorManager.SkinTemperature.StartReadingsAsync();

                #endregion

                #region bandClient.SensorManager.HeartRate
                bandClient.SensorManager.HeartRate.ReportingInterval = TimeSpan.FromSeconds(1);
                bandClient.SensorManager.HeartRate.ReadingChanged += HeartRate_ReadingChanged;

                if (bandClient.SensorManager.HeartRate.GetCurrentUserConsent() != UserConsent.Granted)
                {
                    // user has not consented, request it
                    await bandClient.SensorManager.HeartRate.RequestUserConsentAsync();
                }


                bandClient.SensorManager.HeartRate.StartReadingsAsync();


                #endregion
            }
            else
            {
                bandClient.SensorManager.SkinTemperature.ReadingChanged -= SkinTemperature_ReadingChanged;
                await bandClient.SensorManager.SkinTemperature.StopReadingsAsync();

                bandClient.SensorManager.HeartRate.ReadingChanged += HeartRate_ReadingChanged;
                await bandClient.SensorManager.HeartRate.StopReadingsAsync();



            }
        }

        async void HeartRate_ReadingChanged(object sender, BandSensorReadingEventArgs<IBandHeartRateReading> e)
        {
            if (bandState == BandContactState.Worn)
            {
                await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, async () =>
                {
                    int heartRate = e.SensorReading.HeartRate;
                    lblHeart.Text = heartRate.ToString() + " bpm";
                    if (heartRate >= 60 && heartRate <= 100)
                    {
                        rectHeartGrey.Visibility = Visibility.Collapsed;
                        rectHeartGreen.Visibility = Visibility.Visible;
                        rectHeartRed.Visibility = Visibility.Collapsed;
                    }
                    else
                    {
                        rectHeartGrey.Visibility = Visibility.Collapsed;
                        rectHeartGreen.Visibility = Visibility.Collapsed;
                        rectHeartRed.Visibility = Visibility.Visible;
                    }

                    try
                    {


                        ConnecTheDotsSensor p = new ConnecTheDotsSensor("2298a348-e2f9-4438-ab23-82a3930122ab", "HeartRate", "BPS");
                        p.value = heartRate;
                        p.timecreated = ehh.getFormattedTimeString();
                        p.organization = "organization";
                        p.location = "location";
                        p.displayname = UserName;


                        HttpResponseMessage x = await ehh.SendMessageAsync(p.ToJson());
                    
                    }
                    catch (Exception ex)
                    {
                    }

                }).AsTask();
            }
        }

        async void SkinTemperature_ReadingChanged(object sender, BandSensorReadingEventArgs<IBandSkinTemperatureReading> e)
        {
            if (bandState == BandContactState.Worn)
            {
                await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, async () =>
                {
                    double temp = e.SensorReading.Temperature;
                    lblTemp.Text = temp.ToString() + " °C";
                    if (e.SensorReading.Temperature >= 35)
                    {
                        rectTempGrey.Visibility = Visibility.Collapsed;
                        rectTempGreen.Visibility = Visibility.Collapsed;
                        rectTempRed.Visibility = Visibility.Visible;
                    }
                    else
                    {
                        rectTempGrey.Visibility = Visibility.Collapsed;
                        rectTempGreen.Visibility = Visibility.Visible;
                        rectTempRed.Visibility = Visibility.Collapsed;
                    }

                    try
                    {
       

                        ConnecTheDotsSensor q = new ConnecTheDotsSensor("41613409-7e93-4e33-9cdd-d99eba60d126", "SkinTemperature", "C");
                        q.value = temp;
                        q.timecreated = ehh.getFormattedTimeString();
                        q.organization = "organization";
                        q.location = "location";
                        q.displayname = UserName;

                        HttpResponseMessage y = await ehh.SendMessageAsync(q.ToJson());
                    }
                    catch (Exception ex)
                    {
                    }

                }).AsTask();
            }
        }

        protected override void OnNavigatedFrom(Windows.UI.Xaml.Navigation.NavigationEventArgs e)
        {
            base.OnNavigatedFrom(e);

            try
            {
                bandClient.SensorManager.SkinTemperature.ReadingChanged -= SkinTemperature_ReadingChanged;
                bandClient.SensorManager.SkinTemperature.StopReadingsAsync();
            }
            catch (Exception) { }

            try
            {
                bandClient.SensorManager.HeartRate.ReadingChanged += HeartRate_ReadingChanged;
                bandClient.SensorManager.HeartRate.StopReadingsAsync();
            }
            catch (Exception) { }

            try
            {
                bandClient.SensorManager.Contact.StopReadingsAsync();
            }
            catch (Exception) { }
            if (bandClient != null && e.NavigationMode != Windows.UI.Xaml.Navigation.NavigationMode.New)
            {
                bandClient.Dispose();
                bandClient = null;
            }
        }

        void Current_Suspending(object sender, Windows.ApplicationModel.SuspendingEventArgs e)
        {

            try
            {
                bandClient.SensorManager.SkinTemperature.ReadingChanged -= SkinTemperature_ReadingChanged;
                bandClient.SensorManager.SkinTemperature.StopReadingsAsync();
            }
            catch (Exception) { }

            try
            {
                bandClient.SensorManager.HeartRate.ReadingChanged += HeartRate_ReadingChanged;
                bandClient.SensorManager.HeartRate.StopReadingsAsync();
            }
            catch (Exception) { }

            try
            {
                bandClient.SensorManager.Contact.StopReadingsAsync();
            }
            catch (Exception) { }
            if (bandClient != null)
            {
                bandClient.Dispose();
                bandClient = null;
            }

   
        }

        void Current_Resuming(object sender, object e)
        {
            doWork();
        }

        #region archive

  

        #endregion
    }
}
