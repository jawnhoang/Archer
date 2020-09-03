from flask_login import login_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.routing import ValidationError
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    studentName = StringField("First/Last Name", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email taken. Please use a different email.')


class SurveyForm(FlaskForm):
    major = SelectField(u'Major', choices=[('Advertising', 'Advertising'),
                                           ('Aerospace Engineering', 'Aerospace Engineering'),
                                           ('African American Studies', 'African American Studies'),
                                           ('Anthropology', 'Anthropology'),
                                           ('Applied Mathematics', 'Applied Mathematics'),
                                           ('Art History and Visual Culture', 'Art History and Visual Culture'),
                                           ('Art', 'Art'),
                                           ('Aviation', 'Aviation'),
                                           ('Behavioral Science', 'Behavioral Science'),
                                           ('Biological Science', 'Biological Science'),
                                           ('Biological Science', 'Biological Science'),
                                           ('Biomedical Engineering', 'Biomedical Engineering'),
                                           ('Business Administration', 'Business Administration'),
                                           ('Chemical Engineering', 'Chemical Engineering'),
                                           ('Chemistry', 'Chemistry'),
                                           ('Chicana and Chicano Studies', 'Chicana and Chicano Studies'),
                                           ('Child and Adolescent Development', 'Child and Adolescent Development'),
                                           ('Child and Adolescent Development, Preparation for Teaching', 'Child and Adolescent Development, Preparation for Teaching'),
                                           ('Chinese', 'Chinese'),
                                           ('Civil Engineering', 'Civil Engineering'),
                                           ('Communication Studies', 'Communication Studies'),
                                           ('Communicative Disorders and Sciences', 'Communicative Disorders and Sciences'),
                                           ('Computer Engineering', 'Computer Engineering'),
                                           ('Computer Science', "Computer Science"),
                                           ('Creative Arts', 'Creative Arts'),
                                           ('Dance', 'Dance'),
                                           ('Design Studies', 'Design Studies'),
                                           ('Earth Science', 'Earth Science'),
                                           ('Ecology and Evolution', 'Ecology and Evolution'),
                                           ('Economics', 'Economics'),
                                           ('Electrical Engineering', 'Electrical Engineering'),
                                           ('English', 'English'),
                                           ('English, Preparation for Teaching (Single Subject)', 'English, Preparation for Teaching (Single Subject)'),
                                           ('Environmental Studies', 'Environmental Studies'),
                                           ('Environmental Studies, Preparation for Teaching', 'Environmental Studies, Preparation for Teaching'),
                                           ('Forensic Science', 'Forensic Science'),
                                           ('French', 'French'),
                                           ('French, Preparation for Teaching', 'French, Preparation for Teaching'),
                                           ('General Engineering', 'General Engineering'),
                                           ('Geography', 'Geography'),
                                           ('Geology', 'Geology'),
                                           ('Global Studies', 'Global Studies'),
                                           ('Graphic Design', 'Graphic Design'),
                                           ('History & Social Science Teacher Preparation', 'History & Social Science Teacher Preparation'),
                                           ('History', 'History'),
                                           ('Hospitality, Tourism and Event Management', 'Hospitality, Tourism and Even Management'),
                                           ('Humanities', 'Humanities'),
                                           ('Industrial and Systems Engineering', 'Industrial and Systems Engineering'),
                                           ('Industrial Design', 'Industrial Design'),
                                           ('Industrial Technology', 'Industrial Technology'),
                                           ('Interior Design', 'Interior Design'),
                                           ('Japanese', 'Japanese'),
                                           ('Journalism', 'Journalism'),
                                           ('Justice Studies', 'Justice Studies'),
                                           ('Kinesiology', 'Kinesiology'),
                                           ('Kinesiology, Preparation for Teaching', 'Kinesiology, Preparation for Teaching'),
                                           ('Liberal Studies, Integrated Teacher Education Program', 'Liberal Studies, Integrated Teacher Education Program'),
                                           ('Liberal Studies, Preparation for Teaching', 'Liberal Studies, Preparation for Teaching'),
                                           ('Linguistics', 'Linguistics'),
                                           ('Marine Biology', 'Marine Biology'),
                                           ('Materials Engineering', 'Materials Engineering'),
                                           ('Mathematics', 'Mathematics'),
                                           ('Mathematics, Preparation for Teaching (Integrated)', 'Mathematics, Preparation for Teaching (Integrated)'),
                                           ('Mechanical Engineering', 'Mechanical Engineering'),
                                           ('Meteorology', 'Meteorology'),
                                           ('Music', 'Music'),
                                           ('Nursing', 'Nursing'),
                                           ('Nutritional Science', 'Nutritional Science'),
                                           ('Organizational Studies', 'Organizational Studies'),
                                           ('Packaging', 'Packaging'),
                                           ('Philosophy', 'Philosophy'),
                                           ('Physics', 'Physics'),
                                           ('Political Science', 'Political Science'),
                                           ('Psychology', 'Psychology'),
                                           ('Public Health', 'Public Health'),
                                           ('Public Relations', 'Public Relations'),
                                           ('Radio-Television-Film', 'Radio-Television-Film'),
                                           ('Recreation', 'Recreation'),
                                           ('Social Science', 'Social Science'),
                                           ('Social Work', 'Social Work'),
                                           ('Sociology', 'Sociology'),
                                           ('Software Engineering', 'Software Engineering'),
                                           ('Spanish', 'Spanish'),
                                           ('Special Major', 'Special Major'),
                                           ('Theatre Arts', 'Theatre Arts'),
                                           ('Undeclared', 'Undeclared')])
    outdoor = SelectField(u'Outdoor Activities', choices=[('Airsoft', 'Airsoft'),
                                                          ('Amusement parks', 'Amusement parks'),
                                                          ('Archery', 'Archery'),
                                                          ('Badminton', 'Badminton'),
                                                          ('Backpacking', 'Backpacking'),
                                                          ('Basketball', 'Basketball'),
                                                          ('Baseball', 'Baseball'),
                                                          ('Barbecuing', 'Barbecuing'),
                                                          ('Birdwatching', 'Birdwatching'),
                                                          ('Bowling', 'Bowling'),
                                                          ('Camping', 'Camping'),
                                                          ('Canoeing', 'Canoeing'),
                                                          ('Concerts', 'Concerts'),
                                                          ('Cycling', 'Cycling'),
                                                          ('Dragon boating', 'Dragon boating'),
                                                          ('Diving', 'Diving'),
                                                          ('Driving', 'Driving'),
                                                          ('Fishing', 'Fishing'),
                                                          ('Frisbee', 'Frisbee'),
                                                          ('Football', 'Football'),
                                                          ('Gardening', 'Gardening'),
                                                          ('Going on a road trip', 'Going on a road trip'),
                                                          ('Going out to eat', "Going out to eat"),
                                                          ('Going to the beach', 'Going to the beach'),
                                                          ('Going to the movies', 'Going to the movies'),
                                                          ('Golfing', 'Golfing'),
                                                          ('Hiking', 'Hiking'),
                                                          ('Hockey', 'Hockey'),
                                                          ('Horseriding', 'Horseriding'),
                                                          ('Kayaking', 'Kayaking'),
                                                          ('Kite flying', 'Kite flying'),
                                                          ('Obstacle courses', 'Obstacle courses'),
                                                          ('Paragliding', 'Paragliding'),
                                                          ('Rafting', 'Rafting'),
                                                          ('Rock climbing', 'Rock climbing'),
                                                          ('Running', 'Running'),
                                                          ('Shopping', 'Shopping'),
                                                          ('Skateboarding', 'Skateboarding'),
                                                          ('Skating', 'Skating'),
                                                          ('Skiing', 'Skiing'),
                                                          ('Skydiving', 'Skydiving'),
                                                          ('Snowboarding', 'Snowboarding'),
                                                          ('Soccer', 'Soccer'),
                                                          ('Sporting events', 'Sporting events'),
                                                          ('Stargazing', 'Stargazing'),
                                                          ('Surfing', 'Surfing'),
                                                          ('Swimming', 'Swimming'),
                                                          ('Taking pictures', 'Taking pictures'),
                                                          ('Tennis', 'Tennis'),
                                                          ('Traveling', 'Traveling'),
                                                          ('Vistiing flea markets', 'Visiting flea markets'),
                                                          ('Volleyball', 'Volleyball'),
                                                          ('Volunteering', 'Volunteering'),
                                                          ('Water skiing', 'Water skiing'),
                                                          ('Working out', 'Working out')])
    indoor = SelectField(u'Indoor Activities', choices=[('Baking', 'Baking'),
                                                        ('Board games', 'Board games'),
                                                        ('Blacksmithing', 'Blacksmithing'),
                                                        ('Blogging', 'Blogging'),
                                                        ('Calligraphy', 'Calligraphy'),
                                                        ('Carpentry', 'Carpentry'),
                                                        ('Cleaning', 'Cleaning'),
                                                        ('Cooking', 'Cooking'),
                                                        ('Dance', 'Dance'),
                                                        ('Drawing', 'Drawing'),
                                                        ('Fortune telling', 'Fortune telling'),
                                                        ('Home decor', 'Home decor'),
                                                        ('Juggling', 'Juggling'),
                                                        ('Knitting', 'Knitting'),
                                                        ('Listening to music', 'Listening to music'),
                                                        ('Make-up', 'Make-up'),
                                                        ('Magic', 'Magic'),
                                                        ('Martial arts', 'Martial arts'),
                                                        ('Meditation', 'Meditation'),
                                                        ('Origami', 'Origami'),
                                                        ('Painting', 'Painting'),
                                                        ('Playing an instrument', 'Playing an instrument'),
                                                        ('Pottery', 'Pottery'),
                                                        ('Puzzles', 'Puzzles'),
                                                        ('Reading', "Reading"),
                                                        ('Sculpting', 'Sculpting'),
                                                        ('Sewing', 'Sewing'),
                                                        ('Singing', 'Singing'),
                                                        ('Social media', 'Social media'),
                                                        ('Streaming', 'Streaming'),
                                                        ('Studying', 'Studying'),
                                                        ('Table tennis', 'Table tennis'),
                                                        ('Video games', 'Video games'),
                                                        ('Watching TV', 'Watching TV'),
                                                        ('Writing', 'Writing'),
                                                        ('Yoga', 'Yoga')])
    question = SelectField(u'Security Question', choices=[('maiden name', 'What is your mother maiden name'),
                                                          ("high/college",
                                                                   'Where did you go to high school/college?'),
                                                          ('pet',
                                                                   'What was the name of your first/current/favorite pet?')])
    answer = StringField('Answer', validators=[InputRequired(), Length(min=3, max=50)])


class SurveyUpdateForm(FlaskForm):
    major = SelectField(u'Major', choices=[('Reselect Major...', 'Reselect Major...'),
                                            ('Advertising', 'Advertising'),
                                           ('Aerospace Engineering', 'Aerospace Engineering'),
                                           ('African American Studies', 'African American Studies'),
                                           ('Anthropology', 'Anthropology'),
                                           ('Applied Mathematics', 'Applied Mathematics'),
                                           ('Art History and Visual Culture', 'Art History and Visual Culture'),
                                           ('Art', 'Art'),
                                           ('Aviation', 'Aviation'),
                                           ('Behavioral Science', 'Behavioral Science'),
                                           ('Biological Science', 'Biological Science'),
                                           ('Biological Science', 'Biological Science'),
                                           ('Biomedical Engineering', 'Biomedical Engineering'),
                                           ('Business Administration', 'Business Administration'),
                                           ('Chemical Engineering', 'Chemical Engineering'),
                                           ('Chemistry', 'Chemistry'),
                                           ('Chicana and Chicano Studies', 'Chicana and Chicano Studies'),
                                           ('Child and Adolescent Development', 'Child and Adolescent Development'),
                                           ('Child and Adolescent Development, Preparation for Teaching', 'Child and Adolescent Development, Preparation for Teaching'),
                                           ('Chinese', 'Chinese'),
                                           ('Civil Engineering', 'Civil Engineering'),
                                           ('Communication Studies', 'Communication Studies'),
                                           ('Communicative Disorders and Sciences', 'Communicative Disorders and Sciences'),
                                           ('Computer Engineering', 'Computer Engineering'),
                                           ('Computer Science', "Computer Science"),
                                           ('Creative Arts', 'Creative Arts'),
                                           ('Dance', 'Dance'),
                                           ('Design Studies', 'Design Studies'),
                                           ('Earth Science', 'Earth Science'),
                                           ('Ecology and Evolution', 'Ecology and Evolution'),
                                           ('Economics', 'Economics'),
                                           ('Electrical Engineering', 'Electrical Engineering'),
                                           ('English', 'English'),
                                           ('English, Preparation for Teaching (Single Subject)', 'English, Preparation for Teaching (Single Subject)'),
                                           ('Environmental Studies', 'Environmental Studies'),
                                           ('Environmental Studies, Preparation for Teaching', 'Environmental Studies, Preparation for Teaching'),
                                           ('Forensic Science', 'Forensic Science'),
                                           ('French', 'French'),
                                           ('French, Preparation for Teaching', 'French, Preparation for Teaching'),
                                           ('General Engineering', 'General Engineering'),
                                           ('Geography', 'Geography'),
                                           ('Geology', 'Geology'),
                                           ('Global Studies', 'Global Studies'),
                                           ('Graphic Design', 'Graphic Design'),
                                           ('History & Social Science Teacher Preparation', 'History & Social Science Teacher Preparation'),
                                           ('History', 'History'),
                                           ('Hospitality, Tourism and Event Management', 'Hospitality, Tourism and Even Management'),
                                           ('Humanities', 'Humanities'),
                                           ('Industrial and Systems Engineering', 'Industrial and Systems Engineering'),
                                           ('Industrial Design', 'Industrial Design'),
                                           ('Industrial Technology', 'Industrial Technology'),
                                           ('Interior Design', 'Interior Design'),
                                           ('Japanese', 'Japanese'),
                                           ('Journalism', 'Journalism'),
                                           ('Justice Studies', 'Justice Studies'),
                                           ('Kinesiology', 'Kinesiology'),
                                           ('Kinesiology, Preparation for Teaching', 'Kinesiology, Preparation for Teaching'),
                                           ('Liberal Studies, Integrated Teacher Education Program', 'Liberal Studies, Integrated Teacher Education Program'),
                                           ('Liberal Studies, Preparation for Teaching', 'Liberal Studies, Preparation for Teaching'),
                                           ('Linguistics', 'Linguistics'),
                                           ('Marine Biology', 'Marine Biology'),
                                           ('Materials Engineering', 'Materials Engineering'),
                                           ('Mathematics', 'Mathematics'),
                                           ('Mathematics, Preparation for Teaching (Integrated)', 'Mathematics, Preparation for Teaching (Integrated)'),
                                           ('Mechanical Engineering', 'Mechanical Engineering'),
                                           ('Meteorology', 'Meteorology'),
                                           ('Music', 'Music'),
                                           ('Nursing', 'Nursing'),
                                           ('Nutritional Science', 'Nutritional Science'),
                                           ('Organizational Studies', 'Organizational Studies'),
                                           ('Packaging', 'Packaging'),
                                           ('Philosophy', 'Philosophy'),
                                           ('Physics', 'Physics'),
                                           ('Political Science', 'Political Science'),
                                           ('Psychology', 'Psychology'),
                                           ('Public Health', 'Public Health'),
                                           ('Public Relations', 'Public Relations'),
                                           ('Radio-Television-Film', 'Radio-Television-Film'),
                                           ('Recreation', 'Recreation'),
                                           ('Social Science', 'Social Science'),
                                           ('Social Work', 'Social Work'),
                                           ('Sociology', 'Sociology'),
                                           ('Software Engineering', 'Software Engineering'),
                                           ('Spanish', 'Spanish'),
                                           ('Special Major', 'Special Major'),
                                           ('Theatre Arts', 'Theatre Arts'),
                                           ('Undeclared', 'Undeclared')])
    outdoor = SelectField(u'Outdoor Activities', choices=[('Reselect Outdoor Activity...', 'Reselect Outdoor Activity...'),
                                                        ('Airsoft', 'Airsoft'),
                                                          ('Amusement parks', 'Amusement parks'),
                                                          ('Archery', 'Archery'),
                                                          ('Badminton', 'Badminton'),
                                                          ('Backpacking', 'Backpacking'),
                                                          ('Basketball', 'Basketball'),
                                                          ('Baseball', 'Baseball'),
                                                          ('Barbecuing', 'Barbecuing'),
                                                          ('Birdwatching', 'Birdwatching'),
                                                          ('Bowling', 'Bowling'),
                                                          ('Camping', 'Camping'),
                                                          ('Canoeing', 'Canoeing'),
                                                          ('Concerts', 'Concerts'),
                                                          ('Cycling', 'Cycling'),
                                                          ('Dragon boating', 'Dragon boating'),
                                                          ('Diving', 'Diving'),
                                                          ('Driving', 'Driving'),
                                                          ('Fishing', 'Fishing'),
                                                          ('Frisbee', 'Frisbee'),
                                                          ('Football', 'Football'),
                                                          ('Gardening', 'Gardening'),
                                                          ('Going on a road trip', 'Going on a road trip'),
                                                          ('Going out to eat', "Going out to eat"),
                                                          ('Going to the beach', 'Going to the beach'),
                                                          ('Going to the movies', 'Going to the movies'),
                                                          ('Golfing', 'Golfing'),
                                                          ('Hiking', 'Hiking'),
                                                          ('Hockey', 'Hockey'),
                                                          ('Horseriding', 'Horseriding'),
                                                          ('Kayaking', 'Kayaking'),
                                                          ('Kite flying', 'Kite flying'),
                                                          ('Obstacle courses', 'Obstacle courses'),
                                                          ('Paragliding', 'Paragliding'),
                                                          ('Rafting', 'Rafting'),
                                                          ('Rock climbing', 'Rock climbing'),
                                                          ('Running', 'Running'),
                                                          ('Shopping', 'Shopping'),
                                                          ('Skateboarding', 'Skateboarding'),
                                                          ('Skating', 'Skating'),
                                                          ('Skiing', 'Skiing'),
                                                          ('Skydiving', 'Skydiving'),
                                                          ('Snowboarding', 'Snowboarding'),
                                                          ('Soccer', 'Soccer'),
                                                          ('Sporting events', 'Sporting events'),
                                                          ('Stargazing', 'Stargazing'),
                                                          ('Surfing', 'Surfing'),
                                                          ('Swimming', 'Swimming'),
                                                          ('Taking pictures', 'Taking pictures'),
                                                          ('Tennis', 'Tennis'),
                                                          ('Traveling', 'Traveling'),
                                                          ('Vistiing flea markets', 'Visiting flea markets'),
                                                          ('Volleyball', 'Volleyball'),
                                                          ('Volunteering', 'Volunteering'),
                                                          ('Water skiing', 'Water skiing'),
                                                          ('Working out', 'Working out')])
    indoor = SelectField(u'Indoor Activities', choices=[('Reselect Indoor Activity...', 'Reselect Indoor Activity...'),
                                                        ('Baking', 'Baking'),
                                                        ('Board games', 'Board games'),
                                                        ('Blacksmithing', 'Blacksmithing'),
                                                        ('Blogging', 'Blogging'),
                                                        ('Calligraphy', 'Calligraphy'),
                                                        ('Carpentry', 'Carpentry'),
                                                        ('Cleaning', 'Cleaning'),
                                                        ('Cooking', 'Cooking'),
                                                        ('Dance', 'Dance'),
                                                        ('Drawing', 'Drawing'),
                                                        ('Fortune telling', 'Fortune telling'),
                                                        ('Home decor', 'Home decor'),
                                                        ('Juggling', 'Juggling'),
                                                        ('Knitting', 'Knitting'),
                                                        ('Listening to music', 'Listening to music'),
                                                        ('Make-up', 'Make-up'),
                                                        ('Magic', 'Magic'),
                                                        ('Martial arts', 'Martial arts'),
                                                        ('Meditation', 'Meditation'),
                                                        ('Origami', 'Origami'),
                                                        ('Painting', 'Painting'),
                                                        ('Playing an instrument', 'Playing an instrument'),
                                                        ('Pottery', 'Pottery'),
                                                        ('Puzzles', 'Puzzles'),
                                                        ('Reading', "Reading"),
                                                        ('Sculpting', 'Sculpting'),
                                                        ('Sewing', 'Sewing'),
                                                        ('Singing', 'Singing'),
                                                        ('Social media', 'Social media'),
                                                        ('Streaming', 'Streaming'),
                                                        ('Studying', 'Studying'),
                                                        ('Table tennis', 'Table tennis'),
                                                        ('Video games', 'Video games'),
                                                        ('Watching TV', 'Watching TV'),
                                                        ('Writing', 'Writing'),
                                                        ('Yoga', 'Yoga')])


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=120)])
    submitMsg = SubmitField('send')


# Class needed for resets password page
class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    question = SelectField(u'Security Question', choices=[('maiden name', 'What is your mother maiden name'),
                                                          ("high/college",
                                                           'Where did you go to high school/college?'),
                                                          ('pet',
                                                           'What was the name of your first/current/favorite pet?')])
    answer = StringField('Answer', validators=[InputRequired(), Length(min=3, max=50)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=40)])
    submit = SubmitField('Reset Password')

class ReportForm(FlaskForm):
    reasons = SelectField(u'Reasons', choices=[('Harrasment', 'Harrasment'),
                                                ('Illegal Activities', 'Illegal Activities'),
                                                ('Blackmailing', 'Blackmailing'),
                                                ('Harmful/Racist messages', 'Harmful/Racist messages'),
                                                ('Stalking', 'Stalking')])
    submit = SubmitField('Report')

class NotificationForm(FlaskForm):
    seenNotif = BooleanField('x')
    submit = SubmitField('Clear')


class ProfileForm(FlaskForm):
    username = StringField('Update login username')
    password = PasswordField('Update Password', validators=[EqualTo('confirmPass', message='Passwords must match')])
    confirmPass = PasswordField('Confirm Password')
    picture = FileField('Update Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Update Account')


    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different name.')
'''
    def __init__(self, oldName, *args, **kwargs): #initializes current name to user
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.oldName = oldName
        '''
