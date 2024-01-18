from app.extensions import db
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from itsdangerous import URLSafeTimedSerializer
from app.models.classification_model import Classification
from app.models.genre_model import Genre
from app.models.movie_model import Movie
from app.models.quality_model import Quality
from app.models.subtitle_model import Subtitle
from app.models.view_model import View
from app.services.auth_guard import auth_guard
movie_routes = Blueprint('movies', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}
@movie_routes.route('/classifications', methods=['GET', 'POST'])
@movie_routes.route('/classifications/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard('admin')
def manage_classifications(id=None):
    """
    API endpoint for managing classifications.

    :param id: Optional parameter to specify the ID of a specific classification.
    :return: JSON response with the requested classification(s) information.

    GET method:
        If `id` is provided, returns the classification information for the specified ID.
        If `id` is not provided, returns the information for all classifications.

    POST method:
        Adds a new classification to the database based on the provided JSON data.
        Returns a JSON response with a success message.

    PUT method:
        Updates the classification information for the specified ID based on the provided JSON data.
        Returns a JSON response with a success message.

    DELETE method:
        Deletes the classification with the specified ID from the database.
        Returns a JSON response with a success message.

    """
    if request.method == 'GET':
        if id:
            classification = Classification.query.get(id)
            if not classification:
                return jsonify({'message': 'No classification found!'}), 404

            classification_data = {
                'idClassification': classification.idClassification,
                'dtDescription': classification.dtDescription
            }

            return jsonify(classification_data)

        else:
            classifications = Classification.query.all()
            output = []

            for classification in classifications:
                classification_data = {
                    'idClassification': classification.idClassification,
                    'dtDescription': classification.dtDescription
                }
                output.append(classification_data)

            return jsonify({'classifications': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_classification = Classification(**data)

        db.session.add(new_classification)
        db.session.commit()

        return jsonify({'message':'new classification added'})

    elif request.method == 'PUT':
        data = request.get_json()
        classification = Classification.query.get(id)

        if not classification:
            return jsonify({'message': 'No classification found!'}), 404

        classification.dtDescription = data.get('dtDescription', classification.dtDescription)
        db.session.commit()

        return jsonify({'message':'classification updated'})

    elif request.method == 'DELETE':
        classification = Classification.query.get(id)
        if not classification:
            return jsonify({'message': 'No classification found!'}), 404

        db.session.delete(classification)
        db.session.commit()

        return jsonify({'message':'classification has been deleted'})



@movie_routes.route('/genres', methods=['GET', 'POST'])
@movie_routes.route('/genres/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_genres(id=None):
    """
    Manage Genres

    Handles various operations related to genres.

    :param id: The ID of the genre to manage. Defaults to None.
    :return: Returns the result of the operation as JSON.

    """
    if request.method == 'GET':
        if id:
            genre = Genre.query.get(id)
            if not genre:
                return jsonify({'message': 'No genre found!'}), 404

            genre_data = {
                'idGenre': genre.idGenre,
                'dtDescription': genre.dtDescription
            }

            return jsonify(genre_data)

        else:
            genres = Genre.query.all()
            output = []

            for genre in genres:
                genre_data = {
                    'idGenre': genre.idGenre,
                    'dtDescription': genre.dtDescription
                }
                output.append(genre_data)

            return jsonify({'genres': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_genre = Genre(**data)

        db.session.add(new_genre)
        db.session.commit()

        return jsonify({'message':'new genre added'})

    elif request.method == 'PUT':
        data = request.get_json()
        genre = Genre.query.get(id)

        if not genre:
            return jsonify({'message': 'No genre found!'}), 404

        genre.dtDescription = data.get('dtDescription', genre.dtDescription)
        db.session.commit()

        return jsonify({'message':'genre updated'})

    elif request.method == 'DELETE':
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404

        db.session.delete(genre)
        db.session.commit()

        return jsonify({'message':'genre has been deleted'})

@movie_routes.route('/movies', methods=['GET', 'POST'])
@movie_routes.route('/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_movies(id=None):
    """
    Handles CRUD operations for movies.

    :param id: (int, optional) The ID of the movie to manage.
    :return: (json) The requested movie data or a list of all movies.
    """
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
            movies = Movie.query.all()
            output = []

            for movie in movies:
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
                    'fiLanguage': movie.fiLanguage
                }
                output.append(movie_data)

            return jsonify({'movies': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_movie = Movie(**data)

        db.session.add(new_movie)
        db.session.commit()

        return jsonify({'message': 'new movie added'})

    elif request.method == 'PUT':
        data = request.get_json()
        movie = Movie.query.get(id)

        if not movie:
            return jsonify({'message': 'No movie found!'}), 404

        # update attributes
        movie.dtTitle = data.get('dtTitle', movie.dtTitle)
@movie_routes.route('/qualities', methods=['GET', 'POST'])
@movie_routes.route('/qualities/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_qualities(id=None):
    """
    Manage Qualities

    This method manages qualities based on the HTTP request method. It supports GET, POST, PUT, and DELETE operations.

    :param id: The ID of the quality (optional)
    :return: JSON response with quality data or a message

    GET Method:
    If an ID is provided, it retrieves the specific quality with the given ID. If no quality is found, a 404 error is returned.
    If no ID is provided, it retrieves all qualities from the database and returns them as a list of JSON objects.

    POST Method:
    Creates a new quality using the JSON data provided in the request payload. The new quality is then added to the database.
    Returns a JSON response with a success message.

    PUT Method:
    Updates an existing quality with the provided ID. The JSON data in the request payload is used to update the specified attributes of the quality.
    If no quality is found with the given ID, a 404 error is returned.
    Returns a JSON response with a success message.

    DELETE Method:
    Deletes an existing quality with the provided ID.
    If no quality is found with the given ID, a 404 error is returned.
    Returns a JSON response with a success message.

    """
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
        new_quality = Quality(**data)

        db.session.add(new_quality)
        db.session.commit()

        return jsonify({'message':'new quality added'})

    elif request.method == 'PUT':
        data = request.get_json()
        quality = Quality.query.get(id)

        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        # update attributes
        quality.dtDescription = data.get('dtDescription', quality.dtDescription)
        quality.dtPrice = data.get('dtPrice', quality.dtPrice)

        db.session.commit()

        return jsonify({'message':'Quality updated'})

    elif request.method == 'DELETE':
        quality = Quality.query.get(id)
        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        db.session.delete(quality)
        db.session.commit()

        return jsonify({'message':'Quality has been deleted'})
@movie_routes.route('/subtitles', methods=['GET', 'POST'])
@movie_routes.route('/subtitles/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_subtitles(id=None):
    """
    Manage subtitles.

    :param id: The ID of the subtitle to manage (optional).
    :return: If id is provided, returns the details of the specified subtitle.
             If id is not provided, returns a list of all subtitles.
    :rtype: JSON

    """
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
            subtitles = Subtitle.query.all()
            output = []

            for subtitle in subtitles:
                subtitle_data = {
                    'idSubtitle': subtitle.idSubtitle,
                    'fiMovie': subtitle.fiMovie,
                    'fiLanguage': subtitle.fiLanguage
                }
                output.append(subtitle_data)

            return jsonify({'subtitles': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_subtitle = Subtitle(**data)

        db.session.add(new_subtitle)
        db.session.commit()

        return jsonify({'message':'new subtitle added'})

    elif request.method == 'PUT':
        data = request.get_json()
        subtitle = Subtitle.query.get(id)

        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        subtitle.fiMovie = data.get('fiMovie', subtitle.fiMovie)
        subtitle.fiLanguage = data.get('fiLanguage', subtitle.fiLanguage)

        db.session.commit()

        return jsonify({'message':'Subtitle updated'})

    elif request.method == 'DELETE':
        subtitle = Subtitle.query.get(id)
        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        db.session.delete(subtitle)
        db.session.commit()

        return jsonify({'message':'Subtitle has been deleted'})
@movie_routes.route('/play_movie/<int:id>/')
def play_movie(id) :
    view = db.session.query(View).join(Movie,id == View.idView).filter(Movie.idMovie == id).first()

    # view = session.query(ViewModel).join(MovieModel).filter(MovieModel.c.dtTitle == movie_title).first()

    # if movie_title not in play_count:
    #     play_count[movie_title] = 1
    # else:
    #     play_count[movie_title] += 1


@movie_routes.route('/get_times_played/<int:movieId>/<int:userId>')
def getHowManyTimesMoviePlayed(movieId,userId = None):
    pass
