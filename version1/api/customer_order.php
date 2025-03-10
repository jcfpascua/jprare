<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM customer_order");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customerID'], $data['order_date'], $data['merchantID'])) {
            $stmt = $conn->prepare("INSERT INTO customer_order (customerID, order_date, merchantID) VALUES (?, ?, ?)");
            $stmt->execute([$data['customerID'], $data['order_date'], $data['merchantID']]);
            echo json_encode(["message" => "Customer order added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customer_orderID'], $data['customerID'], $data['order_date'], $data['merchantID'])) {
            $stmt = $conn->prepare("UPDATE customer_order SET customerID = ?, order_date = ?, merchantID = ? WHERE customer_orderID = ?");
            $stmt->execute([$data['customerID'], $data['order_date'], $data['merchantID'], $data['customer_orderID']]);
            echo json_encode(["message" => "Customer order updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM customer_order WHERE customer_orderID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Customer order deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>