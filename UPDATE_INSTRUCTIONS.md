# Update Instructions
# How to Update Your Gmail Event Scanner Files

**Date:** January 30, 2026  
**Issue:** Running old version of files with bugs

---

## 🔍 Problem

You're still running the old version of the code. The error message shows:
```
timeMin=2026-01-30T10%3A00%3A00&timeMax=2026-01-30T10%3A00%3A00
```

This indicates the old `calendar_manager.py` is being used (both times are the same).

---

## ✅ Solution: Update Your Files

You need to download and replace these files:

### Required Updates (2 files)

1. **calendar_manager.py** - Fixed duplicate check bug
2. **email_parser.py** - Improved date parsing

---

## 📋 Step-by-Step Update Process

### Method 1: Download and Replace (Recommended)

**Step 1: Download the updated files**
- Download `calendar_manager.py` from the outputs
- Download `email_parser.py` from the outputs

**Step 2: Navigate to your project directory**
```bash
cd /mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
```

**Step 3: Backup your current files (optional)**
```bash
cp calendar_manager.py calendar_manager.py.backup
cp email_parser.py email_parser.py.backup
```

**Step 4: Replace with new files**
```bash
# Copy the newly downloaded files to the gmail_api directory
# (Overwrite the existing files)
```

**Step 5: Verify the update**
```bash
# Check that the new version has end_time in the duplicate check
grep "end_time = event_body\['end'\]" calendar_manager.py

# Should output: end_time = event_body['end']['dateTime']
```

---

### Method 2: Direct Edit (Alternative)

If you can't download, edit the file directly:

**Edit calendar_manager.py:**
```bash
nano calendar_manager.py
```

**Find line ~109:** (around line 109)
```python
start_time = event_body['start']['dateTime']
```

**Add this line right after it:**
```python
end_time = event_body['end']['dateTime']
```

**Find line ~115:** (around line 115)
```python
timeMax=start_time,
```

**Change it to:**
```python
timeMax=end_time,
```

**Save and exit:** Ctrl+X, Y, Enter

---

## 🧪 Test the Update

After updating, run again:

```bash
./run.sh
```

**Expected behavior:**
1. ✅ No "Duplicate check failed" warning
2. ✅ Event created successfully
3. ✅ If you run again, it should detect the duplicate and skip

---

## 📊 Verify Which Version You Have

**Check if you have the OLD version (buggy):**
```bash
grep -A 5 "def check_duplicate_event" calendar_manager.py | grep -c "end_time"
```
- If output is `0` → You have the OLD version (needs update)
- If output is `1` or more → You have the NEW version (good!)

**Check if you have the NEW version (fixed):**
```bash
grep "end_time = event_body" calendar_manager.py
```
- If output shows the line → You have the NEW version ✅
- If no output → You have the OLD version ❌

---

## 🎯 What Each File Does

### calendar_manager.py (132 lines)
**OLD version (buggy):**
```python
start_time = event_body['start']['dateTime']
# Missing: end_time line
events_result = service.events().list(
    calendarId='primary',
    timeMin=start_time,
    timeMax=start_time,  # ❌ BUG: Same as timeMin
```

**NEW version (fixed):**
```python
start_time = event_body['start']['dateTime']
end_time = event_body['end']['dateTime']  # ✅ Added this line
events_result = service.events().list(
    calendarId='primary',
    timeMin=start_time,
    timeMax=end_time,  # ✅ Fixed: Uses end_time
```

### email_parser.py (124 lines)
**Improvements:**
- Better date format handling (DD/MM/YYYY)
- Current day context
- More explicit examples

---

## 🚨 Common Mistakes

❌ **Don't do this:**
- Copy files to wrong directory
- Edit wrong file
- Forget to save after editing
- Run without updating

✅ **Do this:**
- Update in correct directory: `/mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api/`
- Verify the update worked
- Test after updating

---

## 📝 Verification Checklist

After updating, verify:

- [ ] Downloaded `calendar_manager.py` from outputs
- [ ] Downloaded `email_parser.py` from outputs  
- [ ] Replaced files in `/mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api/`
- [ ] Verified `end_time` line exists in calendar_manager.py
- [ ] Tested with `./run.sh`
- [ ] No more "Duplicate check failed" warning
- [ ] Event created successfully

---

## 🎉 After Successful Update

You should see this in the logs:
```
✅ No "Duplicate check failed: Bad Request" warning
✅ "Duplicate event found: [event name]" (if running second time)
✅ "Event created successfully" (first time)
✅ "Skipping duplicate event" (second time)
```

---

## 🆘 Still Not Working?

If you still see the error after updating:

1. **Verify you updated the right file:**
   ```bash
   cat calendar_manager.py | grep -n "end_time = event_body"
   # Should show line number around 110
   ```

2. **Check file timestamps:**
   ```bash
   ls -la calendar_manager.py email_parser.py
   # Should show recent modification time
   ```

3. **Make sure you're running from the right directory:**
   ```bash
   pwd
   # Should output: /mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
   ```

4. **Restart if needed:**
   - Sometimes WSL caches Python files
   - Exit and restart your terminal
   - Or run: `deactivate && source ../../venv/bin/activate`

---

## 📞 Quick Reference

**Update command (if files downloaded to ~/Downloads):**
```bash
cd /mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
cp ~/Downloads/calendar_manager.py .
cp ~/Downloads/email_parser.py .
./run.sh
```

**Verify update worked:**
```bash
grep "end_time = event_body" calendar_manager.py && echo "✅ Updated!" || echo "❌ Not updated"
```

---

**You're running the OLD version. Please download and replace the updated files!**

**Files to update:**
1. calendar_manager.py
2. email_parser.py

**Location:** `/mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api/`
