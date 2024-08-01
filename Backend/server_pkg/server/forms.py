from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, DateField, TextAreaField, SubmitField, RadioField, SelectMultipleField, widgets
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
from wtforms import ValidationError
from server_pkg.server.models import User
from datetime import date
from flask import request, url_for
from wtforms.validators import NumberRange


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )


class register_form_inf(FlaskForm):

    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Usernames must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    ph_no = StringField(validators=[InputRequired(), Length(10,10), Regexp("^[0-9]*$", 0, "Phone number must have only numbers")])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )
    category = SelectField(
        "Category",
        choices=[
            ("Cooking", "Cooking"),
            ("Fitness", "Fitness"),
            ("Fashion", "Fashion"),
            ("Travel", "Travel"),
            ("Tech", "Tech"),
            ("Education", "Education"),
            ("Lifestyle", "Lifestyle"),
            ("Gaming", "Gaming"),
            ("Health", "Health"),
            ("Beauty", "Beauty"),
            ("Finance", "Finance"),
            ("Parenting", "Parenting"),
            ("Entertainment", "Entertainment"),
            ("Music", "Music"),
            ("Sports", "Sports"),
        ],
        validators=[InputRequired()],
    )

    niche = SelectField(
        "Niche",
        choices=[
            # Cooking
            ("Grill", "Grill"),
            ("Baking", "Baking"),
            ("Vegetarian", "Vegetarian"),
            ("Vegan", "Vegan"),
            ("Culinary Arts", "Culinary Arts"),
            
            # Fitness
            ("Yoga", "Yoga"),
            ("Bodybuilding", "Bodybuilding"),
            ("Cardio", "Cardio"),
            ("CrossFit", "CrossFit"),
            ("Pilates", "Pilates"),
            
            # Fashion
            ("Streetwear", "Streetwear"),
            ("Luxury", "Luxury"),
            ("Sustainable Fashion", "Sustainable Fashion"),
            ("Vintage", "Vintage"),
            ("Accessories", "Accessories"),
            
            # Travel
            ("Backpacking", "Backpacking"),
            ("Luxury Travel", "Luxury Travel"),
            ("Adventure Travel", "Adventure Travel"),
            ("Cultural Tourism", "Cultural Tourism"),
            ("Solo Travel", "Solo Travel"),
            
            # Tech
            ("Gadgets", "Gadgets"),
            ("Software", "Software"),
            ("AI", "AI"),
            ("Gaming Tech", "Gaming Tech"),
            ("Smart Home", "Smart Home"),
            
            # Education
            ("Online Courses", "Online Courses"),
            ("STEM", "STEM"),
            ("Language Learning", "Language Learning"),
            ("Personal Development", "Personal Development"),
            ("Educational Resources", "Educational Resources"),
            
            # Lifestyle
            ("Home Decor", "Home Decor"),
            ("Minimalism", "Minimalism"),
            ("DIY", "DIY"),
            ("Sustainability", "Sustainability"),
            ("Travel Lifestyle", "Travel Lifestyle"),
            
            # Gaming
            ("Esports", "Esports"),
            ("RPG", "RPG"),
            ("Strategy Games", "Strategy Games"),
            ("Mobile Games", "Mobile Games"),
            ("Console Gaming", "Console Gaming"),
            
            # Health
            ("Nutrition", "Nutrition"),
            ("Mental Health", "Mental Health"),
            ("Holistic Health", "Holistic Health"),
            ("Fitness", "Fitness"),
            ("Chronic Illness", "Chronic Illness"),
            
            # Beauty
            ("Skincare", "Skincare"),
            ("Makeup", "Makeup"),
            ("Haircare", "Haircare"),
            ("Nail Art", "Nail Art"),
            ("Beauty Tutorials", "Beauty Tutorials"),
            
            # Finance
            ("Investing", "Investing"),
            ("Personal Finance", "Personal Finance"),
            ("Real Estate", "Real Estate"),
            ("Cryptocurrency", "Cryptocurrency"),
            ("Financial Planning", "Financial Planning"),
            
            # Parenting
            ("Baby Care", "Baby Care"),
            ("Parenting Tips", "Parenting Tips"),
            ("Child Education", "Child Education"),
            ("Family Activities", "Family Activities"),
            ("Teen Parenting", "Teen Parenting"),
            
            # Entertainment
            ("Movies", "Movies"),
            ("TV Shows", "TV Shows"),
            ("Theater", "Theater"),
            ("Celebrity News", "Celebrity News"),
            ("Stand-up Comedy", "Stand-up Comedy"),
            
            # Music
            ("Indie", "Indie"),
            ("Rock", "Rock"),
            ("Pop", "Pop"),
            ("Classical", "Classical"),
            ("Music Production", "Music Production"),
            
            # Sports
            ("Football", "Football"),
            ("Basketball", "Basketball"),
            ("Tennis", "Tennis"),
            ("Running", "Running"),
            ("Swimming", "Swimming"),
        ],
        validators=[InputRequired()],
    )


    def validate_email(self, email):
        if request.path != url_for('influencer_update_dashboard'):
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already registered!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
        
class register_form_spo(FlaskForm):

    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Usernames must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    ph_no = StringField(validators=[InputRequired(), Length(10,10), Regexp("^[0-9]*$", 0, "Phone number must have only numbers")])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )
    industry = SelectField(
        "Industry",
        choices=[
            ("Food & Beverage", "Food & Beverage"),
            ("Health & Wellness", "Health & Wellness"),
            ("Fashion & Apparel", "Fashion & Apparel"),
            ("Travel & Hospitality", "Travel & Hospitality"),
            ("Technology & Electronics", "Technology & Electronics"),
            ("Education", "Education"),
            ("Lifestyle", "Lifestyle"),
            ("Gaming & Esports", "Gaming & Esports"),
            ("Beauty & Personal Care", "Beauty & Personal Care"),
            ("Finance & Banking", "Finance & Banking"),
            ("Parenting & Family", "Parenting & Family"),
            ("Entertainment", "Entertainment"),
            ("Music", "Music"),
            ("Sports & Fitness", "Sports & Fitness"),
            ("Automotive", "Automotive"),
            ("Real Estate", "Real Estate"),
            ("Home & Garden", "Home & Garden"),
            ("Pet Care", "Pet Care"),
            ("Sustainability & Environment", "Sustainability & Environment"),
            ("Non-profit & Charity", "Non-profit & Charity"),
        ],
        validators=[InputRequired()],
    )

    def validate_email(self, email):
        if request.path != url_for('sponsor_update_dashboard'):
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already registered!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
        
class register_form_usr(FlaskForm):

    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Usernames must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    ph_no = StringField(validators=[InputRequired(), Length(10,10), Regexp("^[0-9]*$", 0, "Phone number must have only numbers")])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )

    def validate_email(self, email):
        if request.path != url_for('user_update_dashboard'):
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already registered!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
        
class create_campaign_form(FlaskForm):
    title = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid title"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Title must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    description = TextAreaField(
        validators=[
            InputRequired(),
            Length(3, 200, message="Please provide a valid description"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Description must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    sdate = DateField(
        "Start Date",
        format="%Y-%m-%d",
        validators=[InputRequired()],
        default=date.today(),
    )
    edate = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[InputRequired()],
        default=date.today(),
    )
    
    
    budget = IntegerField(
        validators=[
            InputRequired(),
            NumberRange(min=0, message="Budget must be a positive number")
        ]
    )
    visibility = SelectField(
        "Visibility",
        choices=[
            ("Public", "Public"),
            ("Private", "Private"),
        ],
        validators=[InputRequired()],
    )
    goal = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid goal"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Goal must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )