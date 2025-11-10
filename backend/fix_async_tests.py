#!/usr/bin/env python3
"""
Script de correction automatique des tests async
Corrige test_payments.py et test_sales.py pour ajouter await et @pytest.mark.asyncio

Usage: python fix_async_tests.py
"""
import re
import sys
from pathlib import Path

def fix_async_test_file(filepath: Path) -> int:
    """Fix async test patterns in a test file"""
    print(f"\n📝 Processing {filepath.name}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # Pattern 1: Add @pytest.mark.asyncio and async to test functions
    # Match def test_xxx but not already async
    pattern1 = r'^(def test_\w+\([^)]*\):)'
    replacement1 = r'@pytest.mark.asyncio\nasync \1'

    # Find all test functions that aren't async
    test_funcs = re.finditer(pattern1, content, re.MULTILINE)
    for match in test_funcs:
        func_line = match.group(1)
        # Check if already has @pytest.mark.asyncio before it
        start = match.start()
        preceding = content[max(0, start-50):start]

        if '@pytest.mark.asyncio' not in preceding and 'async def' not in func_line:
            content = content[:match.start()] + replacement1.replace(r'\1', func_line) + content[match.end():]
            changes += 1

    # Pattern 2: Add await before service method calls
    # Look for patterns like: result = service.method(...)
    patterns_to_await = [
        (r'(\s+)(result|success|data|total|count|commission|sale|response) = (service\.\w+\()', r'\1\2 = await \3'),
        (r'(\s+)(result|success|data|total|count|commission|sale|response) = (PaymentsService\(\)\.\w+\()', r'\1\2 = await \3'),
        (r'(\s+)(result|success|data|total|count|commission|sale|response) = (SalesService\(\)\.\w+\()', r'\1\2 = await \3'),
    ]

    for pattern, replacement in patterns_to_await:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes += len(re.findall(pattern, content))
            content = new_content

    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath.name}: {changes} corrections applied")
        return changes
    else:
        print(f"ℹ️  {filepath.name}: No changes needed")
        return 0

def main():
    """Main entry point"""
    backend_dir = Path(__file__).parent
    tests_dir = backend_dir / "tests"

    if not tests_dir.exists():
        print(f"❌ Tests directory not found: {tests_dir}")
        sys.exit(1)

    test_files = [
        tests_dir / "test_payments.py",
        tests_dir / "test_sales.py",
    ]

    total_changes = 0

    print("🔧 Fixing async test files...")
    print("=" * 60)

    for test_file in test_files:
        if not test_file.exists():
            print(f"⚠️  File not found: {test_file}")
            continue

        changes = fix_async_test_file(test_file)
        total_changes += changes

    print("\n" + "=" * 60)
    print(f"✨ Completed! Total corrections: {total_changes}")

    if total_changes > 0:
        print("\n💡 Next steps:")
        print("   1. Review the changes with: git diff tests/")
        print("   2. Run tests: pytest tests/test_payments.py tests/test_sales.py -v")
        print("   3. If all pass, commit: git add tests/ && git commit -m 'fix: async tests'")

if __name__ == "__main__":
    main()
