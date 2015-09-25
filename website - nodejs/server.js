module.exports = require('./lib/sbus');


var http = require("http");
var express = require("express");
var app = express();
var port = process.env.PORT || 1337;


app.use(express.static(__dirname + '/public'));

var server = http.createServer(app);
server.listen(port);

var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({ server: server });



// Set up variables for DEVICES
var serviceBus = 'cspi1-ns',
    eventHubName = 'ehdevices',
    sasKeyName = 'WebSite', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey = 'pAgoae/7zJ+FSvyAVJObDZM0e73dwSrD5GpbiSxySFI=', // The key value
    consumerGroup = 'nodejsconsumergroup',
    numPartitions = 8;
var sbus = require('./lib/sbusclient');
var uriappend = "ConsumerGroups/" + consumerGroup + "/Partitions/";
var hub = sbus.EventHubClient(serviceBus, eventHubName, sasKeyName, sasKey);


// Set up variables for ALERTS
var serviceBus2 = 'cspi1-ns',
    eventHubName2 = 'ehalerts',
    sasKeyName2 = 'WebSite', // A SAS Key Name for the Event Hub, with Receive privilege
    sasKey2 = 'trgtkexrsPgvJZlDTdvsiYQTeMxpPt9DTDkIZfB1lrI=', // The key value
    consumerGroup2 = 'nodejsconsumergroup',
    numPartitions2 = 8;
var sbus2 = require('./lib/sbusclient');
var uriappend2 = "ConsumerGroups/" + consumerGroup2 + "/Partitions/";;
var hub2 = sbus2.EventHubClient(serviceBus2, eventHubName2, sasKeyName2, sasKey2);

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
            //console.log(payload);
		    var tmpstring;
			//multiline
			try {
			
                tmpstring = JSON.stringify(payload.split('\r\n'));
				var jsonObj = JSON.parse( tmpstring  );
		   
		   	for (var item in jsonObj)
					{
					var targetstring =  JSON.stringify(jsonObj[item]);
				    targetstring = targetstring.replace("}", ",\"time\":\"" + JSON.parse(jsonObj[item]).timecreated + "\"}");
				
                    
                    if (isValidJson(targetstring)) {
                        console.log("    sending : " + targetstring);
                        wss.broadcast(targetstring);
                    }
				}
			
			    tmpstring="";
				
			
			}
			//single item
			catch(err) {
				try{
						tmpstring = JSON.stringify(payload);
						tmpstring = tmpstring.replace("}", ",\"time\":\"" + payload.timecreated + "\"}");
                    
                    if (isValidJson(tmpstring)) {
                        console.log("    sending : " + tmpstring);
                        wss.broadcast(tmpstring);
                    }
				}catch (err){
				console.log(err.message);
				}
					tmpstring="";
			}


			
     
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
            //console.log(payload);
		    var tmpstring;
			//multiline
			try {
			
                tmpstring = JSON.stringify(payload.split('\r\n'));
				var jsonObj = JSON.parse( tmpstring  );
		   
		   	for (var item in jsonObj)
					{
					var targetstring =  JSON.stringify(jsonObj[item]);
					targetstring=JSON.parse(targetstring);
				    targetstring = targetstring.replace("}", ",\"time\":\"" + JSON.parse(jsonObj[item]).timecreated + "\"}");
                    
                   if( isValidJson(targetstring)) {
                        console.log("    sending : " + targetstring);
                        wss.broadcast(targetstring);
                    }
  
				}
			
			    tmpstring="";
				

			}
			//single item
			catch(err) {
			try{
					tmpstring = JSON.stringify(payload);
				    tmpstring = tmpstring.replace("}", ",\"time\":\"" + payload.timecreated + "\"}");
                   
                    if (isValidJson(tmpstring)) {
                        console.log("    sending : " + tmpstring);
                        wss.broadcast(tmpstring);
                    }
                    
			}catch (err){
			console.log(err.message);
			}
				
					tmpstring="";
			}

        }
    }
    );
}

function isValidJson(json) {
    try {
        JSON.parse(json);
        return true;
    } catch (e) {
        return false;
    }
}


