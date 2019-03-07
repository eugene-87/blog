from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel


app = Flask(__name__)

# Добавляем конфигурационный файл
app.config.from_object(Config)

# Инициализируем базу данных и передаем ей наше приложение
db = SQLAlchemy(app)

# Инициализируем миграцию базы данных и передаем ей наше приложение
# и базу данных
migrate = Migrate(app, db)

# Инициализируем систему авторизации и передаем ей наше приложение
login = LoginManager(app)

# Указываем какая функция отвечает за авторизацию пользователей
login.login_view = 'login'

# Инициализируем почтовый сервис для восстановления пароля пользователя
mail = Mail(app)

# Инициализируем bootstrap framework
bootstrap = Bootstrap(app)

# Инициализируем конвертер часового пояса
moment = Moment(app)

# Расширение для работы с переводами
babel = Babel(app)

# добавляем декорированную функцию, которая вызывается
# для каждого request чтобы перевести контент на нужный язык

@babel.localeselector
def set_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# Дабавляем логирование ошибок
if not app.debug:
    # --- по эл. почте
    if app.config['MAIL_SERVER']:

        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Blog Failure',
            credentials=auth, secure=secure)

        mail_handler.setLevel(logging.ERROR)

        app.logger.addHandler(mail_handler)

    # --- в файл логов
    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/blog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: \
             %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Blog startup')

from app import routes, models, errors
