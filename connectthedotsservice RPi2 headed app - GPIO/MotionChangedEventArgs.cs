using System;

namespace TemperatureMeasurement
{

    public class MotionChangedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the temperature.
        /// </summary>
        public string Motion { get; private set; }

        /// <summary>
        /// Initializes a new instance of the <see cref="MotionChangedEventArgs"/> class.
        /// </summary>
        /// <param name="temperatue">The temperature.</param>
        public MotionChangedEventArgs(string isMoving)
        {
            this.Motion = isMoving;
        }
    }
}
