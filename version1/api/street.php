<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM street");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['street_name'], $data['barangayID'])) {
            $stmt = $conn->prepare("INSERT INTO street (streetname, barangayID) VALUES (?, ?)");
            $stmt->execute([$data['street_name'], $data['barangayID']]);
            echo json_encode(["message" => "Street added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['streetID'], $data['street_name'], $data['barangayID'])) {
            $stmt = $conn->prepare("UPDATE street SET streetname = ?, barangayID = ? WHERE streetID = ?");
            $stmt->execute([$data['street_name'], $data['barangayID'], $data['streetID']]);
            echo json_encode(["message" => "Street updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM street WHERE streetID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Street deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>