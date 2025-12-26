# -*- coding: utf-8 -*-
from source.extensions.extensios import db
from source.domain.peladas.models import (
    Pelada, Jogador, Temporada, Rodada, Time, TimeJogador,
    Partida, Gol, Votacao, Voto, get_brazil_time
)
from source.utils.pagination import paginate
from datetime import datetime, date
from sqlalchemy import func, desc, case
import pytz

# Posição agora é armazenada como string (nome) diretamente no banco


class PeladaService:
    """Camada de serviço para lógica de negócios relacionada a peladas"""

    @staticmethod
    def criar_pelada(nome, cidade, usuario_gerente_id, fuso_horario='America/Sao_Paulo', logo_url=None, perfil_url=None):
        """Criar uma nova pelada"""
        try:
            nova_pelada = Pelada(
                nome=nome,
                cidade=cidade,
                usuario_gerente_id=usuario_gerente_id,
                fuso_horario=fuso_horario
            )
            if logo_url:
                nova_pelada.logo_url = logo_url
            if perfil_url:
                nova_pelada.perfil_url = perfil_url
            
            db.session.add(nova_pelada)
            db.session.commit()
            return PeladaService._serializar_pelada(nova_pelada), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_pelada_por_id(pelada_id):
        """Obter pelada por ID"""
        try:
            pelada = Pelada.query.get(int(pelada_id))
            if not pelada:
                return None, 'Pelada não encontrada'
            return PeladaService._serializar_pelada(pelada), None
        except (ValueError, TypeError):
            return None, 'ID de pelada inválido'

    @staticmethod
    def obter_perfil_pelada(pelada_id):
        """Obter perfil completo da pelada com gerente, jogadores, temporadas e estatísticas"""
        try:
            pelada = Pelada.query.get(int(pelada_id))
            if not pelada:
                return None, 'Pelada não encontrada'

            jogadores = Jogador.query.filter_by(pelada_id=pelada_id, ativo=True).all()
            temporadas = Temporada.query.filter_by(pelada_id=pelada_id).order_by(Temporada.criado_em.desc()).all()

            total_jogadores = len(jogadores)
            total_temporadas = len(temporadas)

            temporada_ativa = Temporada.query.filter_by(pelada_id=pelada_id, status='ativa').first()

            rodadas_realizadas = 0
            partidas_realizadas = 0
            if temporada_ativa:
                rodadas_realizadas = Rodada.query.filter_by(temporada_id=temporada_ativa.id).count()
                partidas_realizadas = db.session.query(Partida).join(Rodada).filter(
                    Rodada.temporada_id == temporada_ativa.id,
                    Partida.status == 'finalizada'
                ).count()

            perfil = {
                'pelada': PeladaService._serializar_pelada(pelada),  # Usa serialização completa com logo_url e perfil_url
                'gerente': {
                    'id': pelada.gerente.id,
                    'username': pelada.gerente.username,
                    'email': pelada.gerente.email
                } if pelada.gerente else None,
                'estatisticas': {
                    'total_jogadores': total_jogadores,
                    'total_temporadas': total_temporadas,
                    'rodadas_realizadas': rodadas_realizadas,
                    'partidas_realizadas': partidas_realizadas
                },
                'jogadores': [
                    {
                        'id': j.id,
                        'nome_completo': j.nome_completo,
                        'apelido': j.apelido,
                        'telefone': j.telefone,
                        'foto_url': j.foto_url,
                        'criado_em': j.criado_em.isoformat() if j.criado_em else None
                    } for j in jogadores
                ],
                'temporadas': [
                    {
                        'id': t.id,
                        'inicio_mes': t.inicio_mes.isoformat() if t.inicio_mes else None,
                        'fim_mes': t.fim_mes.isoformat() if t.fim_mes else None,
                        'status': t.status,
                        'criado_em': t.criado_em.isoformat() if t.criado_em else None
                    } for t in temporadas[:5]
                ],
                'temporada_ativa': {
                    'id': temporada_ativa.id,
                    'inicio_mes': temporada_ativa.inicio_mes.isoformat() if temporada_ativa.inicio_mes else None,
                    'fim_mes': temporada_ativa.fim_mes.isoformat() if temporada_ativa.fim_mes else None,
                    'status': temporada_ativa.status
                } if temporada_ativa else None
            }

            return perfil, None
        except (ValueError, TypeError):
            return None, 'ID de pelada inválido'
        except Exception as e:
            return None, str(e)

    @staticmethod
    def listar_peladas(page=1, per_page=10, usuario_id=None, ativa=None):
        """Listar peladas com filtros opcionais"""
        try:
            query = Pelada.query

            if usuario_id:
                query = query.filter_by(usuario_gerente_id=usuario_id)
            if ativa is not None:
                query = query.filter_by(ativa=ativa)

            resultado_paginado = paginate(query, page, per_page)

            peladas_serializadas = [
                PeladaService._serializar_pelada(pelada)
                for pelada in resultado_paginado['data']
            ]

            return {
                'data': peladas_serializadas,
                'meta': resultado_paginado['meta']
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def atualizar_pelada(pelada_id, dados):
        """Atualizar uma pelada"""
        try:
            pelada = Pelada.query.get(int(pelada_id))
            if not pelada:
                return None, 'Pelada não encontrada'

            if 'nome' in dados:
                pelada.nome = dados['nome']
            if 'cidade' in dados:
                pelada.cidade = dados['cidade']
            if 'fuso_horario' in dados:
                pelada.fuso_horario = dados['fuso_horario']
            if 'ativa' in dados:
                pelada.ativa = dados['ativa']
            if 'logo_url' in dados:
                pelada.logo_url = dados['logo_url']
            if 'perfil_url' in dados:
                pelada.perfil_url = dados['perfil_url']

            db.session.commit()
            return PeladaService._serializar_pelada(pelada), None
        except (ValueError, TypeError):
            db.session.rollback()
            return None, 'ID de pelada inválido'
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def _serializar_pelada(pelada):
        """Serializa uma pelada para dicionário"""
        return {
            'id': pelada.id,
            'nome': pelada.nome,
            'cidade': pelada.cidade,
            'fuso_horario': pelada.fuso_horario,
            'ativa': pelada.ativa,
            'usuario_gerente_id': pelada.usuario_gerente_id,
            'logo_url': pelada.logo_url,
            'perfil_url': pelada.perfil_url,
            'criado_em': pelada.criado_em.isoformat() if pelada.criado_em else None
        }


class JogadorService:
    """Camada de serviço para lógica de negócios relacionada a jogadores"""

    @staticmethod
    def criar_jogador(pelada_id, nome_completo, apelido=None, telefone=None, foto_url=None):
        """Criar um novo jogador"""
        try:
            novo_jogador = Jogador(
                pelada_id=pelada_id,
                nome_completo=nome_completo,
                apelido=apelido,
                telefone=telefone
            )
            if foto_url:
                novo_jogador.foto_url = foto_url
            db.session.add(novo_jogador)
            db.session.commit()
            return JogadorService._serializar_jogador(novo_jogador), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_jogador_por_id(jogador_id):
        """Obter jogador por ID"""
        try:
            jogador = Jogador.query.get(int(jogador_id))
            if not jogador:
                return None, 'Jogador não encontrado'
            return JogadorService._serializar_jogador(jogador), None
        except (ValueError, TypeError):
            return None, 'ID de jogador inválido'

    @staticmethod
    def listar_jogadores(pelada_id, page=1, per_page=20, ativo=None):
        """Listar jogadores de uma pelada"""
        try:
            query = Jogador.query.filter_by(pelada_id=pelada_id)

            if ativo is not None:
                query = query.filter_by(ativo=ativo)

            resultado_paginado = paginate(query, page, per_page)

            jogadores_serializados = [
                JogadorService._serializar_jogador(jogador)
                for jogador in resultado_paginado['data']
            ]

            return {
                'data': jogadores_serializados,
                'meta': resultado_paginado['meta']
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def atualizar_jogador(jogador_id, dados):
        """Atualizar um jogador"""
        try:
            jogador = Jogador.query.get(int(jogador_id))
            if not jogador:
                return None, 'Jogador não encontrado'

            if 'nome_completo' in dados:
                jogador.nome_completo = dados['nome_completo']
            if 'apelido' in dados:
                jogador.apelido = dados['apelido']
            if 'telefone' in dados:
                jogador.telefone = dados['telefone']
            if 'ativo' in dados:
                jogador.ativo = dados['ativo']
            if 'foto_url' in dados:
                jogador.foto_url = dados['foto_url']

            db.session.commit()
            return JogadorService._serializar_jogador(jogador), None
        except (ValueError, TypeError):
            db.session.rollback()
            return None, 'ID de jogador inválido'
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def _serializar_jogador(jogador):
        """Serializa um jogador para dicionário"""
        return {
            'id': jogador.id,
            'pelada_id': jogador.pelada_id,
            'nome_completo': jogador.nome_completo,
            'apelido': jogador.apelido,
            'telefone': jogador.telefone,
            'foto_url': jogador.foto_url,
            'ativo': jogador.ativo,
            'criado_em': jogador.criado_em.isoformat() if jogador.criado_em else None
        }


class TemporadaService:
    """Camada de serviço para lógica de negócios relacionada a temporadas"""

    @staticmethod
    def criar_temporada(pelada_id, inicio_mes, fim_mes):
        """Criar uma nova temporada"""
        try:
            temporada_ativa = Temporada.query.filter_by(pelada_id=pelada_id, status='ativa').first()
            if temporada_ativa:
                return None, 'Já existe uma temporada ativa. Encerre-a antes de criar uma nova.'

            nova_temporada = Temporada(
                pelada_id=pelada_id,
                inicio_mes=datetime.strptime(inicio_mes, '%Y-%m-%d').date() if isinstance(inicio_mes, str) else inicio_mes,
                fim_mes=datetime.strptime(fim_mes, '%Y-%m-%d').date() if isinstance(fim_mes, str) else fim_mes
            )
            db.session.add(nova_temporada)
            db.session.commit()
            return TemporadaService._serializar_temporada(nova_temporada), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_temporada_por_id(temporada_id):
        """Obter temporada por ID"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'
            return TemporadaService._serializar_temporada(temporada), None
        except (ValueError, TypeError):
            return None, 'ID de temporada inválido'

    @staticmethod
    def listar_temporadas(pelada_id, page=1, per_page=10):
        """Listar temporadas de uma pelada"""
        try:
            query = Temporada.query.filter_by(pelada_id=pelada_id).order_by(Temporada.criado_em.desc())

            resultado_paginado = paginate(query, page, per_page)

            temporadas_serializadas = [
                TemporadaService._serializar_temporada(temporada)
                for temporada in resultado_paginado['data']
            ]

            return {
                'data': temporadas_serializadas,
                'meta': resultado_paginado['meta']
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def encerrar_temporada(temporada_id):
        """Encerrar uma temporada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            temporada.status = 'encerrada'
            db.session.commit()
            return TemporadaService._serializar_temporada(temporada), None
        except (ValueError, TypeError):
            db.session.rollback()
            return None, 'ID de temporada inválido'
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def _serializar_temporada(temporada):
        """Serializa uma temporada para dicionário"""
        return {
            'id': temporada.id,
            'pelada_id': temporada.pelada_id,
            'inicio_mes': temporada.inicio_mes.isoformat() if temporada.inicio_mes else None,
            'fim_mes': temporada.fim_mes.isoformat() if temporada.fim_mes else None,
            'status': temporada.status,
            'criado_em': temporada.criado_em.isoformat() if temporada.criado_em else None
        }


class RodadaService:
    """Camada de serviço para lógica de negócios relacionada a rodadas"""

    @staticmethod
    def criar_rodada(temporada_id, data_rodada, quantidade_times, jogadores_por_time):
        """Criar uma nova rodada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            if temporada.status != 'ativa':
                return None, 'Temporada não está ativa'

            nova_rodada = Rodada(
                temporada_id=temporada_id,
                data_rodada=datetime.strptime(data_rodada, '%Y-%m-%d').date() if isinstance(data_rodada, str) else data_rodada,
                quantidade_times=quantidade_times,
                jogadores_por_time=jogadores_por_time
            )
            db.session.add(nova_rodada)
            db.session.commit()
            return RodadaService._serializar_rodada(nova_rodada), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_rodada_por_id(rodada_id):
        """Obter rodada por ID com partidas"""
        try:
            rodada = Rodada.query.get(int(rodada_id))
            if not rodada:
                return None, 'Rodada não encontrada'

            # Obter partidas da rodada ao invés de times
            partidas = Partida.query.filter_by(rodada_id=rodada_id).all()

            rodada_data = RodadaService._serializar_rodada(rodada)
            rodada_data['partidas'] = [PartidaService._serializar_partida(partida) for partida in partidas]

            return rodada_data, None
        except (ValueError, TypeError):
            return None, 'ID de rodada inválido'

    @staticmethod
    def listar_rodadas(temporada_id, page=1, per_page=10):
        """Listar rodadas de uma temporada"""
        try:
            query = Rodada.query.filter_by(temporada_id=temporada_id).order_by(Rodada.data_rodada.desc())

            resultado_paginado = paginate(query, page, per_page)

            rodadas_serializadas = [
                RodadaService._serializar_rodada(rodada)
                for rodada in resultado_paginado['data']
            ]

            return {
                'data': rodadas_serializadas,
                'meta': resultado_paginado['meta']
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def listar_jogadores_da_rodada(rodada_id, posicao=None, apenas_ativos=True):
        """
        Lista jogadores associados aos times que participaram da rodada (via partidas).

        Retorno: lista de dicts com: id, nome_completo, apelido, posicao, time_id, time_nome
        """
        try:
            rodada = Rodada.query.get(int(rodada_id))
            if not rodada:
                return None, 'Rodada não encontrada'

            partidas = Partida.query.filter_by(rodada_id=rodada_id).all()
            if not partidas:
                return [], None

            time_ids = set()
            for p in partidas:
                if p.time_casa_id:
                    time_ids.add(p.time_casa_id)
                if p.time_fora_id:
                    time_ids.add(p.time_fora_id)

            if not time_ids:
                return [], None

            # Aceitar o nome que vier para filtro
            posicao_filtro = posicao
            if isinstance(posicao_filtro, str):
                posicao_filtro = posicao_filtro.strip()
                if posicao_filtro == '':
                    posicao_filtro = None

            query = (
                db.session.query(TimeJogador, Jogador, Time)
                .join(Jogador, TimeJogador.jogador_id == Jogador.id)
                .join(Time, TimeJogador.time_id == Time.id)
                .filter(TimeJogador.time_id.in_(list(time_ids)))
            )

            if apenas_ativos:
                query = query.filter(Jogador.ativo == True)  # noqa: E712

            if posicao_filtro is not None:
                query = query.filter(TimeJogador.posicao == posicao_filtro)

            # MySQL/MariaDB não suporta "NULLS LAST". Usamos CASE para ordenar NULL por último.
            posicao_null_ultimo = case((TimeJogador.posicao.is_(None), 1), else_=0)
            rows = query.order_by(
                Time.id.asc(),
                posicao_null_ultimo.asc(),
                TimeJogador.posicao.asc(),
                Jogador.nome_completo.asc()
            ).all()

            jogadores = []
            for tj, j, t in rows:
                jogadores.append({
                    'id': j.id,
                    'nome_completo': j.nome_completo,
                    'apelido': j.apelido,
                    'foto_url': j.foto_url,
                    'posicao': tj.posicao,  # Retorna o nome que foi salvo
                    'time_id': t.id,
                    'time_nome': t.nome,
                    'time_escudo_url': t.escudo_url
                })

            return jogadores, None
        except (ValueError, TypeError):
            return None, 'ID de rodada inválido'
        except Exception as e:
            return None, str(e)

    @staticmethod
    def _serializar_rodada(rodada):
        """Serializa uma rodada para dicionário"""
        return {
            'id': rodada.id,
            'temporada_id': rodada.temporada_id,
            'data_rodada': rodada.data_rodada.isoformat() if rodada.data_rodada else None,
            'quantidade_times': rodada.quantidade_times,
            'jogadores_por_time': rodada.jogadores_por_time,
            'status': rodada.status,
            'criado_em': rodada.criado_em.isoformat() if rodada.criado_em else None
        }


class TimeService:
    """Camada de serviço para lógica de negócios relacionada a times"""

    @staticmethod
    def criar_time(temporada_id, nome, cor=None, escudo_url=None):
        """Criar um novo time fixo na temporada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            if temporada.status != 'ativa':
                return None, 'Temporada não está ativa'

            novo_time = Time(
                temporada_id=temporada_id,
                nome=nome,
                cor=cor
            )
            if escudo_url:
                novo_time.escudo_url = escudo_url
            db.session.add(novo_time)
            db.session.commit()
            return TimeService._serializar_time(novo_time), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def adicionar_jogador_ao_time(time_id, jogador_id, capitao=False, posicao=None):
        """Adicionar um jogador ao time
        
        Args:
            posicao: nome da posição (ex: 'Goleiro', 'Atacante') - aceita qualquer string
        """
        try:
            time = Time.query.get(int(time_id))
            if not time:
                return None, 'Time não encontrado'

            jogador = Jogador.query.get(int(jogador_id))
            if not jogador:
                return None, 'Jogador não encontrado'

            ja_no_time = TimeJogador.query.filter_by(time_id=time_id, jogador_id=jogador_id).first()
            if ja_no_time:
                return None, 'Jogador já está neste time'

            # Aceitar o nome que vier, sem conversão
            posicao_nome = posicao.strip() if posicao and isinstance(posicao, str) else posicao

            time_jogador = TimeJogador(
                time_id=time_id,
                jogador_id=jogador_id,
                capitao=capitao,
                posicao=posicao_nome
            )
            db.session.add(time_jogador)
            db.session.commit()
            return {'mensagem': 'Jogador adicionado ao time com sucesso'}, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def remover_jogador_do_time(time_id, jogador_id):
        """Remover um jogador do time"""
        try:
            time_jogador = TimeJogador.query.filter_by(time_id=time_id, jogador_id=jogador_id).first()
            if not time_jogador:
                return None, 'Jogador não encontrado neste time'

            db.session.delete(time_jogador)
            db.session.commit()
            return {'mensagem': 'Jogador removido do time com sucesso'}, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_time_por_id(time_id):
        """Obter time por ID com jogadores"""
        try:
            time = Time.query.get(int(time_id))
            if not time:
                return None, 'Time não encontrado'
            return TimeService._serializar_time_completo(time), None
        except (ValueError, TypeError):
            return None, 'ID de time inválido'

    @staticmethod
    def listar_times_da_temporada(temporada_id, page=1, per_page=20):
        """Listar todos os times de uma temporada"""
        try:
            query = Time.query.filter_by(temporada_id=temporada_id).order_by(Time.criado_em)

            resultado_paginado = paginate(query, page, per_page)

            times_serializados = [
                TimeService._serializar_time_completo(time)
                for time in resultado_paginado['data']
            ]

            return {
                'data': times_serializados,
                'meta': resultado_paginado['meta']
            }, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def _serializar_time(time):
        """Serializa um time básico para dicionário"""
        return {
            'id': time.id,
            'temporada_id': time.temporada_id,
            'nome': time.nome,
            'cor': time.cor,
            'escudo_url': time.escudo_url,
            'pontos': time.pontos,
            'vitorias': time.vitorias,
            'empates': time.empates,
            'derrotas': time.derrotas,
            'gols_marcados': time.gols_marcados,
            'gols_sofridos': time.gols_sofridos,
            'saldo_gols': (time.gols_marcados or 0) - (time.gols_sofridos or 0),
            'criado_em': time.criado_em.isoformat() if time.criado_em else None
        }

    @staticmethod
    def _serializar_time_completo(time):
        """Serializa um time completo com jogadores"""
        jogadores = []
        for tj in time.time_jogadores:
            jogadores.append({
                'id': tj.jogador.id,
                'nome_completo': tj.jogador.nome_completo,
                'apelido': tj.jogador.apelido,
                'telefone': tj.jogador.telefone,
                'foto_url': tj.jogador.foto_url,
                'capitao': tj.capitao,
                'posicao': tj.posicao  # Retorna o nome que foi salvo
            })

        time_data = TimeService._serializar_time(time)
        time_data['jogadores'] = jogadores
        return time_data


class PartidaService:
    """Camada de serviço para lógica de negócios relacionada a partidas"""

    @staticmethod
    def criar_partida(rodada_id, time_casa_id, time_fora_id):
        """Criar uma nova partida"""
        try:
            rodada = Rodada.query.get(int(rodada_id))
            if not rodada:
                return None, 'Rodada não encontrada'

            time_casa = Time.query.get(int(time_casa_id))
            time_fora = Time.query.get(int(time_fora_id))

            if not time_casa or not time_fora:
                return None, 'Um ou ambos os times não foram encontrados'

            # Validar se times pertencem à mesma temporada da rodada
            if time_casa.temporada_id != rodada.temporada_id or time_fora.temporada_id != rodada.temporada_id:
                return None, 'Os times devem pertencer à temporada da rodada'

            nova_partida = Partida(
                rodada_id=rodada_id,
                time_casa_id=time_casa_id,
                time_fora_id=time_fora_id
            )
            db.session.add(nova_partida)
            db.session.commit()
            return PartidaService._serializar_partida(nova_partida), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def iniciar_partida(partida_id):
        """Iniciar uma partida"""
        try:
            partida = Partida.query.get(int(partida_id))
            if not partida:
                return None, 'Partida não encontrada'

            if partida.status != 'agendada':
                return None, 'Partida já foi iniciada ou finalizada'

            partida.inicio = datetime.now()
            partida.status = 'em_andamento'
            db.session.commit()
            return PartidaService._serializar_partida(partida), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def finalizar_partida(partida_id):
        """Finalizar uma partida e calcular pontuação"""
        try:
            partida = Partida.query.get(int(partida_id))
            if not partida:
                return None, 'Partida não encontrada'

            if partida.status == 'finalizada':
                return None, 'Partida já foi finalizada'

            partida.fim = datetime.now()
            partida.status = 'finalizada'

            gols_casa = partida.gols_casa or 0
            gols_fora = partida.gols_fora or 0

            time_casa = partida.time_casa
            time_fora = partida.time_fora

            # Garantir que valores None sejam tratados como 0
            time_casa.gols_marcados = (time_casa.gols_marcados or 0) + gols_casa
            time_casa.gols_sofridos = (time_casa.gols_sofridos or 0) + gols_fora
            time_fora.gols_marcados = (time_fora.gols_marcados or 0) + gols_fora
            time_fora.gols_sofridos = (time_fora.gols_sofridos or 0) + gols_casa

            if gols_casa > gols_fora:
                time_casa.pontos = (time_casa.pontos or 0) + 3
                time_casa.vitorias = (time_casa.vitorias or 0) + 1
                time_fora.derrotas = (time_fora.derrotas or 0) + 1
            elif gols_fora > gols_casa:
                time_fora.pontos = (time_fora.pontos or 0) + 3
                time_fora.vitorias = (time_fora.vitorias or 0) + 1
                time_casa.derrotas = (time_casa.derrotas or 0) + 1
            else:
                time_casa.pontos = (time_casa.pontos or 0) + 1
                time_casa.empates = (time_casa.empates or 0) + 1
                time_fora.pontos = (time_fora.pontos or 0) + 1
                time_fora.empates = (time_fora.empates or 0) + 1

            db.session.commit()
            return PartidaService._serializar_partida(partida), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def obter_partida_por_id(partida_id):
        """Obter partida por ID"""
        try:
            partida = Partida.query.get(int(partida_id))
            if not partida:
                return None, 'Partida não encontrada'
            return PartidaService._serializar_partida_completa(partida), None
        except (ValueError, TypeError):
            return None, 'ID de partida inválido'

    @staticmethod
    def listar_partidas(rodada_id):
        """Listar todas as partidas de uma rodada"""
        try:
            partidas = Partida.query.filter_by(rodada_id=rodada_id).all()
            partidas_serializadas = [PartidaService._serializar_partida(p) for p in partidas]
            return partidas_serializadas, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def _serializar_partida(partida):
        """Serializa uma partida básica para dicionário"""
        return {
            'id': partida.id,
            'rodada_id': partida.rodada_id,
            'time_casa_id': partida.time_casa_id,
            'time_fora_id': partida.time_fora_id,
            'gols_casa': partida.gols_casa,
            'gols_fora': partida.gols_fora,
            'status': partida.status,
            'inicio': partida.inicio.isoformat() if partida.inicio else None,
            'fim': partida.fim.isoformat() if partida.fim else None
        }

    @staticmethod
    def _serializar_partida_completa(partida):
        """Serializa uma partida completa com times e gols"""
        gols = Gol.query.filter_by(partida_id=partida.id).order_by(Gol.minuto).all()

        partida_data = PartidaService._serializar_partida(partida)
        partida_data['time_casa'] = TimeService._serializar_time(partida.time_casa)
        partida_data['time_fora'] = TimeService._serializar_time(partida.time_fora)
        partida_data['gols'] = [GolService._serializar_gol(gol) for gol in gols]

        return partida_data


class GolService:
    """Camada de serviço para lógica de negócios relacionada a gols"""

    @staticmethod
    def registrar_gol(partida_id, time_id, jogador_id, minuto=None, gol_contra=False, assistencia_id=None):
        """Registrar um gol"""
        try:
            partida = Partida.query.get(int(partida_id))
            if not partida:
                return None, 'Partida não encontrada'

            if partida.status != 'em_andamento':
                return None, 'Partida não está em andamento'

            time = Time.query.get(int(time_id))
            jogador = Jogador.query.get(int(jogador_id))

            if not time or not jogador:
                return None, 'Time ou jogador não encontrado'

            if assistencia_id:
                assistente = Jogador.query.get(int(assistencia_id))
                if not assistente:
                    return None, 'Jogador que deu assistência não encontrado'

            novo_gol = Gol(
                partida_id=partida_id,
                time_id=time_id,
                jogador_id=jogador_id,
                minuto=minuto,
                gol_contra=gol_contra,
                assistencia_id=assistencia_id
            )
            db.session.add(novo_gol)

            # Garantir que valores None sejam tratados como 0
            if partida.time_casa_id == time_id:
                if gol_contra:
                    partida.gols_fora = (partida.gols_fora or 0) + 1
                else:
                    partida.gols_casa = (partida.gols_casa or 0) + 1
            else:
                if gol_contra:
                    partida.gols_casa = (partida.gols_casa or 0) + 1
                else:
                    partida.gols_fora = (partida.gols_fora or 0) + 1

            db.session.commit()
            return GolService._serializar_gol(novo_gol), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def remover_gol(gol_id):
        """Remover um gol"""
        try:
            gol = Gol.query.get(int(gol_id))
            if not gol:
                return None, 'Gol não encontrado'

            partida = gol.partida
            if partida.status == 'finalizada':
                return None, 'Não é possível remover gol de partida finalizada'

            # Garantir que valores None sejam tratados como 0
            if partida.time_casa_id == gol.time_id:
                if gol.gol_contra:
                    partida.gols_fora = max((partida.gols_fora or 0) - 1, 0)
                else:
                    partida.gols_casa = max((partida.gols_casa or 0) - 1, 0)
            else:
                if gol.gol_contra:
                    partida.gols_casa = max((partida.gols_casa or 0) - 1, 0)
                else:
                    partida.gols_fora = max((partida.gols_fora or 0) - 1, 0)

            db.session.delete(gol)
            db.session.commit()
            return {'mensagem': 'Gol removido com sucesso'}, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def _serializar_gol(gol):
        """Serializa um gol para dicionário"""
        return {
            'id': gol.id,
            'partida_id': gol.partida_id,
            'time_id': gol.time_id,
            'jogador': {
                'id': gol.jogador.id,
                'nome_completo': gol.jogador.nome_completo,
                'apelido': gol.jogador.apelido,
                'foto_url': gol.jogador.foto_url
            },
            'assistente': {
                'id': gol.assistente.id,
                'nome_completo': gol.assistente.nome_completo,
                'apelido': gol.assistente.apelido,
                'foto_url': gol.assistente.foto_url
            } if gol.assistencia_id else None,
            'minuto': gol.minuto,
            'gol_contra': gol.gol_contra,
            'criado_em': gol.criado_em.isoformat() if gol.criado_em else None
        }


class RankingService:
    """Camada de serviço para rankings e estatísticas"""

    @staticmethod
    def ranking_times_temporada(temporada_id):
        """Ranking de times por pontos na temporada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            # Buscar times da temporada e ordenar por critérios de classificação
            times = Time.query.filter_by(temporada_id=temporada_id).order_by(
                desc(Time.pontos),
                desc(Time.vitorias),
                desc(Time.gols_marcados),
                Time.gols_sofridos
            ).all()

            ranking = []
            for posicao, time in enumerate(times, 1):
                ranking.append({
                    'posicao': posicao,
                    'time': {
                        'id': time.id,
                        'nome': time.nome,
                        'cor': time.cor,
                        'escudo_url': time.escudo_url,
                        'pontos': time.pontos or 0,
                        'vitorias': time.vitorias or 0,
                        'empates': time.empates or 0,
                        'derrotas': time.derrotas or 0,
                        'gols_marcados': time.gols_marcados or 0,
                        'gols_sofridos': time.gols_sofridos or 0,
                        'saldo_gols': (time.gols_marcados or 0) - (time.gols_sofridos or 0),
                        'jogos': (time.vitorias or 0) + (time.empates or 0) + (time.derrotas or 0)
                    }
                })

            return ranking, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def ranking_artilheiros_temporada(temporada_id, limit=10):
        """Ranking de artilheiros na temporada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            rodadas = Rodada.query.filter_by(temporada_id=temporada_id).all()
            rodada_ids = [r.id for r in rodadas]

            partidas = Partida.query.filter(Partida.rodada_id.in_(rodada_ids)).all()
            partida_ids = [p.id for p in partidas]

            artilheiros = db.session.query(
                Jogador.id,
                Jogador.nome_completo,
                Jogador.apelido,
                func.count(Gol.id).label('total_gols')
            ).join(Gol, Gol.jogador_id == Jogador.id).filter(
                Gol.partida_id.in_(partida_ids),
                Gol.gol_contra == False
            ).group_by(Jogador.id).order_by(desc('total_gols')).limit(limit).all()

            ranking = []
            for posicao, artilheiro in enumerate(artilheiros, 1):
                ranking.append({
                    'posicao': posicao,
                    'jogador': {
                        'id': artilheiro.id,
                        'nome_completo': artilheiro.nome_completo,
                        'apelido': artilheiro.apelido,
                        'total_gols': artilheiro.total_gols
                    }
                })

            return ranking, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def ranking_assistencias_temporada(temporada_id, limit=10):
        """Ranking de assistências na temporada"""
        try:
            temporada = Temporada.query.get(int(temporada_id))
            if not temporada:
                return None, 'Temporada não encontrada'

            rodadas = Rodada.query.filter_by(temporada_id=temporada_id).all()
            rodada_ids = [r.id for r in rodadas]

            partidas = Partida.query.filter(Partida.rodada_id.in_(rodada_ids)).all()
            partida_ids = [p.id for p in partidas]

            assistentes = db.session.query(
                Jogador.id,
                Jogador.nome_completo,
                Jogador.apelido,
                func.count(Gol.id).label('total_assistencias')
            ).join(Gol, Gol.assistencia_id == Jogador.id).filter(
                Gol.partida_id.in_(partida_ids),
                Gol.assistencia_id.isnot(None)
            ).group_by(Jogador.id).order_by(desc('total_assistencias')).limit(limit).all()

            ranking = []
            for posicao, assistente in enumerate(assistentes, 1):
                ranking.append({
                    'posicao': posicao,
                    'jogador': {
                        'id': assistente.id,
                        'nome_completo': assistente.nome_completo,
                        'apelido': assistente.apelido,
                        'total_assistencias': assistente.total_assistencias
                    }
                })

            return ranking, None
        except Exception as e:
            return None, str(e)


class VotacaoService:
    """Camada de serviço para lógica de negócios relacionada a votações"""

    @staticmethod
    def _agora_br_naive():
        """Agora em America/Sao_Paulo, mas sem tzinfo (compatível com DATETIME do MySQL/MariaDB)."""
        try:
            return get_brazil_time().replace(tzinfo=None)
        except Exception:
            return datetime.now()

    @staticmethod
    def _parse_datetime(valor):
        """Parse flexível para strings comuns vindas do front."""
        if isinstance(valor, datetime):
            dt = valor
            if getattr(dt, 'tzinfo', None):
                br_tz = pytz.timezone('America/Sao_Paulo')
                return dt.astimezone(br_tz).replace(tzinfo=None)
            return dt
        if not isinstance(valor, str):
            return valor

        v = valor.strip()
        if not v:
            return valor

        # formatos mais comuns
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M'):
            try:
                return datetime.strptime(v, fmt)
            except ValueError:
                pass

        # fallback ISO (sem timezone)
        try:
            # Aceita ISO com timezone (ex: 2025-12-24T15:00:00Z ou 2025-12-24T12:00:00-03:00)
            iso = v.replace('Z', '+00:00')
            dt = datetime.fromisoformat(iso)
            if getattr(dt, 'tzinfo', None):
                br_tz = pytz.timezone('America/Sao_Paulo')
                return dt.astimezone(br_tz).replace(tzinfo=None)
            return dt
        except Exception:
            return valor

    @staticmethod
    def criar_votacao(rodada_id, abre_em, fecha_em, tipo):
        """Criar uma nova votação"""
        try:
            rodada = Rodada.query.get(int(rodada_id))
            if not rodada:
                return None, 'Rodada não encontrada'

            abre_em_dt = VotacaoService._parse_datetime(abre_em)
            fecha_em_dt = VotacaoService._parse_datetime(fecha_em)
            if not isinstance(abre_em_dt, datetime) or not isinstance(fecha_em_dt, datetime):
                return None, 'Formato de data/hora inválido (use YYYY-MM-DD HH:MM:SS ou ISO)'
            if fecha_em_dt <= abre_em_dt:
                return None, 'Data/hora de fechamento deve ser maior que a de abertura'

            nova_votacao = Votacao(
                rodada_id=rodada_id,
                abre_em=abre_em_dt,
                fecha_em=fecha_em_dt,
                tipo=tipo
            )

            agora = VotacaoService._agora_br_naive()
            if abre_em_dt <= agora <= fecha_em_dt:
                nova_votacao.status = 'aberta'
            elif agora > fecha_em_dt:
                nova_votacao.status = 'fechada'
            else:
                nova_votacao.status = 'pendente'

            db.session.add(nova_votacao)
            db.session.commit()
            return VotacaoService._serializar_votacao(nova_votacao), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def registrar_voto(votacao_id, jogador_votante_id, jogador_votado_id, pontos):
        """Registrar um voto"""
        try:
            votacao = Votacao.query.get(int(votacao_id))
            if not votacao:
                return None, 'Votação não encontrada'

            agora = VotacaoService._agora_br_naive()
            if votacao.abre_em and agora < votacao.abre_em:
                return None, 'Votação ainda não abriu'
            if votacao.fecha_em and agora > votacao.fecha_em:
                if votacao.status != 'fechada':
                    votacao.status = 'fechada'
                    db.session.commit()
                return None, 'Votação já foi encerrada'

            # Dentro da janela de tempo: garantir status "aberta"
            if votacao.status != 'aberta':
                votacao.status = 'aberta'
                db.session.commit()

            # Permitir até 3 votos por jogador (ex: 3-2-1), em vez de travar no primeiro voto
            votos_do_votante = Voto.query.filter_by(
                votacao_id=votacao_id,
                jogador_votante_id=jogador_votante_id
            )

            if votos_do_votante.count() >= 3:
                return None, 'Limite de 3 votos atingido para esta votação'

            # Evitar votar mais de uma vez no mesmo jogador dentro da mesma votação
            repetido = votos_do_votante.filter_by(jogador_votado_id=jogador_votado_id).first()
            if repetido:
                return None, 'Você já votou neste jogador nesta votação'

            if int(jogador_votante_id) == int(jogador_votado_id):
                return None, 'Não é permitido votar em si mesmo'

            novo_voto = Voto(
                votacao_id=votacao_id,
                jogador_votante_id=jogador_votante_id,
                jogador_votado_id=jogador_votado_id,
                pontos=pontos
            )
            db.session.add(novo_voto)
            db.session.commit()
            return VotacaoService._serializar_voto(novo_voto), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def resultado_votacao(votacao_id):
        """Agrega os votos de uma votação e retorna ranking por jogador votado."""
        try:
            votacao = Votacao.query.get(int(votacao_id))
            if not votacao:
                return None, 'Votação não encontrada'

            total_votos = db.session.query(func.count(Voto.id)).filter(Voto.votacao_id == votacao_id).scalar() or 0

            agregados = (
                db.session.query(
                    Jogador.id.label('jogador_id'),
                    Jogador.nome_completo.label('nome_completo'),
                    Jogador.apelido.label('apelido'),
                    func.count(Voto.id).label('votos'),
                    func.coalesce(func.sum(Voto.pontos), 0).label('total_pontos')
                )
                .join(Voto, Voto.jogador_votado_id == Jogador.id)
                .filter(Voto.votacao_id == votacao_id)
                .group_by(Jogador.id, Jogador.nome_completo, Jogador.apelido)
                .order_by(desc('total_pontos'), desc('votos'), Jogador.nome_completo.asc())
                .all()
            )

            resultado = []
            for row in agregados:
                votos = int(row.votos or 0)
                pct = (votos / total_votos * 100.0) if total_votos else 0.0
                resultado.append({
                    'jogador': {
                        'id': row.jogador_id,
                        'nome_completo': row.nome_completo,
                        'apelido': row.apelido
                    },
                    'votos': votos,
                    'porcentagem': round(pct, 2),
                    'total_pontos': int(row.total_pontos or 0)
                })

            payload = VotacaoService._serializar_votacao(votacao)
            payload['total_votos'] = int(total_votos)
            payload['resultado'] = resultado
            payload['vencedor'] = resultado[0]['jogador'] if resultado else None

            return payload, None
        except (ValueError, TypeError):
            return None, 'ID de votação inválido'
        except Exception as e:
            return None, str(e)

    @staticmethod
    def resultados_votacoes_da_rodada(rodada_id, tipo=None):
        """Lista todas as votações da rodada e anexa o resultado agregado de cada uma."""
        try:
            rodada = Rodada.query.get(int(rodada_id))
            if not rodada:
                return None, 'Rodada não encontrada'

            query = Votacao.query.filter_by(rodada_id=rodada_id)
            if tipo:
                query = query.filter_by(tipo=tipo)

            votacoes = query.order_by(Votacao.id.desc()).all()
            saida = []
            for v in votacoes:
                res, _ = VotacaoService.resultado_votacao(v.id)
                # resultado_votacao já serializa e agrega; se por algum motivo falhar, cai no básico
                saida.append(res or VotacaoService._serializar_votacao(v))

            return {
                'rodada_id': rodada.id,
                'tipo': tipo,
                'votacoes': saida
            }, None
        except (ValueError, TypeError):
            return None, 'ID de rodada inválido'
        except Exception as e:
            return None, str(e)

    @staticmethod
    def _serializar_votacao(votacao):
        """Serializa uma votação para dicionário"""
        return {
            'id': votacao.id,
            'rodada_id': votacao.rodada_id,
            'abre_em': votacao.abre_em.isoformat() if votacao.abre_em else None,
            'fecha_em': votacao.fecha_em.isoformat() if votacao.fecha_em else None,
            'tipo': votacao.tipo,
            'status': votacao.status
        }

    @staticmethod
    def _serializar_voto(voto):
        """Serializa um voto para dicionário"""
        return {
            'id': voto.id,
            'votacao_id': voto.votacao_id,
            'jogador_votante_id': voto.jogador_votante_id,
            'jogador_votado_id': voto.jogador_votado_id,
            'pontos': voto.pontos,
            'criado_em': voto.criado_em.isoformat() if voto.criado_em else None
        }
