import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
import base64
from faker import Faker
from faker_food import FoodProvider
import time
import tracemalloc
from datetime import datetime
import psutil
from time import time_ns  # Use time_ns for nanosecond precision


# Flask application setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crops.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS
fake = Faker()
fake.add_provider(FoodProvider)

# Crop model
class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    seasonality = db.Column(db.String(50), nullable=False)
    flag_description = db.Column(db.String(50), nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_code = db.Column(db.String(10), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "localName": self.local_name,
            "category": self.category,
            "seasonality": self.seasonality,
            "flagDescription": self.flag_description,
            "harvestDate": self.harvest_date.strftime('%Y-%m-%d'),
            "quantity": self.quantity,
            "itemCode": self.item_code
        }

# Initialize the database
with app.app_context():
    db.create_all()

# Function to generate a unique item code
def generate_item_code():
    crop_count = Crop.query.count()
    return str(crop_count + 1).zfill(5)  # Ensure it's a 5-digit number (e.g., 00001, 00002)

algorithm = "Pigeonhole Sort"

# Route to return the algorithm as a plain text response
@app.route('/algorithm')
def get_algorithm():
    return algorithm  # You can return the algorithm directly as a string

# Route to return the algorithm as a JSON response (optional, in case you need it)
@app.route('/api/algorithm')
def get_algorithm_json():
    return jsonify({'algorithm': algorithm})

# Routes
@app.route('/delete_all_crops', methods=['DELETE'])
def delete_all_crops():
    try:
        # Delete all crop records from the database
        Crop.query.delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'All crops have been deleted.'}), 200
    except Exception as e:
        # Handle and log any exceptions
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/get_crops', methods=['GET'])
def get_crops():
    crops = Crop.query.all()
    return jsonify([crop.to_dict() for crop in crops])

@app.route('/add_crop', methods=['POST'])
def add_crop():
    try:
        crop_data = request.json
        # Check if it's an update or new crop
        if 'id' in crop_data:  # Update existing crop
            crop = Crop.query.get(crop_data['id'])
            if not crop:
                return jsonify({"error": "Crop not found"}), 404
        else:  # Adding new crop
            crop = Crop(
                local_name=crop_data['localName'],
                category=crop_data['category'],
                seasonality=crop_data['seasonality'],
                flag_description=crop_data['flagDescription'],
                harvest_date=datetime.strptime(crop_data['harvestDate'], "%Y-%m-%d"),
                quantity=crop_data['quantity'],
                item_code=generate_item_code()  # Generate unique item code for new crop
            )
            db.session.add(crop)

        # Update the crop data (either new or edited)
        crop.local_name = crop_data['localName']
        crop.category = crop_data['category']
        crop.seasonality = crop_data['seasonality']
        crop.flag_description = crop_data['flagDescription']
        crop.harvest_date = datetime.strptime(crop_data['harvestDate'], "%Y-%m-%d")
        crop.quantity = crop_data['quantity']

        db.session.commit()

        return jsonify({"success": True, "itemCode": crop.item_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    #Function to seed the database with random crops
def seed_database():
    if not Crop.query.first():  # Only seed if the database is empty
        
        for _ in range(10000):
            crop = Crop(
                local_name=fake.random_element(elements=[
                        "Tomato", "Potato", "Rice", "Wheat", "Carrot", "Spinach", "Lettuce", "Onion", "Garlic", 
                        "Corn", "Cucumber", "Cabbage", "Peas", "Soybean", "Oats", "Barley", "Millet", "Tobacco", 
                        "Coffee", "Cocoa", "Cotton", "Banana", "Apple", "Mango", "Papaya", "Guava", "Pineapple", 
                        "Sugarcane", "Tea", "Chili", "Bell Pepper", "Broccoli", "Cauliflower", "Zucchini", 
                        "Pumpkin", "Sweet Potato", "Mustard", "Sunflower", "Groundnut (Peanut)", "Lentils", 
                        "Chickpeas", "Beans", "Sesame", "Quinoa", "Sorghum", "Durum Wheat", "Flaxseed", "Coconut", 
                        "Almond", "Cashew", "Pomegranate", "Strawberry", "Raspberry", "Blueberry", "Blackberry", 
                        "Avocado", "Pear", "Orange", "Lemon", "Lime", "Grapefruit", "Durian", "Lychee", "Date", 
                        "Fig", "Apricot", "Cherry", "Plum", "Peach", "Nectarine", "Kale", "Turnip", "Radish", 
                        "Beetroot", "Artichoke", "Asparagus", "Okra", "Eggplant", "Cilantro", "Parsley", "Thyme", 
                        "Basil", "Rosemary", "Mint", "Taro", "Yam", "Cranberry", "Gooseberry", "Starfruit", 
                        "Jackfruit", "Watermelon", "Honeydew", "Cantaloupe", "Persimmon", "Dragon Fruit", 
                        "Kiwifruit", "Passion Fruit", "Sugar Beet", "Horseradish", "Leek", "Scallion", "Arugula", 
                        "Fennel", "Dill", "Chive", "Endive"
                ]),
                category=fake.random_element(elements=[
                    "Vegetables", "Fruits", "Fibre Crop", "Nut", 
                    "Root and Tuber", "Grain", "Tobacco", "Pulse", "Oil Crop"
                ]),
                seasonality=fake.random_element(elements=["Wet", "Dry", "Wet and Dry"]),
                flag_description=fake.random_element(elements=["Organic", "Non-GMO", "Hybrid", "Heirloom"]),
                harvest_date=fake.date_between(start_date='-1y', end_date='today'),
                quantity=fake.random_int(min=10, max=500),
                item_code=generate_item_code()  # Generate the item code
            )
            db.session.add(crop)
        
        db.session.commit()
        print("Database seeded with 10000 entries.")

@app.before_request
def populate_database():
    seed_database()


@app.route('/delete_crop/<item_code>', methods=['DELETE'])
def delete_crop(item_code):
    try:
        # Fetch crop using itemCode
        crop = Crop.query.filter_by(item_code=item_code).first()
        if crop:
            db.session.delete(crop)
            db.session.commit()
            return jsonify({"success": True, "message": "Crop deleted successfully"}), 200
        else:
            return jsonify({"error": "Crop not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_crop', methods=['PUT'])
def update_crop():
    try:
        crop_data = request.json
        crop = Crop.query.get(crop_data['id'])
        if not crop:
            return jsonify({"error": "Crop not found"}), 404
        
        crop.local_name = crop_data['localName']
        crop.category = crop_data['category']
        crop.seasonality = crop_data['seasonality']
        crop.flag_description = crop_data['flagDescription']
        crop.harvest_date = datetime.strptime(crop_data['harvestDate'], "%Y-%m-%d")
        crop.quantity = crop_data['quantity']
        
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_memory_usage():
    process = psutil.Process(os.getpid())  # Get the current process
    memory_in_mib = process.memory_info().rss / 2**20  # Memory in MiB
    return memory_in_mib

@app.route('/sort_crops', methods=['POST'])
def sort_crops():
    try:
        # Parse request data
        sort_by = request.json.get('sortBy', 'local_name')  # Default to 'local_name' if not provided
        sort_order = request.json.get('sortOrder', 'ascending')  # Default to 'ascending' if not provided
        limit = request.json.get('limit', 10000)  # Default to 1000 if no limit is provided
        is_descending = sort_order == 'descending'

        # Fetch crops from the database with the specified limit
        crops_query = Crop.query.limit(limit).all()

        # Perform sorting with time and space measurement
        sorted_result, metrics = pigeonhole_sort_with_metrics(crops_query, sort_by, is_descending=is_descending)

        # Log metrics to the server console for debugging
        print(f"Sorting by: {sort_by}, Order: {sort_order}, Limit: {limit}")
        print(f"Metrics: Execution Time = {metrics['executionTime']} nanoseconds, "
              f"Start Memory = {metrics['startMemory']} MB, "
              f"End Memory = {metrics['endMemory']} MB, "
              f"Memory Used = {metrics['memoryUsed']} MB")

        # Format the response
        response = {
            "sortedCrops": sorted_result,
            "metrics": metrics
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle and log errors
        print(f"Error during sorting: {e}")
        return jsonify({"error": str(e)}), 500


def pigeonhole_sort_with_metrics(query_result, key, is_descending=False):
    arr = [crop.to_dict() for crop in query_result]  # Convert crops to dictionaries

    # First, attempt to check if the values are numeric or strings
    try:
        values = [crop[key] for crop in arr if key in crop]
    except KeyError:
        raise KeyError(f"The field '{key}' must exist in all crops.")

    # If all values are numeric, apply pigeonhole sort for numbers
    if all(isinstance(val, (int, float)) for val in values):
        return pigeonhole_sort_numeric(arr, key, is_descending)

    # Otherwise, apply pigeonhole sort for strings
    return pigeonhole_sort_string(arr, key, is_descending)

def pigeonhole_sort_numeric(arr, key, is_descending=False):
    # Apply pigeonhole sort logic for numeric values
    values = [crop[key] for crop in arr]
    min_val = min(values)
    max_val = max(values)
    range_size = max_val - min_val + 1

    if range_size > 10**6:  # Arbitrary large limit for safety
        raise ValueError(f"Range size for Pigeonhole Sort ({range_size}) is too large. Consider using a different algorithm.")

    start_time_ns = time_ns()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 2**20  # Memory in MB

    # Create pigeonholes
    holes = [[] for _ in range(range_size)]
    for crop in arr:
        index = crop[key] - min_val
        holes[index].append(crop)

    # Flatten the pigeonholes into a sorted array
    sorted_arr = [crop for hole in holes for crop in hole]

    if is_descending:
        sorted_arr.reverse()

    end_time_ns = time_ns()
    end_memory = process.memory_info().rss / 2**20  # Memory in MiB

    metrics = {
        "executionTime": end_time_ns - start_time_ns,
        "startMemory": round(start_memory, 2),
        "endMemory": round(end_memory, 2),
        "memoryUsed": round(end_memory - start_memory, 2)
    }

    return sorted_arr, metrics

def pigeonhole_sort_string(arr, key, is_descending=False):
    # Apply pigeonhole sort logic for strings
    values = [crop[key] for crop in arr]
    min_val = min(values)
    max_val = max(values)

    start_time_ns = time_ns()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 2**20  # Memory in MB

    # Create pigeonholes (number of possible distinct characters in the string values)
    holes = {val: [] for val in set(values)}
    for crop in arr:
        holes[crop[key]].append(crop)

    # Flatten the pigeonholes into a sorted array
    sorted_arr = [crop for key in sorted(holes.keys()) for crop in holes[key]]

    if is_descending:
        sorted_arr.reverse()

    end_time_ns = time_ns()
    end_memory = process.memory_info().rss / 2**20  # Memory in MiB

    metrics = {
        "executionTime": end_time_ns - start_time_ns,
        "startMemory": round(start_memory, 2),
        "endMemory": round(end_memory, 2),
        "memoryUsed": round(end_memory - start_memory, 2)
    }

    return sorted_arr, metrics


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

@app.route('/crop-inventory')
def loginsuccessful():
    return render_template('loginsuccessful.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/harvest_management')
def pharvest_management():
    return render_template('harvest_management.html')

@app.route('/overview', methods=['GET'])
def overview():
    try:
        # Get total number of crops
        total_crops = Crop.query.count()

        # Get total quantity of all crops
        total_quantity = db.session.query(func.sum(Crop.quantity)).scalar() or 0

        # Get harvest timelines (group by harvest month)
        harvest_timeline = db.session.query(
            func.strftime('%Y-%m', Crop.harvest_date),
            func.count(Crop.id),
            func.sum(Crop.quantity)
        ).group_by(func.strftime('%Y-%m', Crop.harvest_date)).all()

        # Process data for display
        harvest_data = [
            {
                "month": datetime.strptime(month, '%Y-%m').strftime('%B %Y'),
                "crop_count": crop_count,
                "total_quantity": total_quantity
            }
            for month, crop_count, total_quantity in harvest_timeline
        ]

        # Return a JSON response with the overview data
        return jsonify({
            "totalCrops": total_crops,
            "totalQuantity": total_quantity,
            "harvestTimeline": harvest_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
    
