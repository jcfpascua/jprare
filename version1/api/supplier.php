<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        $stmt = $conn->prepare("SELECT * FROM supplier");
        $stmt->execute();
        echo json_encode($stmt->fetchAll());
        break;

    case "POST":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['supplier_name'], $data['contact'], $data['addressID'])) {
            $stmt = $conn->prepare("INSERT INTO supplier (supplier_name, contact, addressID) VALUES (?, ?, ?)");
            $stmt->execute([$data['supplier_name'], $data['contact'], $data['addressID']]);
            echo json_encode(["message" => "Supplier added"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "PUT":
        $data = json_decode(file_get_contents("php://input"), true);
        if (isset($data['supplierID'], $data['supplier_name'], $data['contact'], $data['addressID'])) {
            $stmt = $conn->prepare("UPDATE supplier SET supplier_name = ?, contact = ?, addressID = ? WHERE supplierID = ?");
            $stmt->execute([$data['supplier_name'], $data['contact'], $data['addressID'], $data['supplierID']]);
            echo json_encode(["message" => "Supplier updated"]);
        } else {
            echo json_encode(["error" => "Invalid input"]);
        }
        break;

    case "DELETE":
        if (isset($_GET['id'])) {
            $stmt = $conn->prepare("DELETE FROM supplier WHERE supplierID = ?");
            $stmt->execute([$_GET['id']]);
            echo json_encode(["message" => "Supplier deleted"]);
        } else {
            echo json_encode(["error" => "Invalid ID"]);
        }
        break;

    default:
        echo json_encode(["error" => "Invalid request method"]);
}
?>