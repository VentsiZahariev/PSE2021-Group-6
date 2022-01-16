<?php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', 'localhost');
define('DB_USERNAME', 'PSEgroup6');
define('DB_PASSWORD', 'battlefield4');
define('DB_NAME', 'weather_log');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}

//query to get data  from table
$result = $mysqli->query("SELECT DATE_FORMAT(log_time,'%e %b %H:%i') AS time,ROUND(AVG(temperature),2) AS temperature FROM `pysense` WHERE location = 'saxion' AND log_time BETWEEN DATE_SUB(NOW(),INTERVAL 7 HOUR) AND DATE_SUB(NOW(),INTERVAL 0 HOUR)GROUP BY DATE(log_time),HOUR(log_time)");

//loop through the returned data
$data = array();
foreach ($result as $row) {
  $data[] = $row;
}

//free memory associated with result
$result->close();
//close connection
$mysqli->close();

//now print the data
echo json_encode($data);
