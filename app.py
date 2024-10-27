#pip install flask
#flask autosaves its features -- importance
#static and templates are the standard directories used
#ender_template: used to render html
#bootstrap.com has precoded html which we can use
#use db in flask -- pip install flask-sqlalchemy
#from app import db, app -- to create db
#>>> app.app_context().push()
#>>> db.create_all() 
#sqlite viewer can be used to look at the size of db
#allTodo=Todo.query.all() print(allTodo) --to get alltodos
#jinja2-templating engine in flask
#deploying app on heroku
#pip install gunicorn , pip freeze > requirements.txt , create a file Procfile(used by heroku for deployment)
#on vscode terminal heroku, heroku login
#git init, git add .,git commit -m "Initial commit"
#heroku create todolist-devakrishnasj

from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    #repr method showcases what we need to see

    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello():
    if request.method=='POST':
        title=request.form.get('title')
        desc=request.form.get('desc')                      
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
    #to display all the todos in index.html
    # return "Helloworld"

#can create multiple endpoints
@app.route('/show')
def product():
    allTodo=Todo.query.all()
    print(allTodo)
    return "this is products"

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=request.form.get('title')
        desc=request.form.get('desc')                      
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")


    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

#takes in integer serial no
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

#to run the app and check whether there is any error

if __name__=="__main__":
    app.run(debug=True)
    # app.run(debug=True,port=8000) --to change port
    #debug =True is kept during development to see your errors when deployed make debug=False
