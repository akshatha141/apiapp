from datetime import datetime
from os import name

from flask import (Flask, Request, jsonify, redirect, render_template, request,url_for)

                   
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query

app = Flask(__name__)  # creating the Flask class object
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test7.db'
db=SQLAlchemy(app)
ma=Marshmallow(app)

class TodoSchema(ma.Schema):
    class Meta:
        fields=('id','name','address','city','date_created')
        
todo_schema=TodoSchema()
todos_schema=TodoSchema(many='True')  
    
class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    address=db.Column(db.String(200),nullable=False)
    city=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
def __repr__(self):
    return f'<Task  {self.name}, {self.address}, {self.city} >'    
      
@app.route('/' , methods=['POST','GET'])  
def add_task():
    if request.method == 'POST':
        task_name = request.json['name']
        task_address = request.json['address']
        task_city = request.json['city']
       
        new_task =Todo(name=task_name, address = task_address,city = task_city)
              
        try:
            db.session.add(new_task)
            db.session.commit()
            return todo_schema.jsonify(new_task)
        except:
            return jsonify({'name':'Data not inserted into database'})
    else:
        tasks =Todo.query.all()        
        return todos_schema.jsonify(tasks)
            
@app.route('/<int:id>',methods=['GET'])
def get_task(id):
    task=Todo.query.get_or_404(id)
    return todo_schema.jsonify(task)

@app.route('/<int:id>',methods=['DELETE'])
def delete_task(id):
    delete_msg={"message":"The task is deleted Successfully"}
    task=Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(delete_msg)

@app.route('/<int:id>',methods=['PUT'])   
def update_task(id):
    task=Todo.query.get_or_404(id)
    
    task_name = request.json['name']
    task_address = request.json['address']
    task_city = request.json['city']

    task.name = task_name
    task.address = task_address
    task.city = task_city
    

    
    db.session.commit()
    return todo_schema.jsonify(task)

                                                     
if __name__ == '__main__':
    app.run(debug=True)
