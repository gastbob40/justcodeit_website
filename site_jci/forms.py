# This file contains the different forms of the site

# Import
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FieldList, FormField, TextField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site_jci.models import User


# Login Form
class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur",
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    remember = BooleanField('Se souvenir de moi')

# Registration Form 

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur",
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    permission_level = SelectField('Level de permission',
                                   choices=[("member", 'Membre du projet'), ("administrator", "Administrateur")])

    submit = SubmitField('Enregistrer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Ce nom d'utilisateur est pris. Veuillez en choisir un autre.")

class UpdateAccountForm(FlaskForm):
    username = StringField("Nom d'utilisteur",
                           validators=[DataRequired(), Length(min=2, max=20)])
   
    picture = FileField('Photo de profil', validators=[FileAllowed(['jpg', 'png'])])
    permission_level = SelectField('Level de permission',
                                   choices=[("member", 'Membre du projet'), ("administrator", "Administrateur")])

    password = PasswordField('Changer le mot de passe', validators=[])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[ EqualTo('password')])

    submit = SubmitField('Mettre à jour')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur est pris. Veuillez en choisir un autre.")

    

class PostForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    submit = SubmitField('Poster')