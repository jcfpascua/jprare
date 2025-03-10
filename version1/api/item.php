<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM item");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['item_name'])) {
            $stmt = $conn->prepare("INSERT INTO item (item_name) VALUES (?)");
            $stmt->execute([$data['item_name']]);
            echo json_encode(["message" => "Item added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['itemID'], $data['item_name'])) {
            $stmt = $conn->prepare("UPDATE item SET item_name = ? WHERE itemID = ?");
            $stmt->execute([$data['item_name'], $data['itemID']]);
            echo json_encode(["message" => "Item updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM item WHERE itemID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Item deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>