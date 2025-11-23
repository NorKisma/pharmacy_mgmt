from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# -------------------------
# LOGIN FORM
# -------------------------
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

# -------------------------
# REGISTER FORM (Public)
# -------------------------
class RegisterForm(FlaskForm):
    name = StringField(
        "Full Name", 
        validators=[DataRequired(), Length(min=2, max=120)]
    )
    email = StringField(
        "Email", 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    # Note: Variable name is 'confirm_password' to match your snippet
    confirm_password = PasswordField( 
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Register")

# -------------------------
# CHANGE PASSWORD FORM
# -------------------------
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match.")]
    )
    submit = SubmitField("Update Password")