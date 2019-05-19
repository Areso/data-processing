<?php
ini_set("default_charset",'utf-8');//utf-8 windows-1251
ini_set('display_errors', 1);
error_reporting('E_ALL & E_STRICT');
$params = ($_GET["params"]);
$paramsArray = explode("_", $params);
$longitude = $paramsArray[0];
$latitude = $paramsArray[1];
$layer = $paramsArray[2];
$thecommandtocall = 'python3 /var/www/html/hack/app_intersects.py '.$longitude.' '.$latitude.' '.$layer;
echo $thecommandtocall;
$output = exec($thecommandtocall);
echo $output;
//56.828789,60.621433 0.0 1.0
//curl 51.68.172.115/hack/index.php?params="56.8463371_60.6142361_1.0"
?>
