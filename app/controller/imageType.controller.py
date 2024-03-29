from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from app.config.connection_configuration import engine, quality_table

imageType_controller = Blueprint('quality', __name__)

@imageType_controller.route('/quality', methods=['GET'])
def imageType_controller():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(quality_table).all()
    session.close()
    return jsonify(result)