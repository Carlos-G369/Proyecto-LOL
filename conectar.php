<?php
// configuracion de la base de datos 
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "league_of_legends";

//crear la conexion 
$conn = new mysqli($servername, $username, $password, $dbname);
 
// verificar la conexion 
if ($conn->connect_error) {
    die("Conexion fallida : " . $conn->connect_error);
}else {
    echo "Conexión exitosa";
}

?>