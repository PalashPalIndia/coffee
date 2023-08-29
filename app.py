from flask import Flask, render_template, request, redirect, url_for

from flask_mysqldb import MySQL
app= Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="1234"
app.config['MYSQL_DB']="carbon_collect"

mysql=MySQL(app)



'''@app.route('/')
def hello_world():
    return '<h1> Hello World! </h1>' '''

@app.route('/')
def home_page():
    return render_template('home.html')
    #return '<h1> Home page</h1>'

@app.route('/about/<username>')
def about(username):
    return f'<h1> About Page of {username}</h1>'


@app.route('/contact-us')
def contact():
    return '<h1> Contact Us page </h1>'

@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method=="POST":
        fname=request.form["fname"]
        lname=request.form["lname"]
        village=request.form["village"]
        zip=request.form["zip"]
        phone=request.form["phone"]
        password=request.form["pwd"]
 
        
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(first_name,last_name,village,zip_code,mobile_no,passwd) VALUES (%s,%s,%s,%s,%s,%s)",(fname,lname,village,zip,phone,password))

        mysql.connection.commit()

        cur.close()

        return "you have successfuly registered!!"


        #print(phone)
        #return redirect(url_for("about", username=phone))
    else:
        return render_template('registration.html')

@app.route('/welcome')
def welcome():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data =cur.fetchall()
    
    cur.close()
    
    return render_template('welcome.html', users=data)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method=="POST":
        phone=request.form["phone"]
        password=request.form["pwd"]
 
        
        cur = mysql.connection.cursor()

        #cur.execute("SELECT * FROM users where mobile_no = %s",phone)
        #data =cur.fetchall()
        query = f"SELECT * FROM users WHERE mobile_no = %s"
        data=cur.execute(query, (phone,))
        

        cur.close()

        return render_template('welcome.html', users=data)


        #print(phone)
        #return redirect(url_for("about", username=phone))
    else:
        return render_template('login.html')
    

if __name__=="__main__":
    app.run(debug=True)


