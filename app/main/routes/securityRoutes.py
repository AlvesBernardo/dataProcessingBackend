from app.services.emailSender import send_email
from app.extensions import db
from flask import Blueprint, request, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.account_model import Account
from itsdangerous import URLSafeTimedSerializer
from app.services.jwt_handler import generate_jwt_token, generate_refresh_token, decode_jwt_token
from datetime import datetime, timedelta, timezone
import random
from app.extensions import call_stored_procedure_post
from app.utils.passwordValidation import validate_password
from app.utils.emailValidation import check
from sqlalchemy.exc import SQLAlchemyError
from .routeFunctions import *

security = Blueprint('security', __name__)
s = URLSafeTimedSerializer('secret')

@security.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not verify_data(data,['dtEmail','dtPassword']):
            return jsonify({'message': 'Bad Request'}), 400

        user = None  # Initialize user to None
        if check(data['dtEmail']) and validate_password(data['dtPassword']):
            user = Account.query.filter_by(dtEmail=data['dtEmail']).first()
        else : 
            return jsonify({'message': 'Provided pasword or email is invalid'}), 401
        if user:
            
            if check_if_account_is_blocked(user) :
                return jsonify({"message": "Account blocked for 1 hour due to failed login attempts"}), 403
            if check_password_hash(user.dtPassword, data['dtPassword']):
                user.dtFailedLoginAttempts = 0
                user_info = {"idAccount": user.idAccount, "dtEmail": data['dtEmail']}

                user_info['dtIsAdmin'] = "user" if user.dtIsAdmin == 0 else "admin"
                token = handle_access_token(user_info,user,data)
                db.session.commit()
                print(token)
                return jsonify({'message': 'Logged in successfully', 'token': token}), 200
            else:
                return failed_login_attempt(user)
        else:
           return jsonify({'message': 'This email is not registered on the website'}), 401
    except SQLAlchemyError as e:
        print(e) 
        return jsonify({'message': 'Internal Server Error'}), 500

    
@security.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not verify_data(data,['dtEmail','dtPassword','isAccountBlocked','dtIsAdmin','fiSubscription','fiLanguage','dtRefreshToken']):
        return jsonify({'message': 'Bad Request'}), 400
    elif check(data['dtEmail']) and validate_password(data['dtPassword']):
        user = Account.query.filter_by(dtEmail=data['dtEmail']).first()
        if user:
            return jsonify({"message": "User Already Exists. Please Login"}),409
        else:
            code = "".join([str(random.randint(0, 9)) for _ in range(4)])
            dtEmail_with_code = data['dtEmail'] + code
            new_user = Account(
                dtEmail=data['dtEmail'],
                dtPassword=generate_password_hash(data['dtPassword']),
                isAccountBlocked=bool(data['isAccountBlocked']),
                dtIsAdmin=bool(data['dtIsAdmin']),
                fiSubscription=1,
                fiLanguage=1,
            )

            refresh_token = generate_refresh_token(
                payload={"idAccount": new_user.idAccount, "dtEmail": data['dtEmail']})
            new_user.dtRefreshToken = refresh_token

            db.session.add(new_user)
            db.session.commit()

            code_data = (code, dtEmail_with_code)

            # new_user.append(code_data)

            call_stored_procedure_post("""InsertCode
                                                        @dtEmail = ?,
                                                        @dtPassword = ?,
                                                        @isAccountBlocked = ?,
                                                        @dtIsAdmin = ?,
                                                        @fiSubscription = ?,
                                                        @fiLanguage = ?,
                                                        @dtRefreshToken = ?""", new_user)

            end_message = call_stored_procedure_post("""InsertCode 
                                                                    @Code = ? ,
                                                                    @fiEmail = ? """,
                                                     code_data)

            if not end_message:
                return jsonify({'message': 'Registered successfully', 'code': code, 'email': dtEmail_with_code}), 201
            else:
                return jsonify(
                    {'message': 'Registration successful, but code could not be added', 'error_message': end_message,
                     'code': code, 'email': dtEmail_with_code}), 409


@security.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not verify_data(data,['dtEmail']):
        return jsonify({'message': 'Bad Request'}), 400
    email = data['dtEmail']
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    elif check(email):
        user = Account.query.filter_by(dtEmail=email).first()
        if not user:
            return jsonify({'message': 'User does not exist'}), 404

        token = s.dumps(email, salt='email-confirm')

        link = url_for('security.reset_password', token=token, _external=True, _scheme='https')
        subject = 'Password Reset Requested'
        body = 'Please follow this link to reset your password: {}'.format(link)

        send_email(email, subject, body)

        return jsonify({'message': 'An email has been sent with instructions to reset your password.'}), 200


@security.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400

    if check(email):
        user = Account.query.filter_by(dtEmail=email).first()

        if not user:
            return jsonify({'message': 'User does not exist'}), 404

        new_password = request.form.get('dtPassword')
        if not new_password:
            return jsonify({'message': 'Password is required'}), 400
        elif validate_password(new_password):
            user.dtPassword = generate_password_hash(new_password)
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'Your password has been reset!'}), 200
