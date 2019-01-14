# This file contains the different forms of the site

# Import
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FieldList, FormField, TextField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site.models import User
from site import db


# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

# Registration Form 

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur",
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    permission_level = SelectField("Sélectionner le niveau d'autorisation",
                                   choices=[("visitor", 'Visiteur'), ("administrator", "Administrator")])

    submit = SubmitField('Créer le compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Ce nom d'utilisateur est pris. Veuillez en choisir un autre.")
