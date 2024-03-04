from app.extensions import db
from app.extensions import call_stored_procedure_get, call_stored_procedure_post
from flask import Blueprint, request, jsonify, Response
from itsdangerous import URLSafeTimedSerializer
from app.models.genre_model import Genre
from app.models.movie_model import Movie
from app.models.quality_model import Quality
from app.models.subtitle_model import Subtitle
from app.services.auth_guard import auth_guard
import io
import csv
from dateutil.parser import parse

movie_routes = Blueprint('movies', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}


@movie_routes.route('/classifications', methods=['GET', 'POST'])
@movie_routes.route('/classifications/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_classifications(id=None):
    if request.method == 'GET':
        if id:
            classification_data = {'id': id, 'description': 'Example Classification'}
        else:
            classification_data = [{'id': 1, 'description': 'Classification 1'},
                                   {'id': 2, 'description': 'Classification 2'}]

        if 'text/csv' in request.headers.get('Accept', ''):
            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(['id', 'description'])
            cw.writerows(
                [classification['id'], classification['description']] for classification in classification_data)
            output = si.getvalue()
            return Response(output, mimetype='text/csv')
        else:
            return jsonify(classification_data)

    elif request.method == 'POST':
        if request.content_type == 'text/csv':
            csv_file = request.files['file']
        elif request.content_type == 'application/json':
            data = request.get_json()
        return jsonify({'message': 'Classification added or updated'})

    elif request.method == 'PUT':
        data = request.get_json()
        return jsonify({'message': 'Classification updated'})

    elif request.method == 'DELETE':
        return jsonify({'message': 'Classification deleted'})
    else:
        return jsonify({'message': 'Method not allowed'}), 405


@auth_guard('admin')
@movie_routes.route('/genres', methods=['GET', 'POST'])
@movie_routes.route('/genres/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_genres(id=None):
    if request.method == 'GET':
        if id:
            genre = Genre.query.get(id)
            if not genre:
                return jsonify({'message': 'No genre found!'}), 404
            genre_data = {'idGenre': genre.idGenre, 'dtDescription': genre.dtDescription}
        else:
            genres = Genre.query.all()
            genre_data = [{'idGenre': genre.idGenre, 'dtDescription': genre.dtDescription} for genre in genres]

        if 'text/csv' in request.headers.get('Accept', ''):
            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(['idGenre', 'dtDescription'])
            cw.writerows([[genre['idGenre'], genre['dtDescription']] for genre in genre_data])
            output = si.getvalue()
            return Response(output, mimetype='text/csv')
        else:
            return jsonify({'genres': genre_data})

    elif request.method == 'POST':
        if request.content_type == 'text/csv':
            csv_file = request.files['file']
        elif request.content_type == 'application/json':
            data = request.get_json()
        return jsonify({'message': 'Genre added'})

    elif request.method == 'PUT':
        data = request.get_json()
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404
        genre.dtDescription = data['dtDescription']
        db.session.commit()
        return jsonify({'message': 'Genre updated'})

    elif request.method == 'DELETE':
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404
        db.session.delete(genre)
        db.session.commit()
        return jsonify({'message': 'Genre deleted'})

    else:
        return jsonify({'message': 'Method not allowed'}), 405


@movie_routes.route('/movies', methods=['GET', 'POST'])
@movie_routes.route('/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
def manage_movies(id=None):
    if request.method == 'GET':
        if id:
            movie = Movie.query.get(id)
            if not movie:
                return jsonify({'message': 'No movie found!'}), 404
            movie_data = {
                'idMovie': movie.idMovie,
                'dtTitle': movie.dtTitle,
                'dtYear': movie.dtYear,
                'dtAmountOfEp': movie.dtAmountOfEp,
                'dtAmountOfSeasons': movie.dtAmountOfSeasons,
                'dtLength': str(movie.dtLength),
                'dtMinAge': movie.dtMinAge,
                'fiType': movie.fiType,
                'fiGenre': movie.fiGenre,
                'fiClassification': movie.fiClassification,
                'fiLanguage': movie.fiLanguage
            }
            return jsonify(movie_data)

        else:
            movies = call_stored_procedure_get(procedure_name="GetAllMovies")
            return jsonify({'movies': movies})

    elif request.method == 'POST':
        data = request.get_json()
        new_language_data = (data['dtTitle'], parse(data['dtYear']), data['dtAmountOfEP'], data['dtAmountOfSeasons'],
                             parse(data['dtLength']),
                             data['dtMinAge'], data['fiType'], data['fiLanguage'], data['fiClassification'],
                             data['fiGenre'],)
        end_message = call_stored_procedure_post("""InsertNewMovie 
                                                                    @dtTitle = ? ,
                                                                    @dtYear = ? ,
                                                                    @dtAmountOfEp = ?,
                                                                    @dtAmountOfSeasons = ? ,
                                                                    @dtLength = ? ,
                                                                    @dtMinAge = ? , 
                                                                    @fiType = ? ,
                                                                    @fiLanguage = ?,
                                                                    @fiClassification = ?,
                                                                    @fiGenre = ? 
                                                                    """, new_language_data)
        if not end_message:
            return jsonify({'message': 'new movie added'})
        else:
            return jsonify({'message': 'movie could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        movie = Movie.query.get(id)

        if not movie:
            return jsonify({'message': 'No movie found!'}), 404

        movie.dtTitle = data.get('dtTitle', movie.dtTitle)
    elif request.method == 'DELETE':
        end_message = call_stored_procedure_post("DeleteMovieAndRelatedContent @MovieID = ? ", (id,))
        if not end_message:
            return jsonify({'message': 'movie deleted'})
        else:
            return jsonify({'message': 'movie could not be deleted', 'error_message': end_message})


@movie_routes.route('/qualities', methods=['GET', 'POST'])
@movie_routes.route('/qualities/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
def manage_qualities(id=None):

    if request.method == 'GET':
        if id:
            quality = Quality.query.get(id)
            if not quality:
                return jsonify({'message': 'No Quality found!'}), 404
            quality_data = {
                'idType': quality.idType,
                'dtDescription': quality.dtDescription,
                'dtPrice': quality.dtPrice
            }
            return jsonify(quality_data)
        else:
            qualities = Quality.query.all()
            output = []
            for quality in qualities:
                quality_data = {
                    'idType': quality.idType,
                    'dtDescription': quality.dtDescription,
                    'dtPrice': quality.dtPrice
                }
                output.append(quality_data)
            return jsonify({'qualities': output})
    elif request.method == 'POST':
        data = request.get_json()
        new_profile_data = (data['dtDescription'], data['dtPrice'])
        end_message = call_stored_procedure_post("""InsertQuality
                                                                @dtDescription = ?,
                                                                @dtPrice = ?
                                                                """, new_profile_data)
        if not end_message:
            return jsonify({'message': 'new quality added'})
        else:
            return jsonify({'message': 'quality could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        quality = Quality.query.get(id)

        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        quality.dtDescription = data.get('dtDescription', quality.dtDescription)
        quality.dtPrice = data.get('dtPrice', quality.dtPrice)

        db.session.commit()

        return jsonify({'message': 'Quality updated'})

    elif request.method == 'DELETE':
        quality = Quality.query.get(id)
        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        db.session.delete(quality)
        db.session.commit()

        return jsonify({'message': 'Quality has been deleted'})


@movie_routes.route('/subtitles', methods=['GET', 'POST'])
@movie_routes.route('/subtitles/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
def manage_subtitles(id=None):

    if request.method == 'GET':
        if id:
            subtitle = Subtitle.query.get(id)
            if not subtitle:
                return jsonify({'message': 'No subtitle found!'}), 404
            subtitle_data = {
                'idSubtitle': subtitle.idSubtitle,
                'fiMovie': subtitle.fiMovie,
                'fiLanguage': subtitle.fiLanguage
            }
            return jsonify(subtitle_data)

        else:
            subtitles = call_stored_procedure_get("GetAllSubtitles")

            return jsonify({'subtitles': subtitles})

    elif request.method == 'POST':
        data = request.get_json()

        new_subscription_data = (data['fiMovie'], data['fiLanguage'])
        end_message = call_stored_procedure_post("""InsertSubtitle
                                                                    @fiMovie = ?,
                                                                    @fiLanguage = ?
                                                                """, new_subscription_data)
        if not end_message:
            return jsonify({'message': 'new Subtitle added'})
        else:
            return jsonify({'message': 'Subtitle could not be added', 'error_message': end_message})

    elif request.method == 'PUT':
        data = request.get_json()
        subtitle = Subtitle.query.get(id)

        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        subtitle.fiMovie = data.get('fiMovie', subtitle.fiMovie)
        subtitle.fiLanguage = data.get('fiLanguage', subtitle.fiLanguage)

        db.session.commit()

        return jsonify({'message': 'Subtitle updated'})

    elif request.method == 'DELETE':
        subtitle = Subtitle.query.get(id)
        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        db.session.delete(subtitle)
        db.session.commit()

        return jsonify({'message': 'Subtitle has been deleted'})
