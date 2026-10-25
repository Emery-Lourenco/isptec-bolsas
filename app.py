# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NECESSÁRIOS DO FLASK E SQLALCHEMY
# ==============================================================================
import importlib.util  # Permite verificar que bibliotecas (drivers) estão instaladas
import os  # Biblioteca nativa para ler variáveis de ambiente do sistema
import sys  # Permite ler os comandos escritos no terminal (ferramenta de contas)
from datetime import datetime, timezone, date, timedelta  # Registo de carimbos temporais
from functools import wraps  # Usado para criar o "guarda" que exige sessão iniciada
from dotenv import (
    load_dotenv,  # Carrega as configurações secretas do ficheiro .env
)
from flask import (
    Flask,  # O motor central que cria a aplicação web
    flash,  # Mensagens de alerta amigáveis no ecrã (sucesso, erro)
    jsonify,  # Converte dicionários Python em JSON para a API do Chatbot
    redirect,  # Função para redirecionar o utilizador para outra página
    render_template,  # Função que carrega o ficheiro HTML e injeta dados lá dentro
    request,  # Objeto que captura os dados enviados pelo formulário do browser
    session,  # Gestão da sessão de utilizadores logados
    url_for,  # Cria URLs automáticas baseadas no nome das funções Python
)

from flask_sqlalchemy import SQLAlchemy  # A ferramenta (ORM) que faz a ponte entre Python e o PostgreSQL
from sqlalchemy import func  # Funções SQL (lower/trim) para comparar e-mails sem diferenças de maiúsculas
from sqlalchemy.exc import IntegrityError  # Erro lançado quando a BD recusa um dado repetido (ex.: e-mail)
from werkzeug.security import (  # Utilitários nativos para senhas seguras (RNF04)
    check_password_hash,
    generate_password_hash,
)

# Carrega o ficheiro .env local antes de iniciar as configurações
load_dotenv()

# Constante de segurança que define o único e-mail autorizado a deter privilégios administrativos
EMAIL_ADMIN_OFICIAL = "admin@unibolsas.co.ao"

# ==============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO WEB
# ==============================================================================
app = Flask(__name__)


@app.after_request
def impedir_cache_de_paginas_de_sessao(resposta):
    """Evita que páginas autenticadas reapareçam pelo histórico após o logout."""
    resposta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private, max-age=0"
    resposta.headers["Pragma"] = "no-cache"
    resposta.headers["Expires"] = "0"
    return resposta

# CHAVE SECRETA DA SESSÃO:
# O Flask precisa de uma chave para encriptar os cookies de sessão no browser do utilizador.
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "chave_secreta_mvp_isptec_2026"
)

# ==============================================================================
# CONFIGURAÇÃO DA BASE DE DADOS (POSTGRESQL)
# ==============================================================================
# Lê a string de conexão remota definida no ficheiro .env para proteger as credenciais
def ler_url_da_base_de_dados():
    """Lê o DATABASE_URL do .env e corrige os erros mais comuns antes de ligar."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL não encontrada. Crie o ficheiro .env na raiz do projeto "
            "(ao lado do app.py) com a chave de ligação à base de dados."
        )
    # O SQLAlchemy só aceita "postgresql://"; algumas chaves vêm com "postgres://"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    # Versões novas do SQLAlchemy usam por defeito o driver "psycopg" e as antigas o "psycopg2".
    # Para funcionar com o que estiver instalado, indicamos o driver de forma explícita.
    if url.startswith("postgresql://"):
        if importlib.util.find_spec("psycopg2") is not None:
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        elif importlib.util.find_spec("psycopg") is not None:
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


app.config["SQLALCHEMY_DATABASE_URI"] = ler_url_da_base_de_dados()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Liga a extensão SQLAlchemy à nossa aplicação Flask
db = SQLAlchemy(app)


# ==============================================================================
# MODELO RELACIONAL (POSTGRESQL ORM NORMALIZADO - REQUISITOS DO MVP)
# ==============================================================================


# 1. TABELA DE UTILIZADORES (Atende UC01, UC02 / RF01, RF02, RNF04)
class Utilizador(db.Model):
    __tablename__ = "utilizadores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default="candidato")
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pedidos_contacto = db.relationship("PedidoContacto", backref="candidato", lazy=True)
    contratacoes = db.relationship("ContratacaoMentoria", backref="candidato", lazy=True)
    bolsas_guardadas = db.relationship("BolsaGuardada", backref="candidato", cascade="all, delete-orphan", lazy=True)

    def definir_senha(self, senha_limpa):
        self.senha_hash = generate_password_hash(senha_limpa)

    def verificar_senha(self, senha_limpa):
        return check_password_hash(self.senha_hash, senha_limpa)


# 2. TABELA DE BOLSAS (Atende UC03 a UC06 / RF03 a RF13)
class Bolsa(db.Model):
    __tablename__ = "bolsas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    entidade = db.Column(db.String(150), nullable=False, default="Entidade Oficial")
    pais_destino = db.Column(db.String(100), nullable=False, default="Angola")
    tipo = db.Column(db.String(20), nullable=False, default="externa")
    cobertura = db.Column(db.String(20), nullable=False, default="integral")
    custos_bolseiro = db.Column(db.Text, nullable=True)
    nivel_estudo = db.Column(db.String(50), nullable=True)
    area_estudo = db.Column(db.String(100), nullable=True)
    elegivel_angolanos = db.Column(db.Boolean, nullable=False, default=True)
    data_limite = db.Column(db.Date, nullable=True)
    link_oficial = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    beneficio_resumo = db.Column(db.String(150), nullable=True, default="Propinas integrais + subsídio")
    ativa = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    itens_cobertos = db.relationship("BolsaItemCoberto", backref="bolsa", cascade="all, delete-orphan", lazy=True)
    bolseiros = db.relationship("BolseiroVoluntario", backref="bolsa_rel", lazy=True)
    guardada_por = db.relationship("BolsaGuardada", backref="bolsa", cascade="all, delete-orphan", lazy=True)


# 3. TABELA ASSOCIATIVA NORMALIZADA DE ITENS COBERTOS (Atende RF10 - 1FN e 2FN)
class BolsaItemCoberto(db.Model):
    __tablename__ = "bolsa_itens_cobertos"

    id = db.Column(db.Integer, primary_key=True)
    bolsa_id = db.Column(db.Integer, db.ForeignKey("bolsas.id", ondelete="CASCADE"), nullable=False)
    item = db.Column(db.String(50), nullable=False)


# 4. TABELA DE BOLSEIROS VOLUNTÁRIOS (Atende UC07, UC09 / RF14, RF15, RNF06, RNF07)
class BolseiroVoluntario(db.Model):
    __tablename__ = "bolseiros_voluntarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    situacao = db.Column(db.String(50), nullable=False)
    bolsa_id = db.Column(db.Integer, db.ForeignKey("bolsas.id", ondelete="SET NULL"), nullable=True)
    bolsa_nome_externo = db.Column(db.String(150), nullable=True)
    pais = db.Column(db.String(100), nullable=False)
    universidade = db.Column(db.String(150), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.String(50), nullable=False)
    apresentacao = db.Column(db.Text, nullable=False)
    relato = db.Column(db.Text, nullable=False)
    email_privado = db.Column(db.String(120), nullable=False)
    verificado = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pedidos_contacto = db.relationship("PedidoContacto", backref="bolseiro", lazy=True)


# 5. TABELA DE INTERMEDIAÇÃO DE PEDIDOS DE CONTACTO (Atende UC08, UC10 / RF17, RF18, RNF06)
class PedidoContacto(db.Model):
    __tablename__ = "pedidos_contacto"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey("utilizadores.id", ondelete="CASCADE"), nullable=False)
    bolseiro_id = db.Column(db.Integer, db.ForeignKey("bolseiros_voluntarios.id", ondelete="CASCADE"), nullable=False)
    pergunta = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    data_pedido = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# 6. TABELA DO CATÁLOGO DE MENTORIAS (Atende UC11, UC13 / RF19, RF20)
class Mentoria(db.Model):
    __tablename__ = "mentorias"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    duracao = db.Column(db.String(50), nullable=False)
    preco_kz = db.Column(db.Numeric(10, 2), nullable=False)
    nome_mentor = db.Column(db.String(120), nullable=False, default="Equipa de Mentoria")
    ativa = db.Column(db.Boolean, nullable=False, default=True)

    contratacoes = db.relationship("ContratacaoMentoria", backref="mentoria", lazy=True)


# 7. TABELA DE CONTRATAÇÕES DE MENTORIA COM PAGAMENTO SIMULADO (Atende UC12, UC14 / RF21 a RF23)
class ContratacaoMentoria(db.Model):
    __tablename__ = "contratacoes_mentoria"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey("utilizadores.id", ondelete="CASCADE"), nullable=False)
    mentoria_id = db.Column(db.Integer, db.ForeignKey("mentorias.id", ondelete="CASCADE"), nullable=False)
    data_preferida = db.Column(db.String(100), nullable=False)
    status_pagamento = db.Column(db.String(20), nullable=False, default="Pendente")
    data_contratacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# 8. TABELA ASSOCIATIVA NORMALIZADA DE BOLSAS GUARDADAS / FAVORITAS (Atende RF11, UC06 - 1FN, 2FN e 3FN)
class BolsaGuardada(db.Model):
    __tablename__ = "bolsas_guardadas"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey("utilizadores.id", ondelete="CASCADE"), nullable=False)
    bolsa_id = db.Column(db.Integer, db.ForeignKey("bolsas.id", ondelete="CASCADE"), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint("candidato_id", "bolsa_id", name="uq_candidato_bolsa_guardada"),)


# ==============================================================================
# POVOAMENTO INICIAL DE DADOS DE TESTE (SEEDS)
# ==============================================================================
def criar_dados_iniciais():
    """Garante a existência de dados mínimos reais para demonstração do MVP."""
    try:
        # 1. Criar o Administrador Inicial único caso não exista
        admin_existente = Utilizador.query.filter_by(tipo="admin").first()
        if not admin_existente:
            novo_admin = Utilizador(
                nome="Admin",
                email=EMAIL_ADMIN_OFICIAL,
                tipo="admin"
            )
            novo_admin.definir_senha(os.getenv("ADMIN_SENHA", "1234"))  # pode mudar no .env
            db.session.add(novo_admin)
            db.session.commit()
            print(f"Conta de Administrador criada com sucesso ({EMAIL_ADMIN_OFICIAL})!")

        # 2. Criar bolseiros voluntários se a tabela estiver vazia
        if BolseiroVoluntario.query.count() == 0:
            bolseiros_iniciais = [
                BolseiroVoluntario(
                    nome="Domingas Neto",
                    situacao="Bolseira atual",
                    bolsa_nome_externo="Bolsa Governo de Portugal",
                    pais="Portugal",
                    universidade="Universidade de Lisboa",
                    curso="Mestrado em Engenharia Informática",
                    ano="2.º Ano",
                    apresentacao="Aluna bolseira com foco em tecnologias web e cloud.",
                    relato="O custo de vida exige organização, mas a adaptação é tranquila.",
                    email_privado="domingas.neto@exemplo.ao",
                    verificado=True,
                ),
                BolseiroVoluntario(
                    nome="Josenilson Luciano",
                    situacao="Antigo bolseiro",
                    bolsa_nome_externo="Bolsa Mérito INAGBE",
                    pais="Angola",
                    universidade="ISPTEC",
                    curso="Engenharia Informática",
                    ano="Licenciado",
                    apresentacao="Mentor especializado em equivalências e preparação de processos.",
                    relato="Manter a média acima de 15 valores foi fundamental para a atribuição.",
                    email_privado="josenilson.luciano@exemplo.ao",
                    verificado=True,
                ),
                BolseiroVoluntario(
                    nome="Emerson Lourenço",
                    situacao="Bolseiro atual",
                    bolsa_nome_externo="Programa Chevening",
                    pais="Reino Unido",
                    universidade="University of Oxford",
                    curso="Engenharia de Software",
                    ano="1.º Ano",
                    apresentacao="Mentor técnico para redação de cartas de motivação e testes de inglês.",
                    relato="A preparação da candidatura com 6 meses de antecedência fez toda a diferença.",
                    email_privado="emerson.lourenco@exemplo.ao",
                    verificado=True,
                ),
            ]
            db.session.bulk_save_objects(bolseiros_iniciais)
            db.session.commit()

        # 3. Criar catálogo de mentorias se estiver vazio
        if Mentoria.query.count() == 0:
            mentorias_iniciais = [
                Mentoria(
                    titulo="Revisão Completa de Carta de Motivação",
                    descricao="Análise linha a linha dos teus objetivos com sugestões práticas de melhoria.",
                    duracao="45 minutos",
                    preco_kz=15000.00,
                    nome_mentor="Eng. Emerson Lourenço",
                ),
                Mentoria(
                    titulo="Preparação de Documentação e Equivalências",
                    descricao="Orientação sobre autenticação no MIREX, Ministério e consulados para bolsas externas.",
                    duracao="1 hora",
                    preco_kz=20000.00,
                    nome_mentor="Dr. Josenilson Luciano",
                ),
            ]
            db.session.bulk_save_objects(mentorias_iniciais)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Aviso durante a inicialização de dados: {e}")


# ==============================================================================
# FUNÇÕES AUXILIARES DE SESSÃO E CONTROLO DE ACESSO
# ==============================================================================
def utilizador_atual():
    """Devolve o Utilizador que tem sessão iniciada, ou None se ninguém entrou."""
    utilizador_id = session.get("utilizador_id")
    if utilizador_id is None:
        return None
    return db.session.get(Utilizador, utilizador_id)


def buscar_utilizador_por_email(email):
    """Procura um utilizador pelo e-mail, ignorando maiúsculas/minúsculas e espaços."""
    email = (email or "").strip().lower()
    if not email:
        return None
    return Utilizador.query.filter(func.lower(func.trim(Utilizador.email)) == email).first()


def parece_hash(valor):
    """Diz se o texto guardado na coluna senha_hash já é uma senha encriptada (hash)."""
    return (valor or "").startswith(("scrypt:", "pbkdf2:", "$2a$", "$2b$", "$2y$", "$argon2"))


def senha_correta(utilizador, senha):
    """Confere a palavra-passe digitada com a guardada na base de dados."""
    try:
        if utilizador.verificar_senha(senha):
            return True
    except (ValueError, TypeError):
        pass
    if not parece_hash(utilizador.senha_hash) and utilizador.senha_hash == senha:
        utilizador.definir_senha(senha)
        db.session.commit()
        return True
    return False


def iniciar_sessao(utilizador):
    """Guarda na sessão os dados essenciais de quem acabou de entrar."""
    session.clear()
    session["utilizador_id"] = utilizador.id
    session["utilizador_nome"] = utilizador.nome
    session["utilizador_tipo"] = utilizador.tipo


def login_obrigatorio(funcao):
    """'Guarda' das páginas privadas: sem sessão iniciada, envia para o login."""
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if utilizador_atual() is None:
            session.clear()
            flash("Inicie sessão para continuar.", "warning")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return verificar


def admin_obrigatorio(funcao):
    """'Guarda' exclusivo do painel administrativo: só utilizadores admin entram."""
    @wraps(funcao)
    def verificar_admin(*args, **kwargs):
        utilizador = utilizador_atual()
        if utilizador is None:
            session.clear()
            flash("Inicie sessão como administrador para continuar.", "warning")
            return redirect(url_for("login"))
        if utilizador.tipo != "admin":
            flash("Acesso não autorizado: área reservada exclusivamente à administração.", "danger")
            return redirect(url_for("dashboard"))
        return funcao(*args, **kwargs)
    return verificar_admin


# ==============================================================================
# ROTAS E LÓGICA DE NEGÓCIO (ENDPOINTS)
# ==============================================================================


# ROTA 1: PÁGINA PRINCIPAL COM FILTROS DE PESQUISA (Atende UC03, UC07, UC11)
@app.route("/")
def index():
    termo_pesquisa = request.args.get("pesquisa", "").strip()
    filtro_pais = request.args.get("pais", "").strip()
    filtro_nivel = request.args.get("nivel", "").strip()

    query = Bolsa.query.filter_by(ativa=True, elegivel_angolanos=True)

    if termo_pesquisa:
        termo = f"%{termo_pesquisa}%"
        query = query.filter(
            (Bolsa.titulo.ilike(termo))
            | (Bolsa.descricao.ilike(termo))
            | (Bolsa.entidade.ilike(termo))
            | (Bolsa.area_estudo.ilike(termo))
        )

    if filtro_pais and filtro_pais != "Todos os Países":
        query = query.filter(Bolsa.pais_destino.ilike(filtro_pais))

    if filtro_nivel and filtro_nivel != "Todos os Níveis":
        query = query.filter(Bolsa.nivel_estudo.ilike(filtro_nivel))

    bolsas_disponiveis = query.order_by(Bolsa.id.desc()).all()
    bolseiros_destaque = BolseiroVoluntario.query.filter_by(verificado=True).limit(6).all()
    mentorias_catalogo = Mentoria.query.filter_by(ativa=True).all()

    return render_template(
        "index.html",
        bolsas=bolsas_disponiveis,
        bolseiros=bolseiros_destaque,
        mentorias=mentorias_catalogo,
        termo_pesquisa=termo_pesquisa,
        filtro_pais=filtro_pais,
        filtro_nivel=filtro_nivel,
    )


# ROTA 2: API DO CHATBOT REGRA/PALAVRAS-CHAVE (Atende UC15 / RF24, RF25)
@app.route("/api/chatbot", methods=["POST"])
def chatbot_responder():
    dados = request.get_json() or {}
    mensagem = dados.get("mensagem", "").strip().lower()

    if not mensagem:
        return jsonify({"resposta": "Por favor, escreve uma pergunta para que te possa ajudar."})

    if "integral" in mensagem or "100%" in mensagem or "comparticipada" in mensagem or "integrais" in mensagem:
        total_integrais = Bolsa.query.filter_by(ativa=True, cobertura="integral").count()
        return jsonify({
            "resposta": f"Atualmente temos {total_integrais} bolsa(s) 100% comparticipada(s) no portal. As bolsas integrais cobrem propinas e alojamento sem custos diretos para ti."
        })

    elif "mentoria" in mensagem or "preço" in mensagem or "custo" in mensagem or "valor" in mensagem:
        mentorias = Mentoria.query.filter_by(ativa=True).all()
        lista_mentorias = ", ".join([f"{m.titulo} ({int(m.preco_kz):,} Kz)".replace(",", ".") for m in mentorias])
        return jsonify({
            "resposta": f"Oferecemos mentorias pagas para apoiar a tua candidatura: {lista_mentorias}. Podes agendar na secção Mentorias."
        })

    elif "inagbe" in mensagem or "angola" in mensagem or "interna" in mensagem:
        total_internas = Bolsa.query.filter_by(ativa=True, tipo="interna").count()
        return jsonify({
            "resposta": f"Temos {total_internas} bolsa(s) internas em Angola. Podes consultar os requisitos e prazos diretamente no nosso catálogo com o filtro de país 'Angola'."
        })

    elif "documento" in mensagem or "requisito" in mensagem or "papel" in mensagem:
        return jsonify({
            "resposta": "Os documentos habituais incluem: Certificado de Habilitações autenticado, Cópia do BI, Carta de Motivação e Carta de Recomendação. Cada bolsa detalha os seus requisitos no respetivo cartão."
        })

    return jsonify({
        "resposta": "Sou o UniX! Podes perguntar-me sobre 'bolsas integrais', 'mentorias e preços', 'bolsas do INAGBE' ou 'documentos necessários'."
    })


# ROTA 3: CRIAÇÃO DE CONTA DE UTILIZADOR (Atende UC01 / RF01, RNF04)
@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():
    if utilizador_atual() is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha:
            flash("Por favor, preencha todos os campos obrigatórios.", "danger")
            return render_template("criar_conta.html")

        if len(senha) < 6:
            flash("A palavra-passe deve ter pelo menos 6 caracteres.", "danger")
            return render_template("criar_conta.html")

        if senha != confirmar_senha:
            flash("As palavras-passe introduzidas não coincidem.", "danger")
            return render_template("criar_conta.html")

        utilizador_existente = buscar_utilizador_por_email(email)
        if utilizador_existente:
            flash("Este e-mail já se encontra registado. Tente iniciar sessão.", "warning")
            return render_template("criar_conta.html")

        novo_candidato = Utilizador(
            nome=nome,
            email=email,
            tipo="candidato",
        )
        novo_candidato.definir_senha(senha)

        try:
            db.session.add(novo_candidato)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Este e-mail já se encontra registado. Tente iniciar sessão.", "warning")
            return render_template("criar_conta.html")

        iniciar_sessao(novo_candidato)
        flash(f"Conta criada com sucesso! Bem-vindo, {novo_candidato.nome}.", "success")
        return redirect(url_for("dashboard"))

    return render_template("criar_conta.html")


# ROTA 4: INÍCIO DE SESSÃO COM REDIRECIONAMENTO INTELIGENTE (Atende UC02 / RF02)
@app.route("/login", methods=["GET", "POST"])
def login():
    utilizador = utilizador_atual()
    if utilizador is not None:
        # Se for admin vai para o painel admin; se for candidato vai para o dashboard
        return redirect(url_for("dashboard_admin" if utilizador.tipo == "admin" else "dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Preencha o e-mail e a palavra-passe.", "danger")
            return render_template("login.html")

        utilizador = buscar_utilizador_por_email(email)
        if utilizador is None or not senha_correta(utilizador, senha):
            flash("E-mail ou palavra-passe incorretos.", "danger")
            return render_template("login.html")

        iniciar_sessao(utilizador)
        flash(f"Bem-vindo de volta, {utilizador.nome}!", "success")

        # Redireciona de acordo com o papel na base de dados
        if utilizador.tipo == "admin":
            return redirect(url_for("dashboard_admin"))
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ROTA 5: TERMINAR SESSÃO (Atende UC02 / RF02)
@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada com sucesso.", "info")
    return redirect(url_for("login"))


# ATALHOS PARA OS LINKS DO FRONT
@app.route("/index.html")
def atalho_index():
    return redirect(url_for("index"))


@app.route("/login.html")
def atalho_login():
    return redirect(url_for("login"))


@app.route("/criar_conta.html")
def atalho_criar_conta():
    return redirect(url_for("criar_conta"))


@app.route("/dashboard.html")
def atalho_dashboard():
    return redirect(url_for("dashboard"))


# ROTA 6: PAINEL EXCLUSIVO DO CANDIDATO (Atende UC14 / RF23)
@app.route("/dashboard")
@login_obrigatorio
def dashboard():
    utilizador = utilizador_atual()

    bolsas_disponiveis = Bolsa.query.filter_by(ativa=True).order_by(Bolsa.id.desc()).all()
    bolseiros_lista = BolseiroVoluntario.query.filter_by(verificado=True).all()
    mentorias_lista = Mentoria.query.filter_by(ativa=True).all()

    minhas_contratacoes = (
        ContratacaoMentoria.query.filter_by(candidato_id=utilizador.id)
        .order_by(ContratacaoMentoria.data_contratacao.desc())
        .all()
    )
    meus_pedidos = (
        PedidoContacto.query.filter_by(candidato_id=utilizador.id)
        .order_by(PedidoContacto.data_pedido.desc())
        .all()
    )

    registos_guardados = (
        BolsaGuardada.query.filter_by(candidato_id=utilizador.id)
        .order_by(BolsaGuardada.criado_em.desc())
        .all()
    )
    minhas_bolsas_guardadas = [registo.bolsa for registo in registos_guardados if registo.bolsa]
    ids_bolsas_guardadas = {registo.bolsa_id for registo in registos_guardados}

    return render_template(
        "dashboard_candidato.html",
        bolsas=bolsas_disponiveis,
        bolseiros=bolseiros_lista,
        mentorias=mentorias_lista,
        nome_candidato=utilizador.nome,
        minhas_contratacoes=minhas_contratacoes,
        meus_pedidos=meus_pedidos,
        minhas_bolsas_guardadas=minhas_bolsas_guardadas,
        ids_bolsas_guardadas=ids_bolsas_guardadas,
    )


# ROTA 7: GUARDAR OU REMOVER BOLSA DOS FAVORITOS (Atende UC06 / RF11)
@app.route("/guardar-bolsa/<int:bolsa_id>", methods=["POST"])
@login_obrigatorio
def guardar_bolsa(bolsa_id):
    utilizador = utilizador_atual()

    bolsa = db.session.get(Bolsa, bolsa_id)
    if bolsa is None or not bolsa.ativa:
        flash("Bolsa não encontrada ou inativa.", "danger")
        return redirect(url_for("dashboard"))

    guardada = BolsaGuardada.query.filter_by(candidato_id=utilizador.id, bolsa_id=bolsa.id).first()

    if guardada:
        db.session.delete(guardada)
        db.session.commit()
        flash(f'Bolsa "{bolsa.titulo}" removida dos teus favoritos.', "info")
    else:
        novo_favorito = BolsaGuardada(candidato_id=utilizador.id, bolsa_id=bolsa.id)
        db.session.add(novo_favorito)
        db.session.commit()
        flash(f'Bolsa "{bolsa.titulo}" guardada com sucesso nos teus favoritos!', "success")

    return redirect(url_for("dashboard") + "#guardadas")


# ROTA 8: PEDIR CONTACTO COM UM BOLSEIRO (Atende UC08 / RF17)
@app.route("/pedir-contacto/<int:bolseiro_id>", methods=["POST"])
@login_obrigatorio
def pedir_contacto(bolseiro_id):
    utilizador = utilizador_atual()

    bolseiro = db.session.get(BolseiroVoluntario, bolseiro_id)
    if bolseiro is None or not bolseiro.verificado:
        flash("Esse bolseiro não está disponível.", "danger")
        return redirect(url_for("dashboard"))

    pedido_pendente = PedidoContacto.query.filter_by(
        candidato_id=utilizador.id, bolseiro_id=bolseiro.id, status="Pendente"
    ).first()
    if pedido_pendente:
        flash(f"Já tem um pedido pendente para {bolseiro.nome}.", "warning")
        return redirect(url_for("dashboard") + "#bolseiros-comunidade")

    pergunta = request.form.get("pergunta", "").strip()
    if not pergunta:
        pergunta = "Gostaria de conversar sobre a minha candidatura."

    novo_pedido = PedidoContacto(
        candidato_id=utilizador.id,
        bolseiro_id=bolseiro.id,
        pergunta=pergunta,
    )
    db.session.add(novo_pedido)
    db.session.commit()

    flash(f"Pedido enviado! A equipa vai encaminhá-lo a {bolseiro.nome}.", "success")
    return redirect(url_for("dashboard") + "#bolseiros-comunidade")


# ROTA 9: CONTRATAR UMA MENTORIA (Atende UC12 / RF21)
@app.route("/contratar-mentoria/<int:mentoria_id>", methods=["POST"])
@login_obrigatorio
def contratar_mentoria(mentoria_id):
    utilizador = utilizador_atual()

    mentoria = db.session.get(Mentoria, mentoria_id)
    if mentoria is None or not mentoria.ativa:
        flash("Essa mentoria não está disponível.", "danger")
        return redirect(url_for("dashboard"))

    por_pagar = ContratacaoMentoria.query.filter_by(
        candidato_id=utilizador.id, mentoria_id=mentoria.id, status_pagamento="Pendente"
    ).first()
    if por_pagar:
        flash("Já solicitou esta mentoria e falta confirmar o pagamento.", "warning")
        return redirect(url_for("dashboard") + "#mentores-tecnicos")

    data_preferida = request.form.get("data_preferida", "").strip()
    if not data_preferida:
        data_preferida = "A combinar com o mentor"

    nova_contratacao = ContratacaoMentoria(
        candidato_id=utilizador.id,
        mentoria_id=mentoria.id,
        data_preferida=data_preferida,
    )
    db.session.add(nova_contratacao)
    db.session.commit()

    flash(f'Mentoria "{mentoria.titulo}" solicitada. Falta confirmar o pagamento.', "success")
    return redirect(url_for("dashboard") + "#mentores-tecnicos")


# ROTA 10: PAGAMENTO SIMULADO DA MENTORIA (Atende UC12 / RF22)
@app.route("/pagar-mentoria/<int:contratacao_id>", methods=["POST"])
@login_obrigatorio
def pagar_mentoria(contratacao_id):
    utilizador = utilizador_atual()

    contratacao = db.session.get(ContratacaoMentoria, contratacao_id)
    if contratacao is None or contratacao.candidato_id != utilizador.id:
        flash("Contratação não encontrada.", "danger")
        return redirect(url_for("dashboard"))

    if contratacao.status_pagamento == "Pago":
        flash("Esta mentoria já está paga.", "info")
    else:
        contratacao.status_pagamento = "Pago"
        db.session.commit()
        flash("Pagamento (simulado) confirmado com sucesso!", "success")

    return redirect(url_for("dashboard") + "#mentores-tecnicos")


# ==============================================================================
# ROTAS DO PAINEL DE ADMINISTRAÇÃO (Atende UC06, UC09, UC10, UC13 | RF08 a RF14)
# ==============================================================================


# ROTA 11: PAINEL ADMINISTRATIVO GERAL
@app.route("/admin")
@admin_obrigatorio
def dashboard_admin():
    # 1. Estatísticas em tempo real calculadas no PostgreSQL
    total_bolsas_ativas = Bolsa.query.filter_by(ativa=True).count()
    total_mentores = Mentoria.query.filter_by(ativa=True).count()
    total_candidatos = Utilizador.query.filter_by(tipo="candidato").count()

    # Bolsas a expirar nos próximos 15 dias
    hoje = date.today()
    limite_expiracao = hoje + timedelta(days=15)
    bolsas_a_expirar = Bolsa.query.filter(
        Bolsa.ativa == True,
        Bolsa.data_limite != None,
        Bolsa.data_limite >= hoje,
        Bolsa.data_limite <= limite_expiracao
    ).count()

    # 2. Listagens completas para gestão
    todas_as_bolsas = Bolsa.query.order_by(Bolsa.id.desc()).all()
    todos_os_bolseiros = BolseiroVoluntario.query.order_by(BolseiroVoluntario.id.desc()).all()
    todas_as_mentorias = Mentoria.query.order_by(Mentoria.id.desc()).all()
    pedidos_contacto_pendentes = PedidoContacto.query.order_by(PedidoContacto.data_pedido.desc()).all()

    return render_template(
        "dashbord_admin.html",
        total_bolsas=total_bolsas_ativas,
        bolsas_expirar=bolsas_a_expirar,
        total_mentores=total_mentores,
        total_candidatos=total_candidatos,
        bolsas=todas_as_bolsas,
        bolseiros=todos_os_bolseiros,
        mentorias=todas_as_mentorias,
        pedidos=pedidos_contacto_pendentes,
    )


# ROTA 12: CADASTRAR NOVA BOLSA (Atende UC06 / RF08, RF09, RF10)
@app.route("/admin/cadastrar-bolsa", methods=["POST"])
@admin_obrigatorio
def admin_cadastrar_bolsa():
    titulo = request.form.get("titulo", "").strip()
    entidade = request.form.get("entidade", "").strip()
    pais_destino = request.form.get("pais_destino", "").strip()
    area_estudo = request.form.get("area_estudo", "").strip()
    nivel_estudo = request.form.get("nivel_estudo", "").strip()
    cobertura = request.form.get("cobertura", "integral").strip()
    data_limite_str = request.form.get("data_limite", "").strip()
    link_oficial = request.form.get("link_oficial", "").strip()
    beneficio_resumo = request.form.get("beneficio_resumo", "").strip()
    descricao = request.form.get("descricao", "").strip()

    data_limite = None
    if data_limite_str:
        try:
            data_limite = datetime.strptime(data_limite_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    nova_bolsa = Bolsa(
        titulo=titulo,
        entidade=entidade or "Entidade Oficial",
        pais_destino=pais_destino or "Angola",
        tipo="interna" if pais_destino.lower() == "angola" else "externa",
        cobertura=cobertura,
        area_estudo=area_estudo,
        nivel_estudo=nivel_estudo,
        data_limite=data_limite,
        link_oficial=link_oficial or "https://inagbe.gov.ao/#/home",
        beneficio_resumo=beneficio_resumo or "Propinas integrais + subsídio",
        descricao=descricao,
        elegivel_angolanos=True,
        ativa=True
    )
    db.session.add(nova_bolsa)
    db.session.commit()

    flash(f'Bolsa "{titulo}" cadastrada e publicada com sucesso!', "success")
    return redirect(url_for("dashboard_admin"))


# ROTA 13: ELIMINAR OU DESATIVAR BOLSA (Atende UC06 / RF08)
@app.route("/admin/eliminar-bolsa/<int:bolsa_id>", methods=["POST"])
@admin_obrigatorio
def admin_eliminar_bolsa(bolsa_id):
    bolsa = db.session.get(Bolsa, bolsa_id)
    if bolsa:
        db.session.delete(bolsa)
        db.session.commit()
        flash(f'Bolsa "{bolsa.titulo}" eliminada com sucesso da plataforma.', "info")
    else:
        flash("Bolsa não encontrada.", "danger")
    return redirect(url_for("dashboard_admin"))


# ==============================================================================
# FERRAMENTA DE CONTAS (terminal): VER e ARRANJAR contas na base de dados
# ==============================================================================
AJUDA_CONTAS = """Comandos disponíveis:
  python app.py contas listar
  python app.py contas testar EMAIL SENHA
  python app.py contas definir EMAIL SENHA [--nome "Nome"]"""


def estado_da_senha(utilizador):
    """Descreve em palavras o formato da senha guardada (sem a mostrar)."""
    valor = utilizador.senha_hash or ""
    if valor.startswith(("scrypt:", "pbkdf2:")):
        return "senha encriptada (hash do Flask) - OK"
    if parece_hash(valor):
        return "hash de OUTRO tipo (não reconhecido) - use o comando 'definir'"
    return "senha em TEXTO SIMPLES - converte-se no 1.º login, ou use 'definir'"


def listar_contas():
    utilizadores = Utilizador.query.order_by(Utilizador.id).all()
    if not utilizadores:
        print("Não há nenhuma conta na base de dados.")
        return
    print("%-4s %-34s %-22s %-10s %s" % ("ID", "E-MAIL", "NOME", "TIPO", "SENHA"))
    for u in utilizadores:
        print("%-4s %-34s %-22s %-10s %s" % (u.id, u.email, u.nome[:22], u.tipo, estado_da_senha(u)))
    print("\nTotal: %d conta(s)." % len(utilizadores))


def testar_login(email, senha):
    utilizador = buscar_utilizador_por_email(email)
    if utilizador is None:
        print("NÃO ENTRARIA: não existe nenhuma conta com o e-mail '%s'." % email.strip())
        parte_inicial = email.split("@")[0].strip().lower()
        parecidos = [u.email for u in Utilizador.query.all() if parte_inicial in u.email.lower()]
        if parecidos:
            print("E-mails parecidos na base de dados: " + ", ".join(parecidos))
        print("Dica: use 'listar' para ver os e-mails existentes, ou 'definir' para criar/arranjar a conta.")
        return
    valor = utilizador.senha_hash or ""
    try:
        certa = utilizador.verificar_senha(senha)
    except (ValueError, TypeError):
        certa = False
    if not certa and not parece_hash(valor) and valor == senha:
        certa = True
    if certa:
        print("ENTRARIA: conta '%s' (%s), tipo %s. Senha: %s." % (utilizador.email, utilizador.nome, utilizador.tipo, estado_da_senha(utilizador)))
    else:
        print("NÃO ENTRARIA: a conta '%s' existe, mas a senha não corresponde." % utilizador.email)
        print("Estado da senha guardada: " + estado_da_senha(utilizador))
        print("Dica: use 'definir' para guardar a senha certa.")


def definir_conta(email, senha, nome=None):
    email = email.strip().lower()
    if len(senha) < 4:
        print("A senha é demasiado curta.")
        return

    utilizador = buscar_utilizador_por_email(email)
    tipo_atribuido = "admin" if email == EMAIL_ADMIN_OFICIAL else "candidato"

    if utilizador is None:
        utilizador = Utilizador(
            nome=nome or email.split("@")[0], 
            email=email, 
            tipo=tipo_atribuido
        )
        db.session.add(utilizador)
        acao = "CRIADA"
    else:
        if nome:
            utilizador.nome = nome
        if utilizador.email != EMAIL_ADMIN_OFICIAL:
            utilizador.tipo = "candidato"
        acao = "ATUALIZADA"

    utilizador.email = email
    utilizador.definir_senha(senha)
    db.session.commit()
    print("Conta %s: %s (%s), tipo %s. Já pode entrar com esta senha." % (acao, utilizador.email, utilizador.nome, utilizador.tipo))


def valor_da_opcao(args, nome_opcao):
    """Devolve o valor escrito a seguir a uma opção (ex.: --nome "Ana"), ou None."""
    if nome_opcao in args:
        posicao = args.index(nome_opcao)
        if posicao + 1 < len(args):
            return args[posicao + 1]
    return None


def executar_comando_contas(args):
    """Lê o comando escrito no terminal (listar/testar/definir) e executa-o."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    comando = args[0] if args else ""
    try:
        with app.app_context():
            if comando == "listar":
                listar_contas()
            elif comando == "testar" and len(args) >= 3:
                testar_login(args[1], args[2])
            elif comando == "definir" and len(args) >= 3:
                definir_conta(args[1], args[2], valor_da_opcao(args, "--nome"))
            else:
                print(AJUDA_CONTAS)
    except Exception as erro:
        print("Não foi possível conectar com a base de dados: %s" % erro)


# ==============================================================================
# BLOCO DE EXECUÇÃO LOCAL E CRIAÇÃO DAS TABELAS
# ==============================================================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "contas":
        executar_comando_contas(sys.argv[2:])
        sys.exit(0)

    with app.app_context():
        print("A sincronizar modelos normalizados com a nuvem (Neon)...")
        db.create_all()
        criar_dados_iniciais()
        print("Base de dados sincronizada e povoada com sucesso!")

    app.run(debug=True)