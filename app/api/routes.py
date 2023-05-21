from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Pokemon, pokemon_schema, pokemons_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/test')
def hiddenpage():
    return {'fox': 'liquor'}

#Create
@api.route('/poketeam', methods = ['POST'])
@token_required
def catch(current_user_token):
    name = request.json['name']
    type = request.json['type']
    item = request.json['item']
    level = request.json['level']
    shiny = request.json['shiny']
    user_token = current_user_token.token

    print(f"Who's that Pokemon??? \n It's:  {current_user_token.token} \n")

    pocketMonster = Pokemon(name, type, item, level, user_token=user_token)
    db.session.add(pocketMonster)
    db.session.commit()

    response = pokemon_schema.dump(pocketMonster)
    return jsonify(response)

@api.route('/poketeam', methods = ['GET'])
@token_required
def view_team(current_user_token):
    a_user = current_user_token.token
    pokemonsters = Pokemon.query.filter_by(user_token = a_user).all()
    response = pokemons_schema.dump(pokemonsters)
    return jsonify(response)

@api.route('/poketeam/<id>', methods = ['POST', 'PUT'])
@token_required
def update_pokemon(current_user_token, id):
    pokemon = Pokemon.query.get(id)
    pokemon.name = request.json['name']
    pokemon.type = request.json['type']
    pokemon.item = request.json['item']
    pokemon.level = request.json['level']
    pokemon.user_token = current_user_token

    db.session.commit()
    response = pokemon_schema.dump(pokemon)
    return jsonify(response)