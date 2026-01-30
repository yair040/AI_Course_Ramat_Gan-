# Security Guidelines
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**CRITICAL: READ BEFORE DEPLOYMENT**

---

## 🔒 Security Overview

This document outlines critical security practices for the Gmail Event Scanner application to ensure **NO API keys, credentials, or sensitive data are ever exposed**.

---

## ⚠️ CRITICAL SECURITY RULES

### Rule 1: NEVER Commit Credentials to Git

**Files that MUST NEVER be committed:**

```
credentials/credentials.json      ❌ NEVER COMMIT
credentials/token.pickle          ❌ NEVER COMMIT
../../Anthropic_API_Key/*        ❌ NEVER COMMIT
*.dat files                       ❌ NEVER COMMIT
api_key.*                         ❌ NEVER COMMIT
key.txt*                          ❌ NEVER COMMIT
config.yaml (if contains secrets) ❌ NEVER COMMIT (use config.yaml.example)
```

### Rule 2: Use .gitignore Properly

**Ensure .gitignore includes:**

```gitignore
# CRITICAL - Credentials and API Keys
credentials/
../../Anthropic_API_Key/
*.pickle
*.dat
api_key.*
key.txt*
credentials.json
token.pickle

# Configuration with secrets
config.yaml.local
*.secret.*

# Logs (may contain sensitive data)
log/
*.log
*.log.*
```

### Rule 3: Environment Variables (Alternative Approach)

**Instead of files, consider using environment variables:**

```bash
# Set in your shell profile (.bashrc, .zshrc)
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

**Update auth_manager.py to support env vars:**

```python
# Priority: env var > file
api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    # Fall back to file method
    api_key = load_from_file()
```

---

## 🔐 API Key Management

### Google API Credentials

**Location:** `./credentials/`

**Files:**
- `credentials.json` - OAuth 2.0 client credentials from Google Cloud Console
- `token.pickle` - Generated authentication token (auto-created)

**Security Measures:**

1. **Download Securely:**
   - Download `credentials.json` from Google Cloud Console
   - Transfer securely (encrypted transfer, secure USB, etc.)
   - Delete from Downloads folder after moving

2. **File Permissions:**
   ```bash
   chmod 600 credentials/credentials.json
   chmod 600 credentials/token.pickle
   ```

3. **Backup Securely:**
   - Store backup in encrypted location
   - Use password manager or encrypted vault
   - Never email or share via unencrypted channels

### Anthropic API Key

**Location:** `../../Anthropic_API_Key/`

**Files:**
- `api_key.dat` (primary)
- `key.txt` (fallback)
- `key.txt.pub` (fallback)

**Security Measures:**

1. **Create Securely:**
   ```bash
   cd ../../
   mkdir -p Anthropic_API_Key
   cd Anthropic_API_Key
   
   # Create with restricted permissions
   touch api_key.dat
   chmod 600 api_key.dat
   
   # Edit with secure editor
   nano api_key.dat
   # Paste key, save, exit
   ```

2. **Verify Permissions:**
   ```bash
   ls -la ../../Anthropic_API_Key/
   # Should show: -rw------- (600)
   ```

3. **Never Log API Keys:**
   - The code is designed to NOT log API keys
   - Verify logger calls don't include sensitive data
   - Review logs before sharing

---

## 📋 Pre-Deployment Security Checklist

Before deploying or sharing this project:

- [ ] Verify `.gitignore` includes all sensitive paths
- [ ] Check no credentials in `credentials/` are tracked by git
- [ ] Ensure `../../Anthropic_API_Key/` is not in repository
- [ ] Review all Python files for hardcoded secrets
- [ ] Check logs don't contain API keys or tokens
- [ ] Verify file permissions on credential files (600)
- [ ] Test that credentials load from files, not code
- [ ] Confirm `config.yaml` doesn't contain secrets
- [ ] Review documentation for exposed secrets
- [ ] Scan repository with secret detection tool

---

## 🔍 Secret Scanning

### Using git-secrets

**Install:**
```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install
```

**Configure:**
```bash
cd /path/to/gmail_api
git secrets --install
git secrets --register-aws
git secrets --add 'sk-ant-[a-zA-Z0-9-_]+'  # Anthropic keys
git secrets --add 'AIza[0-9A-Za-z-_]{35}'  # Google API keys
```

**Scan:**
```bash
git secrets --scan
git secrets --scan-history
```

### Manual Review

**Search for potential secrets:**
```bash
# Search for API key patterns
grep -r "sk-ant-" .
grep -r "AIza" .
grep -r "api_key.*=" . --include="*.py"

# Search for hardcoded credentials
grep -r "password.*=" . --include="*.py"
grep -r "token.*=" . --include="*.py"
```

---

## 🚨 What to Do If Credentials Are Exposed

### If Committed to Git

**1. Immediately Revoke:**
- Google: Regenerate OAuth client credentials
- Anthropic: Regenerate API key in console

**2. Remove from Git History:**
```bash
# Using BFG Repo-Cleaner
bfg --delete-files credentials.json
bfg --replace-text passwords.txt  # File with secrets to replace

# Using git-filter-repo
git filter-repo --path credentials/ --invert-paths
```

**3. Force Push (if remote):**
```bash
git push --force --all
```

**4. Notify:**
- If public repository, assume compromised
- Rotate all credentials immediately
- Monitor for unusual activity

### If Shared via Email/Chat

**1. Revoke immediately**
**2. Generate new credentials**
**3. Notify recipient to delete**

---

## 🛡️ Code Security Practices

### In auth_manager.py

**✅ GOOD - Loads from file:**
```python
with open(key_path, 'r') as f:
    api_key = f.read().strip()
    return api_key
```

**❌ BAD - Hardcoded:**
```python
api_key = "sk-ant-api03-xxxxxxxxxxxx"  # NEVER DO THIS
```

### In logger Configuration

**✅ GOOD - Doesn't log sensitive data:**
```python
logger.info("Loading Anthropic API key from api_key.dat")
```

**❌ BAD - Logs API key:**
```python
logger.info(f"API key: {api_key}")  # NEVER DO THIS
```

### In Error Messages

**✅ GOOD - Generic error:**
```python
raise FileNotFoundError("API key file not found")
```

**❌ BAD - Exposes path:**
```python
raise FileNotFoundError(f"API key not found at {full_path_with_secrets}")
```

---

## 📝 Secure Configuration Management

### Configuration File Strategy

**Option 1: Template + Local (Recommended)**

```bash
# Keep in repository (safe)
config.yaml.example

# Keep locally only (in .gitignore)
config.yaml
```

**Setup:**
```bash
# User copies and edits
cp config.yaml.example config.yaml
nano config.yaml
```

**Option 2: Split Configuration**

```yaml
# config.yaml (in repository)
search_criteria:
  subject_keyword: ""  # No sensitive data

# config.local.yaml (in .gitignore)
api_keys:
  anthropic: "loaded-from-file"  # Reference only
```

---

## 🔐 Additional Security Measures

### 1. Principle of Least Privilege

**Google API Scopes:**
Only request necessary scopes:
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Read only
    'https://www.googleapis.com/auth/gmail.modify',    # Mark as read
    'https://www.googleapis.com/auth/calendar'         # Calendar access
]
```

Don't request:
- `gmail.full_access` (too broad)
- Unnecessary scopes

### 2. Token Expiration

**OAuth tokens expire automatically**
- Short-lived access tokens
- Refresh tokens for renewal
- Automatic refresh in code

### 3. API Key Rotation

**Best Practice:**
- Rotate Anthropic API key every 90 days
- Keep old key active during transition
- Update all instances
- Revoke old key after verification

### 4. Logging Best Practices

**What to Log:**
- ✅ Operation performed
- ✅ Timestamp
- ✅ Success/failure
- ✅ Generic error messages

**What NOT to Log:**
- ❌ API keys
- ❌ OAuth tokens
- ❌ Passwords
- ❌ Email content (may contain PII)
- ❌ Full file paths with usernames

### 5. Network Security

**WSL Environment:**
- Use WSL2 (better network isolation)
- Consider firewall rules
- Monitor outbound connections

**API Connections:**
- Always use HTTPS (enforced by APIs)
- Verify SSL certificates
- Use official API endpoints only

---

## 📊 Security Audit Log

### Regular Security Checks

**Weekly:**
- [ ] Review recent git commits for secrets
- [ ] Check file permissions on credentials
- [ ] Verify .gitignore is up to date

**Monthly:**
- [ ] Scan logs for sensitive data
- [ ] Review API usage in Google Cloud Console
- [ ] Check for unauthorized access
- [ ] Update dependencies for security patches

**Quarterly:**
- [ ] Rotate API keys
- [ ] Review and update security policies
- [ ] Audit user access (if multi-user)

---

## 🆘 Emergency Procedures

### Suspected Compromise

**1. Immediate Actions:**
```bash
# Stop all running instances
pkill -f gmail_api

# Revoke credentials
# - Google: console.cloud.google.com
# - Anthropic: console.anthropic.com
```

**2. Investigation:**
```bash
# Check logs for unusual activity
grep -i "error\|unauthorized\|failed" log/app.log*

# Review git history
git log --all --full-history -- credentials/

# Check file access
ls -la credentials/
stat credentials/credentials.json
```

**3. Recovery:**
- Generate new credentials
- Update all instances
- Review security measures
- Document incident

---

## 📚 Resources

### Official Documentation

- **Google OAuth 2.0:** https://developers.google.com/identity/protocols/oauth2
- **Anthropic Security:** https://docs.anthropic.com/security
- **OWASP Secrets Management:** https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password

### Tools

- **git-secrets:** https://github.com/awslabs/git-secrets
- **truffleHog:** https://github.com/trufflesecurity/truffleHog
- **detect-secrets:** https://github.com/Yelp/detect-secrets

---

## ✅ Final Security Verification

Before considering the project secure:

```bash
# 1. No credentials in git
git ls-files | xargs grep -l "sk-ant-\|AIza\|api_key.*="

# 2. .gitignore working
git status --ignored | grep credentials

# 3. File permissions correct
ls -la credentials/ ../../Anthropic_API_Key/

# 4. No secrets in logs
grep -r "sk-ant-\|AIza" log/

# 5. Config doesn't contain secrets
cat config.yaml | grep -i "key\|secret\|password"
```

**All checks should return no results or only .gitignore references.**

---

## 📞 Security Contacts

**If you discover a security issue:**

1. **DO NOT** create a public GitHub issue
2. **DO NOT** share details publicly
3. **DO** contact project maintainer directly
4. **DO** provide details of the vulnerability

---

**Remember: Security is not a one-time setup, it's an ongoing practice.**

**Last Updated:** January 29, 2026  
**Author:** Yair Levi  
**Status:** Active Security Policy
