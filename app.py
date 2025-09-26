from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo}-{self.title}"
    

@app.route("/", methods=['GET','POST'])
def hello_world():

    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["desc"]


        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
        #print(allTodo)
    return render_template("index.html",allTodo=allTodo)
    # return "<p>Hello Flas!</p>"

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>Products</p>"

@app.route("/update/<int:SNo>", methods=['GET','POST'])
def update(SNo):
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["desc"]
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(SNo=SNo).first()
    # db.session.delete(Todo)
    # db.session.commit()
    # print(Todo)
    return render_template("update.html",todo=todo)

@app.route("/delete/<int:SNo>")
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    print(todo)
    return redirect("/")
           
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the .db file
        print("Database created successfully!")
    app.run(debug=True)