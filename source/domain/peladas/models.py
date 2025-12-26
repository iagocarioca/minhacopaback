from source.extensions.extensios import db
from datetime import datetime
import pytz

def get_brazil_time():
    """Retorna o horário atual do Brasil (Brasília - UTC-3)"""
    brazil_tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(brazil_tz)

class Pelada(db.Model):
    __tablename__ = 'peladas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_gerente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    fuso_horario = db.Column(db.String(50), nullable=False, default='America/Sao_Paulo')
    logo_url = db.Column(db.String(255), nullable=True)  # Caminho da imagem de logotipo
    perfil_url = db.Column(db.String(255), nullable=True)  # Caminho da imagem de perfil (maior)
    ativa = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    gerente = db.relationship('User', back_populates='peladas_gerenciadas', lazy=True)
    temporadas = db.relationship('Temporada', back_populates='pelada', lazy=True)
    jogadores = db.relationship('Jogador', back_populates='pelada', lazy=True)

    def __init__(self, nome, cidade, usuario_gerente_id, fuso_horario='America/Sao_Paulo'):
        self.nome = nome
        self.cidade = cidade
        self.usuario_gerente_id = usuario_gerente_id
        self.fuso_horario = fuso_horario

    def ativar(self):
        self.ativa = True

class Jogador(db.Model):
    __tablename__ = 'jogadores'

    id = db.Column(db.Integer, primary_key=True)
    pelada_id = db.Column(db.Integer, db.ForeignKey('peladas.id'), nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    apelido = db.Column(db.String(50), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    foto_url = db.Column(db.String(255), nullable=True)  # Caminho da foto do jogador
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    pelada = db.relationship('Pelada', back_populates='jogadores', lazy=True)
    time_jogadores = db.relationship('TimeJogador', back_populates='jogador', lazy=True)
    gols = db.relationship('Gol', foreign_keys='Gol.jogador_id', back_populates='jogador', lazy=True)
    votos_dados = db.relationship('Voto', foreign_keys='Voto.jogador_votante_id', back_populates='jogador_votante', lazy=True)
    votos_recebidos = db.relationship('Voto', foreign_keys='Voto.jogador_votado_id', back_populates='jogador_votado', lazy=True)

    def __init__(self, pelada_id, nome_completo, apelido=None, telefone=None):
        self.pelada_id = pelada_id
        self.nome_completo = nome_completo
        self.apelido = apelido
        self.telefone = telefone


class Temporada(db.Model):
    __tablename__ = 'temporadas'

    id = db.Column(db.Integer, primary_key=True)
    pelada_id = db.Column(db.Integer, db.ForeignKey('peladas.id'), nullable=False)
    inicio_mes = db.Column(db.Date, nullable=False)
    fim_mes = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='ativa')
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamento
    pelada = db.relationship('Pelada', back_populates='temporadas', lazy=True)
    rodadas = db.relationship('Rodada', back_populates='temporada', lazy=True)
    times = db.relationship('Time', back_populates='temporada', lazy=True)

    def __init__(self, pelada_id, inicio_mes, fim_mes):
        self.pelada_id = pelada_id
        self.inicio_mes = inicio_mes
        self.fim_mes = fim_mes

class Rodada(db.Model):
    __tablename__ = 'rodadas'

    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(db.Integer, db.ForeignKey('temporadas.id'), nullable=False)
    data_rodada = db.Column(db.Date, nullable=False)
    quantidade_times = db.Column(db.Integer, nullable=False)
    jogadores_por_time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pendente')
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    temporada = db.relationship('Temporada', back_populates='rodadas', lazy=True)
    partidas = db.relationship('Partida', back_populates='rodada', lazy=True)
    votacoes = db.relationship('Votacao', back_populates='rodada', lazy=True)

    def __init__(self, temporada_id, data_rodada, quantidade_times, jogadores_por_time):
        self.temporada_id = temporada_id
        self.data_rodada = data_rodada
        self.quantidade_times = quantidade_times
        self.jogadores_por_time = jogadores_por_time


class Time(db.Model):
    __tablename__ = 'times'

    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(db.Integer, db.ForeignKey('temporadas.id'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(30), nullable=True)  # Ex: "azul", "vermelho", "verde"
    escudo_url = db.Column(db.String(255), nullable=True)  # Caminho do escudo do time
    pontos = db.Column(db.Integer, default=0)
    vitorias = db.Column(db.Integer, default=0)
    empates = db.Column(db.Integer, default=0)
    derrotas = db.Column(db.Integer, default=0)
    gols_marcados = db.Column(db.Integer, default=0)
    gols_sofridos = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    temporada = db.relationship('Temporada', back_populates='times', lazy=True)
    time_jogadores = db.relationship('TimeJogador', back_populates='time', lazy=True, cascade='all, delete-orphan')
    gols = db.relationship('Gol', back_populates='time', lazy=True)
    partidas_casa = db.relationship('Partida', foreign_keys='Partida.time_casa_id', back_populates='time_casa', lazy=True)
    partidas_fora = db.relationship('Partida', foreign_keys='Partida.time_fora_id', back_populates='time_fora', lazy=True)

    def __init__(self, temporada_id, nome, cor=None):
        self.temporada_id = temporada_id
        self.nome = nome
        self.cor = cor


class TimeJogador(db.Model):
    __tablename__ = 'time_jogadores'

    id = db.Column(db.Integer, primary_key=True)
    time_id = db.Column(db.Integer, db.ForeignKey('times.id'), nullable=False)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    capitao = db.Column(db.Boolean, default=False)
    posicao = db.Column(db.String(50), nullable=True)  # Mudado para String para aceitar nome da posição

    #relacionamentos
    time = db.relationship('Time', back_populates='time_jogadores', lazy=True)
    jogador = db.relationship('Jogador', back_populates='time_jogadores', lazy=True)

    def __init__(self, time_id, jogador_id, capitao=False, posicao=None):
        self.time_id = time_id
        self.jogador_id = jogador_id
        self.capitao = capitao
        self.posicao = posicao


class Partida(db.Model):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True)
    rodada_id = db.Column(db.Integer, db.ForeignKey('rodadas.id'), nullable=False)
    time_casa_id = db.Column(db.Integer, db.ForeignKey('times.id'), nullable=False)
    time_fora_id = db.Column(db.Integer, db.ForeignKey('times.id'), nullable=False)
    inicio = db.Column(db.DateTime, nullable=True)
    fim = db.Column(db.DateTime, nullable=True)
    gols_casa = db.Column(db.Integer, default=0)
    gols_fora = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='agendada')

    #relacionamentos
    rodada = db.relationship('Rodada', back_populates='partidas', lazy=True)
    time_casa = db.relationship('Time', foreign_keys=[time_casa_id], back_populates='partidas_casa', lazy=True)
    time_fora = db.relationship('Time', foreign_keys=[time_fora_id], back_populates='partidas_fora', lazy=True)
    gols = db.relationship('Gol', back_populates='partida', lazy=True)

    def __init__(self, rodada_id, time_casa_id, time_fora_id):
        self.rodada_id = rodada_id
        self.time_casa_id = time_casa_id
        self.time_fora_id = time_fora_id


class Gol(db.Model):
    __tablename__ = 'gols'

    id = db.Column(db.Integer, primary_key=True)
    partida_id = db.Column(db.Integer, db.ForeignKey('partidas.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('times.id'), nullable=False)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    assistencia_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=True)
    minuto = db.Column(db.Integer, nullable=True)
    gol_contra = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    partida = db.relationship('Partida', back_populates='gols', lazy=True)
    time = db.relationship('Time', back_populates='gols', lazy=True)
    jogador = db.relationship('Jogador', foreign_keys=[jogador_id], back_populates='gols', lazy=True)
    assistente = db.relationship('Jogador', foreign_keys=[assistencia_id], lazy=True)

    def __init__(self, partida_id, time_id, jogador_id, minuto=None, gol_contra=False, assistencia_id=None):
        self.partida_id = partida_id
        self.time_id = time_id
        self.jogador_id = jogador_id
        self.minuto = minuto
        self.gol_contra = gol_contra
        self.assistencia_id = assistencia_id


class Votacao(db.Model):
    __tablename__ = 'votacoes'

    id = db.Column(db.Integer, primary_key=True)
    rodada_id = db.Column(db.Integer, db.ForeignKey('rodadas.id'), nullable=False)
    abre_em = db.Column(db.DateTime, nullable=False)
    fecha_em = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pendente')

    #relacionamentos
    rodada = db.relationship('Rodada', back_populates='votacoes', lazy=True)
    votos = db.relationship('Voto', back_populates='votacao', lazy=True)

    def __init__(self, rodada_id, abre_em, fecha_em, tipo):
        self.rodada_id = rodada_id
        self.abre_em = abre_em
        self.fecha_em = fecha_em
        self.tipo = tipo


class Voto(db.Model):
    __tablename__ = 'votos'

    id = db.Column(db.Integer, primary_key=True)
    votacao_id = db.Column(db.Integer, db.ForeignKey('votacoes.id'), nullable=False)
    jogador_votante_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    jogador_votado_id = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    pontos = db.Column(db.SmallInteger, nullable=False)
    criado_em = db.Column(db.DateTime, default=get_brazil_time)

    #relacionamentos
    votacao = db.relationship('Votacao', back_populates='votos', lazy=True)
    jogador_votante = db.relationship('Jogador', foreign_keys=[jogador_votante_id], back_populates='votos_dados', lazy=True)
    jogador_votado = db.relationship('Jogador', foreign_keys=[jogador_votado_id], back_populates='votos_recebidos', lazy=True)

    def __init__(self, votacao_id, jogador_votante_id, jogador_votado_id, pontos):
        self.votacao_id = votacao_id
        self.jogador_votante_id = jogador_votante_id
        self.jogador_votado_id = jogador_votado_id
        self.pontos = pontos