<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM merchant");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchant_name'], $data['addressID'])) {
            $stmt = $conn->prepare("INSERT INTO merchant (merchant_name, addressID) VALUES (?, ?)");
            $stmt->execute([$data['merchant_name'], $data['addressID']]);
            echo json_encode(["message" => "Merchant added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchantID'], $data['merchant_name'], $data['addressID'])) {
            $stmt = $conn->prepare("UPDATE merchant SET merchant_name = ?, addressID = ? WHERE merchantID = ?");
            $stmt->execute([$data['merchant_name'], $data['addressID'], $data['merchantID']]);
            echo json_encode(["message" => "Merchant updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM merchant WHERE merchantID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Merchant deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>