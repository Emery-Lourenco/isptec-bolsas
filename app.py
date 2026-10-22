# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NECESSÁRIOS DO FLASK E SQLALCHEMY
# ==============================================================================
import os  # Biblioteca nativa para ler variáveis de ambiente do sistema
from datetime import datetime, timezone  # Registo de carimbos temporais
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
from werkzeug.security import (  # Utilitários nativos para senhas seguras (RNF04)
    check_password_hash,
    generate_password_hash,
)

# Carrega o ficheiro .env local antes de iniciar as configurações
load_dotenv()

# ==============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO WEB
# ==============================================================================
app = Flask(__name__)

# CHAVE SECRETA DA SESSÃO:
# O Flask precisa de uma chave para encriptar os cookies de sessão no browser do utilizador.
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "chave_secreta_mvp_isptec_2026"
)

# ==============================================================================
# CONFIGURAÇÃO DA BASE DE DADOS (POSTGRESQL)
# ==============================================================================
# Lê a string de conexão remota definida no ficheiro .env para proteger as credenciais
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
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


# ==============================================================================
# POVOAMENTO INICIAL DE DADOS DE TESTE (SEEDS)
# ==============================================================================
def criar_dados_iniciais():
    """Garante a existência de dados mínimos reais para demonstração do MVP."""
    try:
        # Criar bolseiros voluntários se a tabela estiver vazia
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

        # Criar catálogo de mentorias se estiver vazio
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


# ROTA 3: PAINEL EXCLUSIVO DO CANDIDATO (Atende UC14, UC28 / RF23, RF44)
@app.route("/dashboard")
def dashboard():
    # Obtém todas as bolsas ativas da base de dados PostgreSQL
    bolsas_disponiveis = Bolsa.query.filter_by(ativa=True).order_by(Bolsa.id.desc()).all()
    # Obtém bolseiros voluntários verificados
    bolseiros_lista = BolseiroVoluntario.query.filter_by(verificado=True).all()
    # Obtém o catálogo de mentorias
    mentorias_lista = Mentoria.query.filter_by(ativa=True).all()

    # Nome do candidato exibido (dinâmico ou padrão enquanto o login não está concluído)
    nome_usuario = session.get("utilizador_nome", "Mário Silva")

    return render_template(
        "dashboard_candidato.html",
        bolsas=bolsas_disponiveis,
        bolseiros=bolseiros_lista,
        mentorias=mentorias_lista,
        nome_candidato=nome_usuario,
    )


# ==============================================================================
# BLOCO DE EXECUÇÃO LOCAL E CRIAÇÃO DAS TABELAS
# ==============================================================================
if __name__ == "__main__":
    with app.app_context():
        print("A sincronizar modelos normalizados com a nuvem (Neon)...")
        db.create_all()
        criar_dados_iniciais()
        print("Base de dados sincronizada e povoada com sucesso!")

    app.run(debug=True)