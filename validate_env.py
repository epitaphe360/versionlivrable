#!/usr/bin/env python3
"""
Script de validation .env
Usage: python validate_env.py [--env-file .env]
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Variables REQUISES pour démarrage
REQUIRED_VARS = {
    'SUPABASE_URL': {
        'description': 'URL du projet Supabase',
        'example': 'https://xxxxx.supabase.co',
        'min_length': 10,
    },
    'SUPABASE_SERVICE_ROLE_KEY': {
        'description': 'Service role key Supabase',
        'example': 'eyJhbGc...',
        'min_length': 50,
    },
    'JWT_SECRET': {
        'description': 'Secret pour signature JWT',
        'example': 'généré avec secrets.token_urlsafe(64)',
        'min_length': 32,
        'security_critical': True,
    },
    'DATABASE_URL': {
        'description': 'URL connexion PostgreSQL',
        'example': 'postgresql://user:pass@host:5432/db',
        'min_length': 20,
    },
}

# Variables RECOMMANDÉES
RECOMMENDED_VARS = {
    'STRIPE_SECRET_KEY': 'Paiements Stripe',
    'OPENAI_API_KEY': 'Content Studio IA',
    'WHATSAPP_ACCESS_TOKEN': 'WhatsApp Business',
    'SENTRY_DSN': 'Error tracking',
}

def validate_env(env_file='.env'):
    """Valider fichier .env"""
    
    # Charger .env
    env_path = Path(env_file)
    if not env_path.exists():
        print(f"❌ Fichier {env_file} introuvable")
        print(f"   Créez-le à partir de .env.example")
        return False
    
    load_dotenv(env_file)
    
    print(f"🔍 Validation de {env_file}")
    print("="*60)
    
    errors = []
    warnings = []
    
    # Vérifier variables requises
    print("\n📋 VARIABLES REQUISES")
    for var, config in REQUIRED_VARS.items():
        value = os.getenv(var)
        
        if not value:
            errors.append(f"❌ {var}: MANQUANT")
            print(f"  ❌ {var}")
            print(f"      Description: {config['description']}")
            print(f"      Exemple: {config['example']}")
        elif len(value) < config['min_length']:
            errors.append(f"❌ {var}: Trop court ({len(value)} chars, min {config['min_length']})")
            print(f"  ⚠️  {var}: TROP COURT ({len(value)} chars)")
        elif config.get('security_critical') and value in ['test', 'dev', 'changeme', 'secret']:
            errors.append(f"❌ {var}: Valeur par défaut dangereuse")
            print(f"  ❌ {var}: VALEUR PAR DÉFAUT (dangereux !)")
        else:
            print(f"  ✅ {var} ({len(value)} chars)")
    
    # Vérifier variables recommandées
    print("\n📋 VARIABLES RECOMMANDÉES")
    for var, description in RECOMMENDED_VARS.items():
        value = os.getenv(var)
        if not value:
            warnings.append(f"⚠️  {var}: Manquant - {description}")
            print(f"  ⚠️  {var}: Manquant ({description})")
        else:
            print(f"  ✅ {var}")
    
    # Statistiques
    print(f"\n📊 STATISTIQUES")
    total_vars = len([k for k in os.environ.keys() if not k.startswith('_')])
    print(f"  Total variables: {total_vars}")
    print(f"  Requises définies: {len(REQUIRED_VARS) - len(errors)}/{len(REQUIRED_VARS)}")
    print(f"  Recommandées définies: {len(RECOMMENDED_VARS) - len(warnings)}/{len(RECOMMENDED_VARS)}")
    
    # Résultat final
    print(f"\n{'='*60}")
    if errors:
        print("❌ VALIDATION ÉCHOUÉE")
        print(f"\nErreurs ({len(errors)}):")
        for error in errors:
            print(f"  {error}")
    else:
        print("✅ VALIDATION RÉUSSIE")
    
    if warnings:
        print(f"\nAvertissements ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")
    
    print(f"{'='*60}")
    
    return len(errors) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Valider fichier .env')
    parser.add_argument('--env-file', default='.env.example', help='Chemin vers fichier .env')
    args = parser.parse_args()
    
    print("⚙️  VALIDATION CONFIGURATION .ENV")
    print()
    
    try:
        success = validate_env(args.env_file)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
