from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Flask application setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crops.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS

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

# Routes
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

@app.route('/sort_crops', methods=['POST'])
def sort_crops():
    try:
        sort_by = request.json.get('sortBy')
        sort_order = request.json.get('sortOrder')
        is_descending = sort_order == 'descending'
        
        # Fetch all crops from the database
        crops = Crop.query.all()

        # Perform sorting
        sorted_crops = shell_sort(crops, sort_by, is_descending=is_descending)
        return jsonify(sorted_crops)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Wrapper functions for specific sorting needs
def shell_sort(query_result, key, custom_order=None, is_date=False, is_descending=False):
    arr = [crop.to_dict() for crop in query_result]
    n = len(arr)
    gap = n // 2

    def compare(val1, val2):
        if is_date:
            val1 = datetime.strptime(val1, "%Y-%m-%d") if val1 else None
            val2 = datetime.strptime(val2, "%Y-%m-%d") if val2 else None
        if custom_order:
            return custom_order.index(val1) - custom_order.index(val2)
        return (val1 > val2) - (val1 < val2)

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and compare(temp[key], arr[j - gap][key]) < 0:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr if not is_descending else arr[::-1]

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

if __name__ == '__main__':
    app.run(debug=True)
