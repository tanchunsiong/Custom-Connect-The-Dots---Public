//based off http://danialk.github.io/blog/2014/04/12/arduino-and-nodejs-communication-with-serial-ports/
module.exports = require('./lib/sbus');

  
// Set up variables
var serviceBus = 'cspi1-ns',
    eventHubName = 'ehdevices',
    sasKeyName = 'D1', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey = 'Ck7zXkmQXSM1ocrf+2WxugAl5BA7VTgQVAYAEIX72SY=', // The key value
    consumerGroup = 'nodejsconsumergroup',
    numPartitions = 8;
var uriappend = "ConsumerGroups/" + consumerGroup + "/Partitions/";

var sbus= require('./lib/sbusclient');
var hub = sbus.EventHubClient(serviceBus, eventHubName, sasKeyName, sasKey);

var SerialPort = require("serialport").SerialPort;
//this is for windows based systems
var sp = new SerialPort("COM7", {
    baudrate: 9600
});
//this is for linux and macos based systems
//var sp = new SerialPort("/dev/tty.usbmodem1421");

try {
    var WebSocket = require('ws');
    var ws = new WebSocket('ws://cspi1nodejs.azurewebsites.net/');
    
    ws.on('open', function open() {
        console.log('connected');
    });
    
    ws.on('message', function (data, flags) {
        var received_msg = data;
        if (received_msg.indexOf("command") >= 0) {
            console.log('received ' + received_msg);
            sp.write(received_msg + "\n", function (err, results) {
                console.log('err ' + err);
                console.log('results ' + results);
            });
        }
    });
}
catch (err) {
   
}


var tempString = "";
sp.on("open", function () {
    console.log('open');
    sp.on('data', function (data) {
        //not first string
        if (data.toString().indexOf("{") == -1) {
            tempString += data.toString();
        }
        //if is first string
        else {
            tempString = data.toString();
        }
        //if end of string
        if (tempString.indexOf("}") >= 0) {
            
            
            var d = new Date().toISOString();
            var len = d.length - 1;
            var timecreated = d.substr(0, len) + "0000Z";
            var timecreatedindex = tempString.toString().indexOf("timenow");
            var timecreatedindexend = timecreatedindex + 7;
            var completeddata = tempString.toString().substr(0, timecreatedindex) + timecreated + tempString.toString().substr(timecreatedindexend);
            
            hub.send(completeddata, null, function (tx_err) {
                if (tx_err) {
                    console.log(tx_err);
                    tempString = "";
                }
                else {
                    console.log('data sent: ' + completeddata);
                    tempString = "";
                }
            });
        }
      
    });

});



