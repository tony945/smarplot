// Global variables

let temp = [];
let light = [];
let moist = [];

// 導覽列

$(function () { $("#statistics_panel").addClass("active"); });


// Load packages 

google.charts.load('current', { packages: ['corechart', 'line'] });
google.charts.load('current', { packages: ['corechart', 'scatter'] });


// Trigger onload

google.charts.setOnLoadCallback(() => {
    $.ajax({
        type: "GET",
        url: "/statistics_panel_shift/",
        data: { 'timerange': 'day', },
        success: function (result) {
            result.forEach(element => {
               
                let Datenow = new Date(element.create_time.slice(0,-1))
                let year = Datenow.getFullYear();
                let month = Datenow.getMonth();
                let date = Datenow.getDate();
                let hour = Datenow.getHours();
                let minute = Datenow.getMinutes();
                console.log(Datenow);
                console.log(year,month,date,hour,minute);
                temp.push([new Date(year, month, date, hour, minute), element.temperature]);
                moist.push([new Date(year, month, date, hour, minute), element.soil, element.air]);
                light.push([new Date(year, month, date, hour, minute), element.light]);
            });

            drawMoistChart(moist);
            drawLightChart(light);
            drawTempChart(temp);
            drawWateringChart();
        }
    });
});


// Set EventListener

$(window).resize(function () {
    drawMoistChart(moist);
    drawTempChart(temp);
    drawLightChart(light);
    drawWateringChart();
});

$(function () {
    $(".dropdown-menu").on("click", ".dropdown-item", function () {
        var timeRange = this.id
        switch (timeRange) {
            case 'year':
                $('#navbardrop').html("年(year)")
                break;
            case 'month':
                $('#navbardrop').html("月(month)")
                break;
            case 'day':
                $('#navbardrop').html("日(day)")
                break;
        }

        // sends the timerange chosen from the dropdown list 
        $.ajax({
            type: "GET", url: "/statistics_panel_shift/",
            data: { 'timerange': timeRange, },
            success: function (result) {
                // data = JSON.stringify(result)
                let temp = [];
                let light = [];
                let moist = [];
                switch (timeRange) {
                    case 'year':
                        result.forEach(element => {
                            let Datenow = new Date(element.create_time);
                            let year = Datenow.getFullYear();
                            let month = Datenow.getMonth();
                            temp.push([new Date(year, month), element.temperature]);
                            moist.push([new Date(year, month), element.soil, element.air]);
                            light.push([new Date(year, month), element.light]);
                        });
                        break;
                    case 'month':
                        result.forEach(element => {
                            let Datenow = new Date(element.create_time);
                            let year = Datenow.getFullYear();
                            let month = Datenow.getMonth();
                            let date = Datenow.getDate();
                            temp.push([new Date(year, month, date), element.temperature]);
                            moist.push([new Date(year, month, date), element.soil, element.air]);
                            light.push([new Date(year, month, date), element.light]);
                        });
                        break;
                    case 'day':
                        result.forEach(element => {
                            let Datenow = new Date(element.create_time.slice(0,-1))
                            let year = Datenow.getFullYear();
                            let month = Datenow.getMonth();
                            let date = Datenow.getDate();
                            let hour = Datenow.getHours();
                            let minute = Datenow.getMinutes();
                            temp.push([new Date(year, month, date, hour, minute), element.temperature]);
                            moist.push([new Date(year, month, date, hour, minute), element.soil, element.air]);
                            light.push([new Date(year, month, date, hour, minute), element.light]);
                        });
                        break;
                }

                drawMoistChart(moist);
                drawLightChart(light);
                drawTempChart(temp);
                drawWateringChart();
            }
        });
    });
});


// Shuts downloading anime and show chart

window.setTimeout((() => {
    $("#chartContainer").css("visibility", "visible");
    $("#spin").css("display", "none");
}), 1000);


// Chart of Moisture
function drawMoistChart(input = []) {
    var data = new google.visualization.DataTable();
    let moistData = input;
    data.addColumn('date', '時間');
    data.addColumn('number', '土壤濕度');
    data.addColumn('number', '空氣濕度');
    data.addRows(moistData);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Humidity'
        },
        colors: ['#a52714', '#097138'],
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div1'));

    chart.draw(data, options);
    chart.setSelection([{ row: 38, column: 1 }]);
}


// Chart of Temp
function drawTempChart(input = []) {
    var data = new google.visualization.DataTable();
    let tempData = input;

    data.addColumn('date', '時間');
    data.addColumn('number', '溫度');
    data.addRows(tempData);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Temperature'
        },
        colors: ['#a52714', '#097138'],
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div2'));
    chart.draw(data, options);
    chart.setSelection([{ row: 38, column: 1 }]);
}


// Chart of Light
function drawLightChart(input = []) {
    var data = new google.visualization.DataTable();
    var lightData = input;

    data.addColumn('date', '時間');
    data.addColumn('number', '光照強度');
    data.addRows(lightData);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Light'
        },
        colors: ['#a52714', '#097138'],
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    var chart1 = new google.visualization.LineChart(document.getElementById('chart_div3'));
    chart1.draw(data, options);
    chart1.setSelection([{ row: 38, column: 1 }]);
}


// Chart of record of watering
function drawWateringChart(input = []) {
    var data = new google.visualization.DataTable();
    let record;
    if (input && input.length) {
        record = input;
    }
    else {
        record = [
            // [10, 1], [13, 1],
            // [25, 1], [40, 1],
            // [56, 1]
        ];
    }

    data.addColumn('date', 'X');
    data.addColumn('number', '次數');
    data.addRows(record);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Watering Times'
        },
        colors: ['#a52714', '#097138'],
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('chart_div4'));
    chart.draw(data, options);
    chart.setSelection([{ row: 38, column: 1 }]);
}

