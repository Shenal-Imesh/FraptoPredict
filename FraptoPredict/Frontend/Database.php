<?php


// Connect to the MySQL database
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "fraptopredict";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
} else {
    echo "ndsufhbusidnfsdijniajsndciajsdkanckaslncjsak"
}

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  } else {
    echo "Connected successfully to the database";
  }

mysqli_select_db($conn, $dbname);


// Insert the signup details into the users table
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["name"]) && isset($_POST["email"]) && isset($_POST["password"])) {
  $name = $_POST["name"];
  $email = $_POST["email"];
  $password = $_POST["password"];

  $sql = "INSERT INTO users (name, email, password) VALUES ('$name', '$email', '$password')";
  if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
    header("Refresh:2; url=HomePage.html");
    exit();
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
    header("Location: Webpage.html");
    exit();
  }
}

// Perform login validation
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["email"]) && isset($_POST["password"])) {
  $email = $_POST["email"];
  $password = $_POST["password"];

  $sql = "SELECT * FROM users WHERE email='$email' AND password='$password'";
  $result = $conn->query($sql);

  if ($result->num_rows > 0) {
    // User exists, login successful
    echo "Login successful";
    header("Location: HomePage.html");
    exit();
  } else {
    // User does not exist, login failed
    echo "Invalid email or password";
    header("Location: Webpage.html");
    exit();
  }
}

$conn->close();
?>
