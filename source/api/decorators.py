# -*- coding: utf-8 -*-
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from source.domain.users.models import User
from source.extensions.extensios import db
from source.domain.peladas.models import (
    Pelada, Temporada, Rodada, Time, Jogador, Partida, Gol, Votacao
)


def afiliado_required(f):
    """
    Decorador para verificar se o usuário é AFILIADO

    Uso:
        @afiliado_required
        def minha_rota():
            ...
    """
    @wraps(f)
    def decorador(*args, **kwargs):
      
        id_usuario = get_jwt_identity()
        usuario = User.query.get(int(id_usuario))

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario.tipo_usuario != 'afiliado':
            return jsonify({'erro': 'Acesso negado. Apenas afiliados podem acessar'}), 403

        return f(*args, **kwargs)

    return decorador


def admin_required(f):
    """
    Decorador para verificar se o usuário é ADMIN

    Uso:
        @admin_required
        def minha_rota():
            ...
    """
    @wraps(f)
    def decorador(*args, **kwargs):

        id_usuario = get_jwt_identity()
        usuario = User.query.get(int(id_usuario))

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario.tipo_usuario != 'admin':
            return jsonify({'erro': 'Acesso negado. Apenas administradores podem acessar'}), 403

        return f(*args, **kwargs)

    return decorador


def produtor_required(f):
    """
    Decorador para verificar se o usuário é PRODUTOR

    Uso:
        @produtor_required
        def minha_rota():
            ...
    """
    @wraps(f)
    def decorador(*args, **kwargs):
        id_usuario = get_jwt_identity()
        usuario = User.query.get(int(id_usuario))

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario.tipo_usuario != 'produtor':
            return jsonify({'erro': 'Acesso negado. Apenas produtores podem acessar'}), 403

        return f(*args, **kwargs)

    return decorador


def tipo_usuario_required(*tipos_permitidos):
    """
    Decorador GENÉRICO para verificar múltiplos tipos de usuário

    Uso:
        @tipo_usuario_required('admin', 'produtor')
        def minha_rota():
            ...
    """
    def decorador_real(f):
        @wraps(f)
        def decorador(*args, **kwargs):
            # Pegar o ID do usuário do token JWT
            id_usuario = get_jwt_identity()
            usuario = User.query.get(int(id_usuario))
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404

            if usuario.tipo_usuario not in tipos_permitidos:
                tipos_str = ', '.join(tipos_permitidos)
                return jsonify({
                    'erro': f'Acesso negado. Apenas {tipos_str} podem acessar'
                }), 403

            return f(*args, **kwargs)

        return decorador

    return decorador_real


# ==================== ESCOPO DE ACESSO (PELADAS) ====================
# Regra: o usuário só pode acessar/alterar recursos dentro de peladas onde ele é o gerente (criador).

def _usuario_logado_id():
    id_usuario = get_jwt_identity()
    try:
        return int(id_usuario)
    except (ValueError, TypeError):
        return None


def _acesso_negado():
    return jsonify({'erro': 'Acesso negado. Recurso fora do seu escopo.'}), 403


def pelada_owner_required(f):
    """Garante que `pelada_id` do path pertence ao usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        pelada_id = kwargs.get('pelada_id')
        if not usuario_id or pelada_id is None:
            return _acesso_negado()

        existe = db.session.query(Pelada.id).filter(
            Pelada.id == int(pelada_id),
            Pelada.usuario_gerente_id == int(usuario_id)
        ).first()

        if not existe:
            return _acesso_negado()

        return f(*args, **kwargs)
    return decorador


def jogador_owner_required(f):
    """Garante que `jogador_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        jogador_id = kwargs.get('jogador_id')
        if not usuario_id or jogador_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Jogador.id)
            .join(Pelada, Jogador.pelada_id == Pelada.id)
            .filter(Jogador.id == int(jogador_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def temporada_owner_required(f):
    """Garante que `temporada_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        temporada_id = kwargs.get('temporada_id')
        if not usuario_id or temporada_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Temporada.id == int(temporada_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def rodada_owner_required(f):
    """Garante que `rodada_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        rodada_id = kwargs.get('rodada_id')
        if not usuario_id or rodada_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Rodada.id)
            .join(Temporada, Rodada.temporada_id == Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Rodada.id == int(rodada_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def time_owner_required(f):
    """Garante que `time_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        time_id = kwargs.get('time_id')
        if not usuario_id or time_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Time.id)
            .join(Temporada, Time.temporada_id == Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Time.id == int(time_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def partida_owner_required(f):
    """Garante que `partida_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        partida_id = kwargs.get('partida_id')
        if not usuario_id or partida_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Partida.id)
            .join(Rodada, Partida.rodada_id == Rodada.id)
            .join(Temporada, Rodada.temporada_id == Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Partida.id == int(partida_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def gol_owner_required(f):
    """Garante que `gol_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        gol_id = kwargs.get('gol_id')
        if not usuario_id or gol_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Gol.id)
            .join(Partida, Gol.partida_id == Partida.id)
            .join(Rodada, Partida.rodada_id == Rodada.id)
            .join(Temporada, Rodada.temporada_id == Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Gol.id == int(gol_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador


def votacao_owner_required(f):
    """Garante que `votacao_id` pertence a uma pelada do usuário logado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_id = _usuario_logado_id()
        votacao_id = kwargs.get('votacao_id')
        if not usuario_id or votacao_id is None:
            return _acesso_negado()

        existe = (
            db.session.query(Votacao.id)
            .join(Rodada, Votacao.rodada_id == Rodada.id)
            .join(Temporada, Rodada.temporada_id == Temporada.id)
            .join(Pelada, Temporada.pelada_id == Pelada.id)
            .filter(Votacao.id == int(votacao_id), Pelada.usuario_gerente_id == int(usuario_id))
            .first()
        )
        if not existe:
            return _acesso_negado()
        return f(*args, **kwargs)
    return decorador
