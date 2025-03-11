<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM barangay");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['barangayName'], $data['cityID'])) {
            $stmt = $conn->prepare("INSERT INTO barangay (barangayName, cityID) VALUES (?, ?)");
            $stmt->execute([$data['barangayName'], $data['cityID']]);
            echo json_encode(["message" => "Barangay added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['barangayID'], $data['barangayName'], $data['cityID'])) {
            $stmt = $conn->prepare("UPDATE barangay SET barangayName = ?, cityID = ? WHERE barangayID = ?");
            $stmt->execute([$data['barangayName'], $data['cityID'], $data['barangayID']]);
            echo json_encode(["message" => "Barangay updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM barangay WHERE barangayID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Barangay deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>
