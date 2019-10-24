import sqlalchemy as sqlalchemy
from flask  import Flask ,render_template ,request ,redirect,url_for
#render_template is used to sent html file in return.
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

##Database

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/sameer/PycharmProjects/TodoList/todo.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(200))
    complete=db.Column(db.Boolean)

#Route when nothing in the url

@app.route('/')
def index():
    incomplete=Todo.query.filter_by(complete=False).all()   #retreive all data from table where complete value is False.
    complete=Todo.query.filter_by(complete=True).all()
    return render_template('index.html',incomplete=incomplete,complete=complete)
#Flask will try to find the HTML file in the templates folder, in the same folder in which this script is present.

#https://realpython.com/primer-on-jinja-templating/


###Adding items
@app.route('/add',methods=['POST'])
def add():
    todo=Todo(text=request.form['todoitem'],complete=False)
    db.session.add(todo)  #insert a record to mapped table.
    db.session.commit()
#makes to stay on the home screen.
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
        todo=Todo.query.filter_by(id=int(id)).first()
        todo.complete=True
        db.session.commit()
        return redirect(url_for('index'))

if(__name__=='__main__'):
    app.run(ssl_context='adhoc')