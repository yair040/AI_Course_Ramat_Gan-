# Troubleshooting Guide
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Last Updated:** January 29, 2026

---

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'gmail_api'"

**Error Message:**
```
Error while finding module specification for 'gmail_api.main' 
(ModuleNotFoundError: No module named 'gmail_api')
```

**Cause:**
The application was being run as a Python module when it should be run as a script.

**Solution:**
Use the correct run method:

```bash
# Correct way (recommended)
./run.sh

# Or directly
python main.py

# NOT this:
python -m gmail_api.main  # ❌ Don't use this
```

---

### Issue 2: Virtual Environment Not Activated

**Error Message:**
```
venv not found
```

**Solution:**
```bash
# Navigate to venv location
cd ../..

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Return to project
cd AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api

# Install dependencies
pip install -r requirements.txt
```

---

### Issue 3: Permission Denied on run.sh

**Error Message:**
```
Permission denied: ./run.sh
```

**Solution:**
```bash
chmod +x run.sh
./run.sh
```

---

### Issue 4: Credentials Not Found

**Error Message:**
```
FileNotFoundError: Credentials file not found: ./credentials/credentials.json
```

**Solution:**
1. Download `credentials.json` from Google Cloud Console
2. Place it in the correct location:
```bash
mkdir -p credentials
mv ~/Downloads/client_secret_*.json credentials/credentials.json
chmod 600 credentials/credentials.json
```

---

### Issue 5: Anthropic API Key Not Found

**Error Message:**
```
FileNotFoundError: No valid Anthropic API key found in ./Anthropic_API_Key
```

**Solution:**
```bash
# Create directory
mkdir -p Anthropic_API_Key

# Create key file
echo "your-api-key-here" > Anthropic_API_Key/api_key.dat

# Set permissions
chmod 600 Anthropic_API_Key/api_key.dat
```

---

### Issue 6: Import Errors

**Error Message:**
```
ImportError: No module named 'google.auth'
```

**Cause:**
Dependencies not installed or virtual environment not activated.

**Solution:**
```bash
# Activate virtual environment
source ../../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep google
```

---

### Issue 7: Configuration Error

**Error Message:**
```
ValueError: At least one search criterion must be configured
```

**Cause:**
No search criterion set in `config.yaml`.

**Solution:**
Edit `config.yaml` and set ONE of these:
```yaml
search_criteria:
  subject_keyword: "meeting"    # Set this
  sender_email: ""              # Or this
  label: ""                     # Or this
  unread_only: false            # Or set to true
```

---

### Issue 8: Gmail API Quota Exceeded

**Error Message:**
```
Gmail API error: Quota exceeded
```

**Solution:**
- Wait for quota reset (usually daily)
- Reduce `max_emails_per_scan` in `config.yaml`
- Increase `scan_interval_seconds` in polling mode

---

### Issue 9: OAuth Browser Not Opening

**Issue:**
When running for the first time, browser doesn't open for OAuth.

**Solution:**
1. Check if you're in a headless environment (WSL without display)
2. If yes, the URL should be printed in the console
3. Copy the URL and open it in your Windows browser
4. Complete authentication
5. The token will be saved for future use

---

### Issue 10: Log Directory Issues

**Error Message:**
```
Permission denied: ./log/app.log
```

**Solution:**
```bash
# Create log directory with proper permissions
mkdir -p log
chmod 755 log

# If files already exist, fix permissions
chmod 644 log/*.log
```

---

### Issue 11: Git Tracking Credentials

**Issue:**
Git is tracking credential files.

**Solution:**
```bash
# 1. Remove from git (keeps local files)
git rm --cached credentials/credentials.json
git rm --cached credentials/token.pickle
git rm --cached -r Anthropic_API_Key/

# 2. Verify .gitignore exists
ls -la .gitignore

# 3. If .gitignore doesn't exist, rename gitignore.txt
mv gitignore.txt .gitignore

# 4. Verify it's working
git status --ignored | grep -E "credentials|Anthropic"
```

---

### Issue 12: Token Expired

**Error Message:**
```
google.auth.exceptions.RefreshError: Token has been expired
```

**Solution:**
```bash
# Remove old token
rm credentials/token.pickle

# Run application again - will prompt for re-authentication
./run.sh
```

---

### Issue 13: Email Parsing Fails

**Error Message:**
```
Failed to parse email: Missing meeting date
```

**Cause:**
Email doesn't contain clear meeting information.

**Solution:**
- This is normal for emails that don't have meeting details
- Check the email manually
- Adjust search criteria to be more specific
- The application will skip this email and continue

---

### Issue 14: Duplicate Events

**Issue:**
Same event created multiple times.

**Cause:**
Running in one-time mode multiple times, or email wasn't marked as read.

**Solution:**
- The application checks for duplicates automatically
- Use polling mode instead (marks emails as read)
- Manually delete duplicate events in Google Calendar

---

### Issue 15: WSL Path Issues

**Error Message:**
```
No such file or directory: /mnt/c/...
```

**Solution:**
Make sure you're using WSL paths:
```bash
# Correct
cd /mnt/c/Users/yair0/AI_continue/...

# Not Windows paths
cd C:\Users\yair0\AI_continue\...
```

---

## Quick Diagnostic Commands

### Check Virtual Environment
```bash
which python
# Should show: /mnt/c/Users/yair0/AI_continue/venv/bin/python
```

### Check Installed Packages
```bash
pip list | grep -E "(google|anthropic|yaml)"
```

### Check Credentials Exist
```bash
ls -la credentials/
ls -la Anthropic_API_Key/
```

### Check File Permissions
```bash
ls -la credentials/credentials.json
# Should show: -rw------- (600)
```

### Check Configuration
```bash
cat config.yaml
# Verify at least one search criterion is set
```

### Check Logs
```bash
tail -50 log/app.log
# Review recent log entries
```

### Test Python Import
```bash
python -c "import google.auth; print('Google auth OK')"
python -c "import anthropic; print('Anthropic OK')"
python -c "import yaml; print('YAML OK')"
```

---

## Still Having Issues?

1. **Check the logs:**
   ```bash
   cat log/app.log
   ```

2. **Run with verbose logging:**
   Edit `config.yaml`:
   ```yaml
   system:
     log_level: "DEBUG"
   ```

3. **Verify all prerequisites:**
   - Python 3.8+: `python --version`
   - Virtual environment activated: `which python`
   - Dependencies installed: `pip list`
   - Credentials in place: `ls credentials/`
   - API key in place: `ls Anthropic_API_Key/`
   - Configuration set: `cat config.yaml`

4. **Read documentation:**
   - `README.md` - Full user guide
   - `INSTALLATION_GUIDE.md` - Setup steps
   - `SECURITY.md` - Security issues
   - `SETUP.md` - Quick setup

5. **Common mistakes:**
   - ❌ Running `python -m gmail_api.main`
   - ❌ Not activating virtual environment
   - ❌ Missing dependencies
   - ❌ Wrong file paths
   - ❌ Missing credentials
   - ❌ No search criterion configured

---

## Getting Help

**Before asking for help, collect this information:**

```bash
# System info
uname -a
python --version

# Virtual environment
which python
pip list

# File structure
ls -la
ls -la credentials/
ls -la Anthropic_API_Key/

# Configuration
cat config.yaml

# Recent logs
tail -100 log/app.log

# Git status
git status
```

Share this information when asking for help.

---

**Last Updated:** January 29, 2026  
**Most Common Issue:** Using `python -m gmail_api.main` instead of `python main.py` ✅
