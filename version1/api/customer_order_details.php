<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM customer_order_details");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customer_orderID'], $data['item_id'], $data['quantity'], $data['total'])) {
            $stmt = $conn->prepare("INSERT INTO customer_order_details (customer_orderID, item_id, quantity, total) VALUES (?, ?, ?, ?)");
            $stmt->execute([$data['customer_orderID'], $data['item_id'], $data['quantity'], $data['total']]);
            echo json_encode(["message" => "Customer order detail added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customer_order_detailsID'], $data['customer_orderID'], $data['item_id'], $data['quantity'], $data['total'])) {
            $stmt = $conn->prepare("UPDATE customer_order_details SET customer_orderID = ?, item_id = ?, quantity = ?, total = ? WHERE customer_order_detailsID = ?");
            $stmt->execute([$data['customer_orderID'], $data['item_id'], $data['quantity'], $data['total'], $data['customer_order_detailsID']]);
            echo json_encode(["message" => "Customer order detail updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM customer_order_details WHERE customer_order_detailsID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Customer order detail deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>