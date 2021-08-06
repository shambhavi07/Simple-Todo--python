
# Importing Flask as web framework 
# Importing SQLAlchemy to store the data
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
db.create_all()

# url routes to the associated function to perform specified tasks
# URL route for the index page
@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list = todo_list)

# URL route when something is added to the todolist
@app.route("/add", methods= ["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

# URL route when some note is upadted (complete or not completed) on the todolist
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo= Todo.query.filter_by(id= todo_id).first()
    todo.complete= not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

# URL route when a note is deleted
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo= Todo.query.filter_by(id= todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "_main_":
    
    app.run(debug=True)
