#!/bin/bash

# Migration script from v1.0 to v2.0
echo "🔄 Migrating FLUX Image Generator from v1.0 to v2.0..."

# Backup old files
echo "📦 Creating backup of old files..."
mkdir -p backup_v1
cp main.py backup_v1/ 2>/dev/null || true
cp enhanced_main.py backup_v1/ 2>/dev/null || true
cp prompt_tester_main.py backup_v1/ 2>/dev/null || true
cp -r src/flux_generator backup_v1/ 2>/dev/null || true

# Install new dependencies
echo "📦 Installing new dependencies..."
pip install click pyyaml

# Create necessary directories
echo "📁 Creating new directory structure..."
mkdir -p config
mkdir -p tests

# Test the new CLI
echo "🧪 Testing new CLI interface..."
python flux_generator.py --help

echo "✅ Migration completed!"
echo ""
echo "📝 What's new in v2.0:"
echo "  - Unified CLI: python flux_generator.py"
echo "  - Better structure: modular architecture"
echo "  - Configuration: config/config.yaml"
echo "  - Tests: pytest tests/"
echo ""
echo "🚀 Try the new commands:"
echo "  python flux_generator.py info"
echo "  python flux_generator.py config --show"
echo "  python flux_generator.py generate --count 5" 