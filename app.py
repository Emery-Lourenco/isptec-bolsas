from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURAÇÃO DA BASE DE DADOS POSTGRESQL
# Substitui 'postgres', 'tua_senha' e 'db_bolsas_isptec' pelos teus dados reais do PostgreSQL!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/db_bolsas_isptec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO DA TABELA DE BOLSAS (Para testar a ligação)
class Bolsa(db.Model):
    __tablename__ = 'bolsas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

# ROTA PRINCIPAL: Mostra as bolsas e o chat básico
@app.route('/')
def index():
    # Vai buscar todas as bolsas à base de dados PostgreSQL
    bolsas_listadas = Bolsa.query.all()
    return render_template('index.html', bolsas=bolsas_listadas)

# ROTA PARA ADICIONAR UMA BOLSA (Teste do Admin)
@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    
    nova_bolsa = Bolsa(titulo=titulo, descricao=descricao)
    db.session.add(nova_bolsa)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas automaticamente se não existirem
    app.run(debug=True)