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

# MySQL configurations
mysql_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'root',  # Change this to your MySQL username
    'password': 'root',  # Change this to your MySQL password
    'database': 'rents'  # Change this to your MySQL database name
}

# SQLAlchemy database setup
engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(**mysql_config))
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


# Create the table in the database
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

carousel_images = [
    'https://is1-2.housingcdn.com/01c16c28/169120c556b55c17c2b73b9a755f5e74/v0/fs/3_bhk_independent_house-for-rent-haldia_riverside_estates_limited-Purba+Medinipur-bedroom.jpg',
    'https://cf.bstatic.com/xdata/images/hotel/max1024x768/496372177.jpg?k=cf4427eaf1ea929a679d29f61b892eef2e3e55ed5ff8fed3cd1ef6ca0c6bb90b&o=&hp=1',
    'https://cf.bstatic.com/xdata/images/hotel/max1024x768/472220329.jpg?k=f527727b1826834f9c66ae9bd3176ea7a67ca9cd7a32aa1c944c924c3a387928&o=&hp=1'
]

card_data = [
    {
        'image': 'https://housing-images.n7net.in/01c16c28/0ba5768cba5bbb4608b1136d8bab700f/v0/fs-large/3_bhk_independent_house-for-rent-kshudiram_nagar-Purba+Medinipur-bedroom.jpg',
        'description': '2 BHK House for Rent in Gandhi Nagar, Haldia',
        'add_date': '12/01/2024',
        'owner_name': 'John Doe',
        'contact_number': '123-456-7890',
        'monthly_rent': 'Rs 1000',
        'residence_type': 'Apartment',
        'num_bathrooms': 2,
        'attached_kitchen': 'Yes',
        'shopping_mall': 'Nearby',
        'num_beds': 2,
        'transport_facility': 'Available',
        'medical_shops': 'Nearby',
        'num_food_mess': 1,
        'time_to_market': '10 minutes',
        'time_to_college': '15 minutes',
        'playground': 'Available'
    },
    {
        'image': 'https://img.staticmb.com/mbphoto/property/cropped_images/2022/Dec/27/Photo_h180_w240/64832959_1_hatsAppImage20221222at11.53.27AM_180_240.jpeg',
        'description': '4 BHK Residential House For Rent Azad Hind Nagar',
        'add_date': '16/12/2023',
        'owner_name': 'Jane Smith',
        'contact_number': '987-654-3210',
        'monthly_rent': 'Rs 1500',
        'residence_type': 'House',
        'num_bathrooms': 3,
        'attached_kitchen': 'Yes',
        'shopping_mall': 'Within 1 mile',
        'num_beds': 4,
        'transport_facility': 'Available',
        'medical_shops': 'Within 2 miles',
        'num_food_mess': 2,
        'time_to_market': '15 minutes',
        'time_to_college': '20 minutes',
        'playground': 'Not available'
    },
    {
        'image': 'https://imgcy.trivago.com/c_limit,d_dummy.jpeg,f_auto,h_600,q_auto,w_600//hotelier-images/b0/69/121fa46c21c2186c624bd39a95e68025dd3a3271354c147ac90100b9c0dd.jpeg',
        'description': '3 BHK House for Rent in Khudiram Nagar, Haldia',
        'add_date': '11/02/2024',
        'owner_name': 'Michael Johnson',
        'contact_number': '456-789-0123',
        'monthly_rent': 'Rs 1200',
        'residence_type': 'Villa',
        'num_bathrooms': 3,
        'attached_kitchen': 'Yes',
        'shopping_mall': 'Within 0.5 miles',
        'num_beds': 3,
        'transport_facility': 'Available',
        'medical_shops': 'Within 1 mile',
        'num_food_mess': 1,
        'time_to_market': '12 minutes',
        'time_to_college': '18 minutes',
        'playground': 'Available'
    }
]
houses = House.query.all()


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

@app.route('/add_house', methods=['GET', 'POST'])
def add_house():
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
            attached_kitchen=form.attached_kitchen.data,
            shopping_mall=form.shopping_mall.data,
            num_beds=form.num_beds.data,
            transport_facility=form.transport_facility.data,
            medical_shops=form.medical_shops.data,
            num_food_mess=form.num_food_mess.data,
            time_to_market=form.time_to_market.data,
            time_to_college=form.time_to_college.data,
            playground=form.playground.data
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_house)
        session.commit()
        session.close()
        return redirect(url_for('success'))
    return render_template('add_house.html', form=form)
@app.route('/success')
def success():
    return 'House added successfully!'


if __name__ == '__main__':
    app.run(debug=True)

