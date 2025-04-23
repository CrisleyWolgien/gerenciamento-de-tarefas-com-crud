from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Inicializando o Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Definindo o modelo Task
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    description = db.Column(db.String(100), unique=True, nullable=False)  
    completed = db.Column(db.Boolean, default=False) 

#crud read
# Rota para a página inicial
@app.route("/")
def index():
    # Buscando as tarefas no banco de dados
    tasks = Tasks.query.all()  # Agora está acessando o banco de dados
    return render_template("index.html", tasks=tasks)

#crud Criar tarefa
@app.route("/create", methods=["POST"])
def create_task():
    description = request.form['description']

    #valida a tarefa
    existind_task = Tasks.query.filter_by(description = description). first()
    if existind_task:
        return "erro: task já existe", 400


    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


#crud delete
@app.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')
    
#crud update
@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        task.description = request.form['description']
        db.session.commit()
    return redirect('/')


#concluir tarefa
@app.route("/completed/<int:task_id>", methods=['POST'])
def completed_task(task_id):
    task = Tasks.query.get(task_id)
    if task:
        task.completed = 'completed' in request.form  # Checkbox marcado = True
        db.session.commit()
    return redirect('/')



# Rodando o app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas, se ainda não existirem
    app.run(debug=True)  # Modo de depuração ativado
