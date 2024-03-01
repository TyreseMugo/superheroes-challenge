from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Super, Ability, SuperAbility

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Welcome to the superpowers API</h1>'

# Get all supers
@app.route('/supers', methods=['GET'])
def get_supers():
    supers = Super.query.all()
    super_list = [{'id': super.id, 'name': super.name, 'super_name': super.super_name} for super in supers]
    return jsonify(super_list)

# Get a specific super by ID
@app.route('/supers/<int:super_id>', methods=['GET'])
def get_super(super_id):
    super = Super.query.get(super_id)
    if super:
        result = {
            "id": super.id,
            "name": super.name,
            "super_name": super.super_name,
            "abilities": [
                {"id": super_ability.ability.id, "name": super_ability.ability.name, "description": super_ability.ability.description}
                for super_ability in super.super_abilities
            ],
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Super not found"}), 404

# Get all abilities
@app.route('/abilities', methods=['GET'])
def get_abilities():
    abilities = Ability.query.all()
    ability_list = [{'id': ability.id, 'name': ability.name, 'description': ability.description} for ability in abilities]
    return jsonify(ability_list)

# Get a specific ability by ID
@app.route('/abilities/<int:ability_id>', methods=['GET'])
def get_ability(ability_id):
    ability = Ability.query.get(ability_id)
    if ability:
        ability_data = {'id': ability.id, 'name': ability.name, 'description': ability.description}
        return jsonify(ability_data)
    else:
        return make_response(jsonify({'error': 'Ability not found'}), 404)

# Update an ability by ID
@app.route('/abilities/<int:ability_id>', methods=['PATCH'])
def update_ability(ability_id):
    ability = Ability.query.get(ability_id)
    if ability:
        data = request.get_json()
        ability.description = data.get('description', ability.description)
        try:
            db.session.commit()
            return jsonify({'id': ability.id, 'name': ability.name, 'description': ability.description})
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 400)
    else:
        return make_response(jsonify({'error': 'Ability not found'}), 404)

# Create a new SuperAbility
@app.route('/super_abilities', methods=['POST'])
def create_super_ability():
    data = request.get_json()
    super_id = data.get('super_id')
    ability_id = data.get('ability_id')
    strength = data.get('strength')

    if super_id is None or ability_id is None or strength is None:
        return make_response(jsonify({'errors': ['Missing required data']}), 400)

    super = Super.query.get(super_id)
    ability = Ability.query.get(ability_id)

    if not super or not ability:
        return make_response(jsonify({'errors': ['Super or Ability not found']}), 404)

    new_super_ability = SuperAbility(super=super, ability=ability, strength=strength)

    try:
        db.session.add(new_super_ability)
        db.session.commit()
        return jsonify({'id': super.id, 'name': super.name, 'super_name': super.super_name, 'abilities': [{'id': ability.id, 'name': ability.name, 'description': ability.description}]})
    except Exception as e:
        return make_response(jsonify({'errors': [str(e)]}), 400)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
