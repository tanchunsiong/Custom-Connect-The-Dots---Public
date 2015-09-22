var dataFlows = {};
var bulkMode = false;
var self;
var $message;
String.prototype.hashCode = function () {
    var hash = 0;
    if (this.length == 0) return hash;
    for (var i = 0, len = this.length; i < len; i++) {
        var chr = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + chr;
        hash |= 0;
    }
    return hash;
};

function onError(evt) {
    
}

function onOpen(evt) {
   
}
function checkBulkMode(evt) {
    if (evt.bulkData != undefined) {
        bulkMode = evt.bulkData;

        // alert all charts
        for (var id in dataFlows) {
            if (dataFlows[id].chart)
                dataFlows[id].chart.setBulkMode(bulkMode);
        }
    }
}
function updateChart(item, measurenameHash) {

    var series = self.series[0];
    var redrawVal = true;
    var shiftVal = false;

    if (series.data && series.data.length > 25) { shiftVal = true; }

    var newseries = {

        x: 0,
        y: 0,
        name: ""
    };

    newseries.name = item.measurename;
    newseries.x = Date.parse(item.timecreated);
    newseries.y = item.value;

    var series = self.get(measurenameHash);
    if (series) { // series already exists
        series.addPoint([newseries.x, newseries.y], redrawVal, shiftVal);
    } else { //  new series
        self.addSeries({
            name: item.displayname + ":" + item.measurename,
            data: [newseries],
            id: measurenameHash
        });
    }
}

function updateGauge(controlname, heartbeat) {
    var chart = $(controlname).highcharts(),
          point,
          newVal,
          inc;

    if (chart) {
        point = chart.series[0].points[0];
        
        newVal = heartbeat;

   

        point.update(newVal);
    }

}
function addNewDataFlow(eventObject) {
    var measurenameOriginal = eventObject['measurename'] + eventObject['displayname'];
    var measurenameHash = measurenameOriginal.hashCode();
    updateChart(eventObject, measurenameHash);

    if (eventObject['measurename'] == "SSH Failed Login Attempt" && eventObject['displayname'] == "Average SSH Failed Login Attempt") {
        updateGauge('#container-speed', eventObject.value);
    }

    if (eventObject['measurename'] == "HeartRate" && eventObject['displayname'] == "Tan Chun Siong") {
        updateGauge('#container-speed2', eventObject.value);
    }
   
    
    
    // create chart if necessary
    //if (!dataFlows.hasOwnProperty(measurenameHash)) {
    //    dataFlows[measurenameHash] = {
    //        containerId: 'chart_' + measurenameHash,
    //        controllerId: 'controller_' + measurenameHash,
    //        dataSourceFilter: new d3CTDDataSourceFilter(dataFlows.dataSource, { measurename: measurenameOriginal }),
    //        flows: {}
    //    };
    //    // create flows controller
    //    $('#controllersContainer').append('<ul id="' + dataFlows[measurenameHash].controllerId + '" style="top: ' + (Object.keys(dataFlows).length - 2) * 300 + 'px;" class="controller"></ul>');
    //    dataFlows[measurenameHash].controller = new d3ChartControl(dataFlows[measurenameHash].controllerId)
    //                .attachToDataSource(dataFlows[measurenameHash].dataSourceFilter);

    //    // add new div object
    //    $('#chartsContainer').height((Object.keys(dataFlows).length - 1) * 300 + 'px');
    //    $('#chartsContainer').append('<div id="' + dataFlows[measurenameHash].containerId + '" style="top: ' + (Object.keys(dataFlows).length - 2) * 300 + 'px;" class="chart"></div>');
    //    // create chart
    //    dataFlows[measurenameHash].chart = (new d3Chart(dataFlows[measurenameHash].containerId))
    //                .addEventListeners({ 'loading': onLoading, 'loaded': onLoaded })
    //                .attachToDataSource(dataFlows[measurenameHash].dataSourceFilter)
    //                .setFilter(dataFlows[measurenameHash].controller)
    //                .setBulkMode(bulkMode);

    //};

    //// add new flow
    //var newFlow = new d3DataFlow(eventObject.guid);

    ////addNewSensorOption(newFlow, eventObject);

    //dataFlows[measurenameHash].flows[eventObject.guid] = newFlow;

    //dataFlows[measurenameHash].chart.addFlow(newFlow, 0);

    //$(window).resize();
}
function onNewEvent(evt) {
    var eventObject = evt.owner;
    var flowCnt = dataFlows.length;

    // check bulk mode
    checkBulkMode(eventObject);

    // check object necessary properties
    if (!eventObject.hasOwnProperty('guid') || !eventObject.hasOwnProperty('measurename')) return;
    var measurenameHash = eventObject['measurename'].hashCode();
    // auto add flows
    if (!dataFlows.hasOwnProperty(measurenameHash) || !dataFlows[measurenameHash].flows.hasOwnProperty(eventObject['guid']))
        addNewDataFlow(eventObject);

    //if (eventObject.alerttype != null) {
    //    var table = $('#alertTable').DataTable();
    //    var time = new Date(eventObject.timecreated);

    //    // Check if we already have this one in the table already to prevent duplicates
    //    var indexes = table.rows().eq(0).filter(function (rowIdx) {
    //        if (
    //            table.cell(rowIdx, 0).data().getTime() == time.getTime() && table.cell(rowIdx, 1).data() == eventObject.displayname && table.cell(rowIdx, 2).data() == eventObject.alerttype) {
    //            return true;
    //        }
    //        return false;
    //    });

    //    //// The alert is a new one, lets display it
    //    //if (indexes.length == 0) {
    //    //    // For performance reasons, we want to limit the number of items in the table to a max of 20. 
    //    //    // We will remove the oldest from the list
    //    //    if (table.data().length > 19) {
    //    //        // Search for the oldest time in the list of alerts
    //    //        var minTime = table.data().sort(

    //    //            function (a, b) {
    //    //                return (a[0] > b[0]) - (a[0] < b[0])
    //    //            })[0][0];
    //    //        // Delete the oldest row
    //    //        table.rows(

    //    //            function (idx, data, node) {
    //    //                return data[0].getTime() == minTime.getTime();
    //    //            }).remove();
    //    //    }

    //    //    // Add the new alert to the table
    //    //    var message = 'message';
    //    //    if (eventObject.message != null) message = eventObject.message;
    //    //    table.row.add([
    //    //        time,
    //    //        eventObject.displayname,
    //    //        eventObject.alerttype,
    //    //        message
    //    //    ]).draw();

    //    //}
    //}
}
$(function () {
    $(document).ready(function () {

        // create datasource
        var sss = (window.location.protocol.indexOf('s') > 0 ? "s" : "");
       // var uri = 'ws://localhost:51716/api/websocketconnect?clientId=none';
        var uri = 'ws://cspi2.azurewebsites.net/api/websocketconnect?clientId=none';
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        initGauge('#container-speed','SSH Attempts');
        initGauge('#container-speed2', 'Heartbeat of Tan Chun Siong');
        initGraph();
        var connection = new WebSocket(uri);
        
        dataFlows.dataSource = new d3CTDDataSourceSocket(uri).addEventListeners({ 'eventObject': onNewEvent, 'error': onError, 'open': onOpen });

      
    });
});
function initGraph() {
    $('#container').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    $message = $('#message');

                  
                    self = this;
                 
                }
            }
        },
        title: {
            text: 'Real Live Data of Presenters on Stage'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = 0; i < 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.random()
                    });
                }
                return data;
            }())
        }]

    });

}
function initGauge(controlname, displayname) {

    var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The speed gauge
    $(controlname).highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 200,
            title: {
                text: displayname
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'Speed',
            data: [0],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">Per Sec</span></div>'
            },
            tooltip: {
                valueSuffix: ' BPS'
            }
        }]

    }));

   
  
}