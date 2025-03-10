<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM expense_details");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['expenseID'], $data['expense_typeID'], $data['amount'])) {
            $stmt = $conn->prepare("INSERT INTO expense_details (expenseID, expense_typeID, amount) VALUES (?, ?, ?)");
            $stmt->execute([$data['expenseID'], $data['expense_typeID'], $data['amount']]);
            echo json_encode(["message" => "Expense detail added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['expenseID'], $data['expense_typeID'], $data['amount'])) {
            $stmt = $conn->prepare("UPDATE expense_details SET expense_typeID = ?, amount = ? WHERE expenseID = ?");
            $stmt->execute([$data['expense_typeID'], $data['amount'], $data['expenseID']]);
            echo json_encode(["message" => "Expense detail updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM expense_details WHERE expenseID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Expense detail deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>