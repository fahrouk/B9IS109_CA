from flask import Flask, render_template, url_for, request, redirect, session, jsonify, make_response
import hashlib
import pdfkit
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

#define routes
# route fro the home page
@app.route('/')
def index():
    return render_template("index.html")

# Route to display login page
@app.route('/signin', methods=['GET'])
def login_page():
    return render_template('signin.html')


# Rouete to handle Login form submission
@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database for the user
        c.execute('SELECT * FROM users WHERE email=?', (email,))
        user = c.fetchone()
        
        # If user exists and password matches, redirect to dashboard page
        if user:
            # Validate password
            password_hashed = hashlib.sha256(password.encode()).hexdigest()
            if user[3] == password_hashed:
                # Store user session
                session['id'] = user[0]
                session['email'] = email
                session['compname'] = user[1]
                session['addr1'] = user[4]
                session['city'] = user[6]
                session['country'] = user[7]
                session['zipcode'] = user[8]

                return redirect(url_for('dashboard'))
            else:
                error = "Invalid username or password"
                return render_template('signin.html', error=error)
        else:
            error = "Invalid username or password"
            return render_template('signin.html', error=error)

    return render_template('signin.html')


# Route to display registration page
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


# Route to handle registration form submission
# Connect to the SQLite database

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        compname = request.form['compname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        addr1 = request.form['addr1']
        addr2 = request.form['addr2']
        city = request.form['city']
        country = request.form['country']
        zipcode = request.form['zipcode']

       

        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match"
            return render_template('signup.html', error=error)
        
        # Check if user already exists
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            error = "Email already exists"
            return render_template('signup.html', error=error)
        
        # Hash password
        password_hashed = hashlib.sha256(password.encode()).hexdigest()

        # Insert user into the database
        c.execute('INSERT INTO users (compname, email, password, addr1, addr2, city, country, zipcode) VALUES (?,?,?,?,?,?,?,?)', 
                  (compname, email, password_hashed, addr1, addr2, city, country, zipcode,))
        conn.commit()
        
        # Redirect to login page
        return redirect(url_for('signin'))
    
    return render_template('signup.html')

# route to the dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', email=session['email'], 
                               compname=session.get('compname'),
                               address=session.get('addr1'),
                               city=session.get('city'),
                               country=session.get('country'),
                               zipcode=session.get('zipcode'),
                               id =session.get('id'),
                               )
    
    else:
        return redirect(url_for('signin'))
    
# Route to handle the billing form submission
@app.route('/billing', methods=['POST'])
def billing():
    if request.method == 'POST':
        # Ensure user is logged in
        if 'email' not in session:
            return jsonify({'success': False, 'error': 'User is not logged in'})

        try:
            # Extract form data
            compname = request.form['compname']
            creators_email = session['email']  # Get the email from the session
            address = request.form['address']
            city = request.form['city']
            country = request.form['country']
            zipcode = request.form['zipcode']
            startdate = request.form['startdate']
            duedate = request.form['duedate']

            # Extract image and PDF data
            imageData = request.files['imageData'].read()
            pdfData = request.files['pdfData'].read()

            # Connect to the database
            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            # Insert form data and captured content into the database
            c.execute("INSERT INTO invoices (compname, creators_email, address, city, country, zipcode, startdate, duedate, image_data, pdf_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (compname, creators_email, address, city, country, zipcode, startdate, duedate, imageData, pdfData))
            
            # Commit changes and close connection
            conn.commit()
            conn.close()

            # Return success message
            return jsonify({'success': True, 'message': 'File has been created successfully'})

        except Exception as e:
            # Log the exception for debugging
            print("An error occurred:", str(e))
            # Return error message
            return jsonify({'success': False, 'error': 'An error occurred while processing the request'})

    return jsonify({'success': False, 'error': 'Method not allowed'})
    
# Route for the confirmation page
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Define route to fetch invoice data
@app.route('/myfiles')
def myfiles():
    if 'email' in session:
        # Connect to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Query the invoice table to fetch data
        c.execute("SELECT compname,startdate,duedate,image_data FROM invoices WHERE creators_email=?", (session['email'],))
        data = c.fetchall()

        # Close the database connection
        conn.close()

        # Return JSON response
        return jsonify(data)

    return 'Unauthorized', 401

    
# route to logout  
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(debug=True)
