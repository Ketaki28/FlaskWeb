from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#dburi = 'sqlite:///' + os.path.join(basedir, 'data/app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.sqlite3'
app.config['SECRET_KEY'] = "random string"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    emp_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))

    def __init__(self, emp_id,name, email, password):
        self.emp_id=emp_id
        self.name = name
        self.email = email
        self.password = password

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    try:
        if request.method == 'POST':
            if not request.form['emp_id'] or not request.form['name'] or not request.form['email'] or not request.form['password']:
                flash('Please enter all the fields', 'error')
            else:
                if request.form['password'] == request.form['password_confirm']:
                    emp = Employee(request.form['emp_id'], request.form['name'], request.form['email'], request.form['password'])
                    db.session.add(emp)
                    db.session.commit()
                    flash('Record was successfully added')
                else:
                    flash('Password Mismatch!!')
    except BaseException as e:
            print(e)

    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            if not request.form['emp_id'] or not request.form['password']:
                flash('Please enter all the fields', 'error')
            else:
                emp_id= request.form['emp_id']
                emp = Employee.query.filter_by(emp_id=emp_id).first()
                if request.form['password'] == emp.password:
                    flash('Login Successful')
                    return render_template('home.html')
                else:
                    flash('Emaployee id or password mismatch')

    except BaseException as e:
            print(e)

    return render_template('login.html')




@app.route('/vote')
def vote():
    return render_template('vote.html')


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)






