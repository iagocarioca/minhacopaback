# -*- coding: utf-8 -*-
from source.extensions.extensios import db
from source.domain.users.models import User
from source.utils.pagination import paginate
from flask_jwt_extended import create_access_token, create_refresh_token


class UserService:
    """Camada de serviço para lógica de negócios relacionada a usuários"""

    @staticmethod
    def criar_usuario(nome_usuario, email, senha):
        """
        Criar um novo usuário

        Args:
            nome_usuario: Nome de usuário do usuário
            email: Email do usuário
            senha: Senha do usuário (será criptografada)

        Returns:
            tuple: (dicionario_usuario, mensagem_erro)

        Raises:
            Exception: Se a operação no banco de dados falhar
        """
        # Verificar se o nome de usuário já existe
        if User.query.filter_by(username=nome_usuario).first():
            return None, 'Nome de usuário já existe'

        # Verificar se o email já existe
        if User.query.filter_by(email=email).first():
            return None, 'Email já existe'

        # Criar novo usuário
        try:
            novo_usuario = User(username=nome_usuario, email=email, password=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            return novo_usuario.to_dict(), None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def autenticar_usuario(nome_usuario, senha):
        """
        Autenticar um usuário e gerar tokens

        Args:
            nome_usuario: Nome de usuário do usuário
            senha: Senha do usuário

        Returns:
            tuple: (dicionario_dados_autenticacao, mensagem_erro)
            dicionario_dados_autenticacao contém: token_acesso, token_atualizacao, usuario
        """
        usuario = User.query.filter_by(username=nome_usuario).first()

        if not usuario or not usuario.check_password(senha):
            return None, 'Credenciais inválidas'

        # Criar tokens JWT - CORREÇÃO: Converter user.id para string
        token_acesso = create_access_token(identity=str(usuario.id))
        token_atualizacao = create_refresh_token(identity=str(usuario.id))

        return {
            'token_acesso': token_acesso,
            'token_atualizacao': token_atualizacao,
            'usuario': usuario.to_dict()
        }, None

    @staticmethod
    def obter_usuario_por_id(id_usuario):
        """
        Obter usuário por ID

        Args:
            id_usuario: ID do usuário (pode ser string ou int)

        Returns:
            tuple: (dicionario_usuario, mensagem_erro)
        """
        try:
            # Converter para int se for uma string
            id_usuario = int(id_usuario)
            usuario = User.query.get(id_usuario)

            if not usuario:
                return None, 'Usuário não encontrado'

            return usuario.to_dict(), None
        except (ValueError, TypeError):
            return None, 'ID de usuário inválido'


    @staticmethod
    def atualizar_token_acesso(id_usuario):
        """
        Gerar um novo token de acesso

        Args:
            id_usuario: ID do usuário (pode ser string ou int)

        Returns:
            tuple: (dicionario_token, mensagem_erro)
        """
        try:
            # Verificar se o usuário existe
            id_usuario = int(id_usuario)
            usuario = User.query.get(id_usuario)

            if not usuario:
                return None, 'Usuário não encontrado'

            token_acesso = create_access_token(identity=str(id_usuario))
            return {'token_acesso': token_acesso}, None
        except (ValueError, TypeError):
            return None, 'ID de usuário inválido'
        
    
        
    @staticmethod
    def _serializar_usuario(usuario):
        """
        Serializa um usuário com suas informações

        Args:
            usuario: Objeto User

        Returns:
            dict: Dicionário com dados do usuário
        """
        return {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'status': usuario.status,
            'tipo_usuario': usuario.tipo_usuario,
            'created_at': usuario.created_at.isoformat() if usuario.created_at else None,
            'updated_at': usuario.updated_at.isoformat() if usuario.updated_at else None
        }

    @staticmethod
    def listar_todos_usuarios(page=1, per_page=10):
        """
        Listar todos os usuários com paginação

        Args:
            page: Número da página (padrão: 1)
            per_page: Itens por página (padrão: 10)

        Returns:
            tuple: (dicionario_resposta_paginada, mensagem_erro)
        """
        try:
            query = User.query

            # Aplicar paginação padronizada
            resultado_paginado = paginate(query, page, per_page)

            # Serializar usuários
            usuarios_serializados = [
                UserService._serializar_usuario(usuario)
                for usuario in resultado_paginado['data']
            ]

            return {
                'data': usuarios_serializados,
                'meta': resultado_paginado['meta']
            }, None

        except Exception as e:
            return None, str(e)
