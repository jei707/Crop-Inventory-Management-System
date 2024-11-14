from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS

# Shell Sort with enhanced comparisons
def shell_sort(arr, key, custom_order=None, is_date=False, is_descending=False):
    n = len(arr)
    gap = n // 2

    # Inner helper function for comparing values
    def compare(val1, val2):
        # Date comparison
        if is_date:
            try:
                val1 = datetime.strptime(val1, "%Y-%m-%d") if val1 else None
                val2 = datetime.strptime(val2, "%Y-%m-%d") if val2 else None
            except ValueError:
                val1, val2 = None, None  # Handle invalid dates as None
        # Custom order comparison
        elif custom_order:
            if val1 not in custom_order:
                val1 = float('inf')  # If it's not in the custom order, treat it as infinity
            if val2 not in custom_order:
                val2 = float('inf')
            val1 = custom_order.index(val1) if val1 is not None else float('inf')
            val2 = custom_order.index(val2) if val2 is not None else float('inf')
        # Integer comparison
        elif isinstance(val1, int) and isinstance(val2, int):
            pass  # Integers are compared naturally
        else:
            # Fallback for string comparison (e.g., Local Name)
            val1, val2 = str(val1), str(val2)

        # Compare based on descending order
        if val1 is None:  # Handle None values first
            return False if is_descending else True
        elif val2 is None:
            return True if is_descending else False

        return (val1 < val2) if not is_descending else (val1 > val2)

    # Sorting logic with Shell Sort
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and compare(arr[j - gap][key], temp[key]):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr

# Crop Categories, Seasonality, and Flag Descriptions
CATEGORY_ORDER = ["Vegetable", "Fruit", "Herb", "Grain"]
SEASONALITY_ORDER = ["Year-round", "Winter", "Summer", "Fall", "Spring"]
FLAG_DESCRIPTION_ORDER = ["Organic", "Non-Organic", "Imported", "Local"]

crop_inventory = []  # Initialize the crop inventory

# Wrapper functions for specific sorting needs
def shell_sort_local_name(arr, is_descending):
    return shell_sort(arr, "localName", is_descending=is_descending)

def shell_sort_category(arr, is_descending):
    return shell_sort(arr, "category", custom_order=CATEGORY_ORDER, is_descending=is_descending)

def shell_sort_seasonality(arr, is_descending):
    return shell_sort(arr, "seasonality", custom_order=SEASONALITY_ORDER, is_descending=is_descending)

def shell_sort_item_code(arr, is_descending):
    return shell_sort(arr, "itemCode", is_descending=is_descending)

def shell_sort_flag_description(arr, is_descending):
    return shell_sort(arr, "flagDescription", custom_order=FLAG_DESCRIPTION_ORDER, is_descending=is_descending)

def shell_sort_harvest_date(arr, is_descending):
    return shell_sort(arr, "harvestDate", is_date=True, is_descending=is_descending)

def shell_sort_quantity(arr, is_descending):
    return shell_sort(arr, "quantity", is_descending=is_descending)

# Flask application setup
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/loggedout')
def loggedout():
    return render_template('loggedout.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginsuccessful')
def loginsuccessful():
    return render_template('loginsuccessful.html')

@app.route('/sort_crops', methods=['POST'])
def sort_crops():
    try:
        # Get the field to sort by and the order (ascending/descending) from the request
        sort_by = request.json.get('sortBy')
        sort_order = request.json.get('sortOrder')  # Ascending or descending

        # Ensure that the sort_by field is valid
        if sort_by not in ['localName', 'category', 'seasonality', 'itemCode', 'year', 'flagDescription', 'harvestDate', 'quantity']:
            return jsonify({"error": "Invalid sort field"}), 400
        
        # Determine the sort order
        is_descending = sort_order == 'descending'

        # Use Shell Sort based on the 'sortBy' field
        if sort_by == 'localName':
            sorted_crops = shell_sort_local_name(crop_inventory, is_descending)
        elif sort_by == 'category':
            sorted_crops = shell_sort_category(crop_inventory, is_descending)
        elif sort_by == 'seasonality':
            sorted_crops = shell_sort_seasonality(crop_inventory, is_descending)
        elif sort_by == 'itemCode':
            sorted_crops = shell_sort_item_code(crop_inventory, is_descending)
        elif sort_by == 'year':
            sorted_crops = shell_sort_year(crop_inventory, is_descending)
        elif sort_by == 'flagDescription':
            sorted_crops = shell_sort_flag_description(crop_inventory, is_descending)
        elif sort_by == 'harvestDate':
            sorted_crops = shell_sort_harvest_date(crop_inventory, is_descending)
        elif sort_by == 'quantity':
            sorted_crops = shell_sort_quantity(crop_inventory, is_descending)

        # Return the sorted list of crops
        return jsonify(sorted_crops)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_crops', methods=['GET'])
def get_crops():
    return jsonify(crop_inventory)

@app.route('/add_crop', methods=['POST'])
def add_crop():
    try:
        # Get the data sent in the request
        crop_data = request.json

        # Automatically generate itemCode if it doesn't exist
        if 'itemCode' not in crop_data:
            crop_data['itemCode'] = generate_item_code(crop_data)

        # Validate input data (e.g., ensure all required fields are present)
        required_fields = ['localName', 'category', 'seasonality', 'flagDescription', 'harvestDate', 'quantity']
        for field in required_fields:
            if field not in crop_data:
                return jsonify({"error": f"{field} is missing"}), 400
        
        # Add the crop to the crop_inventory
        crop_inventory.append(crop_data)
        
        # Return success response
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dropdown-options', methods=['GET'])
def dropdown_options():
    # Return the dropdown options in JSON format
    return jsonify({
        "category": CATEGORY_ORDER,
        "seasonality": SEASONALITY_ORDER,
        "flagDescription": FLAG_DESCRIPTION_ORDER
    })

def generate_item_code(crop_data):
    # Example function to generate item code: this can be adjusted based on your logic
    return str(len(crop_inventory) + 1)  # Generate item code based on the current inventory size

if __name__ == '__main__':
    app.run(debug=True)
