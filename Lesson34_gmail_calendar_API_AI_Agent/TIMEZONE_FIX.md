# Timezone Fix
# Gmail Event Scanner - Fix Calendar Time Issues

**Issue:** Events appear 2 hours late in calendar  
**Cause:** Configuration using UTC instead of Israel time  
**Solution:** Change timezone in config.yaml

---

## 🕐 The Problem

**What you see in email:**
- Meeting: 10:00 AM - 11:00 AM

**What appears in calendar:**
- Meeting: 12:00 PM - 1:00 PM (2 hours later!)

**Why:** The application is using UTC timezone, but you're in Israel (UTC+2).

---

## ✅ Quick Fix (30 seconds)

### Step 1: Edit config.yaml

```bash
cd /mnt/c/Users/yair0/AI_continue/Lesson34_Gmail_API_AI_Agents/gmail_api
nano config.yaml
```

### Step 2: Find the calendar section

Look for this section (around line 46):
```yaml
calendar:
  timezone: "UTC"
```

### Step 3: Change to Israel timezone

**Change it to:**
```yaml
calendar:
  timezone: "Asia/Jerusalem"
```

### Step 4: Save and exit

Press: `Ctrl+X`, then `Y`, then `Enter`

---

## 🧪 Test It

### Delete the incorrect event (optional)

Go to Google Calendar and delete the event created at 12:00 PM.

### Run the application again

```bash
./run.sh
```

**Now the event should appear at the correct time: 10:00 AM - 11:00 AM** ✅

---

## 🌍 Other Timezone Options

If you're not in Israel, use your correct timezone:

### Common Timezones

| Location | Timezone String |
|----------|----------------|
| Israel | `Asia/Jerusalem` |
| United States (Eastern) | `America/New_York` |
| United States (Pacific) | `America/Los_Angeles` |
| United States (Central) | `America/Chicago` |
| United States (Mountain) | `America/Denver` |
| United Kingdom | `Europe/London` |
| France/Germany | `Europe/Paris` |
| India | `Asia/Kolkata` |
| Japan | `Asia/Tokyo` |
| Australia (Sydney) | `Australia/Sydney` |
| Brazil (São Paulo) | `America/Sao_Paulo` |

### Find Your Timezone

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

Look for your timezone in the "TZ identifier" column.

---

## 📝 Understanding Timezone Offsets

### Israel Time (Asia/Jerusalem)
- **Winter (Standard Time):** UTC+2
- **Summer (Daylight Saving):** UTC+3
- The system handles DST automatically

### How it Works

1. Email says: "10:00 AM"
2. Application interprets: "10:00 AM in Asia/Jerusalem timezone"
3. Google Calendar stores: "10:00 AM Israel time"
4. When you view in calendar: Shows "10:00 AM" (your local time)

### What Was Happening Before

1. Email says: "10:00 AM"
2. Application interprets: "10:00 AM in UTC"
3. Google Calendar stores: "10:00 AM UTC"
4. When you view in calendar: Shows "12:00 PM" (UTC+2 = 10:00+2:00)

---

## 🔍 Verify Your Configuration

After editing config.yaml:

```bash
grep -A 1 "timezone:" config.yaml
```

**Should show:**
```yaml
  timezone: "Asia/Jerusalem"
```

---

## ⚠️ Important Notes

### For Existing Events

Changing the timezone in config.yaml only affects **NEW** events. Old events will still show the wrong time.

**Options:**
1. **Delete old events** in Google Calendar
2. **Edit old events** manually in Google Calendar
3. **Leave them** - they'll stay at the wrong time

### For Future Events

All new events created after changing the timezone will use the correct time.

### Timezone vs Calendar Display

- The **timezone in config.yaml** determines how times are **stored**
- Your **Google Calendar timezone setting** determines how times are **displayed**
- Make sure both are set to your local timezone

---

## 🚨 Common Mistakes

### ❌ Wrong Timezone Format

```yaml
timezone: "Israel"  # Wrong - not a valid timezone
timezone: "GMT+2"   # Wrong - use IANA names
timezone: "IST"     # Wrong - ambiguous (India/Israel/Ireland?)
```

### ✅ Correct Timezone Format

```yaml
timezone: "Asia/Jerusalem"  # Correct - IANA timezone name
```

---

## 📋 Complete Example config.yaml

```yaml
search_criteria:
  subject_keyword: "meeting"
  sender_email: ""
  label: ""
  unread_only: false

polling:
  scan_interval_seconds: 300

calendar:
  timezone: "Asia/Jerusalem"  # ← Changed this!

system:
  log_level: "INFO"
  max_emails_per_scan: 50
  api_retry_attempts: 3
  enable_multiprocessing: true
  max_workers: 4
```

---

## ✅ Verification Checklist

After making the change:

- [ ] Edited `config.yaml`
- [ ] Changed `timezone: "UTC"` to `timezone: "Asia/Jerusalem"`
- [ ] Saved the file
- [ ] Verified with `grep -A 1 "timezone:" config.yaml`
- [ ] Deleted incorrect calendar event (optional)
- [ ] Ran `./run.sh` again
- [ ] New event appears at correct time (10:00 AM)

---

## 🎉 Expected Result

**Before fix:**
```
Email time: 10:00 AM - 11:00 AM
Calendar shows: 12:00 PM - 1:00 PM  ❌
```

**After fix:**
```
Email time: 10:00 AM - 11:00 AM
Calendar shows: 10:00 AM - 11:00 AM  ✅
```

---

## 💡 Pro Tip

If you travel frequently or work with people in different timezones, you can:

1. **Keep config.yaml at your home timezone** (Asia/Jerusalem)
2. **Let Google Calendar handle display** (it converts automatically)
3. **Everyone sees events in their local time**

This way, when you create an event at "10:00 AM", it's stored as "10:00 AM Israel time", and people in New York see it as "3:00 AM" their time.

---

## 🆘 Still Not Working?

### Check Your Actual File

```bash
cat config.yaml | grep -A 2 "calendar:"
```

Should show:
```yaml
calendar:
  timezone: "Asia/Jerusalem"
```

### Verify the Change Was Applied

```bash
python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['calendar']['timezone'])"
```

Should output: `Asia/Jerusalem`

### Check Google Calendar Settings

1. Go to Google Calendar settings
2. Check "Time zone" under "General"
3. Make sure it's set to your local timezone too

---

**That's it! Your calendar events will now appear at the correct time.** 🎉

**Quick command:**
```bash
sed -i 's/timezone: "UTC"/timezone: "Asia\/Jerusalem"/' config.yaml
```

This automatically updates the file for you!
