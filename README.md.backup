# ApkPatcher - Google OAuth Fix Edition

[![GitHub](https://img.shields.io/badge/GitHub-baretoaldo-blue?style=for-the-badge&logo=github)](https://github.com/baretoaldo/ApkPatcher)
[![Fixed](https://img.shields.io/badge/Google_OAuth-FIXED-success?style=for-the-badge)](https://github.com/baretoaldo/ApkPatcher)

> **🔧 Modified Version:** This is a fixed version of ApkPatcher that resolves Google OAuth login issues in patched APKs.

## ✅ What's New in This Fork

### Google OAuth Login Fix
- **Problem Solved:** Apps with "Login via Google" now work correctly after patching
- **Selective SSL Bypass:** Google OAuth domains excluded from certificate manipulation
- **API Capture Still Works:** Non-OAuth endpoints remain fully capturable

### Key Changes
- ✅ Google OAuth login **SUCCESS** (accounts.google.com, oauth2.googleapis.com)
- ✅ App API endpoints **CAPTURABLE** (api.yourapp.com, etc.)
- ✅ Firebase/Google APIs **SUPPORTED** (with user certificates)
- ✅ Backward compatible with all existing ApkPatcher features

---

## 🎯 Why This Fork?

**Original ApkPatcher Issue:**
```
[❌] Patch APK with Google OAuth
[❌] Install and try "Login via Google"
[❌] Result: Blank screen / No response / Login failed
```

**This Fixed Version:**
```
[✅] Patch APK with this fork
[✅] Install and try "Login via Google"
[✅] Result: Login SUCCESS! + API capture works!
```

---

## 📦 Installation Method
-------
**💢 Requirement PKG 💢**

    termux-setup-storage && pkg update -y && pkg upgrade -y && pkg install python -y

**👉🏻 To install ApkPatcher, Run only any one cmd from the Installation Method**

**💢 PYPI ( Just Testing ) 💢**

    pip install ApkPatcherX

[![PyPI](https://img.shields.io/badge/pypi-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)](https://pypi.org/project/ApkPatcherX) [![Version](https://img.shields.io/pypi/v/ApkPatcherX?label=&style=for-the-badge&color=FF8C00&labelColor=FF8C00)](https://pypi.org/project/ApkPatcherX)


**1st. Method**

`💢 For Latest Commit ( From Main  Branch )  💢`

    pip install --force-reinstall https://github.com/TechnoIndian/ApkPatcher/archive/refs/heads/main.zip

`Or`

    pip install --force-reinstall https://github.com/TechnoIndian/ApkPatcher/archive/refs/heads/main.tar.gz

`Or`

    curl -Ls https://github.com/TechnoIndian/Tools/releases/download/Tools/ApkPatcher.sh | bash

**2nd. Method**

    pkg install python git && pip install git+https://github.com/TechnoIndian/ApkPatcher.git


Uninstall ApkPatcher
-----

    pip uninstall ApkPatcherX


---

## 🚀 Usage

### Basic Usage (Same as Original!)

**Patch APK with SSL Bypass**
```bash
ApkPatcher -i YourApp.apk
```

**With Custom Certificate**
```bash
ApkPatcher -i YourApp.apk -c YourCert.pem
```
    
`With Your Certificate ( Input Your pem/ crt / cert Path )`

    ApkPatcher -i YourApkPath.apk -c YourCertificatePath.cert

`Multiple Certificate`

    ApkPatcher -i YourApkPath.apk -c /sdcard/HttpCanary/certs/HttpCanary.pem /sdcard/Download/Reqable/reqable-ca.crt /sdcard/Download/ProxyPinCA.crt

`If using emulator on PC then use Flag: -e`

    ApkPatcher -i YourApkPath.apk -e -c YourCertificatePath.cert

**Mode -i & -f / -p ➸ Flutter & Pairip SSL Bypass**

    ApkPatcher -i YourApkPath.apk -f

`For Pairip`

    ApkPatcher -i YourApkPath.apk -p

`With Your Certificate ( Input Your pem / crt / cert Path )`

    ApkPatcher -i YourApkPath.apk -f -p -c YourCertificatePath.cert

**Mode -i & -D ➸ Android ID & Smali Patcher**

`With Your Android ID ( Input Your Custom 16 Digit Android ID )`

    ApkPatcher -i YourApkPath.apk -D 7e9f51f096bd5c83

**Mode -i & -pkg Spoof Package Detection (Dex/Manifest/Res)**

    ApkPatcher -i YourApkPath.apk -pkg

**Mode -i & -P ➸ Purchase/Paid/Price**

    ApkPatcher -i YourApkPath.apk -P

**Mode -i & --rmads / rmsc / -rmu ➸ Bypass Ads & Screenshot / USB Restriction**

`Remove Ads Flag: -rmads`

    ApkPatcher -i YourApkPath.apk -rmads

`Bypass Screenshot Restriction Flag: -rmsc`

    ApkPatcher -i YourApkPath.apk -rmsc

`Bypass USB Debugging Permission Flag: -rmu`

    ApkPatcher -i YourApkPath.apk -rmu

**Mode -i & -skip ➸ Skip Patch (e.g., getAcceptedIssuers)**

    ApkPatcher -i YourApkPath.apk -skip getAcceptedIssuers

**Mode -i & -A ➸ AES Logs Inject**

`AES MT Logs Inject`

    ApkPatcher -i YourApkPath.apk -A

`Do U Want Separate AES.smali Dex`

    ApkPatcher -i YourApkPath.apk -A -s

**Mode i & -r ➸ Random/Fake Device Info**

`Random/Fake Device Info`

    ApkPatcher -i YourApkPath.apk -r

`With Your Android ID ( Input Your Custom 16 Digit Android ID )`

    ApkPatcher -i YourApkPath.apk -r -D 7e9f51f096bd5c83

**Mode -m ➸ Only Merge Apk**

    ApkPatcher -m YourApkPath.apk

**Mode -C ➸ Credits & Instruction**

    ApkPatcher -C
    
**Mode -h ➸ Help**

    ApkPatcher -h

**Mode -O ➸ Other Patch Flags**

    ApkPatcher -O

---

## 🧪 Testing Google OAuth Fix

### Test Case: TikTok/Instagram/Any App with Google Login

```bash
# 1. Patch the APK
ApkPatcher -i TikTok.apk -c /sdcard/HttpCanary/certs/HttpCanary.pem

# 2. Install patched APK
adb install TikTok_Patched.apk

# 3. Open app and test
# - Click "Login via Google"
# - Expected: ✅ LOGIN SUCCESS (not blank screen!)
# - Check HttpCanary: ✅ API calls captured (non-OAuth traffic)
```

### Expected Results

| Test | Before (Original) | After (This Fork) |
|------|-------------------|-------------------|
| Google OAuth Login | ❌ Failed | ✅ **SUCCESS** |
| API Capture | ✅ Works | ✅ **Works** |
| Overall | ❌ Unusable | ✅ **Fully Functional** |

---

## 🔍 Technical Details

### What Changed?

**File Modified:** `ApkPatcher/Patch/Cert_Net_Config.py`

**3-Tier Priority System:**

1. **Priority 1: Google OAuth (NO BYPASS)**
   - `accounts.google.com` → Normal SSL validation
   - `oauth2.googleapis.com` → Normal SSL validation
   - Result: **Login works!** ✅

2. **Priority 2: Google APIs (USER CERT ALLOWED)**
   - `googleapis.com`, `firebaseio.com`, `fcm.googleapis.com`
   - Result: Capturable with user certificates ⚠️

3. **Priority 3: All Other Domains (FULL BYPASS)**
   - `api.yourapp.com`, `cdn.yourapp.com`, etc.
   - Result: **Fully capturable!** ✅

### Why This Works?

Google OAuth servers detect certificate manipulation and reject authentication. By excluding OAuth domains from SSL bypass, we allow normal certificate validation for login while maintaining full capture capability for app-specific endpoints.

---

## 📖 Documentation

- **[GOOGLE_OAUTH_FIX_README.md](GOOGLE_OAUTH_FIX_README.md)** - Detailed fix explanation
- **Original ApkPatcher:** [TechnoIndian/ApkPatcher](https://github.com/TechnoIndian/ApkPatcher)

---

## 🙏 Credits

- **Original ApkPatcher:** [TechnoIndian](https://github.com/TechnoIndian/ApkPatcher)
- **Google OAuth Fix:** [baretoaldo](https://github.com/baretoaldo)
- **Community:** [@rktechnoindians](https://t.me/rktechnoindians)

---

## ⚖️ Legal Disclaimer

⚠️ **Educational & Security Research Purposes Only**

**Use this tool ONLY for:**
- ✅ Testing your own applications
- ✅ Bug bounty programs (with proper authorization)
- ✅ Security research (ethical & legal)

**DO NOT use for:**
- ❌ Piracy or bypassing premium features
- ❌ Hacking applications without authorization
- ❌ Violating Terms of Service
- ❌ Any illegal activities

**Use at your own risk.** The authors are not responsible for misuse of this tool.

---

## 📞 Support

- **GitHub Issues:** [Report bugs here](https://github.com/baretoaldo/ApkPatcher/issues)
- **Original Project:** [TechnoIndian/ApkPatcher](https://github.com/TechnoIndian/ApkPatcher)
- **Community:** [Telegram Channel](https://t.me/rktechnoindians)

---

## 📝 Note

This is a **modified fork** for educational purposes. All credits for the original ApkPatcher go to [TechnoIndian](https://github.com/TechnoIndian). This fork specifically addresses Google OAuth login issues while maintaining all original functionality.

**Star ⭐ this repo if the Google OAuth fix helped you!**
