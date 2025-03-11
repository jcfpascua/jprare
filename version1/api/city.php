<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM city");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['cityName'])) {
            $stmt = $conn->prepare("INSERT INTO city (cityName) VALUES (?)");
            $stmt->execute([$data['cityName']]);
            echo json_encode(["message" => "City added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['cityID'], $data['cityName'])) {
            $stmt = $conn->prepare("UPDATE city SET cityName = ? WHERE cityID = ?");
            $stmt->execute([$data['cityName'], $data['cityID']]);
            echo json_encode(["message" => "City updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM city WHERE cityID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "City deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>
