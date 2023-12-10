#!/usr/bin/env python3

from flask import Flask, jsonify, abort
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_data = Bakery.query.all()

    serialized_bakeries = [bakery.to_dict() for bakery in bakeries_data]

    return jsonify(serialized_bakeries)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    with app.app_context():
        
        bakery = Bakery.query.session.get(Bakery, id)

        if bakery:
            
            serialized_bakery = bakery.to_dict()
        
            return jsonify(serialized_bakery), 200
        else:
            return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_data = BakedGood.query.order_by(BakedGood.price.desc()).all()

    serialized_baked_goods = [baked_good.to_dict() for baked_good in baked_goods_data]

    return jsonify(serialized_baked_goods)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if not most_expensive:
        abort(404)

    serialized_most_expensive = most_expensive.to_dict()

    response = jsonify(serialized_most_expensive)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
