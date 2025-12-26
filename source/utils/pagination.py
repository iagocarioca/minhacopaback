"""
Utilitário de paginação padronizado para toda a aplicação.
Padrão: 10 itens por página, resposta com objeto 'meta'
"""

from math import ceil
from typing import Any, Dict, List


def paginate(query, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Aplica paginação a uma query SQLAlchemy e retorna resposta padronizada.

    Args:
        query: Query SQLAlchemy a ser paginada
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 10)

    Returns:
        Dict com 'data' (lista de items) e 'meta' (metadados de paginação)
    """
    # Validar parâmetros
    page = max(1, page)
    per_page = max(1, min(per_page, 100))  # Máximo 100 itens por página

    # Contar total de registros
    total = query.count()

    # Calcular total de páginas
    total_pages = ceil(total / per_page) if total > 0 else 1

    # Ajustar página se exceder o total
    page = min(page, total_pages)

    # Aplicar paginação
    offset = (page - 1) * per_page
    items = query.limit(per_page).offset(offset).all()

    # Montar resposta padronizada
    return {
        'data': items,
        'meta': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_next_page': page < total_pages,
            'has_previous_page': page > 1
        }
    }


def paginate_list(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Aplica paginação a uma lista em memória e retorna resposta padronizada.

    Args:
        items: Lista de items a ser paginada
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 10)

    Returns:
        Dict com 'data' (lista de items paginada) e 'meta' (metadados de paginação)
    """
    # Validar parâmetros
    page = max(1, page)
    per_page = max(1, min(per_page, 100))  # Máximo 100 itens por página

    # Total de items
    total = len(items)

    # Calcular total de páginas
    total_pages = ceil(total / per_page) if total > 0 else 1

    # Ajustar página se exceder o total
    page = min(page, total_pages)

    # Calcular offset e slice
    offset = (page - 1) * per_page
    paginated_items = items[offset:offset + per_page]

    # Montar resposta padronizada
    return {
        'data': paginated_items,
        'meta': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_next_page': page < total_pages,
            'has_previous_page': page > 1
        }
    }
