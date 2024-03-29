import json
from app import create_app
from app.models.subscription_model import Subcription
from app.models.language_model import Language
from app.models.profile_model import Profile
from app.models.view_model import View
from flask_testing import TestCase


class TestRoutes(TestCase):
    def create_app(self):
        self.app = create_app('testing')
        return self.app


    def setUp(self):
        self.test_subscription = Subcription.query.filter_by(idSubscription=1).first()
        self.test_language = Language.query.filter_by(idLanguage=1).first()
        self.test_profile = Profile.query.filter_by(idProfile=10).first()
        self.test_view = View.query.filter_by(idView=15).first()


        def test_manage_subscriptions(self):
            response = self.client.post('/subscriptions', data=json.dumps(self.test_subscription),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.get('/subscriptions')
            self.assert200(response)

            response = self.client.get('/subscriptions/1')
            self.assert200(response)

            response = self.client.post('/subscriptions/1', data=json.dumps(self.test_subscription),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.delete('/subscriptions/1')
            self.assert200(response)


        def test_manage_languages(self):
            response = self.client.post('/languages', data=json.dumps(self.test_language),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.get('/languages')
            self.assert200(response)

            response = self.client.get('/languages/1')
            self.assert200(response)

            response = self.client.post('/languages/1', data=json.dumps(self.test_language),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.delete('/languages/1')
            self.assert200(response)


        def test_manage_profiles(self):
            response = self.client.post('/profiles', data=json.dumps(self.test_profile),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.get('/profiles')
            self.assert200(response)

            response = self.client.get('/profiles/1')
            self.assert200(response)

            response = self.client.post('/profiles/1', data=json.dumps(self.test_profile),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.delete('/profiles/1')
            self.assert200(response)


        def test_manage_views(self):
            response = self.client.post('/views', data=json.dumps(self.test_view), content_type='application/json')
            self.assert200(response)

            response = self.client.get('/views')
            self.assert200(response)

            response = self.client.get('/views/1')
            self.assert200(response)

            response = self.client.post('/views/1', data=json.dumps(self.test_view), content_type='application/json')
            self.assert200(response)

            response = self.client.delete('/views/1')
            self.assert200(response)


        def test_manage_non_existent_subscription(self):
            response = self.client.get('/subscriptions/9999')
            self.assert404(response)

            response = self.client.put('/subscriptions/9999', data=json.dumps(self.test_subscription),
                                       content_type='application/json')
            self.assert404(response)

            response = self.client.delete('/subscriptions/9999')
            self.assert404(response)


        def test_manage_languages_without_data(self):
            response = self.client.post('/languages', data=json.dumps({}), content_type='application/json')
            self.assert400(response)

            response = self.client.put('/languages/1', data=json.dumps({}), content_type='application/json')
            self.assert400(response)


        def test_create_profile_with_existing_id(self):
            existing_profile = Profile.query.filter_by(idProfile=10).first()
            response = self.client.post('/profiles', data=json.dumps(existing_profile), content_type='application/json')
            self.assert400(response)


        def test_manage_views_with_invalid_data(self):
            invalid_test_view = View.query.filter_by(idView=100).first()
            response = self.client.post('/views', data=json.dumps(invalid_test_view), content_type='application/json')
            self.assert400(response)

            response = self.client.put('/views/1', data=json.dumps(invalid_test_view), content_type='application/json')
            self.assert400(response)


        def test_manage_non_existent_language(self):
            response = self.client.get('/languages/9999')
            self.assert404(response)

            response = self.client.put('/languages/9999', data=json.dumps(self.test_language),
                                       content_type='application/json')
            self.assert404(response)

            response = self.client.delete('/languages/9999')
            self.assert404(response)


        def test_manage_non_existent_profile(self):
            response = self.client.get('/profiles/9999')
            self.assert404(response)

            response = self.client.put('/profiles/9999', data=json.dumps(self.test_profile),
                                       content_type='application/json')
            self.assert404(response)

            response = self.client.delete('/profiles/9999')
            self.assert404(response)


        def test_manage_non_existent_view(self):
            response = self.client.get('/views/9999')
            self.assert404(response)

            response = self.client.put('/views/9999', data=json.dumps(self.test_view), content_type='application/json')
            self.assert404(response)

            response = self.client.delete('/views/9999')
            self.assert404(response)


        def test_post_invalid_subscription(self):
            invalid_subscription = Subcription.query.filter_by(idSubscription=1000).first()
            response = self.client.post('/subscriptions', data=json.dumps(invalid_subscription),
                                        content_type='application/json')
            self.assert400(response)


        def test_post_invalid_language(self):
            invalid_language = Language.query.filter_by(idLanguage=1000).first()
            response = self.client.post('/languages', data=json.dumps(invalid_language),
                                        content_type='application/json')
            self.assert400(response)


        def test_post_invalid_profile(self):
            invalid_profile = Profile.query.filter_by(idProfile=10000).first()
            response = self.client.post('/profiles', data=json.dumps(invalid_profile), content_type='application/json')
            self.assert400(response)


        def test_post_invalid_view(self):
            invalid_view = View.query.filter_by(idView=1000).first()
            response = self.client.post('/views', data=json.dumps(invalid_view), content_type='application/json')
            self.assert400(response)


        def test_empty_db(self):
            response = self.client.get('/subscriptions')
            self.assert200(response)
            self.assertEqual(response.json, [])

            response = self.client.get('/languages')
            self.assert200(response)
            self.assertEqual(response.json, [])

            response = self.client.get('/profiles')
            self.assert200(response)
            self.assertEqual(response.json, [])

            response = self.client.get('/views')
            self.assert200(response)
            self.assertEqual(response.json, [])


        def test_login(self):
            response = self.client.post('/login', data=json.dumps(self.test_user), content_type='application/json')
            self.assert200(response)
            self.assertIn('token', response.json)

            wrong_email_user = {"dtEmail": "wrong@example.com", "dtPassword": self.test_user["dtPassword"]}
            response = self.client.post('/login', data=json.dumps(wrong_email_user), content_type='application/json')
            self.assert401(response)

            wrong_password_user = {"dtEmail": self.test_user["dtEmail"], "dtPassword": "wrongpassword"}
            response = self.client.post('/login', data=json.dumps(wrong_password_user), content_type='application/json')
            self.assert401(response)


        def test_register(self):
            new_user = {"dtEmail": "newuser@example.com", "dtPassword": "newpassword"}
            response = self.client.post('/register', data=json.dumps(new_user), content_type='application/json')
            self.assert201(response)
            response = self.client.post('/register', data=json.dumps(self.test_user), content_type='application/json')
            self.assert409(response)


        def test_forgot_password(self):
            response = self.client.post('/forgot-password', data=json.dumps({"dtEmail": self.test_user["dtEmail"]}),
                                        content_type='application/json')
            self.assert200(response)

            response = self.client.post('/forgot-password', data=json.dumps({"dtEmail": "nonexist@example.com"}),
                                        content_type='application/json')
            self.assert404(response)


        def test_reset_password(self):
            response = self.client.post('/reset-password/invalidtoken', data=json.dumps({"dtPassword": "newpassword"}),
                                        content_type='application/json')
            self.assert400(response)


        def test_register_missing_fields(self):
            incomplete_data = {
                'dtEmail': 'incomplete@example.com',
                # 'dtPassword': 'password'  # missing this field
            }
            response = self.client.post('/register', data=json.dumps(incomplete_data), content_type='application/json')
            self.assert400(response)


        def test_reset_without_password(self):
            reset_token = 'some-token'
            response = self.client.post(f'/reset-password/{reset_token}', data=json.dumps({}),
                                        content_type='application/json')
            self.assert400(response)


        def test_register_existing_email(self):
            existing_email = self.test_user['dtEmail']
            response = self.client.post('/register', data=json.dumps(dict(dtEmail=existing_email, dtPassword='passwd')),
                                        content_type='application/json')
            self.assert409(response)


        def test_reset_password_wrong_token(self):
            response = self.client.post('/reset-password/wrong-token', data=json.dumps({'dtPassword': 'newPass'}),
                                        content_type='application/json')
            self.assert400(response)


        def test_send_email(self):
            response = self.client.post('/sendEmail', data=json.dumps({
                'recieverEmail': 'receiver@example.com',
                'subject': 'Hello',
                'body': 'Hello from Flask'
            }), content_type='application/json')
            self.assert200(response)


        def test_manage_classifications(self):
            response = self.client.get('/classifications')
            self.assert200(response)

            new_classification = {"dtDescription": "My new classification"}
            response = self.client.post('/classifications', data=json.dumps(new_classification),
                                        content_type='application/json')
            self.assert200(response)


        def test_manage_genres(self):
            response = self.client.get('/genres')
            self.assert200(response)

            new_genre = {"dtDescription": "My new genre"}
            response = self.client.post('/genres', data=json.dumps(new_genre), content_type='application/json')
            self.assert200(response)


        def test_manage_movies(self):
            response = self.client.get('/movies')
            self.assert200(response)


        def test_manage_qualities(self):
            response = self.client.get('/qualities')
            self.assert200(response)

            new_quality = {"dtDescription": "Great Quality", "dtPrice": 10.0}
            response = self.client.post('/qualities', data=json.dumps(new_quality), content_type='application/json')
            self.assert200(response)


        def test_manage_subtitles(self):
            response = self.client.get('/subtitles')
            self.assert200(response)


        def test_manage_classifications_put_delete(self):
            new_classification = {"dtDescription": "New Classification for testing PUT and DELETE"}
            response = self.client.post('/classifications', data=json.dumps(new_classification),
                                        content_type='application/json')
            self.assert200(response)
            classification_id = 1

            updated_classification = {"dtDescription": "Updated Description"}
            response = self.client.put(f'/classifications/{classification_id}', data=json.dumps(updated_classification),
                                       content_type='application/json')
            self.assert200(response)

            response = self.client.delete(f'/classifications/{classification_id}')
            self.assert200(response)


        def test_manage_genres_put_delete(self):
            genre_id = 2

            updated_genre = {"dtDescription": "Updated Description"}
            response = self.client.put(f'/genres/{genre_id}', data=json.dumps(updated_genre),
                                       content_type='application/json')
            self.assert200(response)

            response = self.client.delete(f'/genres/{genre_id}')
            self.assert200(response)


        def test_manage_qualities_put_delete(self):
            quality_id = 3
            updated_quality = {"dtDescription": "Updated Quality Description", "dtPrice": 20.0}
            response = self.client.put(f'/qualities/{quality_id}', data=json.dumps(updated_quality),
                                       content_type='application/json')
            self.assert200(response)

            response = self.client.delete(f'/qualities/{quality_id}')
            self.assert200(response)


        def test_manage_subtitles_put_delete(self):
            subtitle_id = 4

            updated_subtitle = {"fiMovie": 2, "fiLanguage": 3}
            response = self.client.put(f'/subtitles/{subtitle_id}', data=json.dumps(updated_subtitle),
                                       content_type='application/json')
            self.assert200(response)

            response = self.client.delete(f'/subtitles/{subtitle_id}')
            self.assert200(response)
