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

    if (eventObject['displayname'] == "Temp Average") {
        updateGauge('#container-speed', eventObject.value);
    }

    if (eventObject['displayname'] == "Light Average") {
        updateGauge('#container-speed2', eventObject.value);
    }



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

}
$(function () {
    $(document).ready(function () {

        var sss = (window.location.protocol.indexOf('s') > 0 ? "s" : "");
        var uri = 'ws' + sss + '://' + window.location.host + '/api/websocketconnect?clientId=none';
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        initGauge('#container-speed', 'Temperature Average');
        initGauge('#container-speed2', 'Light Average');
        initGraph();
        var connection = new WebSocket(uri);

        dataFlows.dataSource = new highchartCTDDataSourceSocket(uri).addEventListeners({ 'eventObject': onNewEvent, 'error': onError, 'open': onOpen });


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
            text: 'Real Live Data Sensors'
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
            name: 'Avg',
            data: [0],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">Your own unit</span></div>'
            },
            tooltip: {
                valueSuffix: ' C'
            }
        }]

    }));



}