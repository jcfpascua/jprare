<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM address");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['description'], $data['streetID'])) {
            $stmt = $conn->prepare("INSERT INTO address (description, streetID) VALUES (?, ?)");
            $stmt->execute([$data['description'], $data['streetID']]);
            echo json_encode(["message" => "Address added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['addressID'], $data['description'], $data['streetID'])) {
            $stmt = $conn->prepare("UPDATE address SET description = ?, streetID = ? WHERE addressID = ?");
            $stmt->execute([$data['description'], $data['streetID'], $data['addressID']]);
            echo json_encode(["message" => "Address updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM address WHERE addressID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Address deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>
