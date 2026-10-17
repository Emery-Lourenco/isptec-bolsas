# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NECESSÁRIOS DO FLASK E SQLALCHEMY
# ==============================================================================
import os  # Biblioteca nativa para ler variáveis de ambiente do sistema
from dotenv import (
    load_dotenv,  # Carrega as configurações secretas do ficheiro .env
)
from flask import (
    Flask,  # O motor central que cria a aplicação web
    redirect,  # Função para redirecionar o utilizador para outra página
    render_template,  # Função que carrega o ficheiro HTML e injeta dados lá dentro
    request,  # Objeto que captura os dados enviados pelo formulário do browser
    url_for,  # Cria URLs automáticas baseadas no nome das funções Python
)
from flask_sqlalchemy import (
    SQLAlchemy,  # A ferramenta (ORM) que faz a ponte entre Python e o PostgreSQL
)

# Carrega o ficheiro .env local antes de iniciar as configurações
load_dotenv()

# ==============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO WEB
# ==============================================================================
# Cria a instância principal da aplicação Flask
app = Flask(__name__)

# ==============================================================================
# CONFIGURAÇÃO DA BASE DE DADOS (POSTGRESQL)
# ==============================================================================
# Lê a string de conexão remota definida no ficheiro .env para proteger as credenciais
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# Desativa alertas desnecessários de modificação de objetos para poupar memória RAM
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Liga a extensão SQLAlchemy à nossa aplicação Flask
db = SQLAlchemy(app)


# ==============================================================================
# MODELO RELACIONAL (TABELA NO POSTGRESQL REPRESENTADA EM CLASSE PYTHON)
# ==============================================================================
class Bolsa(db.Model):
  # Define o nome exato da tabela no PostgreSQL
  __tablename__ = "bolsas"

  # Coluna 'id': Chave Primária (PK), número inteiro que cresce sozinho (auto-increment)
  id = db.Column(db.Integer, primary_key=True)

  # Coluna 'titulo': Texto de até 150 caracteres, campo obrigatório (nullable=False)
  titulo = db.Column(db.String(150), nullable=False)

  # Coluna 'descricao': Texto longo para colocar critérios, prazos e requisitos
  descricao = db.Column(db.Text, nullable=False)


# ==============================================================================
# ROTAS E LÓGICA DE NEGÓCIO (ENDPOINTS)
# ==============================================================================


# ROTA 1: PÁGINA PRINCIPAL (Consulta e visualização)
# Quando o utilizador acede ao endereço "/" via método GET (leitura padrão)
@app.route("/")
def index():
  # 1. Faz uma query ao PostgreSQL equivalente a: SELECT * FROM bolsas;
  todas_as_bolsas = Bolsa.query.all()

  # 2. Carrega o ficheiro 'index.html' e envia a variável 'bolsas' com os dados da BD
  return render_template("index.html", bolsas=todas_as_bolsas)


# ROTA 2: PROCESSAMENTO DO FORMULÁRIO DO ADMIN (Criação de novos registos)
# Esta rota só aceita requisições do tipo POST (quando dados são enviados)
@app.route("/adicionar", methods=["POST"])
def adicionar():
  # 1. Extrai os valores escritos nos campos do formulário através do atributo name=""
  titulo_vindo_do_html = request.form.get("titulo")
  descricao_vinda_do_html = request.form.get("descricao")

  # 2. Cria um novo objeto da classe Bolsa com os dados capturados
  nova_bolsa = Bolsa(
      titulo=titulo_vindo_do_html, descricao=descricao_vinda_do_html
  )

  # 3. Adiciona o objeto à sessão atual da base de dados (preparação)
  db.session.add(nova_bolsa)

  # 4. Confirma a transação, executando o INSERT INTO no PostgreSQL
  db.session.commit()

  # 5. Após gravar, redireciona o navegador de volta para a rota 'index'
  return redirect(url_for("index"))


# ==============================================================================
# BLOCO DE EXECUÇÃO LOCAL DO SERVIDOR
# ==============================================================================
if __name__ == "__main__":
  # O bloco 'with app.app_context()' garante acesso às configurações da aplicação
  with app.app_context():
    # Cria automaticamente as tabelas no PostgreSQL caso elas ainda não existam
    db.create_all()

  # Inicia o servidor local com o modo de depuração ativado (recarrega ao salvar)
  app.run(debug=True)