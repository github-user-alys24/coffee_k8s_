<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataViewer</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #db9335;
            color: white;
            padding: 10px 0;
        }
        header h1 {
            margin: 0;
            text-align: center;
        }
        nav ul {
            list-style: none;
            padding: 0;
            text-align: center;
        }
        nav ul li {
            display: inline;
            margin: 0 10px;
        }
        nav ul li button {
            background: none;
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        main {
            padding: 20px;
            text-align: center;
        }
        .page {
            display: none;
        }
        .active {
            display: block;
        }
		footer {
            background-color: #db9335;
			color: white;
            text-align: center; 
			width: 100%;
			position: fixed;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
        }
    </style>
</head>
<body>
    <header>
        <h1>Coffee</h1>
        <nav>
            <ul>
                <li><button onclick="showPage('home')">Home</button></li>
				<li><button onclick="showPage('inspect')">dataUnderstanding</button></li>
                <li><button onclick="showPage('preprocessing')">preProcessing</button></li>
                <li><button onclick="showPage('training')">modelTraining</button></li>
				<li><button onclick="showPage('inference')">inference</button></li>
				<li><button onclick="showPage('prediction')">prediction</button></li>
            </ul>
        </nav>
    </header>
    <main>
        <div id="home" class="page active">
            <h2>Welcome!</h2>
            <p>Coffee Shop Data</p>
			<p>This is the home page of the website.</p>
        </div>
       <div id="inspect" class="page">
            <h2>dataUnderstanding</h2>
            <p>Top 25 rows of raw data</p>
			<button onclick="openDataInNewTab()">View Data</button>
			<p>Revenue by Product Categories</p>
			<button onclick="open1DataInNewTab()">View Products Data</button>
			<p>Graphs on total revenue by store location and product_type</p>
			<button onclick="open1GraphInNewTab()">View Graphs</button>
        </div>
        <div id="preprocessing" class="page">
            <h2>preProcessing</h2>
            <p>Data from Preprocessing Service</p>
			<p>View X and y data</p>
			<button onclick="viewShape()">View Shape</button>
			<p>View Graphical Data in a new Tab</p>
            <button onclick="openGraphInNewTab()">View Graph</button>
			<p> </p>
			<h3>preProcessed data</h3>
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Hour</th>
                        <th>Revenue</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Fetch the JSON data from the preprocessing service
                    $json_url = 'http://localhost:8080/';
                    $json = @file_get_contents($json_url);

                    // Check if the file_get_contents was successful
                    if ($json === FALSE) {
                        echo "<tr><td colspan='3'>Error fetching data from $json_url</td></tr>";
                    } else {
                        // Decode the JSON data
                        $data = json_decode($json, true); // Decode as an associative array

                        // Check if json_decode was successful
                        if (json_last_error() !== JSON_ERROR_NONE) {
                            echo "<tr><td colspan='3'>Error decoding JSON</td></tr>";
                        } else {
                            // Check if data is an array
                            if (is_array($data)) {
                                // Loop through the data and display it in table rows
                                foreach ($data as $record) {
                                    $month = htmlspecialchars($record['Month']);
                                    $hour = htmlspecialchars($record['Hour']);
                                    $revenue = htmlspecialchars($record['Revenue']);
                                    echo "<tr><td>$month</td><td>$hour</td><td>$revenue</td></tr>";
                                }
                            } else {
                                echo "<tr><td colspan='3'>No data available</td></tr>";
                            }
                        }
                    }
                    ?>
                </tbody>
			</table>
		</div>
		<div id="training" class="page">
            <h2>modelTraining</h2>
			<p>Check if models were saved successfully</p>
			<button onclick="window.open('http://localhost:8082/gbt')">gbt_model.pkl</button>
			<h3>Gradient Boosted Trees</h3>
			<table>
                <thead>
                    <tr> 
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Fetch the JSON data from the preprocessing service
                    $json_url = 'http://localhost:8082/';
                    $json = @file_get_contents($json_url);

                    // Check if the file_get_contents was successful
                    if ($json === FALSE) {
                        echo "<tr><td colspan='3'>Error fetching data from $json_url</td></tr>";
                    } else {
                        // Decode the JSON data
                        $data = json_decode($json, true); // Decode as an associative array

                        // Check if json_decode was successful
                        if (json_last_error() !== JSON_ERROR_NONE) {
                            echo "<tr><td colspan='3'>Error decoding JSON</td></tr>";
                        } else {
                            // Check if data is an array
                            if (is_array($data)) {
                                // Loop through the data and display it in table rows
                                foreach ($data as $record) {
                                    $metric = htmlspecialchars($record['Metric']);
                                    $value = htmlspecialchars($record['Value']);
                                    echo "<tr><td>$metric</td><td>$value</td></tr>";
                                }
                            } else {
                                echo "<tr><td colspan='3'>No data available</td></tr>";
                            }
                        }
                    }
                    ?>
                </tbody>
			</table>
			<p> </p>
			<p>Feature Importances for GBT</p>
			<button onclick="featureImpt1()">View Feature Importances for GBT</button>
        </div>
        <div id="prediction" class="page">
            <h2>prediction</h2>
            <p>View performance of the models, prints first 25 rows</p>
			<h3>Gradient Boosted Trees</h3>
			<table>
                <thead>
                    <tr> 
                        <th>Actual</th>
                        <th>Predicted</th>
						<th>Difference %</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Fetch the JSON data from the preprocessing service
                    $json_url = 'http://localhost:8083/';
                    $json = @file_get_contents($json_url);

                    // Check if the file_get_contents was successful
                    if ($json === FALSE) {
                        echo "<tr><td colspan='3'>Error fetching data from $json_url</td></tr>";
                    } else {
                        // Decode the JSON data
                        $data = json_decode($json, true); // Decode as an associative array

                        // Check if json_decode was successful
                        if (json_last_error() !== JSON_ERROR_NONE) {
                            echo "<tr><td colspan='3'>Error decoding JSON</td></tr>";
                        } else {
                            // Check if data is an array
                            if (is_array($data)) {
                                // Loop through the data and display it in table rows
                                foreach ($data as $record) {
                                    $actual = htmlspecialchars($record['Actual']);
                                    $predicted = htmlspecialchars($record['Predicted']);
									$difference = htmlspecialchars($record['Difference %']);
                                    echo "<tr><td>$actual</td><td>$predicted</td><td>$difference</td></tr>";
                                }
                            } else {
                                echo "<tr><td colspan='3'>No data available</td></tr>";
                            }
                        }
                    }
                    ?>
                </tbody>
			</table>
        </div>
		<div id="inference" class="page">
            <h2>inference</h2>
			<p>Insert Month to get Predicted Potential Overall Revenue</p>
			<p>Predicts from June 2023 onwards (Month 6)</p>
			<h2>Enter Month</h2>
			<form action="http://localhost:8084/predict" method="post">
                <input type="number" id="month" name="month" min="1" max="100" required>
                <input type="submit" value="Submit">
            </form>
		</div>
    </main>
		<footer>
			<p>&copy; 2024 cutie patooties</p>
		</footer>
	<script>
		function showPage(pageId) {
			// Hide all pages
			const pages = document.querySelectorAll('.page');
			pages.forEach(page => page.classList.remove('active'));

			// Show the selected page
			const activePage = document.getElementById(pageId);
			activePage.classList.add('active');
		}

		function openGraphInNewTab() {
			window.open('http://localhost:8080/graph');
		}
		
		function openDataInNewTab() {
			window.open('http://localhost:8080/top25rows');
		}

		function open1DataInNewTab() {
			window.open('http://localhost:8080/products');
		}

		function open1GraphInNewTab() {
			window.open('http://localhost:8080/1graph');
		}

		function viewShape() {
			window.open('http://localhost:8082/shape');
		}

		function featureImpt() {
			window.open('http://localhost:8082/importances_rf');
		}

		function featureImpt1() {
			window.open('http://localhost:8082/importances_gbt');
		}
	</script>	
	</body>
</html>