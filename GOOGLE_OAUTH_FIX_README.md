# 🔧 ApkPatcher - Google OAuth Login Fix

## ✅ What's Fixed
- **Google OAuth Login now works!** Apps with "Login via Google" will authenticate successfully
- **API capture still works** for all non-OAuth endpoints
- **Selective SSL bypass** prevents Google from detecting certificate manipulation

## 🎯 Key Changes

### Modified File: `ApkPatcher/Patch/Cert_Net_Config.py`

**3-Tier Priority System:**

1. **Priority 1: Google OAuth (NO BYPASS)**
   - `accounts.google.com`
   - `oauth2.googleapis.com`
   - `www.googleapis.com`
   - `android.clients.google.com`
   - Uses system certificates only → Login SUCCESS ✅

2. **Priority 2: Google APIs (USER CERT ALLOWED)**
   - `googleapis.com`, `firebaseio.com`, `fcm.googleapis.com`
   - Allows user certificates → Post-login API capture possible ⚠️

3. **Priority 3: All Other Domains (FULL BYPASS)**
   - Wildcard `*` for app-specific domains
   - Full SSL bypass → Complete API capture ✅

## 🚀 Installation

### Quick Install
```bash
# Download this repository
git clone https://github.com/YOUR_USERNAME/ApkPatcher.git
cd ApkPatcher

# Install
pip install .
```

### Or Update Existing Installation
```bash
# Backup original
APKPATCHER_PATH=$(pip show ApkPatcherX | grep Location | cut -d' ' -f2)/ApkPatcher
cp "$APKPATCHER_PATH/Patch/Cert_Net_Config.py" "$APKPATCHER_PATH/Patch/Cert_Net_Config.py.backup"

# Replace with fixed version
cp ApkPatcher/Patch/Cert_Net_Config.py "$APKPATCHER_PATH/Patch/Cert_Net_Config.py"
```

## 📱 Usage (Same as Before!)

```bash
# Patch APK with Google OAuth login
ApkPatcher -i YourApp.apk -c YourCert.pem

# Install and test
adb install YourApp_Patched.apk
```

## 🧪 Test Results

| Test Case | Before | After |
|-----------|--------|-------|
| Google OAuth Login | ❌ Failed | ✅ **SUCCESS** |
| App API Capture | ✅ Works | ✅ **Works** |
| Google OAuth Traffic Capture | ⚠️ Captured (but login failed) | ❌ Not captured (expected) |

## 📊 Example: TikTok App

**Before Fix:**
```
[❌] Click "Login via Google" → Blank screen / Error
[✅] HttpCanary captures accounts.google.com
[❌] Login fails anyway
```

**After Fix:**
```
[✅] Click "Login via Google" → Login SUCCESS!
[❌] accounts.google.com NOT captured (expected)
[✅] api.tiktok.com/* captured successfully
[✅] App works perfectly
```

## 🔒 Security Note

⚠️ **This tool disables SSL verification for non-Google domains!**

**Only use for:**
- ✅ Testing your own apps
- ✅ Bug bounty (with authorization)
- ✅ Security research (ethical)

**Never use for:**
- ❌ Piracy / premium bypass
- ❌ Hacking other people's apps
- ❌ Violating Terms of Service

## 🙏 Credits

- **Original ApkPatcher**: [TechnoIndian](https://github.com/TechnoIndian/ApkPatcher)
- **Google OAuth Fix**: Selective SSL bypass implementation
- **Community**: [@rktechnoindians](https://t.me/rktechnoindians)

## 📞 Support

- **Telegram**: [t.me/rktechnoindians](https://t.me/rktechnoindians)
- **Issues**: [GitHub Issues](https://github.com/TechnoIndian/ApkPatcher/issues)

---

**Happy Hacking! (Ethically & Legally)** 🎉
