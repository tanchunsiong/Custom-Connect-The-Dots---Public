using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace TemperatureMeasurement
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {

        SensorSource sensor = null;

        public MainPage()
        {
            this.InitializeComponent();

            this.Loaded += MainPage_Loaded;
            this.Unloaded += MainPage_Unloaded;
        }

        private void MainPage_Unloaded(object sender, RoutedEventArgs e)
        {
            if (sensor != null)
                sensor.Dispose();
        }

        private void MainPage_Loaded(object sender, RoutedEventArgs e)
        {


            sensor = new SensorSource();
            sensor.StateChanged += async (s, args) =>
            {
                await Dispatcher.RunAsync(Windows.UI.Core.CoreDispatcherPriority.Normal, () =>
                {
                    if (args.IsRunning)
                    {
                        sensorStatus.Text = "Sensor Status: Running";
                        icon.Foreground = new SolidColorBrush(Colors.Black);
                    }
                    else
                    {
                        sensorStatus.Text = "Sensor Status: Stopped";
                        tbkValue.Text = "";
                        icon.Foreground = new SolidColorBrush(Colors.Gray);
                    }
                });
            };

            sensor.ValueChanged += Sensor_ValueChanged;
            sensor.MotionValueChanged += Sensor_MotionValueChanged;
            sensor.LightValueChanged += Sensor_LightValueChanged;
        }

        private async void Sensor_LightValueChanged(object sender, LightChangedEventArgs e)
        {
            await Dispatcher.RunAsync(Windows.UI.Core.CoreDispatcherPriority.Normal, async () =>
            {
                LightTxValue.Text = e.Light.ToString();

            });
        }

        private async void Sensor_MotionValueChanged(object sender, MotionChangedEventArgs e)
        {
            await Dispatcher.RunAsync(Windows.UI.Core.CoreDispatcherPriority.Normal, async () =>
            {
                motionTxValue.Text = e.Motion.ToString();

            });

        }

        private async void Sensor_ValueChanged(object sender, TemperatureChangedEventArgs e)
        {
            await Dispatcher.RunAsync(Windows.UI.Core.CoreDispatcherPriority.Normal, async () =>
            {
                tbkValue.Text = String.Format("{0:F02} °C", e.Temperature);

            });

        }


        private async void toggleSwitch_Toggled(object sender, RoutedEventArgs e)
        {
            if (toggleSwitch.IsOn)
            {
                sensor.Start();


            }
            else
            {
                sensor.Stop();



            }
        }
    }
}
