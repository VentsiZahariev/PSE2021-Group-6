<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="refresh" content="180">
 <meta http-equiv="content-type" content="text/html:charset=utf-8"/>
 <title>TechJunkGigs</title>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
</head>
<body>
<div class="container">
  <div class="columns">

  <div class="column">
<div id="temp_chart"></div>
<!--<p id="test"></p> -->
</div>

<div class="column">
  <div id="chart_div_hum"></div>
</div>
</div>

<div class="columns">
  <div class="column">
      <div id="chart_div_pre"></div>
        </div>
        <div class="column">
          <div id="chart_div_light"></div>
        </div>

   </div>
</div>

 <script type="text/javascript">

document.addEventListener('DOMContentLoaded', () => {

    const checkboxEns = document.getElementById('hideEns')
    const checkboxWie1 = document.getElementById('hideWie1')
    const checkboxGro = document.getElementById('hideGro')
    const checkboxWie2 = document.getElementById('hideWie2')
    const checkboxShowAll = document.getElementById('showAll')

 google.charts.load('current', {'packages':['corechart']});
 google.charts.setOnLoadCallback(drawChart);
google.charts.setOnLoadCallback(drawHum);
google.charts.setOnLoadCallback(drawPre);
google.charts.setOnLoadCallback(drawLight);

 function drawChart() {
 var data = new google.visualization.arrayToDataTable([
['Time','Wierden - In','Saxion'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}

//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(temperature),2) AS temperature FROM `pysense` WHERE location = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)GROUP BY DATE(log_time),HOUR(log_time)");
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(temperature),2) AS temperature FROM`pysense` WHERE location = 'saxion' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)GROUP BY DATE(log_time),HOUR(log_time)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['temperature'].",".$row1['temperature']."],";
}
?>
]);

 var data1 = new google.visualization.arrayToDataTable([
['Time','Wierden - Out','Gronau'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}
//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,temperature FROM `dragino` WHERE location  = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
//loop through the returned data
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,temperature FROM `dragino` WHERE location = 'gronau' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['temperature'].",".$row1['temperature']."],";
}
?>
]);
var joinedData = google.visualization.data.join(data, data1, 'full', [[0, 0]],[1,2],[1,2]);
var options = {
            interpolateNulls:true,
 hAxis: {
        title: 'Time',
        titleTextStyle: {
            bold: true
        }
      },
      vAxis: {
        title: 'Temperature (      C)',
        titleTextStyle: {
            bold: true,
            italic: false
        }
      },
      series: {
        1: {curveType: 'function'}
      },
      legend: {
          position: 'top'
      }
                };
var chart = new google.visualization.LineChart(document.getElementById('temp_chart'));
chart.draw(joinedData, options)

  checkboxShowAll.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      chart.draw(view, options);
    }
  })

  checkboxEns.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 3, 4]);
      chart.draw(view, options);
    }
  })

  checkboxWie1.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([2, 3, 4]);
      chart.draw(view, options);
    }
  })

  checkboxGro.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 2, 3]);
      chart.draw(view, options);
    }
  })

  checkboxWie2.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 2, 4]);
      chart.draw(view, options);
    }
  })

};

function drawPre(){
var data = new google.visualization.arrayToDataTable([
['Time','Wierden - In','Saxion'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}


//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(pressure),2) AS pressure FROM `pysense` WHERE location = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR) GROUP BY DATE(log_time),HOUR(log_time)");
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(pressure),2) AS pressure FROM `pysense` WHERE location = 'saxion' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR) GROUP BY DATE(log_time),HOUR(log_time)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['pressure'].",".$row1['pressure']."],";
}
?>
]);

var options = {
            interpolateNulls:true,
 hAxis: {
        title: 'Time',
        titleTextStyle: {
            bold: true
        }
      },
      vAxis: {
        title: 'Pressure (Pa )',
        titleTextStyle: {
            bold: true,
            italic: false
        }
      },
      series: {
        1: {curveType: 'function'}
      },
      legend: {
          position: 'top'
      }
                };
var chart1 = new google.visualization.LineChart(document.getElementById('chart_div_hum'));
chart1.draw(data, options)

  checkboxShowAll.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart1.draw(view, options);
    }
  })

  checkboxEns.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      view.hideColumns([1]);
      chart1.draw(view, options);
    }
  })

  checkboxWie1.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      view.hideColumns([2]);
      chart1.draw(view, options);
    }
  })

 checkboxGro.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart1.draw(view, options);
    }
  })

  checkboxWie2.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart1.draw(view, options);
    }
  })

};

function drawHum(){
 var data = new google.visualization.arrayToDataTable([
['Time','Wierden - Out','Gronau'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}
//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,humidity FROM `dragino` WHERE location = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,humidity FROM `dragino` WHERE location = 'gronau' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['humidity'].",".$row1['humidity']."],";
}
?>
]);

var options = {
            interpolateNulls:true,
 hAxis: {
        title: 'Time',
        titleTextStyle: {
            bold: true
        }
      },
      vAxis: {
        title: 'Humidity (% )',
        titleTextStyle: {
            bold: true,
            italic: false
        }
      },
      series: {
        1: {curveType: 'function'}
      },
      legend: {
          position: 'top'
      }
                };
var chart = new google.visualization.LineChart(document.getElementById('chart_div_pre'));
chart.draw(data, options)

  checkboxShowAll.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart.draw(view, options);
    }
  })

  checkboxWie2.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      view.hideColumns([2]);
      chart.draw(view, options);
    }
  })

  checkboxGro.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      view.hideColumns([1]);
      chart.draw(view, options);
    }
  })

 checkboxEns.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart.draw(view, options);
    }
  })

  checkboxWie1.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(data);
      chart.draw(view, options);
    }
  })

};

function drawLight(){
 var data = new google.visualization.arrayToDataTable([
['Time','Wierden - In','Saxion'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}

//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(light),2) AS light FROM `pysense` WHERE location = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR) GROUP BY DATE(log_time),HOUR(log_time)");
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(light),2) AS light FROM `pysense` WHERE location = 'saxion' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR) GROUP BY DATE(log_time),HOUR(log_time)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['light'].",".$row1['light']."],";
}
?>
]);


 var data1 = new google.visualization.arrayToDataTable([
['Time','Wierden - Out','Gronau'],
<?php
$mysqli = new mysqli('localhost', 'PSEgroup6', 'battlefield4', 'weather_log');

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}
//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,light FROM `dragino` WHERE location  = 'wierden' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
//loop through the returned data
$result1 = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,light FROM `dragino` WHERE location = 'gronau' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)");
while (( $row=$result->fetch_assoc())& ($row1=$result1->fetch_assoc())) {
  echo "['".$row['time']."',".$row['light'].",".$row1['light']."],";
}
?>
]);

var joinedData = google.visualization.data.join(data, data1, 'full', [[0, 0]],[1,2],[1,2]);
var options = {
            interpolateNulls:true,
 hAxis: {
        title: 'Time',
        titleTextStyle: {
            bold: true
        }
      },
      vAxis: {
        title: 'Light(%)',
        titleTextStyle: {
            bold: true,
            italic: false
        }
      },
      series: {
        1: {curveType: 'function'}
      },
      legend: {
          position: 'top'
      }
                };
var chart = new google.visualization.LineChart(document.getElementById('chart_div_light'));
chart.draw(joinedData, options)

  checkboxShowAll.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      chart.draw(view, options);
    }
  })

  checkboxEns.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 3, 4]);
      chart.draw(view, options);
    }
  })

  checkboxWie1.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([2, 3, 4]);
      chart.draw(view, options);
    }
  })

  checkboxGro.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 2, 3]);
      chart.draw(view, options);
    }
  })

  checkboxWie2.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      view = new google.visualization.DataView(joinedData);
      view.hideColumns([1, 2, 4]);
      chart.draw(view, options);
    }
  })

};

});

  </script>

</body>
</html>
