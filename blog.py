from app import app, db
from app.models import User, Post
from pprint import pprint


# Преимпортируем модули для быстрого использования в flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'pprint': pprint}
