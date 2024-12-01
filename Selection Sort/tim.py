<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crop Inventory System</title>
    <link rel="icon" href="../static/cropwise_logo.png" type="image/x-icon">
    <link rel="icon" href="../static/cropwise_logo.png" sizes="32x32">
    <link rel="stylesheet" href="../static/style.css">
</head>
<body>

    <nav>
        <div class="logo-container">
            <img src="../static/cropwise_logo.png" alt="Logo" class="logo">
            <h1>CropWise</h1>
        </div>
        <ul>
            <li class="account-dropdown">
                <a href="#account">My Account | admin</a>
                <div class="dropdown-content">
                    <a href="/profile">
                      <img src="../static/profile.png" alt="Profile Icon" class="dropdown-icon"> Profile
                    </a>

                    <a href="/">
                      <img src="../static/logout.png" alt="Profile Icon" class="dropdown-icon">
                      Logout</a>
                </div>
            </li>
        </ul>
    </nav>
    
    <div class="main-nav">
        <ul>
            <li><a href="/home">Home</a></li>
            <li><a href="/crop-inventory">Crop Inventory</a></li>
            <li><a href="/harvest_management">Harvest Management</a></li>
            <li><a href="/contact">Contact Us</a></li>
        </ul>
    </div>

    <div class="container">
        <button id="toggle-add-crop-form">+ New Crop</button>
        <button id="delete-all-button" onclick="deleteAllCrops()">Delete All Crops</button>

        <form id="add-crop-form" style="display:none;">
            <h2 id="form-title">Add Crop</h2>
            <input type="text" id="localName" placeholder="Local Name" required>
            <select id="category" required>
                <option value="" disabled selected>Select Category</option>
                <option value="Vegetables">Vegetables</option>
                <option value="Fruits">Fruits</option>
                <option value="Fibre Crop">Fibre Crop</option>
                <option value="Nut">Nut</option>
                <option value="Root and Tuber">Root and Tuber</option>
                <option value="Grain">Grain</option>
                <option value="Tobacco">Tobacco</option>
                <option value="Pulse">Pulse</option>
                <option value="Oil Crop">Oil Crop</option>
            </select>
            <select id="seasonality" required>
                <option value="" disabled selected>Select Seasonality</option>
                <option value="Wet">Wet</option>
                <option value="Dry">Dry</option>
                <option value="Wet and Dry">Wet and Dry</option>
            </select>
            <select id="flagDescription" required>
                <option value="" disabled selected>Select Flag Description</option>
                <option value="Organic">Organic</option>
                <option value="Non-GMO">Non-GMO</option>
                <option value="Hybrid">Hybrid</option>
                <option value="Heirloom">Heirloom</option>
            </select>
            <input type="date" id="harvestDate" required>
            <input type="number" id="quantity" placeholder="Quantity" required>
            <button type="button" id="add-crop-button" onclick="addCrop()">Add Crop</button>
            <button type="button" id="update-crop-button" onclick="updateCrop()" style="display:none;">Update Crop</button>
        </form>

        <div class="search-bar">
            <input type="text" id="search-input" placeholder="Search for crops..." onkeyup="search()">
        </div>

        <div id="crop-list-container">
            <div id="crop-table">
                <h2>Crop List</h2>
                <div id="sort-options" class="sort-by-dropdown">
                    <select id="sortBy" onchange="sortCrops()">
                        <option value="" disabled selected>Sort By</option>
                        <option value="itemCode">Item Code</option>
                        <option value="localName">Local Name</option>
                        <option value="category">Category</option>
                        <option value="seasonality">Seasonality</option>
                        <option value="flagDescription">Flag Description</option>
                        <option value="harvestDate">Harvest Date</option>
                        <option value="quantity">Quantity</option>
                    </select>
                
                    
                
                    <select id="cropLimit" onchange="sortCrops()">
                        <option value="" disabled selected>Number of Crops to Sort</option>
                        <option value="1000">1000</option>
                        <option value="5000">5000</option>
                        <option value="10000">10000</option>
                    </select>
                
                    <button id="toggle-metrics">Show Complexity Metrics</button>
                </div>
            
                <div id="complexity-metrics-modal" class="modal">
                    <div class="modal-content">
                        <button id="close-metrics-modal" class="close-button">&times;</button>
                        <h3>Complexity Measurements</h3>
                        <p><strong>Sorting Algorithm:</strong> <span id="algorithmDisplay">N/A</span></p>
                        <p><strong>Execution Time:</strong> <span id="execution-time">N/A</span></p>
                        <p><strong>Memory Usage:</strong> <span id="memory-used"> N/A </span></p>
                        <p><strong>Start Memory:</strong> <span id="start-memory">N/A</span></p>
                        <p><strong>End Memory:</strong> <span id="end-memory">N/A</span></p>
                    </div>
                </div>
            
                <table>
                    <thead>
                        <tr>
                            <th>Item Code</th>
                            <th>Local Name</th>
                            <th>Category</th>
                            <th>Seasonality</th>
                            <th>Flag Description</th>
                            <th>Harvest Date</th>
                            <th>Quantity(kg)</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="crop-list">
                        <!-- Crop entries will be populated here -->
                    </tbody>
                </table>
            </div>
        </div>
        
    <script>
        let crops = [];  // Keep track of crops data locally
        let editIndex = null;

        function fetchAlgorithm() {
            fetch('/algorithm')  // You can also use '/api/algorithm' if using JSON
                .then(response => response.text())  // Parse the response as text
                .then(data => {
                    document.getElementById('algorithmDisplay').innerText = data;
                })
                .catch(error => {
                    console.error('Error fetching algorithm:', error);
                });
        }
        window.onload = fetchAlgorithm;

        // Fetch and display crops when page loads or after adding a crop
        function fetchAndDisplayCrops() {
            fetch('/get_crops')
                .then(response => response.json())
                .then(data => {
                    crops = data;  // Update the crops array with the new data
                    displayCrops(crops);  // Display the crops in the table
                })
                .catch(error => console.error('Error fetching crops:', error));
        }

        // Add crop (this will now create a new crop)
        function addCrop() {
            const localName = document.getElementById('localName').value;
            const category = document.getElementById('category').value;
            const seasonality = document.getElementById('seasonality').value;
            const flagDescription = document.getElementById('flagDescription').value;
            const harvestDate = document.getElementById('harvestDate').value;
            const quantity = document.getElementById('quantity').value;

            const crop = {
                localName,
                category,
                seasonality,
                flagDescription,
                harvestDate,
                quantity
            };

            fetch('/add_crop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(crop)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchAndDisplayCrops();  // Refresh the crop list after adding
                    document.getElementById('add-crop-form').reset();
                    document.getElementById('add-crop-form').style.display = 'none';
                } else {
                    alert('Failed to add crop.');
                }
            })
            .catch(error => {
                console.error('Error adding crop:', error);
                alert('Error adding crop.');
            });
        }

                // Delete all crops function
                function deleteAllCrops() {
            // Confirm action with the user
            if (!confirm("Are you sure you want to delete all crops? This action cannot be undone.")) {
                return;
            }

            // Send a DELETE request to the backend
            fetch('/delete_all_crops', {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    crops = []; // Clear the local crops array
                    displayCrops(crops); // Refresh the display
                    alert('All crops have been deleted successfully.');
                } else {
                    alert('Failed to delete all crops.');
                }
            })
            .catch(error => console.error('Error deleting all crops:', error));
        }


        // Update existing crop
        function updateCrop() {
            const localName = document.getElementById('localName').value;
            const category = document.getElementById('category').value;
            const seasonality = document.getElementById('seasonality').value;
            const flagDescription = document.getElementById('flagDescription').value;
            const harvestDate = document.getElementById('harvestDate').value;
            const quantity = document.getElementById('quantity').value;

            const crop = {
                id: crops[editIndex].id,  // Include the crop ID for updating
                localName,
                category,
                seasonality,
                flagDescription,
                harvestDate,
                quantity
            };

            fetch('/update_crop', {
                method: 'PUT', // Use PUT method
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(crop)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchAndDisplayCrops();  // Refresh the crop list after updating
                    document.getElementById('add-crop-form').reset();  // Clear the form
                    document.getElementById('add-crop-form').style.display = 'none';  // Hide the form
                    document.getElementById('add-crop-button').style.display = 'block';  // Show Add Crop button
                    document.getElementById('update-crop-button').style.display = 'none';  // Hide Update button
                } else {
                    alert('Failed to update crop.');
                }
            })
            .catch(error => console.error('Error updating crop:', error));
        }

        // Edit crop function (sets the form for editing)
        function editCrop(index) {
            const crop = crops[index];
            document.getElementById('localName').value = crop.localName;
            document.getElementById('category').value = crop.category;
            document.getElementById('seasonality').value = crop.seasonality;
            document.getElementById('flagDescription').value = crop.flagDescription;
            document.getElementById('harvestDate').value = crop.harvestDate;
            document.getElementById('quantity').value = crop.quantity;

            editIndex = index;  // Set the index of the crop being edited
            document.getElementById('add-crop-button').style.display = 'none';
            document.getElementById('update-crop-button').style.display = 'block';
            document.getElementById('add-crop-form').style.display = 'block';
        }

        document.addEventListener("DOMContentLoaded", function () {
            const toggleMetricsButton = document.getElementById("toggle-metrics");
            const metricsModal = document.getElementById("complexity-metrics-modal");
            const closeButton = document.getElementById("close-metrics-modal");

            // Toggle modal visibility
            toggleMetricsButton.addEventListener("click", function () {
                const isHidden = metricsModal.style.display === "none" || metricsModal.style.display === "";
                metricsModal.style.display = isHidden ? "block" : "none";
                toggleMetricsButton.innerText = isHidden ? "Hide Complexity Metrics" : "Show Complexity Metrics";
            });

            // Close modal when clicking the close button
            closeButton.addEventListener("click", function () {
                metricsModal.style.display = "none";
                toggleMetricsButton.innerText = "Show Complexity Metrics";
            });

            // Close modal when clicking outside the modal content
            window.addEventListener("click", function (event) {
                if (event.target === metricsModal) {
                    metricsModal.style.display = "none";
                    toggleMetricsButton.innerText = "Show Complexity Metrics";
                }
            });
        });

                
        // Sort crops
        function sortCrops() {
            const sortBy = document.getElementById('sortBy').value;
            const cropLimit = document.getElementById("cropLimit").value;

            // Send request to the server to sort crops
            fetch('/sort_crops', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ sortBy, limit: parseInt(cropLimit) })
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.sortedCrops) {
                    crops = data.sortedCrops; // Update the local crops array with the sorted crops
                    displayCrops(crops); // Re-display crops in the sorted order
                    updateComplexityMetrics(data.metrics); // Call the function to display metrics
                } else {
                    console.error("Error fetching sorted crops:", data.error);
                }
            })
            .catch((error) => console.error("Error sorting crops:", error));
        }

        // Display crops in the table
        function displayCrops(crops) {
            const cropList = document.getElementById("crop-list");
            cropList.innerHTML = ""; // Clear existing list

            crops.forEach((crop, index) => {
                const cropRow = document.createElement("tr");
                cropRow.innerHTML = `
                    <td>${crop.itemCode}</td>
                    <td>${crop.localName}</td>
                    <td>${crop.category}</td>
                    <td>${crop.seasonality}</td>
                    <td>${crop.flagDescription}</td>
                    <td>${crop.harvestDate}</td>
                    <td>${crop.quantity}</td>
                    <td>
                        <button onclick="editCrop(${index})">Edit</button>
                        <button onclick="deleteCrop(${index})">Delete</button>
                    </td>
                `;
                cropList.appendChild(cropRow);
            });
        }

        // Function to update and display the complexity metrics
        function updateComplexityMetrics(metrics) {

            
            // Update execution time element
            document.getElementById("execution-time").innerText = metrics.executionTime
                ? metrics.executionTime + " nanoseconds" 
                : "N/A";

            // Update start memory element
            document.getElementById("start-memory").innerText = metrics.startMemory
                ? metrics.startMemory + " MB" 
                : "N/A";

            // Update end memory element
            document.getElementById("end-memory").innerText = metrics.endMemory
                ? metrics.endMemory + " MB" 
                : "N/A";

            // Update memory used element
            document.getElementById("memory-used").innerText = metrics.memoryUsed
                ? metrics.memoryUsed + " MiB" 
                : "N/A";

            // Optionally, update other metrics if you have them
            document.getElementById("other-metrics").innerText = metrics.otherMetrics
                ? metrics.otherMetrics
                : "N/A";
        }
        


        // Delete crop function
        function deleteCrop(index) {
            const crop = crops[index];

            // Make a DELETE request to the server to delete the crop
            fetch(`/delete_crop/${crop.itemCode}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    crops.splice(index, 1);  // Remove from local array
                    displayCrops(crops);      // Refresh the display
                } else {
                    alert('Failed to delete crop.');
                }
            })
            .catch(error => console.error('Error deleting crop:', error));
        }

        // Search function
        function search() {
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            const filteredCrops = crops.filter(crop => {
                return crop.localName.toLowerCase().includes(searchTerm) ||
                    crop.category.toLowerCase().includes(searchTerm) ||
                    crop.seasonality.toLowerCase().includes(searchTerm) ||
                    crop.itemCode.toString().includes(searchTerm) ||
                    crop.flagDescription.toLowerCase().includes(searchTerm) ||
                    crop.harvestDate.toLowerCase().includes(searchTerm) ||
                    crop.quantity.toString().includes(searchTerm);
            });
            displayCrops(filteredCrops);
        }

        // Initialize the page by fetching crops
        document.addEventListener("DOMContentLoaded", function() {
            fetchAndDisplayCrops();
            
            document.getElementById('toggle-add-crop-form').addEventListener('click', function() {
                const form = document.getElementById('add-crop-form');
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>
