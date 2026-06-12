from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TODO.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

# Route: View all tasks & Main Form
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# Route: Add a new task
@app.route('/add', methods=['POST'])
def add():
    task_title = request.form.get('task')
    if task_title:
        new_task = Todo(title=task_title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Route: Handle updates
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task_to_update.title = request.form.get('task')
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "There was an error updating that task."
    else:
        return render_template('update.html', task=task_to_update)

# Route: Delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was an error deleting that task."

# Initialize database tables and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)