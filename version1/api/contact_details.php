<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM contact_details");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customerID'], $data['value'])) {
            $stmt = $conn->prepare("INSERT INTO contact_details (customerID, value) VALUES (?, ?)");
            $stmt->execute([$data['customerID'], $data['value']]);
            echo json_encode(["message" => "Contact detail added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['contactID'], $data['customerID'], $data['value'])) {
            $stmt = $conn->prepare("UPDATE contact_details SET customerID = ?, value = ? WHERE contactID = ?");
            $stmt->execute([$data['customerID'], $data['value'], $data['contactID']]);
            echo json_encode(["message" => "Contact detail updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM contact_details WHERE contactID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Contact detail deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>