# Installation Guide
# Gmail Event Scanner & Calendar Integration

**Author:** Yair Levi  
**Quick Start Guide**

---

## ⚠️ SECURITY FIRST

**Before proceeding, understand these critical security rules:**

1. **NEVER commit credentials to git**
2. **NEVER hardcode API keys in code**
3. **ALWAYS use .gitignore to exclude sensitive files**
4. **READ `SECURITY.md` before deployment**

**Files to NEVER commit:**
- `credentials/credentials.json`
- `credentials/token.pickle`
- `../../Anthropic_API_Key/*`

---

## 📋 Checklist

Before you begin, ensure you have:

- [ ] WSL (Windows Subsystem for Linux) running Ubuntu
- [ ] Python 3.8 or higher installed
- [ ] Google Account with Gmail and Calendar
- [ ] Anthropic API Key
- [ ] Git installed (optional)

---

## 🚀 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd C:\Users\yair0\AI_continue\Lesson34_Gmail_API_AI_Agents\gmail_api
```

Or in WSL:
```bash
cd /mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
```

---

### Step 2: Create Virtual Environment

**Navigate to venv location:**
```bash
cd ../..
```

**Create virtual environment:**
```bash
python3 -m venv venv
```

**Verify creation:**
```bash
ls -la venv/
```

You should see `bin/`, `lib/`, `include/`, etc.

---

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt:
```
(venv) user@machine:~$
```

---

### Step 4: Navigate Back to Project

```bash
cd AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
```

---

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Collecting google-auth>=2.25.0
Collecting google-auth-oauthlib>=1.2.0
...
Successfully installed google-auth-2.25.0 ...
```

**Verify installation:**
```bash
pip list | grep google
```

---

### Step 6: Set Up Google API Credentials

#### A. Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click "Create Project"
3. Name: "Gmail Event Scanner"
4. Click "Create"

#### B. Enable APIs

1. Go to "APIs & Services" > "Library"
2. Search and enable:
   - **Gmail API**
   - **Google Calendar API**

#### C. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS"
3. Select "OAuth client ID"
4. Application type: "Desktop app"
5. Name: "Gmail Scanner Desktop"
6. Click "Create"
7. Click "DOWNLOAD JSON"

#### D. Place Credentials

```bash
# Create credentials directory
mkdir -p credentials

# Move downloaded file
mv ~/Downloads/client_secret_*.json credentials/credentials.json
```

**Verify:**
```bash
ls -la credentials/
```

You should see `credentials.json`.

---

### Step 7: Set Up Anthropic API Key

#### A. Get API Key

1. Go to: https://console.anthropic.com/
2. Navigate to "API Keys"
3. Create new key or copy existing
4. Save it securely

#### B. Create Key Directory

```bash
# Navigate to correct location
cd ../..
mkdir -p Anthropic_API_Key
cd Anthropic_API_Key
```

#### C. Save API Key

**Option 1: Using echo**
```bash
echo "your-api-key-here" > api_key.dat
```

**Option 2: Using nano**
```bash
nano api_key.dat
# Paste your key, press Ctrl+X, Y, Enter
```

**Verify:**
```bash
cat api_key.dat
# Should show your API key
```

**Secure the file:**
```bash
chmod 600 api_key.dat
```

#### D. Return to Project

```bash
cd ../AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
```

---

### Step 8: Verify Security Setup

**CRITICAL: Verify no secrets will be committed**

```bash
# 1. Check .gitignore exists and is configured
cat gitignore.txt  # Review the file
mv gitignore.txt .gitignore  # Rename it

# 2. Verify git ignores credential files
git status --ignored

# Should show:
# Ignored files:
#   credentials/
#   ../../Anthropic_API_Key/

# 3. Set proper file permissions
chmod 600 credentials/credentials.json
chmod 600 ../../Anthropic_API_Key/api_key.dat

# 4. Verify no secrets in tracked files
git ls-files | xargs grep -l "sk-ant-\|AIza" || echo "✓ No secrets found"
```

**If git tracking shows credentials:**
```bash
# Remove from git (keeps local copy)
git rm --cached credentials/credentials.json
git rm --cached -r ../../Anthropic_API_Key/
```

---

### Step 9: Configure Application

**Copy template:**
```bash
cp config.yaml config.example.yaml  # Keep backup
```

**Edit configuration:**
```bash
nano config.yaml
```

**Example configuration:**
```yaml
search_criteria:
  subject_keyword: "meeting"
  sender_email: ""
  label: ""
  unread_only: true

polling:
  scan_interval_seconds: 300

calendar:
  timezone: "America/New_York"  # Change to your timezone
```

**Save and exit:** `Ctrl+X`, `Y`, `Enter`

---

### Step 9: Create Log Directory

```bash
mkdir -p log
```

---

### Step 10: First Run

**Make run script executable:**
```bash
chmod +x run.sh
```

**Run the application:**
```bash
./run.sh
```

Or:
```bash
python -m gmail_api.main
```

---

## ✅ Verification

### Check Installation

**1. Virtual Environment:**
```bash
which python
# Should show: /path/to/venv/bin/python
```

**2. Packages:**
```bash
pip list | grep -E "(google|anthropic|yaml)"
```

Should show:
- google-api-python-client
- google-auth
- anthropic
- PyYAML

**3. Project Structure:**
```bash
tree -L 2 -I '__pycache__|*.pyc'
```

Should show:
```
.
├── __init__.py
├── main.py
├── tasks.py
├── config.py
├── gmail_scanner.py
├── calendar_manager.py
├── email_parser.py
├── auth_manager.py
├── logger_setup.py
├── config.yaml
├── requirements.txt
├── credentials/
│   └── credentials.json
└── log/
```

**4. Credentials:**
```bash
ls -la credentials/
ls -la ../../Anthropic_API_Key/
```

---

## 🔧 First-Time OAuth Flow

When you run the application for the first time:

1. **Browser Opens:**
   - Automatic OAuth consent screen
   - Google sign-in page

2. **Grant Permissions:**
   - Gmail: Read and modify
   - Calendar: Manage events

3. **Token Saved:**
   - Creates `credentials/token.pickle`
   - Future runs won't need browser

---

## 🧪 Test Run

### One-Time Mode Test

```bash
./run.sh
# Select: 1 (One-time mode)
```

**Expected:**
- "Authenticating with Google APIs..."
- "Connecting to Gmail..."
- "Loading Anthropic API key..."
- Search results or "No emails found"

### Polling Mode Test

```bash
./run.sh
# Select: 2 (Polling mode)
# Wait for one scan cycle
# Press Ctrl+C to stop
```

**Expected:**
- Continuous scanning messages
- Log entries every interval
- Graceful shutdown on Ctrl+C

---

## 🐛 Troubleshooting

### Issue: `venv not found`

**Solution:**
```bash
cd ../..
python3 -m venv venv
```

---

### Issue: `No module named 'google'`

**Solution:**
```bash
source ../../venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: `credentials.json not found`

**Solution:**
```bash
ls credentials/
# If empty, download from Google Cloud Console
```

---

### Issue: `Invalid Anthropic API key`

**Solution:**
```bash
cat ../../Anthropic_API_Key/api_key.dat
# Verify key is correct and properly formatted
```

---

### Issue: `Permission denied: ./run.sh`

**Solution:**
```bash
chmod +x run.sh
./run.sh
```

---

## 📚 Next Steps

After successful installation:

1. **Read documentation:**
   - `README.md` - Complete usage guide
   - `PRD.md` - Product requirements
   - `Claude.md` - AI integration details

2. **Configure search criteria:**
   - Edit `config.yaml`
   - Choose ONE search criterion
   - Adjust polling interval

3. **Test with real emails:**
   - Send yourself a test meeting invite
   - Run in one-time mode
   - Verify calendar event created

4. **Set up automation:**
   - Run in polling mode
   - Monitor logs
   - Adjust configuration as needed

---

## 📞 Support

If you encounter issues:

1. Check the logs: `cat log/app.log`
2. Review README.md troubleshooting section
3. Verify all prerequisites are met
4. Check file permissions

---

## 🎉 Success!

You've successfully installed Gmail Event Scanner!

**Quick reference:**
```bash
# Activate venv
source ../../venv/bin/activate

# Run application
./run.sh

# View logs
tail -f log/app.log

# Deactivate venv
deactivate
```

---

**Happy scanning! 🚀**
