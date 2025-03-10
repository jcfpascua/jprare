<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM expense");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['expense_date'], $data['total'], $data['merchantID'], $data['qty'], $data['title'])) {
            $stmt = $conn->prepare("INSERT INTO expense (expense_date, total, merchantID, qty, title) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$data['expense_date'], $data['total'], $data['merchantID'], $data['qty'], $data['title']]);
            echo json_encode(["message" => "Expense added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['expenseID'], $data['expense_date'], $data['total'], $data['merchantID'], $data['qty'], $data['title'])) {
            $stmt = $conn->prepare("UPDATE expense SET expense_date = ?, total = ?, merchantID = ?, qty = ?, title = ? WHERE expenseID = ?");
            $stmt->execute([$data['expense_date'], $data['total'], $data['merchantID'], $data['qty'], $data['title'], $data['expenseID']]);
            echo json_encode(["message" => "Expense updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM expense WHERE expenseID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Expense deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>