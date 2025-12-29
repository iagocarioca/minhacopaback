# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, current_app
from source.domain.peladas.services import (
    PeladaService, JogadorService, TemporadaService, RodadaService,
    TimeService, PartidaService, GolService, RankingService, VotacaoService
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Response
from source.api.decorators import (
    pelada_owner_required, jogador_owner_required, temporada_owner_required, rodada_owner_required,
    time_owner_required, partida_owner_required, gol_owner_required, votacao_owner_required
)
import os
from werkzeug.utils import secure_filename
from datetime import datetime

pelada_bp = Blueprint('pelada', __name__)

# Extensões permitidas para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def salvar_imagem_pelada(arquivo, tipo='logo'):
    """
    Salva uma imagem de pelada no servidor
    
    Args:
        arquivo: objeto FileStorage do Flask
        tipo: 'logo' ou 'perfil'
    
    Returns:
        str: caminho relativo da imagem salva ou None se houver erro
    """
    if not arquivo or not allowed_file(arquivo.filename):
        return None
    
    # Criar estrutura de pastas: static/uploads/peladas/
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'peladas')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único: timestamp_nome_seguro.extensao
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = secure_filename(arquivo.filename)
    nome_base, extensao = os.path.splitext(filename)
    novo_nome = f"{tipo}_{timestamp}{extensao}"
    
    caminho_completo = os.path.join(upload_dir, novo_nome)
    arquivo.save(caminho_completo)
    
    # Retornar caminho relativo para acessar via URL: /static/uploads/peladas/nome.jpg
    return f"/static/uploads/peladas/{novo_nome}"


def salvar_imagem_jogador(arquivo):
    """
    Salva uma foto de jogador no servidor
    
    Args:
        arquivo: objeto FileStorage do Flask
    
    Returns:
        str: caminho relativo da imagem salva ou None se houver erro
    """
    if not arquivo or not allowed_file(arquivo.filename):
        return None
    
    # Criar estrutura de pastas: static/uploads/jogadores/
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'jogadores')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único: timestamp_nome_seguro.extensao
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = secure_filename(arquivo.filename)
    nome_base, extensao = os.path.splitext(filename)
    novo_nome = f"foto_{timestamp}{extensao}"
    
    caminho_completo = os.path.join(upload_dir, novo_nome)
    arquivo.save(caminho_completo)
    
    # Retornar caminho relativo para acessar via URL: /static/uploads/jogadores/nome.jpg
    return f"/static/uploads/jogadores/{novo_nome}"


def salvar_imagem_time(arquivo):
    """
    Salva um escudo de time no servidor
    
    Args:
        arquivo: objeto FileStorage do Flask
    
    Returns:
        str: caminho relativo da imagem salva ou None se houver erro
    """
    if not arquivo or not allowed_file(arquivo.filename):
        return None
    
    # Criar estrutura de pastas: static/uploads/times/
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'times')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único: timestamp_nome_seguro.extensao
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = secure_filename(arquivo.filename)
    nome_base, extensao = os.path.splitext(filename)
    novo_nome = f"escudo_{timestamp}{extensao}"
    
    caminho_completo = os.path.join(upload_dir, novo_nome)
    arquivo.save(caminho_completo)
    
    # Retornar caminho relativo para acessar via URL: /static/uploads/times/nome.jpg
    return f"/static/uploads/times/{novo_nome}"



@pelada_bp.route('/', methods=['POST'])
@jwt_required()
def criar_pelada():
    """
    Criar uma nova pelada
    
    Aceita multipart/form-data com:
    - nome (obrigatório)
    - cidade (obrigatório)
    - fuso_horario (opcional, default: 'America/Sao_Paulo')
    - logo (opcional, arquivo de imagem)
    - perfil (opcional, arquivo de imagem)
    
    Exemplo de payload (FormData):
        nome: "Pelada do Bairro"
        cidade: "São Paulo"
        fuso_horario: "America/Sao_Paulo"
        logo: [arquivo]
        perfil: [arquivo]
    """
    try:
        logo_url = None
        perfil_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            # Processar FormData
            nome = request.form.get('nome')
            cidade = request.form.get('cidade')
            fuso_horario = request.form.get('fuso_horario', 'America/Sao_Paulo')
            
            # Processar uploads de imagens
            if 'logo' in request.files:
                arquivo_logo = request.files['logo']
                if arquivo_logo and arquivo_logo.filename:
                    logo_url = salvar_imagem_pelada(arquivo_logo, tipo='logo')
            
            if 'perfil' in request.files:
                arquivo_perfil = request.files['perfil']
                if arquivo_perfil and arquivo_perfil.filename:
                    perfil_url = salvar_imagem_pelada(arquivo_perfil, tipo='perfil')
        else:
            # Fallback para JSON (sem imagens)
            dados = request.get_json(silent=True)  # silent=True evita erro 415
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400
            
            nome = dados.get('nome')
            cidade = dados.get('cidade')
            fuso_horario = dados.get('fuso_horario', 'America/Sao_Paulo')
            logo_url = dados.get('logo_url')  # Se vier URL já pronta
            perfil_url = dados.get('perfil_url')

        usuario_gerente_id = get_jwt_identity()

        if not nome or not cidade:
            return jsonify({'erro': 'Nome e cidade são obrigatórios'}), 400

        pelada, erro = PeladaService.criar_pelada(
            nome, cidade, usuario_gerente_id, fuso_horario, logo_url, perfil_url
        )

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Pelada criada com sucesso',
            'pelada': pelada
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/', methods=['GET'])
def listar_peladas():
    """Listar peladas com filtros opcionais (público)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        # Permite filtrar por usuario_id opcionalmente via query parameter
        usuario_id = request.args.get('usuario_id', type=int)
        ativa = request.args.get('ativa', type=lambda x: x.lower() == 'true')

        resultado, erro = PeladaService.listar_peladas(page, per_page, usuario_id, ativa)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/<int:pelada_id>', methods=['GET'])
@jwt_required()
@pelada_owner_required
def obter_pelada(pelada_id):
    """Obter pelada por ID"""
    try:
        pelada, erro = PeladaService.obter_pelada_por_id(pelada_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'pelada': pelada}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/<int:pelada_id>/perfil', methods=['GET'])
def obter_perfil_pelada(pelada_id):
    """Obter perfil completo da pelada com gerente, jogadores, temporadas e estatísticas"""
    try:
        perfil, erro = PeladaService.obter_perfil_pelada(pelada_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify(perfil), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/<int:pelada_id>', methods=['PUT'])
@jwt_required()
@pelada_owner_required
def atualizar_pelada(pelada_id):
    """
    Atualizar uma pelada
    
    Aceita multipart/form-data ou JSON:
    - nome, cidade, fuso_horario, ativa (campos opcionais)
    - logo (opcional, arquivo de imagem) - apenas multipart
    - perfil (opcional, arquivo de imagem) - apenas multipart
    """
    try:
        logo_url = None
        perfil_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            # Processar FormData
            dados = {}
            if request.form.get('nome'):
                dados['nome'] = request.form.get('nome')
            if request.form.get('cidade'):
                dados['cidade'] = request.form.get('cidade')
            if request.form.get('fuso_horario'):
                dados['fuso_horario'] = request.form.get('fuso_horario')
            if request.form.get('ativa'):
                dados['ativa'] = request.form.get('ativa').lower() == 'true'
            
            # Processar uploads de imagens
            if 'logo' in request.files:
                arquivo_logo = request.files['logo']
                if arquivo_logo and arquivo_logo.filename:
                    logo_url = salvar_imagem_pelada(arquivo_logo, tipo='logo')
                    if logo_url:
                        dados['logo_url'] = logo_url
            
            if 'perfil' in request.files:
                arquivo_perfil = request.files['perfil']
                if arquivo_perfil and arquivo_perfil.filename:
                    perfil_url = salvar_imagem_pelada(arquivo_perfil, tipo='perfil')
                    if perfil_url:
                        dados['perfil_url'] = perfil_url
        else:
            # Fallback para JSON (sem imagens)
            dados = request.get_json(silent=True)  # silent=True evita erro 415
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        pelada, erro = PeladaService.atualizar_pelada(pelada_id, dados)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Pelada atualizada com sucesso',
            'pelada': pelada
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE JOGADORES ====================

@pelada_bp.route('/<int:pelada_id>/jogadores', methods=['POST'])
@jwt_required()
@pelada_owner_required
def criar_jogador(pelada_id):
    """
    Criar um novo jogador
    
    Aceita multipart/form-data ou JSON:
    - nome_completo (obrigatório)
    - apelido (opcional)
    - telefone (opcional)
    - foto (opcional, arquivo de imagem) - apenas multipart
    """
    try:
        foto_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            nome_completo = request.form.get('nome_completo')
            apelido = request.form.get('apelido')
            telefone = request.form.get('telefone')
            
            # Processar upload de foto
            if 'foto' in request.files:
                arquivo_foto = request.files['foto']
                if arquivo_foto and arquivo_foto.filename:
                    foto_url = salvar_imagem_jogador(arquivo_foto)
        else:
            dados = request.get_json(silent=True)
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400
            
            nome_completo = dados.get('nome_completo')
            apelido = dados.get('apelido')
            telefone = dados.get('telefone')
            foto_url = dados.get('foto_url')  # Se vier URL já pronta

        if not nome_completo:
            return jsonify({'erro': 'Nome completo é obrigatório'}), 400

        jogador, erro = JogadorService.criar_jogador(pelada_id, nome_completo, apelido, telefone, foto_url)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Jogador criado com sucesso',
            'jogador': jogador
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/<int:pelada_id>/jogadores', methods=['GET'])
@jwt_required()
@pelada_owner_required
def listar_jogadores(pelada_id):
    """Listar jogadores de uma pelada"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        ativo = request.args.get('ativo', type=lambda x: x.lower() == 'true' if x else None)

        resultado, erro = JogadorService.listar_jogadores(pelada_id, page, per_page, ativo)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/jogadores/<int:jogador_id>', methods=['GET'])
@jwt_required()
@jogador_owner_required
def obter_jogador(jogador_id):
    """Obter jogador por ID"""
    try:
        jogador, erro = JogadorService.obter_jogador_por_id(jogador_id)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'jogador': jogador}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/jogadores/<int:jogador_id>', methods=['PUT'])
@jwt_required()
@jogador_owner_required
def atualizar_jogador(jogador_id):
    """
    Atualizar um jogador
    
    Aceita multipart/form-data ou JSON:
    - nome_completo, apelido, telefone, ativo (campos opcionais)
    - foto (opcional, arquivo de imagem) - apenas multipart
    """
    try:
        foto_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            dados = {}
            if request.form.get('nome_completo'):
                dados['nome_completo'] = request.form.get('nome_completo')
            if request.form.get('apelido'):
                dados['apelido'] = request.form.get('apelido')
            if request.form.get('telefone'):
                dados['telefone'] = request.form.get('telefone')
            if request.form.get('ativo'):
                dados['ativo'] = request.form.get('ativo').lower() == 'true'
            
            # Processar upload de foto
            if 'foto' in request.files:
                arquivo_foto = request.files['foto']
                if arquivo_foto and arquivo_foto.filename:
                    foto_url = salvar_imagem_jogador(arquivo_foto)
                    if foto_url:
                        dados['foto_url'] = foto_url
        else:
            dados = request.get_json(silent=True)
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        jogador, erro = JogadorService.atualizar_jogador(jogador_id, dados)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Jogador atualizado com sucesso',
            'jogador': jogador
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE TEMPORADAS ====================

@pelada_bp.route('/<int:pelada_id>/temporadas', methods=['POST'])
@jwt_required()
@pelada_owner_required
def criar_temporada(pelada_id):
    """Criar uma nova temporada"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        inicio_mes = dados.get('inicio_mes')
        fim_mes = dados.get('fim_mes')

        if not inicio_mes or not fim_mes:
            return jsonify({'erro': 'Início e fim da temporada são obrigatórios'}), 400

        temporada, erro = TemporadaService.criar_temporada(pelada_id, inicio_mes, fim_mes)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Temporada criada com sucesso',
            'temporada': temporada
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/<int:pelada_id>/temporadas', methods=['GET'])
@jwt_required()
@pelada_owner_required
def listar_temporadas(pelada_id):
    """Listar temporadas de uma pelada"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        resultado, erro = TemporadaService.listar_temporadas(pelada_id, page, per_page)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>', methods=['GET'])
@jwt_required()
@temporada_owner_required
def obter_temporada(temporada_id):
    """Obter temporada por ID"""
    try:
        temporada, erro = TemporadaService.obter_temporada_por_id(temporada_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'temporada': temporada}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>/encerrar', methods=['POST'])
@jwt_required()
@temporada_owner_required
def encerrar_temporada(temporada_id):
    """Encerrar uma temporada"""
    try:
        temporada, erro = TemporadaService.encerrar_temporada(temporada_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Temporada encerrada com sucesso',
            'temporada': temporada
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE RODADAS ====================

@pelada_bp.route('/temporadas/<int:temporada_id>/rodadas', methods=['POST'])
@jwt_required()
@temporada_owner_required
def criar_rodada(temporada_id):
    """Criar uma nova rodada"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        data_rodada = dados.get('data_rodada')
        quantidade_times = dados.get('quantidade_times')
        jogadores_por_time = dados.get('jogadores_por_time')

        if not data_rodada or not quantidade_times or not jogadores_por_time:
            return jsonify({'erro': 'Data, quantidade de times e jogadores por time são obrigatórios'}), 400

        rodada, erro = RodadaService.criar_rodada(temporada_id, data_rodada, quantidade_times, jogadores_por_time)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Rodada criada com sucesso',
            'rodada': rodada
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>/rodadas', methods=['GET'])
@jwt_required()
@temporada_owner_required
def listar_rodadas(temporada_id):
    """Listar rodadas de uma temporada"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        resultado, erro = RodadaService.listar_rodadas(temporada_id, page, per_page)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/rodadas/<int:rodada_id>', methods=['GET'])
@jwt_required()
@rodada_owner_required
def obter_rodada(rodada_id):
    """Obter rodada por ID com times e jogadores"""
    try:
        rodada, erro = RodadaService.obter_rodada_por_id(rodada_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'rodada': rodada}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE JOGADORES DA RODADA ====================

@pelada_bp.route('/rodadas/<int:rodada_id>/jogadores', methods=['GET'])
def listar_jogadores_rodada(rodada_id):
    """Listar jogadores que participaram da rodada (via times das partidas)"""
    try:
        posicao = request.args.get('posicao')
        apenas_ativos = request.args.get('apenas_ativos', 'true').lower() != 'false'

        jogadores, erro = RodadaService.listar_jogadores_da_rodada(
            rodada_id=rodada_id,
            posicao=posicao,
            apenas_ativos=apenas_ativos
        )

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'jogadores': jogadores}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE TIMES ====================

@pelada_bp.route('/temporadas/<int:temporada_id>/times', methods=['POST'])
@jwt_required()
@temporada_owner_required
def criar_time(temporada_id):
    """
    Criar um novo time fixo na temporada
    
    Aceita multipart/form-data ou JSON:
    - nome (obrigatório)
    - cor (opcional)
    - escudo (opcional, arquivo de imagem) - apenas multipart
    """
    try:
        escudo_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            nome = request.form.get('nome')
            cor = request.form.get('cor')
            
            # Processar upload de escudo
            if 'escudo' in request.files:
                arquivo_escudo = request.files['escudo']
                if arquivo_escudo and arquivo_escudo.filename:
                    escudo_url = salvar_imagem_time(arquivo_escudo)
        else:
            dados = request.get_json(silent=True)
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400
            
            nome = dados.get('nome')
            cor = dados.get('cor')
            escudo_url = dados.get('escudo_url')  # Se vier URL já pronta

        if not nome:
            return jsonify({'erro': 'Nome é obrigatório'}), 400

        time, erro = TimeService.criar_time(temporada_id, nome, cor, escudo_url)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Time criado com sucesso',
            'time': time
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>/times', methods=['GET'])
@jwt_required()
@temporada_owner_required
def listar_times_temporada(temporada_id):
    """Listar todos os times de uma temporada"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        resultado, erro = TimeService.listar_times_da_temporada(temporada_id, page, per_page)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/times/<int:time_id>', methods=['GET'])
@jwt_required()
@time_owner_required
def obter_time(time_id):
    """Obter time por ID com jogadores"""
    try:
        time, erro = TimeService.obter_time_por_id(time_id)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'time': time}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/times/<int:time_id>', methods=['PUT'])
@jwt_required()
@time_owner_required
def atualizar_time(time_id):
    """
    Atualizar um time
    
    Aceita multipart/form-data ou JSON:
    - nome, cor (campos opcionais)
    - escudo (opcional, arquivo de imagem) - apenas multipart
    """
    try:
        escudo_url = None
        
        # Verificar se é multipart/form-data (upload de arquivo) ou JSON
        content_type = request.content_type or ''
        is_multipart = 'multipart/form-data' in content_type
        
        if is_multipart:
            dados = {}
            if request.form.get('nome'):
                dados['nome'] = request.form.get('nome')
            if request.form.get('cor'):
                dados['cor'] = request.form.get('cor')
            
            # Processar upload de escudo
            if 'escudo' in request.files:
                arquivo_escudo = request.files['escudo']
                if arquivo_escudo and arquivo_escudo.filename:
                    escudo_url = salvar_imagem_time(arquivo_escudo)
                    if escudo_url:
                        dados['escudo_url'] = escudo_url
        else:
            dados = request.get_json(silent=True)
            if not dados:
                return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        time, erro = TimeService.atualizar_time(time_id, dados)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Time atualizado com sucesso',
            'time': time
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/times/<int:time_id>/jogadores', methods=['POST'])
@jwt_required()
@time_owner_required
def adicionar_jogador_time(time_id):
    """Adicionar um jogador ao time"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        jogador_id = dados.get('jogador_id')
        capitao = dados.get('capitao', False)
        posicao = dados.get('posicao')

        if not jogador_id:
            return jsonify({'erro': 'ID do jogador é obrigatório'}), 400

        resultado, erro = TimeService.adicionar_jogador_ao_time(time_id, jogador_id, capitao, posicao)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/times/<int:time_id>/jogadores/<int:jogador_id>', methods=['DELETE'])
@jwt_required()
@time_owner_required
def remover_jogador_time(time_id, jogador_id):
    """Remover um jogador do time"""
    try:
        resultado, erro = TimeService.remover_jogador_do_time(time_id, jogador_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE PARTIDAS ====================

@pelada_bp.route('/rodadas/<int:rodada_id>/partidas', methods=['POST'])
@jwt_required()
@rodada_owner_required
def criar_partida(rodada_id):
    """Criar uma nova partida"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        time_casa_id = dados.get('time_casa_id')
        time_fora_id = dados.get('time_fora_id')

        if not time_casa_id or not time_fora_id:
            return jsonify({'erro': 'IDs dos times (casa e fora) são obrigatórios'}), 400

        partida, erro = PartidaService.criar_partida(rodada_id, time_casa_id, time_fora_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Partida criada com sucesso',
            'partida': partida
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/rodadas/<int:rodada_id>/partidas', methods=['GET'])
@jwt_required()
@rodada_owner_required
def listar_partidas(rodada_id):
    """Listar todas as partidas de uma rodada"""
    try:
        partidas, erro = PartidaService.listar_partidas(rodada_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({'partidas': partidas}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/partidas/<int:partida_id>', methods=['GET'])
@jwt_required()
@partida_owner_required
def obter_partida(partida_id):
    """Obter partida por ID"""
    try:
        partida, erro = PartidaService.obter_partida_por_id(partida_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'partida': partida}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/partidas/<int:partida_id>/iniciar', methods=['POST'])
@jwt_required()
@partida_owner_required
def iniciar_partida(partida_id):
    """Iniciar uma partida"""
    try:
        partida, erro = PartidaService.iniciar_partida(partida_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Partida iniciada com sucesso',
            'partida': partida
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/partidas/<int:partida_id>/finalizar', methods=['POST'])
@jwt_required()
@partida_owner_required
def finalizar_partida(partida_id):
    """Finalizar uma partida e calcular pontuação"""
    try:
        partida, erro = PartidaService.finalizar_partida(partida_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Partida finalizada com sucesso',
            'partida': partida
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE GOLS ====================

@pelada_bp.route('/partidas/<int:partida_id>/gols', methods=['POST'])
@jwt_required()
@partida_owner_required
def registrar_gol(partida_id):
    """Registrar um gol"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        time_id = dados.get('time_id')
        jogador_id = dados.get('jogador_id')
        minuto = dados.get('minuto')
        gol_contra = dados.get('gol_contra', False)
        assistencia_id = dados.get('assistencia_id')

        if not time_id or not jogador_id:
            return jsonify({'erro': 'ID do time e do jogador são obrigatórios'}), 400

        gol, erro = GolService.registrar_gol(partida_id, time_id, jogador_id, minuto, gol_contra, assistencia_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Gol registrado com sucesso',
            'gol': gol
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/gols/<int:gol_id>', methods=['DELETE'])
@jwt_required()
@gol_owner_required
def remover_gol(gol_id):
    """Remover um gol"""
    try:
        resultado, erro = GolService.remover_gol(gol_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE RANKINGS ====================

@pelada_bp.route('/temporadas/<int:temporada_id>/ranking/times', methods=['GET'])
def ranking_times(temporada_id):
    """Ranking de times por pontos na temporada"""
    try:
        ranking, erro = RankingService.ranking_times_temporada(temporada_id)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({'ranking': ranking}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>/ranking/artilheiros', methods=['GET'])
def ranking_artilheiros(temporada_id):
    """Ranking de artilheiros na temporada"""
    try:
        limit = request.args.get('limit', 10, type=int)
        ranking, erro = RankingService.ranking_artilheiros_temporada(temporada_id, limit)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({'ranking': ranking}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/temporadas/<int:temporada_id>/ranking/assistencias', methods=['GET'])
def ranking_assistencias(temporada_id):
    """Ranking de assistências na temporada"""
    try:
        limit = request.args.get('limit', 10, type=int)
        ranking, erro = RankingService.ranking_assistencias_temporada(temporada_id, limit)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({'ranking': ranking}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== ROTAS DE VOTAÇÕES ====================

@pelada_bp.route('/rodadas/<int:rodada_id>/votacoes', methods=['GET'])
def listar_votacoes_rodada(rodada_id):
    """Listar votações de uma rodada"""
    try:
        tipo = request.args.get('tipo')
        resultado, erro = VotacaoService.listar_votacoes_rodada(rodada_id, tipo=tipo)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/rodadas/<int:rodada_id>/votacoes', methods=['POST'])
@jwt_required()
@rodada_owner_required
def criar_votacao(rodada_id):
    """Criar uma nova votação"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        abre_em = dados.get('abre_em')
        fecha_em = dados.get('fecha_em')
        tipo = dados.get('tipo')

        if not abre_em or not fecha_em or not tipo:
            return jsonify({'erro': 'Abertura, fechamento e tipo são obrigatórios'}), 400

        votacao, erro = VotacaoService.criar_votacao(rodada_id, abre_em, fecha_em, tipo)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Votação criada com sucesso',
            'votacao': votacao
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/votacoes/<int:votacao_id>', methods=['GET'])
def obter_votacao(votacao_id):
    """Obter uma votação por ID"""
    try:
        votacao, erro = VotacaoService.obter_votacao(votacao_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify(votacao), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/votacoes/<int:votacao_id>/votar', methods=['POST'])
def registrar_voto(votacao_id):
    """Registrar um voto"""
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        jogador_votante_id = dados.get('jogador_votante_id')
        jogador_votado_id = dados.get('jogador_votado_id')
        pontos = dados.get('pontos')

        if not jogador_votante_id or not jogador_votado_id or pontos is None:
            return jsonify({'erro': 'IDs dos jogadores e pontos são obrigatórios'}), 400

        voto, erro = VotacaoService.registrar_voto(votacao_id, jogador_votante_id, jogador_votado_id, pontos)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify({
            'mensagem': 'Voto registrado com sucesso',
            'voto': voto
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/votacoes/<int:votacao_id>/resultado', methods=['GET'])
def obter_resultado_votacao(votacao_id):
    """Obter resultado agregado de uma votação"""
    try:
        resultado, erro = VotacaoService.resultado_votacao(votacao_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        # Compatibilidade com front: expor campos principais também no topo
        return jsonify({
            'votacao': resultado,
            'total_votos': resultado.get('total_votos'),
            'resultado': resultado.get('resultado', []),
            'vencedor': resultado.get('vencedor')
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/rodadas/<int:rodada_id>/votacoes/resultados', methods=['GET'])
def obter_resultados_votacoes_rodada(rodada_id):
    """Obter resultados agregados de todas as votações de uma rodada"""
    try:
        tipo = request.args.get('tipo')
        resultado, erro = VotacaoService.resultados_votacoes_da_rodada(rodada_id, tipo=tipo)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@pelada_bp.route('/votacoes/<int:votacao_id>/encerrar', methods=['POST'])
@jwt_required()
@votacao_owner_required
def encerrar_votacao(votacao_id):
    """Encerrar uma votação"""
    try:
        votacao, erro = VotacaoService.encerrar_votacao(votacao_id)

        if erro:
            codigo_status = 404 if 'não encontrada' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Votação encerrada com sucesso',
            'votacao': votacao
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
