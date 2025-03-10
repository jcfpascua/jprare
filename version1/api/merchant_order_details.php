<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM merchant_order_details");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchant_orderID'], $data['quantity'], $data['details'])) {
            $stmt = $conn->prepare("INSERT INTO merchant_order_details (merchant_orderID, quantity, details) VALUES (?, ?, ?)");
            $stmt->execute([$data['merchant_orderID'], $data['quantity'], $data['details']]);
            echo json_encode(["message" => "Merchant order detail added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['merchant_order_detailsID'], $data['merchant_orderID'], $data['quantity'], $data['details'])) {
            $stmt = $conn->prepare("UPDATE merchant_order_details SET merchant_orderID = ?, quantity = ?, details = ? WHERE merchant_order_detailsID = ?");
            $stmt->execute([$data['merchant_orderID'], $data['quantity'], $data['details'], $data['merchant_order_detailsID']]);
            echo json_encode(["message" => "Merchant order detail updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM merchant_order_details WHERE merchant_order_detailsID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Merchant order detail deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>