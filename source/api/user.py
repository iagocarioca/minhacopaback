# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from source.domain.users.services import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from source.api.decorators import admin_required, produtor_required, afiliado_required, tipo_usuario_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/registrar', methods=['POST'])
def registrar():
    """Registrar um novo usuário"""
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        nome_usuario = dados.get('username')
        email = dados.get('email')
        senha = dados.get('password')

        if not nome_usuario or not email or not senha:
            return jsonify({'erro': 'Nome de usuário, email e senha são obrigatórios'}), 400

        usuario, erro = UserService.criar_usuario(nome_usuario, email, senha)

        if erro:
            codigo_status = 409 if 'já existe' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'usuario': usuario
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Autenticar usuário e retornar tokens"""
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400

        nome_usuario = dados.get('username')
        senha = dados.get('password')

        if not nome_usuario or not senha:
            return jsonify({'erro': 'Nome de usuário e senha são obrigatórios'}), 400

        dados_autenticacao, erro = UserService.autenticar_usuario(nome_usuario, senha)

        if erro:
            return jsonify({'erro': erro}), 401

        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            **dados_autenticacao
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def obter_usuario_atual():
    """Obter todas as informações do usuário autenticado atual"""
    try:
        id_usuario_atual = get_jwt_identity()

        usuario, erro = UserService.obter_usuario_por_id(id_usuario_atual)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'usuario': usuario}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def atualizar():
    """Atualizar token de acesso"""
    try:
        id_usuario_atual = get_jwt_identity()

        dados_token, erro = UserService.atualizar_token_acesso(id_usuario_atual)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify(dados_token), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/atualizar/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(usuario_id):
    """Atualizar informações do usuário"""
    try:
        perfil_data = request.get_json()

        if not perfil_data:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400
        
        usuario_atualizado, erro = UserService.add_perfil_usuario(usuario_id, perfil_data)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario_atualizado
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@user_bp.route('/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obter_usuario_por_id(usuario_id):
    """Obter informações do usuário por ID"""
    try:

        usuario, erro = UserService.obter_usuario_por_id(usuario_id)

        if erro:
            codigo_status = 404 if 'não encontrado' in erro else 400
            return jsonify({'erro': erro}), codigo_status

        return jsonify({'usuario': usuario}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/listar', methods=['GET'])
@jwt_required()
def listar_usuarios():
    """Listar todos os usuários com paginação - APENAS ADMIN"""
    try:
       
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        resultado, erro = UserService.listar_todos_usuarios(page, per_page)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

