from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin":
            return redirect('/dashboard')

    return render_template('login.html')



# Home Redirect
@app.route('/')
def home():
    return redirect('/login')



# Dashboard
@app.route('/dashboard')
def dashboard():

    total = Employee.query.count()

    departments = db.session.query(
        Employee.department
    ).distinct().count()

    new_employees = Employee.query.count()

    return render_template(
        "index.html",
        total=total,
        departments=departments,
        new_employees=new_employees
    )



# Add Employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():

    if request.method == 'POST':

        name = request.form['name']
        department = request.form['department']
        email = request.form['email']

        employee = Employee(
            name=name,
            department=department,
            email=email
        )

        db.session.add(employee)
        db.session.commit()

        return redirect('/view')

    return render_template("add_employee.html")



# View Employees
@app.route('/view')
def view_employee():

    employees = Employee.query.all()

    return render_template(
        "view_employee.html",
        employees=employees
    )



# Edit Employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):

    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':

        employee.name = request.form['name']
        employee.department = request.form['department']
        employee.email = request.form['email']

        db.session.commit()

        return redirect('/view')

    return render_template(
        'edit_employee.html',
        employee=employee
    )



# Delete Employee
@app.route('/delete/<int:id>')
def delete_employee(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)

    db.session.commit()

    return redirect('/view')



# Search Employee
@app.route('/search', methods=['GET', 'POST'])
def search():

    employees = []
    searched = False

    if request.method == 'POST':

        searched = True

        name = request.form['search']

        employees = Employee.query.filter(
            Employee.name.ilike(f"%{name}%")
        ).all()


    return render_template(
        "search_employee.html",
        employees=employees,
        searched=searched
    )



# Logout
@app.route('/logout')
def logout():

    return "<h2>You have logged out successfully!</h2>"



if __name__ == "__main__":
    app.run(debug=True)