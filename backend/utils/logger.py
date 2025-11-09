"""
Logging centralisé et sécurisé
Remplace tous les print() et console.log
Filtre les PII (Personal Identifiable Information)
"""
import logging
import re
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import json


class PIIFilter(logging.Filter):
    """Filtre les informations personnelles sensibles des logs"""

    # Patterns à masquer
    PATTERNS = {
        'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        'phone': re.compile(r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
        'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
        'password': re.compile(r'(password|pwd|passwd)[\s:=]+[^\s]+', re.IGNORECASE),
        'token': re.compile(r'(token|key|secret)[\s:=]+[^\s]+', re.IGNORECASE),
    }

    def filter(self, record: logging.LogRecord) -> bool:
        """Filtre et masque les PII dans le message"""
        if hasattr(record, 'msg'):
            msg = str(record.msg)

            # Masquer les patterns sensibles
            for pattern_name, pattern in self.PATTERNS.items():
                msg = pattern.sub(f'[REDACTED_{pattern_name.upper()}]', msg)

            record.msg = msg

        return True


class StructuredLogger:
    """Logger structuré avec support JSON et niveaux"""

    def __init__(self, name: str = "app"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Handler console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Format structuré
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)

        # Ajouter filtre PII
        console_handler.addFilter(PIIFilter())

        # Ajouter handler si pas déjà présent
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def _log_structured(self, level: str, message: str, **kwargs):
        """Log avec contexte structuré"""
        context = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **kwargs
        }

        log_method = getattr(self.logger, level.lower())
        log_method(json.dumps(context) if kwargs else message)

    def debug(self, message: str, **kwargs):
        """Log niveau DEBUG"""
        self._log_structured('DEBUG', message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log niveau INFO"""
        self._log_structured('INFO', message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log niveau WARNING"""
        self._log_structured('WARNING', message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log niveau ERROR"""
        self._log_structured('ERROR', message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log niveau CRITICAL"""
        self._log_structured('CRITICAL', message, **kwargs)

    def api_call(self, endpoint: str, method: str, status_code: int, duration_ms: float):
        """Log appel API"""
        self.info(
            f"API {method} {endpoint}",
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            duration_ms=duration_ms
        )

    def database_query(self, query: str, duration_ms: float, rows: int):
        """Log requête database (sans PII)"""
        # Masquer les valeurs dans la requête
        safe_query = re.sub(r"'[^']*'", "'***'", query)

        self.debug(
            f"DB Query ({duration_ms:.2f}ms, {rows} rows)",
            query=safe_query[:200],  # Limiter longueur
            duration_ms=duration_ms,
            rows=rows
        )


# Instance globale
logger = StructuredLogger("GetYourShare")


# Fonctions utilitaires pour compatibilité
def log_info(message: str, **kwargs):
    logger.info(message, **kwargs)


def log_error(message: str, **kwargs):
    logger.error(message, **kwargs)


def log_debug(message: str, **kwargs):
    logger.debug(message, **kwargs)


def log_warning(message: str, **kwargs):
    logger.warning(message, **kwargs)
