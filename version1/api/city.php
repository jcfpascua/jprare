<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
header('Access-Control-Allow-Methods: POST, GET, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'config.php';

if (!$conn) {
    echo json_encode(["error" => "Database connection failed"]);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') { // Read
    $query = "SELECT * FROM city";
    $result = $conn->query($query);
    $cities = [];

    if ($result && $result->rowCount() > 0) {
        while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
            $cities[] = $row;
        }
    }

    echo json_encode($cities);
}

elseif ($method === 'POST') { // Create
    $data = json_decode(file_get_contents("php://input"), true);
    if (!isset($data['cityName'])) {
        echo json_encode(["error" => "Missing cityName"]);
        exit;
    }

    $stmt = $conn->prepare("INSERT INTO city (cityName) VALUES (:cityName)");
    $stmt->bindParam(':cityName', $data['cityName']);

    if ($stmt->execute()) {
        echo json_encode(["message" => "City added successfully"]);
    } else {
        echo json_encode(["error" => "Failed to add city"]);
    }
}

elseif ($method === 'PUT') { // Update
    $data = json_decode(file_get_contents("php://input"), true);
    if (!isset($data['cityID'], $data['cityName'])) {
        echo json_encode(["error" => "Missing cityID or cityName"]);
        exit;
    }

    $stmt = $conn->prepare("UPDATE city SET cityName = :cityName WHERE cityID = :cityID");
    $stmt->bindParam(':cityName', $data['cityName']);
    $stmt->bindParam(':cityID', $data['cityID']);

    if ($stmt->execute()) {
        echo json_encode(["message" => "City updated successfully"]);
    } else {
        echo json_encode(["error" => "Failed to update city"]);
    }
}

elseif ($method === 'DELETE') { // Delete
    if (!isset($_GET['id'])) {
        echo json_encode(["error" => "Missing city ID"]);
        exit;
    }

    $stmt = $conn->prepare("DELETE FROM city WHERE cityID = :cityID");
    $stmt->bindParam(':cityID', $_GET['id']);

    if ($stmt->execute()) {
        echo json_encode(["message" => "City deleted successfully"]);
    } else {
        echo json_encode(["error" => "Failed to delete city"]);
    }
}

$conn = null;
?>
