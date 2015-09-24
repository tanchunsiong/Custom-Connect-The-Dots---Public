using System;

namespace TemperatureMeasurement
{

    public class LightChangedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the temperature.
        /// </summary>
        public string Light { get; private set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="TemperatureChangedEventArgs"/> class.
        /// </summary>
        /// <param name="temperatue">The temperatue.</param>
        public LightChangedEventArgs(string Light)
        {
            this.Light = Light;
        }
    }
}
