import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    UPLOAD_FOLDER = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'uploads')

    SECRET_KEY = os.environ.get('SECRET_KEY') or b'_5#y2L"F4Q8z\\n\\xec]/'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'sqlite:////' + os.path.join(
        basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['flask.noreply.message@gmail.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'es']
