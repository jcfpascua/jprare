<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM contact_type");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['title'])) {
            $stmt = $conn->prepare("INSERT INTO contact_type (title) VALUES (?)");
            $stmt->execute([$data['title']]);
            echo json_encode(["message" => "Contact type added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['contact_typeID'], $data['title'])) {
            $stmt = $conn->prepare("UPDATE contact_type SET title = ? WHERE contact_typeID = ?");
            $stmt->execute([$data['title'], $data['contact_typeID']]);
            echo json_encode(["message" => "Contact type updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM contact_type WHERE contact_typeID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Contact type deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>