# Distribution Guide
**Exercise Checking System v1.0.0**

---

## For Package Distributors

This guide is for those distributing the Exercise Checking System package to end users.

---

## Files to Distribute

### Required Files (Send to users)

1. **exercise_checking_system_v1.0.0.tar.gz** (59 KB)
   - **Or** exercise_checking_system_v1.0.0.zip (81 KB)
   - Choose based on user's platform preference
   - Linux/WSL users prefer .tar.gz
   - Windows users may prefer .zip

2. **CHECKSUMS.txt** (207 bytes)
   - For package integrity verification
   - Users can verify the download wasn't corrupted

3. **PACKAGE_SUMMARY.md** (12 KB) - Optional but recommended
   - Provides complete overview
   - Installation quick start
   - Feature list

---

## Files to Keep Internal

### Do NOT Distribute

❌ **credentials.json** - Gmail API credentials
   - Security sensitive
   - Each user must obtain their own
   - See instructions below

❌ **token.pickle** - Gmail API token
   - Auto-generated during first run
   - User-specific
   - Should never be shared

❌ **Original check_exercise/ directory**
   - May contain sensitive data
   - May contain user-specific files
   - Use the cleaned package instead

---

## Distribution Methods

### Method 1: Direct File Transfer

```bash
# What to send:
- exercise_checking_system_v1.0.0.tar.gz (or .zip)
- CHECKSUMS.txt
- PACKAGE_SUMMARY.md (optional)

# Via email, file sharing service, or USB drive
```

### Method 2: File Server

```bash
# Upload to shared drive:
/shared/software/exercise_checking_system/v1.0.0/
├── exercise_checking_system_v1.0.0.tar.gz
├── exercise_checking_system_v1.0.0.zip
├── CHECKSUMS.txt
└── PACKAGE_SUMMARY.md
```

### Method 3: Version Control

```bash
# If using Git (for controlled distribution):
git init
git add exercise_checking_system_package/
git commit -m "Initial release v1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push to private repository
git remote add origin <your-private-repo>
git push origin main --tags
```

---

## User Instructions to Provide

### Step 1: Download and Verify

```bash
# Download the package
# Verify checksum
sha256sum -c CHECKSUMS.txt
```

### Step 2: Extract Package

**For tar.gz:**
```bash
tar -xzf exercise_checking_system_v1.0.0.tar.gz
cd exercise_checking_system_package
```

**For zip:**
```bash
unzip exercise_checking_system_v1.0.0.zip
cd exercise_checking_system_package
```

### Step 3: Obtain Gmail Credentials

**Important:** Users must obtain their own Gmail API credentials

**Instructions for users:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable Gmail API:
   - Navigate to "APIs & Services" → "Library"
   - Search "Gmail API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app"
   - Download JSON file
5. Rename to `credentials.json`
6. Place in package directory

### Step 4: Install and Run

```bash
# Run setup
./setup.sh

# Activate environment
source venv/bin/activate

# Start application
python3 main.py
```

---

## Support Information for Users

### Documentation Included in Package

- **README.md** - User guide and overview
- **INSTALL.md** - Detailed installation instructions
- **PRD.md** - Complete requirements and specifications
- **Claude.md** - Claude AI integration details
- **planning.md** - System architecture
- **tasks.md** - Troubleshooting and tasks

### Common Issues and Solutions

**Issue 1: "credentials.json not found"**
- User must obtain Gmail API credentials
- See "Obtain Gmail Credentials" section above
- File must be named exactly "credentials.json"

**Issue 2: "Python 3 not found"**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Issue 3: "setup.sh permission denied"**
```bash
chmod +x setup.sh
```

**Issue 4: "Module not found" errors**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Version Information

**Current Version:** 1.0.0
**Release Date:** 2025-11-25
**Minimum Python:** 3.8
**Platform:** WSL/Linux

---

## Package Checksums

Provide these to users for verification:

```
SHA256:
tar.gz: 5cd9c020c303853b64b3c47ea85ab1f06c4d5dcbc0d1f70b2da8a8a7f0893a2c
zip:    18101f210f0f3a5e7b290493e1207041b0e944be8c263b90bcbd3d5138dd281a
```

Users can verify with:
```bash
sha256sum exercise_checking_system_v1.0.0.tar.gz
# Should match the hash above
```

---

## What's Included in Package

### Core Components

✓ Main application with menu interface
✓ 4 agent definitions (Gmail, Code Analysis, Greeting, Draft Sender)
✓ 4 agent skills with implementations
✓ Logging system (ring buffer)
✓ Configuration files
✓ Setup automation
✓ Comprehensive documentation

### What Users Must Provide

⚠ Gmail API credentials (credentials.json)
⚠ Internet connection for Gmail/GitHub APIs
⚠ Python 3.8+ installed

---

## License and Usage Terms

**License:** Internal Use Only
**Restrictions:**
- Not for public distribution
- Not for commercial use outside organization
- All rights reserved

**Permitted:**
- Internal use within organization
- Educational purposes (if authorized)
- Development and testing

---

## Update Policy

### How to Distribute Updates

When releasing v1.0.1 or v1.1.0:

1. Create new package with version number
2. Update VERSION file in package
3. Update CHECKSUMS.txt
4. Update PACKAGE_SUMMARY.md
5. Notify users of new version
6. Provide migration guide if needed

### Naming Convention

```
exercise_checking_system_v{MAJOR}.{MINOR}.{PATCH}.{tar.gz|zip}

Examples:
- v1.0.0 - Initial release
- v1.0.1 - Bug fix
- v1.1.0 - New features
- v2.0.0 - Major changes
```

---

## Contact Information

**Package Maintainer:** Yair Levi
**Version:** 1.0.0
**Created:** 2025-11-25

---

## Distribution Checklist

Before distributing to users:

- [ ] Package files created (tar.gz and/or zip)
- [ ] CHECKSUMS.txt generated
- [ ] PACKAGE_SUMMARY.md reviewed
- [ ] credentials.json NOT included
- [ ] token.pickle NOT included
- [ ] Sensitive data removed
- [ ] Version number correct
- [ ] Documentation up to date
- [ ] Installation tested
- [ ] User instructions provided
- [ ] Support contact information included

---

## Quick Distribution Script

```bash
#!/bin/bash
# distribute.sh - Package distribution helper

VERSION="1.0.0"
PKG_NAME="exercise_checking_system_v${VERSION}"

# Create distribution directory
mkdir -p distribution/

# Copy package files
cp ${PKG_NAME}.tar.gz distribution/
cp ${PKG_NAME}.zip distribution/
cp CHECKSUMS.txt distribution/
cp PACKAGE_SUMMARY.md distribution/

# Create README for distributors
cat > distribution/README_DISTRIBUTOR.txt << EOF
Exercise Checking System v${VERSION}
Distribution Package

Files in this directory:
- ${PKG_NAME}.tar.gz - Linux/WSL package
- ${PKG_NAME}.zip - Cross-platform package
- CHECKSUMS.txt - Package checksums
- PACKAGE_SUMMARY.md - Complete package information

Send these files to end users.
Users must obtain their own credentials.json.

For questions, contact: Yair Levi
EOF

echo "Distribution package ready in: distribution/"
ls -lh distribution/
```

---

## End User Quick Start Card

Provide this to users:

```
╔══════════════════════════════════════════════════════════════╗
║         EXERCISE CHECKING SYSTEM - QUICK START               ║
║                      Version 1.0.0                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. EXTRACT PACKAGE:                                         ║
║     tar -xzf exercise_checking_system_v1.0.0.tar.gz         ║
║                                                              ║
║  2. GET CREDENTIALS:                                         ║
║     • Go to console.cloud.google.com                        ║
║     • Enable Gmail API                                       ║
║     • Create OAuth credentials                               ║
║     • Download as credentials.json                           ║
║                                                              ║
║  3. SETUP:                                                   ║
║     cd exercise_checking_system_package                      ║
║     cp /path/to/credentials.json .                          ║
║     ./setup.sh                                              ║
║                                                              ║
║  4. RUN:                                                     ║
║     source venv/bin/activate                                ║
║     python3 main.py                                         ║
║                                                              ║
║  HELP: Read INSTALL.md for detailed instructions            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

**Distribution Guide Version:** 1.0.0
**Last Updated:** 2025-11-25
**Status:** Ready for Distribution
