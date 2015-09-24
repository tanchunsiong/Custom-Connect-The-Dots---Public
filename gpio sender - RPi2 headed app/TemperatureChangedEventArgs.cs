using System;

namespace TemperatureMeasurement
{

    public class TemperatureChangedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the temperature.
        /// </summary>
        public string Temperature { get; private set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="TemperatureChangedEventArgs"/> class.
        /// </summary>
        /// <param name="temperatue">The temperatue.</param>
        public TemperatureChangedEventArgs(string temperatue)
        {
            this.Temperature = temperatue;
        }
    }
}
