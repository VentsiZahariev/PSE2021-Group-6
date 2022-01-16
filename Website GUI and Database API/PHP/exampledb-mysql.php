<?php
$link = mysqli_connect("127.0.0.1", "exampleuser", "pimylifeup", "exampledb");
if($link) {
$query = mysqli_query($link, "SELECT * FROM test");
while($array = mysqli_fetch_array($query)) {
echo $array['data']."<br />";
} }
else {
echo "MySQL error :".mysqli_error();
}
?>
