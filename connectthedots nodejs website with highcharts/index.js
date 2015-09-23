var WebSocketServer = require('ws').Server;
var http = require("http");
var express = require("express");
var app = express();
var port = process.env.PORT || 8080;


app.use(express.static(__dirname + '/public'));
var server = http.createServer(app);
server.listen(port);

var wss = new WebSocketServer({ server: server });



// Set up variables
var serviceBus = 'cspi1-ns',
    eventHubName = 'ehdevices',
    sasKeyName = 'WebSite', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey = 'pAgoae/7zJ+FSvyAVJObDZM0e73dwSrD5GpbiSxySFI=', // The key value
    consumerGroup = 'nodejsconsumergroup',
    numPartitions = 8;

var uriappend = "ConsumerGroups/" + consumerGroup + "/Partitions/";

var Sbus = require('sbus-amqp10');
var hub = Sbus.EventHubClient(serviceBus, eventHubName, sasKeyName, sasKey);


// Set up variables
var serviceBus2 = 'cspi1-ns',
    eventHubName2 = 'ehalerts',
    sasKeyName2 = 'WebSite', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey2 = 'trgtkexrsPgvJZlDTdvsiYQTeMxpPt9DTDkIZfB1lrI=', // The key value
    consumerGroup2 = 'nodejsconsumergroup',
    numPartitions2 = 8;

var uriappend2 = "ConsumerGroups/" + consumerGroup + "/Partitions/";

var Sbus2 = require('sbus-amqp10');
var hub2 = Sbus2.EventHubClient(serviceBus, eventHubName, sasKeyName, sasKey);

wss.broadcast = function broadcast(data) {
    wss.clients.forEach(function each(client) {
        client.send(data);
    });
};

wss.on('connection', function connection(ws) {

    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
        wss.broadcast(message);
    });
  
});

//this is for reading from ehdevices
for (var idx = 0; idx < numPartitions; ++idx) {
    hub.eventHubReceive(uriappend + idx, new Date().getTime() - new Date().getTimezoneOffset(), function callback(rx_err, partition, payload) {
        if (rx_err) {
            console.log(rx_err);
        } else {
            console.log("partition: " + partition);
            console.log(payload);
         
            var tmpstring = JSON.stringify(payload);
            tmpstring = tmpstring.replace("}",",\"time\":\""+payload.timecreated+"\"}");
            wss.broadcast(tmpstring);
        }
    }
    );
}

//this is for reading from ehalerts
for (var idx = 0; idx < numPartitions2; ++idx) {
    hub2.eventHubReceive(uriappend2 + idx, new Date().getTime() - new Date().getTimezoneOffset(), function callback(rx_err, partition, payload) {
        if (rx_err) {
            console.log(rx_err);
        } else {
            console.log("partition: " + partition);
            console.log(payload);
            
            var tmpstring = JSON.stringify(payload);
            tmpstring = tmpstring.replace("}", ",\"time\":\"" + payload.timecreated + "\"}");
            wss.broadcast(tmpstring);
        }
    }
    );
}


