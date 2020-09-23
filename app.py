'''
Title: Simple Periodic Table of Elements API
Author: Brent Pappas
Version: 1.0.0
'''

import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

debug = os.getenv("ENVIRONMENT") != "production"


# Element Class/Model
class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AtomicNumber = db.Column(db.Integer)
    Element = db.Column(db.String(20))
    Symbol = db.Column(db.String(4))
    AtomicMass = db.Column(db.Float)
    NumberofNeutrons = db.Column(db.Integer)
    NumberofProtons = db.Column(db.Integer)
    NumberofElectrons = db.Column(db.Integer)
    Period = db.Column(db.Integer)
    Group = db.Column(db.Integer)
    Phase = db.Column(db.String(10))
    Radioactive = db.Column(db.String(4))
    Natural = db.Column(db.String(4))
    Metal = db.Column(db.String(4))
    Nonmetal = db.Column(db.String(4))
    Metalloid = db.Column(db.String(4))
    Type = db.Column(db.String(25))
    AtomicRadius = db.Column(db.Float)
    Electronegativity = db.Column(db.Float)
    FirstIonization = db.Column(db.Float)
    Density = db.Column(db.Float)
    MeltingPoint = db.Column(db.Float)
    BoilingPoint = db.Column(db.Float)
    NumberOfIsotopes = db.Column(db.Integer)
    Discoverer = db.Column(db.String(300))
    Year = db.Column(db.Integer)
    SpecificHeat = db.Column(db.Float)
    NumberofShells = db.Column(db.Integer)
    NumberofValence = db.Column(db.Integer)

    def init(self):
        pass

    def __repr__(self):
        return f"{Symbol} - {Element}"


# Element Schema
class ElementSchema(ma.Schema):
    class Meta:
        fields = ("AtomicNumber", "Element", "Symbol", "AtomicMass", "NumberofNeutrons", "NumberofProtons", "NumberofElectrons", "Period", "Group", "Phase", "Radioactive", "Natural", "Metal", "Nonmetal", "Metalloid",
                  "Type", "AtomicRadius", "Electronegativity", "FirstIonization", "Density", "MeltingPoint", "BoilingPoint", "NumberOfIsotopes", "Discoverer", "Year", "SpecificHeat", "NumberofShells", "NumberofValence")


# Init schema
element_schema = ElementSchema()
elements_schema = ElementSchema(many=True)


# Get element by atomic number
@app.route("/element/atomic_number/<atomic_number>", methods=["GET"])
def get_element_by_atomic_number(atomic_number):
    element = Element.query.filter_by(AtomicNumber=atomic_number).first()
    if element is None:
        return {"Error": "Element not found"}, 404
    return element_schema.jsonify(element)


# Get element by symbol
@app.route("/element/symbol/<symbol>", methods=["GET"])
def get_element_by_symbol(symbol):
    element = db.session.query(Element).filter(func.lower(
        Element.Symbol) == func.lower(symbol)).first()
    if element is None:
        return {"Error": "Element not found"}, 404
    return element_schema.jsonify(element)


# Get element by name
@app.route("/element/name/<name>", methods=["GET"])
def get_element_by_name(name):
    element = db.session.query(Element).filter(func.lower(
        Element.Element) == func.lower(name)).first()
    if element is None:
        return {"Error": "Element not found"}, 404
    return element_schema.jsonify(element)


# Get all elements
@app.route("/elements", methods=["GET"])
def get_elements():
    all_elements = Element.query.all()
    result = elements_schema.dump(all_elements)
    return jsonify(result)


# Get elements by period
@app.route("/elements/period/<period>", methods=["GET"])
def get_elements_by_period(period):
    elements = Element.query.filter_by(Period=period).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by group
@app.route("/elements/group/<group>", methods=["GET"])
def get_elements_by_group(group):
    elements = Element.query.filter_by(Group=group).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by type
@app.route("/elements/type/<type>", methods=["GET"])
def get_elements_by_type(type):
    elements = db.session.query(Element).filter(func.lower(
        Element.Type) == func.lower(type)).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by natural
@app.route("/elements/natural/<natural>", methods=["GET"])
def get_elements_by_natural(natural):
    elements = db.session.query(Element).filter(func.lower(
        Element.Natural) == func.lower(natural)).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by metal
@app.route("/elements/metal/<metal>", methods=["GET"])
def get_elements_by_metal(metal):
    elements = db.session.query(Element).filter(func.lower(
        Element.Metal) == func.lower(metal)).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by metalloid
@app.route("/elements/metalloid/<metalloid>", methods=["GET"])
def get_elements_by_metalloid(metalloid):
    elements = db.session.query(Element).filter(func.lower(
        Element.Metalloid) == func.lower(metalloid)).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


# Get elements by nonmetal
@app.route("/elements/nonmetal/<nonmetal>", methods=["GET"])
def get_elements_by_nonmetal(nonmetal):
    elements = db.session.query(Element).filter(func.lower(
        Element.Nonmetal) == func.lower(nonmetal)).all()
    result = elements_schema.dump(elements)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=debug)
