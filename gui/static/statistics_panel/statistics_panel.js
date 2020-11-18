// 導覽列

$(function(){$("#statistics_panel").addClass("active");});


// Load packages 

google.charts.load('current', { packages: ['corechart', 'line'] });
google.charts.load('current', { packages: ['corechart', 'scatter'] });

// Set EventListener

google.charts.setOnLoadCallback(() => {
    drawMoistChart();
    drawTempChart();
    drawLightChart();
    drawPressureChart();
    drawWateringChart();
});
$(window).resize(function () {
    drawMoistChart();
    drawTempChart();
    drawLightChart();
    drawPressureChart();
    drawWateringChart();
});

$(function () {
    $(".dropdown-menu").on("click", ".dropdown-item", function() {

        switch (this.id) {
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
        $.ajax({ type:"GET",url: "/statistics_panel_shift/",data:{'timerange':this.id,}, success: function(result){
            // drawMoistChart(result[0]);
            // drawTempChart(result[1]);
            // drawLightChart(result[2]);
            // drawPressureChart(result[3]);
            // drawWateringChart(result[4]);
            console.log(JSON.stringify(result));
          }});
    });

})



// Handles transfer of dropbox title

// Chart of Moisture
function drawMoistChart(input = []) {
    var data = new google.visualization.DataTable();
    let moistData;
    if (input && input.length) {
        moistData = input;
    }
    else {
        moistData = [
            [0, 0, 0], [1, 10, 5], [2, 23, 15], [3, 17, 9], [4, 18, 10], [5, 9, 5],
            [6, 11, 3], [7, 27, 19], [8, 33, 25], [9, 40, 32], [10, 32, 24], [11, 35, 27],
            [12, 30, 22], [13, 40, 32], [14, 42, 34], [15, 47, 39], [16, 44, 36], [17, 48, 40],
            [18, 52, 44], [19, 54, 46], [20, 42, 34], [21, 55, 47], [22, 56, 48], [23, 57, 49],
            [24, 60, 52], [25, 50, 42], [26, 52, 44], [27, 51, 43], [28, 49, 41], [29, 53, 45],
            [30, 55, 47], [31, 60, 52], [32, 61, 53], [33, 59, 51], [34, 62, 54], [35, 65, 57],
            [36, 62, 54], [37, 58, 50], [38, 55, 47], [39, 61, 53], [40, 64, 56], [41, 65, 57],
            [42, 63, 55], [43, 66, 58], [44, 67, 59], [45, 69, 61], [46, 69, 61], [47, 70, 62],
            [48, 72, 64], [49, 68, 60], [50, 66, 58], [51, 65, 57], [52, 67, 59], [53, 70, 62],
            [54, 71, 63], [55, 72, 64], [56, 73, 65], [57, 75, 67], [58, 70, 62], [59, 68, 60],
            [60, 64, 56], [61, 60, 52], [62, 65, 57], [63, 67, 59], [64, 68, 60], [65, 69, 61],
            [66, 70, 62], [67, 72, 64], [68, 75, 67], [69, 80, 72]
        ];
    }
    data.addColumn('number', 'X');
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
    let tempData;
    if (input && input.length) {
        tempData = input;
    }
    else {
        tempData = [
            [0, 20], [1, 25], [2, 30], [3, 25], [4, 35], [5, 15],
            [6, 11], [7, 19], [8, 22], [9, 17], [10, 24], [11, 35],
            [12, 30], [13, 40], [14, 42], [15, 47], [16, 36], [17, 40],
            [18, 44], [19, 46], [20, 34], [21, 47], [22, 48], [23, 49],
            [24, 50], [25, 42], [26, 44], [27, 43], [28, 41], [29, 45],
            [30, 40], [31, 22], [32, 13], [33, 51], [34, 54], [35, 57],
            [36, 54], [37, 50], [38, 47], [39, 53], [40, 56], [41, 57],
            [42, 55], [43, 58], [44, 59], [45, 61], [46, 61], [47, 62],
            [48, 64], [49, 60], [50, 58], [51, 57], [52, 59], [53, 62],
            [54, 36], [55, 40], [56, 35], [57, 27], [58, 32], [59, 20],
            [60, 55], [61, 52], [62, 37], [63, 59], [64, 60], [65, 27],
            [66, 42], [67, 34], [68, 27], [69, 32]
        ];
    }
    data.addColumn('number', 'X');
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
    let lightData;
    if (input && input.length) {
        lightData = input;
    }
    else {
        lightData = [
            [0, 20], [1, 25], [2, 30], [3, 25], [4, 35], [5, 15],
            [6, 11], [7, 19], [8, 22], [9, 17], [10, 24], [11, 35],
            [12, 30], [13, 40], [14, 42], [15, 47], [16, 36], [17, 40],
            [18, 44], [19, 46], [20, 34], [21, 47], [22, 48], [23, 49],
            [24, 52], [25, 42], [26, 44], [27, 43], [28, 41], [29, 45],
            [30, 47], [31, 52], [32, 53], [33, 51], [34, 54], [35, 57],
            [36, 54], [37, 50], [38, 47], [39, 53], [40, 56], [41, 57],
            [42, 55], [43, 58], [44, 59], [45, 61], [46, 61], [47, 62],
            [48, 64], [49, 60], [50, 58], [51, 57], [52, 59], [53, 62],
            [54, 63], [55, 64], [56, 65], [57, 67], [58, 62], [59, 60],
            [60, 56], [61, 52], [62, 57], [63, 59], [64, 60], [65, 61],
            [66, 62], [67, 64], [68, 67], [69, 72]
        ];
    }

    data.addColumn('number', 'X');
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

// Chart of Temp
function drawPressureChart(input = []) {
    var data = new google.visualization.DataTable();
    let presData;
    if (input && input.length) {
        presData = input;
    }
    else {
        presData = [
            [0, 20], [1, 25], [2, 30], [3, 25], [4, 35], [5, 15],
            [6, 11], [7, 19], [8, 22], [9, 17], [10, 24], [11, 35],
            [12, 30], [13, 40], [14, 42], [15, 47], [16, 36], [17, 40],
            [18, 44], [19, 46], [20, 34], [21, 47], [22, 48], [23, 49],
            [24, 50], [25, 42], [26, 44], [27, 43], [28, 41], [29, 45],
            [30, 40], [31, 22], [32, 13], [33, 51], [34, 54], [35, 57],
            [36, 54], [37, 50], [38, 47], [39, 53], [40, 56], [41, 57],
            [42, 55], [43, 58], [44, 59], [45, 61], [46, 61], [47, 62],
            [48, 64], [49, 60], [50, 58], [51, 57], [52, 59], [53, 62],
            [54, 36], [55, 40], [56, 35], [57, 27], [58, 32], [59, 20],
            [60, 55], [61, 52], [62, 37], [63, 59], [64, 60], [65, 27],
            [66, 42], [67, 34], [68, 27], [69, 32]
        ];
    }

    data.addColumn('number', 'X');
    data.addColumn('number', '氣壓');
    data.addRows(presData);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Pessures'
        },
        colors: ['#a52714', '#097138'],
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div4'));
    chart.draw(data, options);
    chart.setSelection([{ row: 38, column: 1 }]);
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
            [5, 1], [10, 1],
            [51, 1], [63, 1],
            [69, 1]
        ];
    }

    data.addColumn('number', 'X');
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

    var chart = new google.visualization.ScatterChart(document.getElementById('chart_div5'));
    chart.draw(data, options);
    chart.setSelection([{ row: 38, column: 1 }]);
}

