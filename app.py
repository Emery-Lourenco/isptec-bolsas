# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NECESSÁRIOS DO FLASK E SQLALCHEMY
# ==============================================================================
import importlib.util  # Permite verificar que bibliotecas (drivers) estão instaladas
import os  # Biblioteca nativa para ler variáveis de ambiente do sistema
import sys  # Permite ler os comandos escritos no terminal (ferramenta de contas)
from datetime import datetime, timezone  # Registo de carimbos temporais
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
<<<<<<< HEAD
from sqlalchemy import func  # Funções SQL (lower/trim) para comparar e-mails sem diferenças de maiúsculas
from sqlalchemy.exc import IntegrityError  # Erro lançado quando a BD recusa um dado repetido (ex.: e-mail)
=======
>>>>>>> origin/main
from werkzeug.security import (  # Utilitários nativos para senhas seguras (RNF04)
    check_password_hash,
    generate_password_hash,
)

# Carrega o ficheiro .env local antes de iniciar as configurações
load_dotenv()

<<<<<<< HEAD
# Constante de segurança que define o único e-mail autorizado a deter privilégios administrativos
EMAIL_ADMIN_OFICIAL = "admin@unibolsas.co.ao"

=======
>>>>>>> origin/main
# ==============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO WEB
# ==============================================================================
app = Flask(__name__)

<<<<<<< HEAD

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

=======
# CHAVE SECRETA DA SESSÃO:
# O Flask precisa de uma chave para encriptar os cookies de sessão no browser do utilizador.
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "chave_secreta_mvp_isptec_2026"
)

>>>>>>> origin/main
# ==============================================================================
# CONFIGURAÇÃO DA BASE DE DADOS (POSTGRESQL)
# ==============================================================================
# Lê a string de conexão remota definida no ficheiro .env para proteger as credenciais
<<<<<<< HEAD
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
=======
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
>>>>>>> origin/main
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
<<<<<<< HEAD
    bolsas_guardadas = db.relationship("BolsaGuardada", backref="candidato", cascade="all, delete-orphan", lazy=True)
=======
>>>>>>> origin/main

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
<<<<<<< HEAD
    guardada_por = db.relationship("BolsaGuardada", backref="bolsa", cascade="all, delete-orphan", lazy=True)
=======
>>>>>>> origin/main


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


<<<<<<< HEAD
# 8. TABELA ASSOCIATIVA NORMALIZADA DE BOLSAS GUARDADAS / FAVORITAS (Atende RF11, UC06 - 1FN, 2FN e 3FN)
class BolsaGuardada(db.Model):
    __tablename__ = "bolsas_guardadas"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey("utilizadores.id", ondelete="CASCADE"), nullable=False)
    bolsa_id = db.Column(db.Integer, db.ForeignKey("bolsas.id", ondelete="CASCADE"), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Restrição de unicidade para evitar guardar a mesma bolsa repetidamente pelo mesmo utilizador
    __table_args__ = (db.UniqueConstraint("candidato_id", "bolsa_id", name="uq_candidato_bolsa_guardada"),)


=======
>>>>>>> origin/main
# ==============================================================================
# POVOAMENTO INICIAL DE DADOS DE TESTE (SEEDS)
# ==============================================================================
def criar_dados_iniciais():
    """Garante a existência de dados mínimos reais para demonstração do MVP."""
    try:
<<<<<<< HEAD
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
=======
        # Criar bolseiros voluntários se a tabela estiver vazia
>>>>>>> origin/main
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

<<<<<<< HEAD
        # 3. Criar catálogo de mentorias se estiver vazio
=======
        # Criar catálogo de mentorias se estiver vazio
>>>>>>> origin/main
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
<<<<<<< HEAD
# FUNÇÕES AUXILIARES DE SESSÃO (pequenas e reutilizadas por várias rotas)
# ==============================================================================
def utilizador_atual():
    """Devolve o Utilizador que tem sessão iniciada, ou None se ninguém entrou."""
    utilizador_id = session.get("utilizador_id")
    if utilizador_id is None:
        return None
    # Vai à base de dados confirmar que a conta ainda existe
    return db.session.get(Utilizador, utilizador_id)


def buscar_utilizador_por_email(email):
    """Procura um utilizador pelo e-mail, ignorando maiúsculas/minúsculas e espaços.

    Assim "Admin@UniBolsas.co.ao" e "admin@unibolsas.co.ao" são tratados como o mesmo e-mail,
    mesmo que a conta tenha sido criada à mão na base de dados.
    """
    email = (email or "").strip().lower()
    if not email:
        return None
    return Utilizador.query.filter(func.lower(func.trim(Utilizador.email)) == email).first()


def parece_hash(valor):
    """Diz se o texto guardado na coluna senha_hash já é uma senha encriptada (hash)."""
    return (valor or "").startswith(("scrypt:", "pbkdf2:", "$2a$", "$2b$", "$2y$", "$argon2"))


def senha_correta(utilizador, senha):
    """Confere a palavra-passe digitada com a guardada na base de dados.

    Também aceita contas antigas criadas à mão com a senha em texto simples: se a senha
    estiver certa, converte-a logo para hash seguro (RNF04) para não ficar exposta.
    """
    try:
        if utilizador.verificar_senha(senha):
            return True
    except (ValueError, TypeError):
        pass  # formato de hash desconhecido: nada a fazer
    # Conta antiga com a senha em texto simples (só se NÃO for um hash, para ninguém
    # conseguir entrar a escrever o próprio hash como se fosse a senha)
    if not parece_hash(utilizador.senha_hash) and utilizador.senha_hash == senha:
        utilizador.definir_senha(senha)
        db.session.commit()
        return True
    return False


def iniciar_sessao(utilizador):
    """Guarda na sessão os dados essenciais de quem acabou de entrar."""
    session.clear()  # limpa qualquer sessão anterior
    session["utilizador_id"] = utilizador.id
    session["utilizador_nome"] = utilizador.nome
    session["utilizador_tipo"] = utilizador.tipo


def login_obrigatorio(funcao):
    """'Guarda' das páginas privadas: sem sessão iniciada, envia para o login.

    Usa-se escrevendo @login_obrigatorio por baixo do @app.route da página.
    """

    @wraps(funcao)
    def verificar(*args, **kwargs):
        if utilizador_atual() is None:
            session.clear()
            flash("Inicie sessão para continuar.", "warning")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)

    return verificar


# ==============================================================================
=======
>>>>>>> origin/main
# ROTAS E LÓGICA DE NEGÓCIO (ENDPOINTS)
# ==============================================================================


# ROTA 1: PÁGINA PRINCIPAL COM FILTROS DE PESQUISA (Atende UC03, UC07, UC11)
@app.route("/")
def index():
    # Extrai parâmetros de pesquisa via GET enviados pelo formulário
    termo_pesquisa = request.args.get("pesquisa", "").strip()
    filtro_pais = request.args.get("pais", "").strip()
    filtro_nivel = request.args.get("nivel", "").strip()

    # Inicia a query base (apenas bolsas ativas e elegíveis para angolanos)
    query = Bolsa.query.filter_by(ativa=True, elegivel_angolanos=True)
<<<<<<< HEAD

    # Aplicação incremental de filtros
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

    # Executa a consulta
    bolsas_disponiveis = query.order_by(Bolsa.id.desc()).all()

    # Carrega bolseiros voluntários verificados para a secção de comunidade
    bolseiros_destaque = BolseiroVoluntario.query.filter_by(verificado=True).limit(6).all()

    # Carrega o catálogo de mentorias ativas
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

    # Regra 1: Dúvidas sobre bolsas integrais / 100% comparticipadas
    if "integral" in mensagem or "100%" in mensagem or "comparticipada" in mensagem or "integrais" in mensagem:
        total_integrais = Bolsa.query.filter_by(ativa=True, cobertura="integral").count()
        return jsonify({
            "resposta": f"Atualmente temos {total_integrais} bolsa(s) 100% comparticipada(s) no portal. As bolsas integrais cobrem propinas e alojamento sem custos diretos para ti."
        })

    # Regra 2: Dúvidas sobre preços ou contratação de mentorias
    elif "mentoria" in mensagem or "preço" in mensagem or "custo" in mensagem or "valor" in mensagem:
        mentorias = Mentoria.query.filter_by(ativa=True).all()
        lista_mentorias = ", ".join([f"{m.titulo} ({int(m.preco_kz):,} Kz)".replace(",", ".") for m in mentorias])
        return jsonify({
            "resposta": f"Oferecemos mentorias pagas para apoiar a tua candidatura: {lista_mentorias}. Podes agendar na secção Mentorias."
        })

    # Regra 3: Dúvidas sobre o INAGBE ou bolsas internas em Angola
    elif "inagbe" in mensagem or "angola" in mensagem or "interna" in mensagem:
        total_internas = Bolsa.query.filter_by(ativa=True, tipo="interna").count()
        return jsonify({
            "resposta": f"Temos {total_internas} bolsa(s) internas em Angola. Podes consultar os requisitos e prazos diretamente no nosso catálogo com o filtro de país 'Angola'."
        })

    # Regra 4: Dúvidas sobre documentos ou requisitos
    elif "documento" in mensagem or "requisito" in mensagem or "papel" in mensagem:
        return jsonify({
            "resposta": "Os documentos habituais incluem: Certificado de Habilitações autenticado, Cópia do BI, Carta de Motivação e Carta de Recomendação. Cada bolsa detalha os seus requisitos no respetivo cartão."
        })

    # Resposta padrão orientadora
    return jsonify({
        "resposta": "Sou o UniX! Podes perguntar-me sobre 'bolsas integrais', 'mentorias e preços', 'bolsas do INAGBE' ou 'documentos necessários'."
    })


# ROTA 3: CRIAÇÃO DE CONTA DE UTILIZADOR (Atende UC01 / RF01, RNF04)
@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():
    # Se o utilizador já tem sessão iniciada, redireciona para o painel
    if utilizador_atual() is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        # 1. Validação de preenchimento dos campos
        if not nome or not email or not senha:
            flash("Por favor, preencha todos os campos obrigatórios.", "danger")
            return render_template("criar_conta.html")

        # 2. Validação do tamanho da palavra-passe (o HTML também exige, mas o servidor confirma)
        if len(senha) < 6:
            flash("A palavra-passe deve ter pelo menos 6 caracteres.", "danger")
            return render_template("criar_conta.html")

        # 3. Validação de coincidência de palavras-passe
        if senha != confirmar_senha:
            flash("As palavras-passe introduzidas não coincidem.", "danger")
            return render_template("criar_conta.html")

        # 4. Validação de unicidade de e-mail na base de dados (1FN)
        utilizador_existente = buscar_utilizador_por_email(email)
        if utilizador_existente:
            flash("Este e-mail já se encontra registado. Tente iniciar sessão.", "warning")
            return render_template("criar_conta.html")

        # 5. Criação do novo candidato com tipo obrigatoriamente restrito a 'candidato'
        novo_candidato = Utilizador(
            nome=nome,
            email=email,
            tipo="candidato",  # Regra de segurança: registos públicos nunca são admin
        )
        novo_candidato.definir_senha(senha)  # Hash encriptado conforme RNF04

        try:
            db.session.add(novo_candidato)
            db.session.commit()
        except IntegrityError:
            # Dois registos com o mesmo e-mail ao mesmo tempo: a BD recusa o segundo
            db.session.rollback()
            flash("Este e-mail já se encontra registado. Tente iniciar sessão.", "warning")
            return render_template("criar_conta.html")

        # 6. Inicia sessão imediatamente após o registo com sucesso
        iniciar_sessao(novo_candidato)
        flash(f"Conta criada com sucesso! Bem-vindo, {novo_candidato.nome}.", "success")
        return redirect(url_for("dashboard"))

    # Pedido GET normal: apresenta o formulário
    return render_template("criar_conta.html")


# ROTA 4: INÍCIO DE SESSÃO (Atende UC02 / RF02)
@app.route("/login", methods=["GET", "POST"])
def login():
    # Quem já entrou não precisa de ver o formulário outra vez
    if utilizador_atual() is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # 1. Os dois campos têm de vir preenchidos
        if not email or not senha:
            flash("Preencha o e-mail e a palavra-passe.", "danger")
            return render_template("login.html")

        # 2. Procura o utilizador na base de dados pelo e-mail e confere a senha encriptada
        utilizador = buscar_utilizador_por_email(email)
        if utilizador is None or not senha_correta(utilizador, senha):
            # Mensagem igual nos dois casos: não revela se o e-mail existe
            flash("E-mail ou palavra-passe incorretos.", "danger")
            return render_template("login.html")

        # 3. Tudo certo: guarda a sessão e segue para o painel
        iniciar_sessao(utilizador)
        flash(f"Bem-vindo de volta, {utilizador.nome}!", "success")
        return redirect(url_for("dashboard"))

    # Pedido GET normal: apresenta o formulário
    return render_template("login.html")


# ROTA 5: TERMINAR SESSÃO (Atende UC02 / RF02)
@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada com sucesso.", "info")
    return redirect(url_for("login"))


# ATALHOS PARA OS LINKS DO FRONT: o HTML antigo usa links como "index.html" e
# "criar_conta.html". Em vez de mexer no front, estas rotas reencaminham para a página certa.
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

    # Obtém todas as bolsas ativas da base de dados PostgreSQL
    bolsas_disponiveis = Bolsa.query.filter_by(ativa=True).order_by(Bolsa.id.desc()).all()
    # Obtém bolseiros voluntários verificados
    bolseiros_lista = BolseiroVoluntario.query.filter_by(verificado=True).all()
    # Obtém o catálogo de mentorias
    mentorias_lista = Mentoria.query.filter_by(ativa=True).all()

    # Dados PESSOAIS do candidato (só os dele): mentorias contratadas e pedidos a bolseiros
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

    # Bolsas GUARDADAS / FAVORITAS do candidato logado (Atende RF11, UC06)
    registos_guardados = (
        BolsaGuardada.query.filter_by(candidato_id=utilizador.id)
        .order_by(BolsaGuardada.criado_em.desc())
        .all()
    )
    # Extrai os objetos Bolsa das associações guardadas
    minhas_bolsas_guardadas = [registo.bolsa for registo in registos_guardados if registo.bolsa]
    # Lista de IDs de bolsas guardadas para destacar o botão no carrossel
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
# O clique no botão marcador submete um POST alternando o estado de favorito
@app.route("/guardar-bolsa/<int:bolsa_id>", methods=["POST"])
@login_obrigatorio
def guardar_bolsa(bolsa_id):
    utilizador = utilizador_atual()

    # 1. A bolsa tem de existir e estar ativa
    bolsa = db.session.get(Bolsa, bolsa_id)
    if bolsa is None or not bolsa.ativa:
        flash("Bolsa não encontrada ou inativa.", "danger")
        return redirect(url_for("dashboard"))

    # 2. Verifica se a bolsa já está nos favoritos do candidato
    guardada = BolsaGuardada.query.filter_by(candidato_id=utilizador.id, bolsa_id=bolsa.id).first()

    if guardada:
        # Se já estava guardada, remove dos favoritos (toggle)
        db.session.delete(guardada)
        db.session.commit()
        flash(f'Bolsa "{bolsa.titulo}" removida dos teus favoritos.', "info")
    else:
        # Se não estava guardada, adiciona à tabela associativa
        novo_favorito = BolsaGuardada(candidato_id=utilizador.id, bolsa_id=bolsa.id)
        db.session.add(novo_favorito)
        db.session.commit()
        flash(f'Bolsa "{bolsa.titulo}" guardada com sucesso nos teus favoritos!', "success")

    return redirect(url_for("dashboard") + "#guardadas")


# ROTA 8: PEDIR CONTACTO COM UM BOLSEIRO (Atende UC08 / RF17)
# O botão "Conversar com Bolseiro" envia um formulário POST para /pedir-contacto/<id do bolseiro>
# Campo opcional do formulário: "pergunta"
@app.route("/pedir-contacto/<int:bolseiro_id>", methods=["POST"])
@login_obrigatorio
def pedir_contacto(bolseiro_id):
    utilizador = utilizador_atual()

    # 1. O bolseiro tem de existir e estar verificado
    bolseiro = db.session.get(BolseiroVoluntario, bolseiro_id)
    if bolseiro is None or not bolseiro.verificado:
        flash("Esse bolseiro não está disponível.", "danger")
        return redirect(url_for("dashboard"))

    # 2. Não permite repetir um pedido que ainda está pendente para o mesmo bolseiro
    pedido_pendente = PedidoContacto.query.filter_by(
        candidato_id=utilizador.id, bolseiro_id=bolseiro.id, status="Pendente"
    ).first()
    if pedido_pendente:
        flash(f"Já tem um pedido pendente para {bolseiro.nome}.", "warning")
        return redirect(url_for("dashboard") + "#bolseiros-comunidade")

    # 3. Guarda o pedido (a equipa encaminha ao bolseiro, sem revelar contactos pessoais)
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
# O botão "Solicitar" envia um formulário POST para /contratar-mentoria/<id da mentoria>
# Campo opcional do formulário: "data_preferida"
@app.route("/contratar-mentoria/<int:mentoria_id>", methods=["POST"])
@login_obrigatorio
def contratar_mentoria(mentoria_id):
    utilizador = utilizador_atual()

    # 1. A mentoria tem de existir e estar ativa
    mentoria = db.session.get(Mentoria, mentoria_id)
    if mentoria is None or not mentoria.ativa:
        flash("Essa mentoria não está disponível.", "danger")
        return redirect(url_for("dashboard"))

    # 2. Não permite contratar outra vez uma mentoria que ainda está por pagar
    por_pagar = ContratacaoMentoria.query.filter_by(
        candidato_id=utilizador.id, mentoria_id=mentoria.id, status_pagamento="Pendente"
    ).first()
    if por_pagar:
        flash("Já solicitou esta mentoria e falta confirmar o pagamento.", "warning")
        return redirect(url_for("dashboard") + "#mentores-tecnicos")

    # 3. Regista a contratação com o pagamento "Pendente"
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
# Não há dinheiro real: apenas muda o estado de "Pendente" para "Pago"
@app.route("/pagar-mentoria/<int:contratacao_id>", methods=["POST"])
@login_obrigatorio
def pagar_mentoria(contratacao_id):
    utilizador = utilizador_atual()

    contratacao = db.session.get(ContratacaoMentoria, contratacao_id)
    # Só o dono da contratação a pode pagar (um candidato nunca mexe nas dos outros)
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
# FERRAMENTA DE CONTAS (terminal): VER e ARRANJAR contas na base de dados
# ------------------------------------------------------------------------------
# Corra na pasta do projeto (onde está o app.py e o .env). Não arranca o site:
#
#   python app.py contas listar
#       Mostra todas as contas (e-mail, nome, tipo e estado da senha). Nunca mostra senhas.
#
#   python app.py contas testar EMAIL SENHA
#       Diz se o login com esse e-mail e senha funcionaria e, se não, porquê. Não altera nada.
#
#   python app.py contas definir EMAIL SENHA [--nome "Nome"]
#       Cria a conta de candidato (se não existir) ou altera a senha de forma segura.
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
        certa = True  # texto simples: o login aceita e converte
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
    
    # REGRA DE SEGURANÇA: Apenas o e-mail oficial pode deter privilégios de administrador
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
        # Não permite que contas normais alterem o seu tipo para admin
        if utilizador.email != EMAIL_ADMIN_OFICIAL:
            utilizador.tipo = "candidato"
        acao = "ATUALIZADA"

    utilizador.email = email  # guarda sempre em minúsculas e sem espaços
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
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # acentos corretos no Windows
    comando = args[0] if args else ""
    try:
        with app.app_context():
            if comando == "listar":
                listar_contas()
            elif comando == "testar" and len(args) >= 3:
                testar_login(args[1], args[2])
            elif comando == "definir" and len(args) >= 3:
                # Blindagem: Não aceita mais o argumento --tipo. A regra é estritamente automática
                definir_conta(args[1], args[2], valor_da_opcao(args, "--nome"))
            else:
                print(AJUDA_CONTAS)
    except Exception as erro:  # ex.: sem internet ou .env em falta
        print("Não foi possível conectar com a base de dados: %s" % erro)
=======

    # Aplicação incremental de filtros
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

    # Executa a consulta
    bolsas_disponiveis = query.order_by(Bolsa.id.desc()).all()

    # Carrega bolseiros voluntários verificados para a secção de comunidade
    bolseiros_destaque = BolseiroVoluntario.query.filter_by(verificado=True).limit(6).all()

    # Carrega o catálogo de mentorias ativas
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

    # Regra 1: Dúvidas sobre bolsas integrais / 100% comparticipadas
    if "integral" in mensagem or "100%" in mensagem or "comparticipada" in mensagem or "integrais" in mensagem:
        total_integrais = Bolsa.query.filter_by(ativa=True, cobertura="integral").count()
        return jsonify({
            "resposta": f"Atualmente temos {total_integrais} bolsa(s) 100% comparticipada(s) no portal. As bolsas integrais cobrem propinas e alojamento sem custos diretos para ti."
        })

    # Regra 2: Dúvidas sobre preços ou contratação de mentorias
    elif "mentoria" in mensagem or "preço" in mensagem or "custo" in mensagem or "valor" in mensagem:
        mentorias = Mentoria.query.filter_by(ativa=True).all()
        lista_mentorias = ", ".join([f"{m.titulo} ({int(m.preco_kz):,} Kz)".replace(",", ".") for m in mentorias])
        return jsonify({
            "resposta": f"Oferecemos mentorias pagas para apoiar a tua candidatura: {lista_mentorias}. Podes agendar na secção Mentorias."
        })

    # Regra 3: Dúvidas sobre o INAGBE ou bolsas internas em Angola
    elif "inagbe" in mensagem or "angola" in mensagem or "interna" in mensagem:
        total_internas = Bolsa.query.filter_by(ativa=True, tipo="interna").count()
        return jsonify({
            "resposta": f"Temos {total_internas} bolsa(s) internas em Angola. Podes consultar os requisitos e prazos diretamente no nosso catálogo com o filtro de país 'Angola'."
        })

    # Regra 4: Dúvidas sobre documentos ou requisitos
    elif "documento" in mensagem or "requisito" in mensagem or "papel" in mensagem:
        return jsonify({
            "resposta": "Os documentos habituais incluem: Certificado de Habilitações autenticado, Cópia do BI, Carta de Motivação e Carta de Recomendação. Cada bolsa detalha os seus requisitos no respetivo cartão."
        })

    # Resposta padrão orientadora
    return jsonify({
        "resposta": "Sou o UniX! Podes perguntar-me sobre 'bolsas integrais', 'mentorias e preços', 'bolsas do INAGBE' ou 'documentos necessários'."
    })
>>>>>>> origin/main


# ==============================================================================
# BLOCO DE EXECUÇÃO LOCAL E CRIAÇÃO DAS TABELAS
# ==============================================================================
if __name__ == "__main__":
<<<<<<< HEAD
    # Modo ferramenta de contas: "python app.py contas listar" (não arranca o site)
    if len(sys.argv) > 1 and sys.argv[1] == "contas":
        executar_comando_contas(sys.argv[2:])
        sys.exit(0)

=======
>>>>>>> origin/main
    with app.app_context():
        print("A sincronizar modelos normalizados com a nuvem (Neon)...")
        db.create_all()
        criar_dados_iniciais()
        print("Base de dados sincronizada e povoada com sucesso!")

    app.run(debug=True)