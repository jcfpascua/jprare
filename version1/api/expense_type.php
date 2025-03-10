<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM expense_type");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['title'])) {
            $stmt = $conn->prepare("INSERT INTO expense_type (title) VALUES (?)");
            $stmt->execute([$data['title']]);
            echo json_encode(["message" => "Expense type added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['expense_typeID'], $data['title'])) {
            $stmt = $conn->prepare("UPDATE expense_type SET title = ? WHERE expense_typeID = ?");
            $stmt->execute([$data['title'], $data['expense_typeID']]);
            echo json_encode(["message" => "Expense type updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM expense_type WHERE expense_typeID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Expense type deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>