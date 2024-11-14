from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS
from shell import (
    shell_sort_local_name, 
    shell_sort_category,
    shell_sort_seasonality,
    shell_sort_item_code,
    shell_sort_year,
    shell_sort_flag_description,
    shell_sort_harvest_date,
    shell_sort_quantity,
    crop_inventory,
    CATEGORY_ORDER,  # Already in your shell.py
    SEASONALITY_ORDER,  # Already in your shell.py
    FLAG_DESCRIPTION_ORDER  # Already in your shell.py
)

app = Flask(__name__)

# Enable CORS to allow cross-origin requests
CORS(app)

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
        # Get the field to sort by from the JSON body
        sort_by = request.json.get('sortBy')
        
        if sort_by not in ['localName', 'category', 'seasonality', 'itemCode', 'year', 'flagDescription', 'harvestDate', 'quantity']:
            return jsonify({"error": "Invalid sort field"}), 400
        
        # Sort and return the sorted list
        sorted_crops = sorted(crop_inventory, key=lambda x: x.get(sort_by, ''))
        print("Sorted crops:", sorted_crops)  # Debugging line
        return jsonify(sorted_crops)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_crops', methods=['GET'])
def get_crops():
    return jsonify(crop_inventory)

@app.route('/add_crop', methods=['POST'])
def add_crop():
    data = request.get_json()
    new_crop = data
    crop_inventory.append(new_crop)
    
    return jsonify({"message": "Crop added successfully", "crop": new_crop})

@app.route('/dropdown-options', methods=['GET'])
def dropdown_options():
    # Return the dropdown options in JSON format
    return jsonify({
        "categories": CATEGORY_ORDER,  # Directly using the list from shell.py
        "seasonality": SEASONALITY_ORDER,  # Directly using the list from shell.py
        "flag_descriptions": FLAG_DESCRIPTION_ORDER  # Directly using the list from shell.py
    })

if __name__ == '__main__':
    app.run(debug=True)