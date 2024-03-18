from flask import Flask, render_template, request, redirect, url_for
import logging
app = Flask(__name__)

# Set the log level to DEBUG
app.logger.setLevel(logging.DEBUG)


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



@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            
            # Here you can process the form data as needed
            # For now, let's just print the data
            print(f"Name: {name}, Email: {email}, Message: {message}")
            
            # Optionally, you can redirect the user to a thank you page
            return redirect(url_for('thank_you_page'))
        
        except KeyError as e:
            # Handle missing form fields
            print(f"Error: Missing form field - {e}")
            return render_template('contact.html', error_message="Please fill out all the fields.")


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



if __name__ == '__main__':
    app.run(debug=True)

