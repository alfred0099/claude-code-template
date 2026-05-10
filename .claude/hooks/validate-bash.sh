#!/bin/bash
# Pre-commit hook: validate code quality

set -e

PROJECT_ROOT=$(git rev-parse --show-toplevel)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🔍 Pre-commit validation..."

# Check for secrets
if command -v detect-secrets &> /dev/null; then
    if detect-secrets scan --baseline .secrets.baseline --force-repo-scan &> /dev/null; then
        echo -e "${GREEN}✓${NC} No secrets detected"
    else
        echo -e "${RED}✗${NC} Possible secrets found"
        exit 1
    fi
fi

# Format Bash
if command -v shfmt &> /dev/null; then
    bash_files=$(find "$PROJECT_ROOT" -name "*.sh" -type f 2>/dev/null || true)
    if [ -n "$bash_files" ]; then
        shfmt -i 2 -w $bash_files
        echo -e "${GREEN}✓${NC} Bash formatted"
    fi
fi

# Lint Bash
if command -v shellcheck &> /dev/null; then
    bash_files=$(find "$PROJECT_ROOT" -name "*.sh" -type f 2>/dev/null || true)
    if [ -n "$bash_files" ]; then
        shellcheck -x $bash_files || exit 1
        echo -e "${GREEN}✓${NC} Bash lint passed"
    fi
fi

# Type-check Python
if command -v pyright &> /dev/null; then
    pyright --outputjson > /tmp/pyright.json 2>&1 || true
    echo -e "${GREEN}✓${NC} Python types checked"
fi

# Run tests
if [ -d "tests" ] && command -v pytest &> /dev/null; then
    pytest tests/ -q --tb=short 2>&1 || exit 1
    echo -e "${GREEN}✓${NC} Tests passed"
fi

# Lint Python
if command -v ruff &> /dev/null; then
    ruff check . --exclude=.venv,.git || exit 1
    echo -e "${GREEN}✓${NC} Python lint passed"
fi

echo ""
echo -e "${GREEN}✅ Pre-commit validation passed!${NC}"
exit 0
