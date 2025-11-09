"""
Database Optimization Utilities
Helpers pour optimiser les N+1 queries avec:
- Eager loading avec fetch_with_relations()
- Batch fetching avec batch_fetch()
- Caching avec cache_decorator()
"""

import functools
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)


class DBOptimizer:
    """Classe pour optimiser les requêtes Supabase"""

    def __init__(self, supabase_client):
        """
        Initialiser l'optimiseur

        Args:
            supabase_client: Client Supabase
        """
        self.supabase = supabase_client
        self._cache = {}
        self._cache_ttl = {}

    # ============================================
    # EAGER LOADING
    # ============================================

    def fetch_with_relations(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        relations: Optional[List[str]] = None,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        desc: bool = True
    ) -> List[Dict]:
        """
        Récupérer des données avec relations joinées (eager loading)

        Évite les N+1 queries en chargeant les relations en une seule requête.

        Args:
            table: Nom de la table
            filters: Dict {column: value} pour filtrer
            relations: List des relations à charger ['users(*)', 'products(*)']
            limit: Limite de résultats
            order_by: Champ pour trier
            desc: Tri descendant (défaut True)

        Returns:
            Liste des données avec relations incluses

        Exemple:
            optimizer.fetch_with_relations(
                'leads',
                filters={'merchant_id': '123', 'status': 'pending'},
                relations=['campaigns(*)', 'merchants(*)'],
                limit=50,
                order_by='created_at'
            )
        """
        try:
            # Construire la requête
            select_clause = '*'
            if relations:
                select_clause = '*,' + ','.join(relations)

            query = self.supabase.table(table).select(select_clause)

            # Ajouter les filtres
            if filters:
                for column, value in filters.items():
                    if isinstance(value, list):
                        # Filtrer sur plusieurs valeurs (IN)
                        query = query.in_(column, value)
                    else:
                        query = query.eq(column, value)

            # Tri
            if order_by:
                query = query.order(order_by, desc=desc)

            # Limite
            if limit:
                query = query.limit(limit)

            # Exécuter
            result = query.execute()

            logger.info(
                f"fetch_with_relations: {table}",
                table=table,
                rows=len(result.data or []),
                relations=relations
            )

            return result.data or []

        except Exception as e:
            logger.error(f"Error fetching {table} with relations: {e}")
            return []

    # ============================================
    # BATCH FETCHING
    # ============================================

    def batch_fetch(
        self,
        table: str,
        ids: List[str],
        columns: str = '*',
        chunk_size: int = 50
    ) -> Dict[str, Dict]:
        """
        Récupérer plusieurs items par IDs en une seule requête

        Évite N requêtes pour N items en groupant les IDs.

        Args:
            table: Nom de la table
            ids: Liste des IDs à récupérer
            columns: Colonnes à récupérer
            chunk_size: Taille des chunks (défaut 50)

        Returns:
            Dict {id: item}

        Exemple:
            items = optimizer.batch_fetch('products', ['id1', 'id2', 'id3'])
            # Retourne: {'id1': {...}, 'id2': {...}, 'id3': {...}}
        """
        try:
            if not ids:
                return {}

            result_dict = {}

            # Traiter par chunks pour éviter les limites d'URL
            for i in range(0, len(ids), chunk_size):
                chunk = ids[i : i + chunk_size]

                result = self.supabase.table(table).select(columns).in_('id', chunk).execute()

                # Indexer par ID
                for item in (result.data or []):
                    result_dict[item['id']] = item

            logger.info(f"batch_fetch: {table}", table=table, count=len(result_dict))

            return result_dict

        except Exception as e:
            logger.error(f"Error batch fetching from {table}: {e}")
            return {}

    def batch_fetch_related(
        self,
        table: str,
        foreign_key: str,
        related_ids: List[str],
        columns: str = '*',
        chunk_size: int = 50
    ) -> List[Dict]:
        """
        Récupérer tous les items liés à plusieurs parents en une requête

        Exemple: Récupérer tous les leads pour plusieurs merchants

        Args:
            table: Nom de la table
            foreign_key: Colonne clé étrangère
            related_ids: Liste des IDs parents
            columns: Colonnes à récupérer
            chunk_size: Taille des chunks

        Returns:
            Liste de tous les items trouvés
        """
        try:
            if not related_ids:
                return []

            all_results = []

            # Traiter par chunks
            for i in range(0, len(related_ids), chunk_size):
                chunk = related_ids[i : i + chunk_size]

                result = (
                    self.supabase.table(table)
                    .select(columns)
                    .in_(foreign_key, chunk)
                    .execute()
                )

                all_results.extend(result.data or [])

            logger.info(
                f"batch_fetch_related: {table}",
                table=table,
                fk=foreign_key,
                count=len(all_results)
            )

            return all_results

        except Exception as e:
            logger.error(f"Error batch fetching related from {table}: {e}")
            return []

    # ============================================
    # CACHING
    # ============================================

    def cache(
        self,
        ttl_seconds: int = 300,
        key_prefix: Optional[str] = None
    ) -> Callable:
        """
        Décorateur pour cacher les résultats des fonctions

        Args:
            ttl_seconds: Durée de vie du cache en secondes
            key_prefix: Préfixe optionnel pour la clé de cache

        Returns:
            Décorateur

        Exemple:
            @optimizer.cache(ttl_seconds=600)
            def get_merchant_kpis(merchant_id):
                return {...}
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Construire une clé de cache
                cache_key = f"{key_prefix or func.__name__}:{str(args)}:{str(kwargs)}"

                # Vérifier le cache
                if cache_key in self._cache:
                    cache_entry = self._cache[cache_key]
                    if datetime.now() < cache_entry['expires']:
                        logger.debug(f"Cache hit: {cache_key}")
                        return cache_entry['value']

                # Exécuter la fonction
                result = func(*args, **kwargs)

                # Stocker en cache
                self._cache[cache_key] = {
                    'value': result,
                    'expires': datetime.now() + timedelta(seconds=ttl_seconds)
                }

                logger.debug(f"Cache miss: {cache_key}")
                return result

            return wrapper
        return decorator

    def clear_cache(self, pattern: Optional[str] = None) -> None:
        """
        Effacer le cache

        Args:
            pattern: Pattern optionnel pour effacer seulement les clés correspondantes
        """
        if pattern is None:
            self._cache.clear()
        else:
            keys_to_remove = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self._cache[key]
            logger.info(f"Cleared {len(keys_to_remove)} cache entries matching {pattern}")

    # ============================================
    # BULK OPERATIONS
    # ============================================

    def bulk_update(
        self,
        table: str,
        updates: List[Dict[str, Any]],
        id_field: str = 'id',
        chunk_size: int = 100
    ) -> int:
        """
        Mettre à jour plusieurs items en une seule opération

        Args:
            table: Nom de la table
            updates: Liste des items à mettre à jour avec id_field
            id_field: Nom du champ ID (défaut 'id')
            chunk_size: Taille des chunks

        Returns:
            Nombre d'items mis à jour

        Exemple:
            optimizer.bulk_update('leads', [
                {'id': 'lead1', 'status': 'validated'},
                {'id': 'lead2', 'status': 'rejected'}
            ])
        """
        try:
            total_updated = 0

            for i in range(0, len(updates), chunk_size):
                chunk = updates[i : i + chunk_size]

                result = self.supabase.table(table).upsert(chunk).execute()
                total_updated += len(result.data or [])

            logger.info(f"bulk_update: {table}", table=table, updated=total_updated)

            return total_updated

        except Exception as e:
            logger.error(f"Error bulk updating {table}: {e}")
            return 0

    def bulk_insert(
        self,
        table: str,
        items: List[Dict[str, Any]],
        chunk_size: int = 100
    ) -> int:
        """
        Insérer plusieurs items en une seule opération

        Args:
            table: Nom de la table
            items: Liste des items à insérer
            chunk_size: Taille des chunks

        Returns:
            Nombre d'items insérés
        """
        try:
            total_inserted = 0

            for i in range(0, len(items), chunk_size):
                chunk = items[i : i + chunk_size]

                result = self.supabase.table(table).insert(chunk).execute()
                total_inserted += len(result.data or [])

            logger.info(f"bulk_insert: {table}", table=table, inserted=total_inserted)

            return total_inserted

        except Exception as e:
            logger.error(f"Error bulk inserting into {table}: {e}")
            return 0

    # ============================================
    # AGGREGATIONS
    # ============================================

    def count_by_field(
        self,
        table: str,
        field: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[Any, int]:
        """
        Compter les occurrences par valeur de champ

        Évite les boucles en Python en utilisant l'aggregation

        Args:
            table: Nom de la table
            field: Champ à grouper
            filters: Filtres optionnels

        Returns:
            Dict {valeur: count}
        """
        try:
            query = self.supabase.table(table).select(field)

            if filters:
                for column, value in filters.items():
                    query = query.eq(column, value)

            result = query.execute()
            data = result.data or []

            # Compter en Python (peut être optimisé avec RPC)
            counts = {}
            for item in data:
                key = item.get(field)
                counts[key] = counts.get(key, 0) + 1

            return counts

        except Exception as e:
            logger.error(f"Error counting by field in {table}: {e}")
            return {}

    def sum_by_field(
        self,
        table: str,
        sum_field: str,
        group_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[Any, float]:
        """
        Somme groupée par champ

        Args:
            table: Nom de la table
            sum_field: Champ à sommer
            group_by: Champ de groupement optionnel
            filters: Filtres optionnels

        Returns:
            Dict {groupe: somme}
        """
        try:
            select_clause = sum_field
            if group_by:
                select_clause = f"{group_by},{sum_field}"

            query = self.supabase.table(table).select(select_clause)

            if filters:
                for column, value in filters.items():
                    query = query.eq(column, value)

            result = query.execute()
            data = result.data or []

            # Grouper et sommer
            if group_by:
                sums = {}
                for item in data:
                    key = item.get(group_by)
                    value = float(item.get(sum_field) or 0)
                    sums[key] = sums.get(key, 0) + value
                return sums
            else:
                # Pas de groupement
                total = sum(float(item.get(sum_field) or 0) for item in data)
                return {'total': total}

        except Exception as e:
            logger.error(f"Error summing in {table}: {e}")
            return {}


# ============================================
# HELPERS FONCTIONNELS
# ============================================

def merge_with_relations(
    items: List[Dict],
    related_items: Dict[str, Dict],
    item_id_field: str,
    relation_field: str
) -> List[Dict]:
    """
    Fusionner les items avec leurs relations

    Utile après un batch_fetch pour joindre les données

    Args:
        items: Liste des items principaux
        related_items: Dict {id: item} des items liés
        item_id_field: Champ ID de l'item principal
        relation_field: Nom du champ pour la relation

    Returns:
        Liste des items avec relations ajoutées

    Exemple:
        leads = [...]
        merchants = optimizer.batch_fetch('users', merchant_ids)
        leads_with_merchants = merge_with_relations(
            leads, merchants, 'merchant_id', 'merchant'
        )
    """
    for item in items:
        related_id = item.get(item_id_field)
        if related_id in related_items:
            item[relation_field] = related_items[related_id]
        else:
            item[relation_field] = None

    return items


def transform_to_dict(
    items: List[Dict],
    key_field: str
) -> Dict[Any, Dict]:
    """
    Transformer une liste en dictionnaire indexé

    Args:
        items: Liste d'items
        key_field: Champ à utiliser comme clé

    Returns:
        Dict {clé: item}
    """
    return {item.get(key_field): item for item in items}
