<?php
// Datos de conexión a la base de datos
$servername = "localhost"; 
$username = "root"; 
$password = ""; 
$database = "league_of_legends"; 

// Crear conexión
$conn = new mysqli($servername, $username, $password, $database);

// Verificar conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}
    

// Consulta SQL para obtener datos de la tabla Jugador
$sql = "SELECT id_jugador, nombre, nivel, region FROM Jugador";
$result = $conn->query($sql);

// Comprobar si hay datos en el resultado
if ($result->num_rows > 0) {
    // Crear tabla HTML
    echo "<table border='1'>";
    echo "<tr><th>ID Jugador</th><th>Nombre</th><th>Nivel</th><th>Región</th></tr>";

    // Mostrar datos en filas
    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . $row["id_jugador"] . "</td>";
        echo "<td>" . $row["nombre"] . "</td>";
        echo "<td>" . $row["nivel"] . "</td>";
        echo "<td>" . $row["region"] . "</td>";
        echo "</tr>";
    }

    echo "</table>";
} else {
    echo "No hay datos en la tabla.";
}

// Cerrar conexión
$conn->close();
?>
