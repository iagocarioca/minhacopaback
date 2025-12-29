# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
import requests
import base64

image_processor_bp = Blueprint('image_processor', __name__)

# URL do webhook n8n
N8N_WEBHOOK_URL = 'https://xai.aurora5.com/test/baixar-binary'


def download_image_as_base64(url):
    """Baixa uma imagem de uma URL e retorna em base64"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Verifica se é uma imagem
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise ValueError(f'URL não retorna uma imagem. Content-Type: {content_type}')
        
        # Converte para base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64, None
    except requests.exceptions.RequestException as e:
        return None, f'Erro ao baixar imagem de {url}: {str(e)}'
    except Exception as e:
        return None, f'Erro ao processar imagem: {str(e)}'


@image_processor_bp.route('/processar-imagens', methods=['POST'])
def processar_imagens():
    """
    Processa duas imagens: baixa das URLs, converte para base64 e envia para n8n
    
    Body JSON esperado:
    {
        "modal_url": "https://...",
        "pessoa_url": "https://..."
    }
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({'erro': 'Nenhum dado fornecido'}), 400
        
        modal_url = dados.get('modal_url')
        pessoa_url = dados.get('pessoa_url')
        
        if not modal_url or not pessoa_url:
            return jsonify({'erro': 'modal_url e pessoa_url são obrigatórios'}), 400
        
        # Baixa e converte ambas as imagens para base64
        modal_base64, erro_modal = download_image_as_base64(modal_url)
        if erro_modal:
            return jsonify({'erro': erro_modal}), 400
        
        pessoa_base64, erro_pessoa = download_image_as_base64(pessoa_url)
        if erro_pessoa:
            return jsonify({'erro': erro_pessoa}), 400
        
        # Prepara payload para enviar ao n8n
        payload_n8n = {
            'modal_url': modal_url,
            'pessoa_url': pessoa_url,
            'modal_base64': modal_base64,
            'pessoa_base64': pessoa_base64
        }
        
        # Envia para o webhook do n8n
        try:
            response_n8n = requests.post(
                N8N_WEBHOOK_URL,
                json=payload_n8n,
                timeout=60,
                headers={'Content-Type': 'application/json'}
            )
            response_n8n.raise_for_status()
            
            return jsonify({
                'mensagem': 'Imagens processadas e enviadas com sucesso',
                'n8n_response': response_n8n.json() if response_n8n.content else None,
                'status_code': response_n8n.status_code
            }), 200
            
        except requests.exceptions.RequestException as e:
            return jsonify({
                'erro': f'Erro ao enviar para n8n: {str(e)}',
                'imagens_processadas': True
            }), 502
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

