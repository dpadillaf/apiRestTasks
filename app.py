from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask( __name__ )

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
db = SQLAlchemy( app )

#Model Task
class Task(db.Model):
    id = db.Column( db.Integer, primary_key = True )
    content = db.Column( db.String( 200 ) )
    done = db.Column( db.Boolean )

#routes
@app.route( '/' )
def home():
    tasks = Task.query.all()
    return render_template( 'index.html', tasks = tasks )

@app.route( '/create-task', methods = ['POST'] )
def createTask():
    task = Task( content = request.form[ 'content' ], done = False )
    db.session.add( task )
    db.session.commit()
    return redirect( url_for( 'home' ) )

@app.route( '/done/<id>')
def doneTask( id ):
    task = Task.query.filter_by( id = int( id ) ).first()
    task.done = not( task.done )
    db.session.commit()
    return redirect( url_for( 'home' ) )

@app.route( '/delete/<id>')
def deleteTask( id ):
    task = Task.query.filter_by( id = int( id ) ).delete()
    db.session.commit()
    return redirect( url_for( 'home' ) )

if __name__ == '__main__':
    app.run( debug=True )