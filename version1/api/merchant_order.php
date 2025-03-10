<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM merchant_order");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchantID'], $data['order_date'], $data['total_amount'])) {
            $stmt = $conn->prepare("INSERT INTO merchant_order (merchantID, order_date, total_amount) VALUES (?, ?, ?)");
            $stmt->execute([$data['merchantID'], $data['order_date'], $data['total_amount']]);
            echo json_encode(["message" => "Merchant order added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchant_orderID'], $data['merchantID'], $data['order_date'], $data['total_amount'])) {
            $stmt = $conn->prepare("UPDATE merchant_order SET merchantID = ?, order_date = ?, total_amount = ? WHERE merchant_orderID = ?");
            $stmt->execute([$data['merchantID'], $data['order_date'], $data['total_amount'], $data['merchant_orderID']]);
            echo json_encode(["message" => "Merchant order updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM merchant_order WHERE merchant_orderID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Merchant order deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>