from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from sqlalchemy import create_engine, Column, String, Integer, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message
from smtplib import SMTPException
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length
import random

app = Flask(__name__)

# Open the file in read mode ('r')
with open(r'static/secretkey.txt', 'r') as file:
    # Read the entire content of the file
    content = file.read()

    app.secret_key = content # Add A secret Key Here

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
app.config['MAIL_PORT'] = '465'  # or your mail server port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rentechspace@fastmail.com'
app.config['MAIL_PASSWORD'] = 'zkukp4r93fhxzfv6'
mail = Mail(app)


# mysql_config = {
#     'host': 'localhost',  # Change this to your MySQL host
#     'user': 'root',  # Change this to your MySQL username
#     'password': 'saif1234',  # Change this to your MySQL password
#     'database': 'rents'  # Change this to your MySQL database name
# }

# # SQLAlchemy database setup
# engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(**mysql_config))

# Postgresql configurations
postgresql_config = {
    'host': 'aws-0-ap-south-1.pooler.supabase.com',  # Change this to your MySQL host
    'port' : '5432',
    'user': 'postgres.innfpftleatzyutlxexe',  # Change this to your MySQL username
    'password': 'haldiarent123',  # Change this to your MySQL password
    'database': 'postgres'  # Change this to your MySQL database name
}

# SQLAlchemy database setup
engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(**postgresql_config))
Base = declarative_base()


# Define Admin model
class Admin_Table(Base):

    ''' 
    First insert the id, user name and password Manually on the data base to access the admin section.

    '''
    __tablename__ = 'Admin_table'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(60), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
# Define Contact model
class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)


# Define the House class
class House(Base):
    __tablename__ = 'houses'

    id = Column(String(10), primary_key=True) #ID Of each houses
    image = Column(String(255)) # Image link
    description = Column(Text) # Description of the house (It mainly containts the Address of the House)
    add_date = Column(Date) # When the house has been registered
    owner_name = Column(String(255)) # Name of the owner
    contact_number = Column(String(15)) # Contact Number  
    monthly_rent = Column(Integer) # Monthly Price of the rent 
    residence_type = Column(String(50)) # Type of room required eg., Single room, Sharing Room , flat etc
    num_bathrooms = Column(Integer) # Numbeer of bathroom
    attached_kitchen = Column(String(3)) # It is yes or no answer so we will save 1 or 0
    shopping_mall = Column(Integer) # It is yes or no answer so we will save 1 or 0
    num_beds = Column(Integer) # Number of besd in a room
    transport_facility = Column(Integer) # It is yes or no answer so we will save 1 or 0x
    medical_shops = Column(Integer) # It is yes or no answer so we will save 1 or 0
    num_food_mess = Column(Integer) # Number of Mess available nearby
    time_to_market = Column(Integer) # Time taken to reach market on foot 5, 10, 15, 20, ... minutes
    time_to_college = Column(Integer) # Time taken to reach College on foot 5, 10, 15, 20, ... minutes
    playground = Column(Integer)# It is yes or no answer so we will save 1 or 0

    def __repr__(self):
        return f'<House {self.id}>'
    
# Define the CarouselImage model
class CarouselImage(Base):
    __tablename__ = 'carousel'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))


# Create the table in the database
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

carousel_images = [
    'https://is1-2.housingcdn.com/01c16c28/169120c556b55c17c2b73b9a755f5e74/v0/fs/3_bhk_independent_house-for-rent-haldia_riverside_estates_limited-Purba+Medinipur-bedroom.jpg',
    'https://cf.bstatic.com/xdata/images/hotel/max1024x768/496372177.jpg?k=cf4427eaf1ea929a679d29f61b892eef2e3e55ed5ff8fed3cd1ef6ca0c6bb90b&o=&hp=1',
    'https://cf.bstatic.com/xdata/images/hotel/max1024x768/472220329.jpg?k=f527727b1826834f9c66ae9bd3176ea7a67ca9cd7a32aa1c944c924c3a387928&o=&hp=1'
]
def loadcarousel():
    try:
        # Query all rows from the CarouselImage table
        session_db = Session()
        queries = session_db.query(CarouselImage).all()
        session_db.close()
        carousel = queries
        # Convert the query result to a list of dictionaries
        carousel_data = [image.url for image in carousel]
        carousel_images.extend(carousel_data)
    except Exception as e:
        print(f"Error extracting data from the database: {e}")
loadcarousel()

card_data = []
def houseload():
    try:
        # Query all rows from the House table
        session_db = Session()
        queries = session_db.query(House).all()
        session_db.close()
        houses = queries
        # Convert the query result to the desired format
        formatted_data = [
            {
                'image': house.image,
                'description': house.description,
                'add_date': house.add_date,
                'owner_name': house.owner_name,
                'contact_number': house.contact_number,
                'monthly_rent': house.monthly_rent,
                'residence_type': house.residence_type,
                'num_bathrooms': house.num_bathrooms,
                'attached_kitchen': house.attached_kitchen,
                'shopping_mall': house.shopping_mall,
                'num_beds': house.num_beds,
                'transport_facility': house.transport_facility,
                'medical_shops': house.medical_shops,
                'num_food_mess': house.num_food_mess,
                'time_to_market': house.time_to_market,
                'time_to_college': house.time_to_college,
                'playground': house.playground
            }
            for house in houses
        ]
        if card_data:
            card_data.clear()
        card_data.extend(formatted_data)
    except Exception as e:
        print(f"Error extracting data from the database: {e}")

houseload()

class HouseForm(FlaskForm):
    image = StringField('Image Link', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])
    add_date = StringField('Registration Date', validators=[DataRequired()])
    owner_name = StringField('Owner Name', validators=[DataRequired(), Length(max=255)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=15)])
    monthly_rent = IntegerField('Monthly Rent', validators=[DataRequired(), NumberRange(min=0)])
    residence_type = SelectField('Residence Type', choices=[('Single Room', 'Single Room'), ('Sharing Room', 'Sharing Room'), ('Flat', 'Flat')], validators=[DataRequired()])
    num_bathrooms = IntegerField('Number of Bathrooms', validators=[DataRequired(), NumberRange(min=0)])
    attached_kitchen = BooleanField('Attached Kitchen')
    shopping_mall = BooleanField('Shopping Mall Nearby')
    num_beds = IntegerField('Number of Beds', validators=[DataRequired(), NumberRange(min=0)])
    transport_facility = BooleanField('Transport Facility Nearby')
    medical_shops = BooleanField('Medical Shops Nearby')
    num_food_mess = IntegerField('Number of Food Mess Nearby', validators=[DataRequired(), NumberRange(min=0)])
    time_to_market = IntegerField('Time to Reach Market (minutes)', validators=[DataRequired(), NumberRange(min=0)])
    time_to_college = IntegerField('Time to Reach College (minutes)', validators=[DataRequired(), NumberRange(min=0)])
    playground = BooleanField('Playground Nearby')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
           # Create a new Contact object
            contact = Contact(name=name, email=email, message=message)

            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Add the Contact object to the session
            session.add(contact)

            # Commit the session to save the data to the database
            session.commit()

            # Close the session
            session.close()

            # Optionally, you can redirect the user to a thank you page
            return render_template('thank_you.html')
        
        except KeyError as e:
            # Handle missing form fields
            print(f"Error: Missing form field - {e}")
            return render_template('contact.html', error_message="Please fill out all the fields.")


# Route for the admin page
@app.route('/admin')
def admin_page():
    # Query the database to retrieve submitted queries
    # Fetch contacts from the database
    if 'username' in session:
        session_db = Session()
        queries = session_db.query(Contact).all()
        session_db.close()
        return render_template('admin.html', queries=queries)
    else:
        return redirect(url_for('admin_login'))



@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session_db = Session()
        user = session_db.query(Admin_Table).filter_by(username=username).first()
        session_db.close()

        if user and user.password == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('admin_page'))
        else:
            return render_template('adminlogin.html', message='Invalid credentials')

    return render_template('adminlogin.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        try:
            data = request.json
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            print(f"name- {name} email- {email} message- {message}")

            # Send email
            msg = Message(subject='Reply to your query', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"Hello {name},\n\nThank you for your message. We have received your query. \
                \n\n{message}\n\nBest regards,\nAdmin"
            mail.send(msg)

            return jsonify({'success': True})

        except SMTPException as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return redirect(url_for('admin_login'))
    
@app.route('/add_image', methods=['POST'])
def add_image():
    if 'username' in session:
        image_url = request.form.get('imageUrl')
        if image_url:
            # Create a new Contact object
            input = CarouselImage(url=image_url)

            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Add the Contact object to the session
            session.add(input)

            # Commit the session to save the data to the database
            session.commit()

            # Close the session
            session.close()
            #carousel_images.append({'url': image_url})

            return jsonify({'message': 'Image added successfully'}), 200, loadcarousel()
        else:
            return jsonify({'error': 'No image URL provided'}), 400
    else:
        return redirect(url_for('admin_login'))

@app.route('/thank_you_page')
def thank_you_page():
    return render_template('thank_you.html')

@app.route('/')
def index():
    return render_template('index.html', cards=card_data, carousel_images=carousel_images)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Route to render the registration form
@app.route('/register', methods=['GET'])
def register():
    return render_template('userRegistration.html')

# Route to handle the registration form submission
@app.route('/register', methods=['POST'])
def register_user():
    # Retrieve form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Add your registration logic here (e.g., validate form inputs, save user to database, etc.)
    # Validate form inputs
    if password != confirm_password:
        return render_template('userRgistration.html', error_message='Passwords do not match')

    # Create a new user instance
    new_user = User(username=username, email=email, password=password)

    # Add the new user to the database
    
    #carousel_images.append({'url': image_url})
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        # Add the Contact object to the session
        session.add(new_user)

        # Commit the session to save the data to the database
        session.commit()

        # Close the session
        session.close()
        return redirect(url_for('registration_success'))
    except :
        session.rollback()
        return render_template('userRegistration.html', error_message='Username or email already exists')


# Route to render a success page after registration
@app.route('/registration-success', methods=['GET'])
def registration_success():
    return render_template('registration_success.html')


# This route handles the form submission for user login
@app.route('/login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)
        # Here you would perform authentication checks, such as querying the database
        # to verify the username and password
        # For this example, let's just check if the username and password are both 'admin'

        session_db = Session()
        user = session_db.query(User).filter_by(username=username).first()
        session_db.close()

        if user and user.password == password:
            # If authentication is successful, redirect to a success page
            session['username'] = username #Session is created for the user
            return redirect(url_for('user_account'))
        else:
            # If authentication fails, render the login page again with an error message
            return render_template('userlogin.html', error='Invalid username or password')
    return render_template('userlogin.html')

# Route for the user account page
@app.route('/user_account')
def user_account():
    if 'username' in session:
        # Query the user's houses from the database
        session_db = Session()
        user = session_db.query(User).filter_by(username=session['username']).first()
        user_houses = session_db.query(House).filter(House.owner_name == session['username']).all()
        session_db.close()
        return render_template('userAccount.html', cards=user_houses, user=user)
    else:
        return redirect(url_for('user_login'))

@app.route('/logout')
def user_logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))

# Route for adding a house (dummy route, you need to implement this)
@app.route('/add_house', methods=['GET', 'POST'])
def add_house():
    if 'username' in session:
        form = HouseForm()
        if form.validate_on_submit():
            new_house = House(
                id = random.randint(1,100),
                image=form.image.data,
                description=form.description.data,
                add_date=form.add_date.data,
                owner_name=form.owner_name.data,
                contact_number=form.contact_number.data,
                monthly_rent=form.monthly_rent.data,
                residence_type=form.residence_type.data,
                num_bathrooms=form.num_bathrooms.data,
                attached_kitchen=int(form.attached_kitchen.data),
                shopping_mall=int(form.shopping_mall.data),
                num_beds=form.num_beds.data,
                transport_facility=int(form.transport_facility.data),
                medical_shops=int(form.medical_shops.data),
                num_food_mess=form.num_food_mess.data,
                time_to_market=form.time_to_market.data,
                time_to_college=form.time_to_college.data,
                playground=int(form.playground.data)
            )
            Session_db = sessionmaker(bind=engine)
            session_db = Session()
            session_db.add(new_house)
            session_db.commit()
            session_db.close()
            return redirect(url_for('user_account')), houseload()
        return render_template('add_house.html', form=form)
    else:
        return redirect(url_for('user_login'))
@app.route('/success')
def success():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)

