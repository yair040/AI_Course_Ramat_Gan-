# Security Checklist
# Gmail Event Scanner - Quick Reference

**Author:** Yair Levi  
**Last Updated:** January 29, 2026

---

## 🚨 CRITICAL: Before ANY Git Operation

```bash
# Run these checks EVERY TIME before committing:

# 1. Check what you're about to commit
git status
git diff --cached

# 2. Scan for API keys
git diff --cached | grep -i "sk-ant-\|AIza\|api_key.*=\|password.*="

# 3. Verify .gitignore is working
git status --ignored | grep -E "credentials|Anthropic_API_Key"

# 4. If anything suspicious found
git reset  # Unstage everything and review
```

---

## ✅ Pre-Deployment Checklist

### Initial Setup
- [ ] `.gitignore` exists and includes all sensitive paths
- [ ] `gitignore.txt` renamed to `.gitignore`
- [ ] Credentials folder exists: `./credentials/`
- [ ] API key folder exists: `../../Anthropic_API_Key/`
- [ ] All credential files have 600 permissions
- [ ] No credentials in git: `git ls-files | xargs grep -l "sk-ant-\|AIza"`

### File Permissions
```bash
# Set proper permissions
chmod 600 credentials/credentials.json
chmod 600 credentials/token.pickle
chmod 600 ../../Anthropic_API_Key/api_key.dat
chmod 600 ../../Anthropic_API_Key/key.txt
chmod 600 ../../Anthropic_API_Key/key.txt.pub
```

### Git Verification
```bash
# Nothing sensitive should be tracked
git ls-files | grep credentials     # Should be empty
git ls-files | grep Anthropic       # Should be empty
git ls-files | grep "\.pickle"      # Should be empty
git ls-files | grep "\.dat"         # Should be empty
```

---

## ❌ NEVER Do This

```python
# ❌ WRONG - Hardcoded API key
api_key = "sk-ant-api03-xxxxxxxxxxxxx"

# ❌ WRONG - API key in config
config = {
    'anthropic_key': 'sk-ant-api03-xxxxxxxxxxxxx'
}

# ❌ WRONG - Logging API key
logger.info(f"Using API key: {api_key}")

# ❌ WRONG - API key in variable name visible in logs
anthropic_key_sk_ant_xxx = load_key()
```

---

## ✅ ALWAYS Do This

```python
# ✅ CORRECT - Load from file
with open(key_path, 'r') as f:
    api_key = f.read().strip()

# ✅ CORRECT - Use environment variable
api_key = os.environ.get('ANTHROPIC_API_KEY')

# ✅ CORRECT - Log filename only
logger.info("Loading API key from api_key.dat")

# ✅ CORRECT - Generic error messages
if not api_key:
    raise FileNotFoundError("API key file not found")
```

---

## 🔍 Files That Must Be Excluded

### In .gitignore (CRITICAL)

```gitignore
# Credentials - NEVER COMMIT
credentials/
../../Anthropic_API_Key/
*.pickle
*.dat
api_key.*
key.txt*
credentials.json
token.pickle

# Logs may contain sensitive data
log/
*.log
*.log.*

# Local config with secrets
config.yaml.local
config.local.yaml
*.secret.*
```

---

## 🚑 Emergency Response

### If Credentials Committed to Git

```bash
# 1. IMMEDIATE - Revoke credentials
# - Google: https://console.cloud.google.com
# - Anthropic: https://console.anthropic.com

# 2. Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch credentials/credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (if remote)
git push --force --all

# 4. Generate new credentials
# Follow setup steps in INSTALLATION_GUIDE.md
```

### If Shared Accidentally

1. **Revoke immediately**
2. **Generate new credentials**
3. **Notify recipient to delete/ignore**
4. **Document incident**

---

## 📋 Regular Security Audits

### Weekly
```bash
# Check recent commits
git log -p -5 | grep -i "api\|key\|secret\|password"

# Verify permissions
ls -la credentials/
ls -la ../../Anthropic_API_Key/
```

### Monthly
```bash
# Scan entire repository
git grep -i "sk-ant-\|AIza" $(git rev-list --all)

# Review access logs (Google Cloud Console)
# Rotate API keys if needed
```

---

## 🎯 Quick Security Test

Run this before any commit or push:

```bash
#!/bin/bash
# save as: security_check.sh

echo "🔍 Security Check Starting..."

# Check 1: Unstaged credentials
if git status --porcelain | grep -E "credentials|Anthropic_API_Key"; then
    echo "❌ FAIL: Credential files detected in changes"
    exit 1
fi

# Check 2: Staged secrets
if git diff --cached | grep -E "sk-ant-|AIza|api_key.*="; then
    echo "❌ FAIL: API keys detected in staged changes"
    exit 1
fi

# Check 3: .gitignore exists
if [ ! -f .gitignore ]; then
    echo "❌ FAIL: .gitignore missing"
    exit 1
fi

# Check 4: .gitignore contains critical paths
if ! grep -q "credentials/" .gitignore; then
    echo "❌ FAIL: .gitignore missing 'credentials/'"
    exit 1
fi

if ! grep -q "Anthropic_API_Key" .gitignore; then
    echo "❌ FAIL: .gitignore missing 'Anthropic_API_Key'"
    exit 1
fi

echo "✅ PASS: All security checks passed"
exit 0
```

**Usage:**
```bash
chmod +x security_check.sh
./security_check.sh && git commit -m "Your message"
```

---

## 📞 Quick Reference

| What | Where | Permission | Git |
|------|-------|------------|-----|
| Google credentials | `./credentials/credentials.json` | 600 | ❌ Exclude |
| Google token | `./credentials/token.pickle` | 600 | ❌ Exclude |
| Anthropic key | `../../Anthropic_API_Key/api_key.dat` | 600 | ❌ Exclude |
| Config template | `config.yaml` | 644 | ✅ Include |
| Config local | `config.yaml.local` | 600 | ❌ Exclude |
| Logs | `./log/*.log` | 644 | ❌ Exclude |
| Code files | `*.py` | 644 | ✅ Include |
| Documentation | `*.md` | 644 | ✅ Include |

---

## 🔗 Full Documentation

For complete security guidelines, see:
- **SECURITY.md** - Comprehensive security documentation
- **INSTALLATION_GUIDE.md** - Secure setup procedures
- **README.md** - Security section

---

**Remember: Security is not optional. It's required.**

**Every commit. Every push. Every time.**

---

## Emergency Contact

**If you discover exposed credentials:**
1. DO NOT panic
2. DO revoke immediately
3. DO read SECURITY.md Section "What to Do If Credentials Are Exposed"
4. DO document what happened
5. DO NOT commit the fix without verifying first

---

**Last Updated:** January 29, 2026  
**Status:** Active Checklist  
**Print this and keep it visible while working!**
