//based off http://danialk.github.io/blog/2014/04/12/arduino-and-nodejs-communication-with-serial-ports/


// Set up variables
var serviceBus = 'cspi1-ns',
    eventHubName = 'ehmessages',
    sasKeyName = 'devicereader', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey = '6OQLW1oQGGDe6Vyan1qrnZeHzKIygMaCPVjPl8isnxE=', // The key value
    consumerGroup = 'nodejsconsumergroup',
    numPartitions = 8;
var uriappend = "ConsumerGroups/" + consumerGroup + "/Partitions/";

var Sbus = require('sbus-amqp10');
var hub = Sbus.EventHubClient(serviceBus, eventHubName, sasKeyName, sasKey);

// Set up variables
var serviceBus2 = 'cspi1-ns',
    eventHubName2 = 'ehdevices',
    sasKeyName2 = 'D1', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey2 = 'Ck7zXkmQXSM1ocrf+2WxugAl5BA7VTgQVAYAEIX72SY=', // The key value
    consumerGroup2 = 'nodejsconsumergroup',
    numPartitions2 = 8;
var uriappend2 = "ConsumerGroups/" + consumerGroup + "/Partitions/";

var Sbus2 = require('sbus-amqp10');
var hub2 = Sbus2.EventHubClient(serviceBus2, eventHubName2, sasKeyName2, sasKey2);

var SerialPort = require("serialport").SerialPort;
//this is for windows based systems
var sp = new SerialPort("COM3", {
    baudrate: 9600
});
//this is for linux and macos based systems
//var sp = new SerialPort("/dev/tty.usbmodem1421");


var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:8080/');

ws.on('open', function open() {
      
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
            
            hub2.send(completeddata, null, function (tx_err) {
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
    



    //for (var idx = 0; idx < numPartitions; ++idx) {
    //    hub.eventHubReceive(uriappend + idx, new Date().getTime() - new Date().getTimezoneOffset(), function callback(rx_err, partition, payload) {
    //        if (rx_err) {
    //            console.log(rx_err);
    //        } else {
    //            console.log("partition: " + partition);
    //            console.log(payload);
				//sp.write(payload + "\n", function (err, results) {
    //                console.log('err ' + err);
    //                console.log('results ' + results);
    //            });
           
    //        }
    //    }
    //    );
    //}
   
   
    
});