from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    TextAreaField, DateTimeField, SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    EqualTo, Email, Length
from app.models import User


##########################
# USER LOG IN FORM
##########################

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remeber me')
    submit = SubmitField('Sign In')


##########################
# USER REGISTRATION FORM
##########################

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[
        DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                "Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "Please use a different email address.")


##########################
# ADD NEW POST FORM
##########################

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    body = TextAreaField(
        'Article text', validators=[DataRequired(), Length(min=1, max=140)])
    created_date = DateTimeField('Created date')
    submit = SubmitField('Submit')


##########################
# EDIT PROFILE INFO FORM
##########################

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")


##############################
# RESET PASSWORD REQUEST FORM
##############################

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def send_password_reset_email(self, user):
        pass


##############################
# RESET PASSWORD REQUEST FORM
##############################

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[
                                    DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
