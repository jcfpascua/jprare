<?php
$dsn = 'mysql:host=localhost;dbname=jprare_database;charset=utf8';
$user = 'root'; // Default username for XAMPP
$pass = ''; // Default password for XAMPP (usually empty)

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

try {
    $conn = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    echo json_encode(["error" => "Connection failed: " . $e->getMessage()]);
    exit;
}
?>
