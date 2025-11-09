#!/usr/bin/env python3
"""
Script pour supprimer tous les console.log en production
Remplace par le logger centralisé
"""
import os
import re
from pathlib import Path
from typing import List, Tuple


class ConsoleLogRemover:
    """Supprime les console.log du frontend"""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.stats = {
            'files_scanned': 0,
            'console_logs_found': 0,
            'console_logs_removed': 0,
            'files_modified': 0
        }

    def find_js_files(self) -> List[Path]:
        """Trouve tous les fichiers JS/JSX"""
        patterns = ['**/*.js', '**/*.jsx']
        files = []

        for pattern in patterns:
            files.extend(self.base_dir.glob(pattern))

        # Exclure node_modules, build, etc.
        files = [
            f for f in files
            if 'node_modules' not in str(f)
            and 'build' not in str(f)
            and 'dist' not in str(f)
            and '.next' not in str(f)
        ]

        return files

    def remove_console_logs(self, content: str) -> Tuple[str, int]:
        """
        Supprime les console.log du contenu
        Retourne (nouveau_contenu, nombre_suppressions)
        """
        # Pattern pour console.log, console.debug, console.warn
        # Mais GARDE console.error (important pour debugging)
        patterns = [
            # console.log simple
            r'console\.log\([^)]*\);?\s*',
            # console.debug
            r'console\.debug\([^)]*\);?\s*',
            # console.warn → logger.warning
            r'console\.warn\(',
            # console.info → logger.info
            r'console\.info\(',
        ]

        modified_content = content
        removals = 0

        # Supprimer console.log et console.debug
        for i, pattern in enumerate(patterns[:2]):
            matches = re.findall(pattern, modified_content)
            removals += len(matches)
            modified_content = re.sub(pattern, '', modified_content)

        # Remplacer console.warn par logger.warning
        warn_pattern = r'console\.warn\('
        if re.search(warn_pattern, modified_content):
            # Ajouter import logger si pas présent
            if 'import logger' not in modified_content and 'from.*logger' not in modified_content:
                # Trouver la première ligne d'import
                import_match = re.search(r'^import ', modified_content, re.MULTILINE)
                if import_match:
                    insert_pos = import_match.start()
                    modified_content = (
                        modified_content[:insert_pos] +
                        "import { logger } from './utils/logger';\n" +
                        modified_content[insert_pos:]
                    )

            modified_content = re.sub(warn_pattern, 'logger.warning(', modified_content)
            removals += len(re.findall(warn_pattern, content))

        # Remplacer console.info par logger.info
        info_pattern = r'console\.info\('
        if re.search(info_pattern, modified_content):
            modified_content = re.sub(info_pattern, 'logger.info(', modified_content)
            removals += len(re.findall(info_pattern, content))

        return modified_content, removals

    def process_file(self, file_path: Path) -> bool:
        """
        Traite un fichier
        Retourne True si modifié
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            new_content, removals = self.remove_console_logs(original_content)

            if removals > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.stats['console_logs_removed'] += removals
                self.stats['files_modified'] += 1

                print(f"✅ {file_path.relative_to(self.base_dir)}: {removals} console.log removed")
                return True

            return False

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False

    def run(self):
        """Execute le nettoyage"""
        print("🔍 Scanning for console.log statements...")
        print(f"📁 Base directory: {self.base_dir}")
        print()

        files = self.find_js_files()
        self.stats['files_scanned'] = len(files)

        print(f"📊 Found {len(files)} JS/JSX files")
        print()

        for file_path in files:
            self.process_file(file_path)

        # Rapport
        print()
        print("=" * 60)
        print("📊 RAPPORT FINAL")
        print("=" * 60)
        print(f"Fichiers scannés:        {self.stats['files_scanned']}")
        print(f"Fichiers modifiés:       {self.stats['files_modified']}")
        print(f"console.log supprimés:   {self.stats['console_logs_removed']}")
        print()

        if self.stats['files_modified'] > 0:
            print("✅ Nettoyage terminé avec succès!")
            print("⚠️  N'oubliez pas d'ajouter le logger dans vos fichiers si nécessaire")
        else:
            print("✅ Aucun console.log trouvé - Code déjà propre!")


def main():
    # Détecter si on est dans frontend/ ou racine
    current_dir = Path.cwd()

    if current_dir.name == 'frontend':
        base_dir = current_dir / 'src'
    else:
        base_dir = current_dir / 'frontend' / 'src'

    if not base_dir.exists():
        print(f"❌ Directory not found: {base_dir}")
        print("Please run from project root or frontend directory")
        return

    remover = ConsoleLogRemover(base_dir)
    remover.run()


if __name__ == "__main__":
    main()
