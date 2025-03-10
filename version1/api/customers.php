<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

// Handle the request method
$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        // Fetch all customers
        $stmt = $conn->prepare("SELECT * FROM customer");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        // Add a new customer
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customer_name'], $data['addressID'])) {
            $stmt = $conn->prepare("INSERT INTO customer (customer_name, addressID) VALUES (?, ?)");
            $stmt->execute([$data['customer_name'], $data['addressID']]);
            echo json_encode(["message" => "Customer added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        // Update a customer
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['customerID'], $data['customer_name'], $data['addressID'])) {
            $stmt = $conn->prepare("UPDATE customer SET customer_name = ?, addressID = ? WHERE customerID = ?");
            $stmt->execute([$data['customer_name'], $data['addressID'], $data['customerID']]);
            echo json_encode(["message" => "Customer updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        // Delete a customer
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM customer WHERE customerID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Customer deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>
