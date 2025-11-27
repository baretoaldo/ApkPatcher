# 🛠️ MTManager + ApkPatcher Google OAuth Fix Guide

## 🎯 Problem yang Diselesaikan

**Before:**
```
Split APK (.apks/.apkm) → Anti-Split merge → Patch → ❌ Google OAuth GAGAL
```

**After (MTManager Workflow):**
```
Split APK → MTManager merge (proper) → Patch (preserve metadata) → ✅ Google OAuth WORKS!
```

---

## 📱 MTManager Workflow (Step-by-Step)

### Preparation

**Yang Anda Butuhkan:**
1. ✅ MTManager installed (latest version)
2. ✅ Split APK file (.apks / .apkm / .xapk)
3. ✅ Custom certificate (HttpCanary/Reqable/Burp)
4. ✅ ApkPatcher (modified version dengan Google OAuth fix)

---

## 🔧 METHOD 1: MTManager Merge + ApkPatcher (RECOMMENDED)

### Step 1: Merge Split APK dengan MTManager

**1.1 Extract Split APK**
```
1. Open MTManager
2. Navigate ke folder .apks/.apkm
3. Long press file → Extract
4. Pilih folder tujuan (e.g., /sdcard/merged/)
5. Wait extraction complete
```

**1.2 Merge dengan MTManager (PROPER WAY)**
```
Option A: Auto Merge
1. Long press .apks file
2. Pilih "APK Editor"
3. Pilih "Merge Split APKs"
4. Output: merged.apk
5. ✅ Metadata preserved better!

Option B: Manual Merge (More Control)
1. Extract all split APKs
2. MTManager → Tools → "APK Merger"
3. Select base.apk sebagai base
4. Add config.arm64_v8a.apk
5. Add config.xxhdpi.apk (jika ada)
6. Add config.*.apk lainnya
7. Merge → Output: merged.apk
```

**1.3 Backup Original Signature Info**
```
1. MTManager → Select merged.apk
2. Klik "View" → "APK Info"
3. Note down:
   - Package name: com.example.app
   - Version code: 123
   - SHA-1: XX:XX:XX:... (IMPORTANT!)
4. Screenshot untuk referensi
```

---

### Step 2: Patch dengan ApkPatcher (Modified)

**2.1 Transfer APK ke Termux/Linux**
```bash
# Copy merged APK dari storage
cp /sdcard/merged/merged.apk ~/

# Or use adb
adb pull /sdcard/merged/merged.apk ~/
```

**2.2 Patch dengan ApkPatcher**
```bash
# Patch dengan preserve Google metadata
ApkPatcher -i merged.apk -c /sdcard/HttpCanary/certs/HttpCanary.pem

# Output: merged_Patched.apk
```

**2.3 Transfer Back ke Device**
```bash
# Copy patched APK back
cp merged_Patched.apk /sdcard/patched/

# Or use adb
adb push merged_Patched.apk /sdcard/patched/
```

---

### Step 3: Sign dengan MTManager (CRITICAL!)

**3.1 Import/Create Custom Keystore**

**Option A: Use Existing Keystore**
```
1. MTManager → Settings → Signature Management
2. Import your .keystore/.jks file
3. Enter password & alias
```

**Option B: Create New Keystore**
```
1. MTManager → Settings → Signature Management
2. "New Key" → Generate
3. Fill details:
   - Alias: mykey
   - Password: yourpassword
   - Validity: 25 years
   - Organization: YourName
4. Save → Note SHA-1 fingerprint!
```

**3.2 Sign APK dengan MTManager**
```
1. MTManager → Select merged_Patched.apk
2. Long press → "Sign APK"
3. Select your keystore
4. Enter password
5. Sign → Output: merged_Patched_signed.apk
6. ✅ APK signed with consistent certificate
```

**3.3 Verify Signature**
```
1. MTManager → View merged_Patched_signed.apk
2. "APK Info" → Check SHA-1
3. Compare dengan SHA-1 yang Anda note sebelumnya
4. Jika BERBEDA → Register SHA-1 baru di Google Console
```

---

### Step 4: Register SHA-1 di Google Console

**4.1 Get SHA-1 from Signed APK**
```
Method 1: MTManager
1. MTManager → View APK → APK Info
2. Copy SHA-1 fingerprint

Method 2: Termux
keytool -list -printcert -jarfile merged_Patched_signed.apk
Copy SHA1 line
```

**4.2 Register di Google Cloud Console**
```
1. Go to: https://console.cloud.google.com/
2. Select your project (or ask app developer)
3. APIs & Services → Credentials
4. Find "OAuth 2.0 Client IDs" → Android
5. Click Edit
6. Add new SHA-1 fingerprint:
   - Name: "Patched APK Debug"
   - SHA-1: [paste from above]
7. Save
8. Wait 5-10 minutes for propagation
```

**⚠️ Note:** Jika Anda BUKAN developer app-nya, Anda perlu:
- Contact developer untuk register SHA-1
- Atau create your own Google OAuth Client ID

---

### Step 5: Install & Test

**5.1 Uninstall Old Version**
```bash
# Via MTManager
Long press old APK → Uninstall

# Via adb
adb uninstall com.example.app
```

**5.2 Install Patched APK**
```
1. MTManager → Select merged_Patched_signed.apk
2. Click "Install"
3. Grant permissions
4. Wait installation complete
```

**5.3 Test Google OAuth Login**
```
1. Open app
2. Click "Login via Google"
3. Select Google account
4. Expected: ✅ Login SUCCESS!
5. Check HttpCanary: ✅ API calls captured
```

---

## 🔧 METHOD 2: MTManager Full Workflow (ALL-IN-ONE)

Jika Anda ingin semua dilakukan di MTManager tanpa Termux:

### Step 1: Merge Split APK
```
(Same as Method 1 - Step 1)
```

### Step 2: Decompile APK dengan MTManager

**2.1 Decompile**
```
1. MTManager → Select merged.apk
2. Long press → "APK Editor"
3. Choose "Decompile (Apktool)"
4. Wait decompile finish
5. Output folder: merged/
```

**2.2 Inject Certificate**
```
1. Navigate to: merged/res/raw/
2. Create folder if not exists
3. Copy your certificate.pem to raw/
4. Rename to: Techno_India.pem
```

**2.3 Create network_security_config.xml**
```
1. Navigate to: merged/res/xml/
2. Create folder if not exists
3. Create file: network_security_config.xml
4. Copy content (see XML below)
```

**network_security_config.xml Content:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config xmlns:android="http://schemas.android.com/apk/res/android">
    
    <!-- PRIORITY 1: Google OAuth - NO BYPASS -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="false">accounts.google.com</domain>
        <domain includeSubdomains="false">oauth2.googleapis.com</domain>
        <domain includeSubdomains="false">www.googleapis.com</domain>
        <domain includeSubdomains="false">android.clients.google.com</domain>
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </domain-config>
    
    <!-- PRIORITY 2: Google APIs - ALLOW USER CERT -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">googleapis.com</domain>
        <domain includeSubdomains="true">gstatic.com</domain>
        <domain includeSubdomains="true">firebaseio.com</domain>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </domain-config>
    
    <!-- PRIORITY 3: ALL OTHER DOMAINS - FULL BYPASS -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">*</domain>
        <trust-anchors>
            <certificates src="@raw/Techno_India" overridePins="true" />
            <certificates src="system" overridePins="true" />
            <certificates src="user" overridePins="true" />
        </trust-anchors>
    </domain-config>
    
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="@raw/Techno_India" overridePins="true" />
            <certificates src="system" overridePins="true" />
            <certificates src="user" overridePins="true" />
        </trust-anchors>
    </base-config>
    
</network-security-config>
```

**2.4 Edit AndroidManifest.xml**
```
1. Open: merged/AndroidManifest.xml
2. Find <application tag
3. Add/Edit attributes:
   android:usesCleartextTraffic="true"
   android:networkSecurityConfig="@xml/network_security_config"

Example:
<application
    android:name="..."
    android:usesCleartextTraffic="true"
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

**2.5 Clean Split Metadata (SELECTIVE)**

⚠️ **IMPORTANT:** Don't remove Google Services metadata!

Edit AndroidManifest.xml:
```xml
<!-- ❌ REMOVE these (App Bundle specific) -->
<meta-data android:name="com.android.vending.derived.apk.splits" ... />
<meta-data android:name="com.android.stamp.source" ... />
<meta-data android:name="com.android.stamp.type" ... />

<!-- ✅ KEEP these (Google Services - IMPORTANT!) -->
<meta-data android:name="com.google.android.gms.version" ... />
<meta-data android:name="com.google.android.gms.games.APP_ID" ... />
<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" ... />
```

---

### Step 3: Rebuild APK

**3.1 Compile**
```
1. MTManager → Select merged/ folder
2. Long press → "APK Editor"
3. Choose "Build (Apktool)"
4. Wait compile finish
5. Output: merged_rebuilt.apk
```

**3.2 Sign APK**
```
1. Select merged_rebuilt.apk
2. Long press → "Sign APK"
3. Use your keystore
4. Output: merged_rebuilt_signed.apk
```

---

### Step 4: Register SHA-1 & Install
```
(Same as Method 1 - Step 4 & 5)
```

---

## 🎓 Advanced Tips

### Tip 1: Preserve Original Signature (IF POSSIBLE)

Jika Anda punya akses ke **original keystore**:

```
1. Extract keystore dari developer
2. MTManager → Import keystore
3. Sign dengan keystore original
4. SHA-1 akan SAMA → No need register new!
```

### Tip 2: Zipalign untuk Performance

```
1. After signing, run zipalign:
   MTManager → Tools → Zipalign
2. Select signed APK
3. Alignment: 4
4. This improves app performance
```

### Tip 3: Verify APK Integrity

```bash
# Check if APK properly signed
jarsigner -verify -verbose -certs merged_signed.apk

# Check if network config injected
aapt dump xmltree merged_signed.apk AndroidManifest.xml | grep networkSecurityConfig
```

### Tip 4: Debugging Login Issues

**If login still fails:**

```
1. Check Logcat:
   adb logcat | grep -i "oauth\|google\|signature"

2. Common errors:
   - "API_DISABLED" → Google OAuth not enabled in project
   - "DEVELOPER_ERROR" → SHA-1 not registered
   - "SIGN_IN_FAILED" → Package name mismatch
   - "INTERNAL_ERROR" → Metadata missing

3. Verify metadata preserved:
   aapt dump badging merged_signed.apk | grep -i google
```

---

## 📊 Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Login blank screen | SHA-1 not registered | Register SHA-1 di Google Console |
| "DEVELOPER_ERROR" | Package name / SHA-1 mismatch | Check package name + SHA-1 |
| "API_DISABLED" | OAuth not enabled in project | Ask developer to enable OAuth |
| Metadata missing | Aggressive manifest cleaning | Preserve Google Services metadata |
| Signature verification failed | Keystore mismatch | Use consistent keystore |
| App crashes on launch | Missing native libs | Ensure all split libs merged |

---

## 🔍 Verification Checklist

**Before Install:**
- [ ] Certificate injected (res/raw/Techno_India.pem)
- [ ] network_security_config.xml created
- [ ] AndroidManifest updated (networkSecurityConfig)
- [ ] Google Services metadata preserved
- [ ] APK signed with consistent keystore
- [ ] SHA-1 registered di Google Console (wait 5-10 min)

**After Install:**
- [ ] App launches without crash
- [ ] Click "Login via Google" → Account selector appears
- [ ] Select account → Login SUCCESS (not blank screen)
- [ ] App loads user data
- [ ] HttpCanary captures API calls (non-OAuth traffic)

---

## 📝 Summary

**MTManager Workflow Benefits:**
- ✅ Better control over signing process
- ✅ Can preserve Google Services metadata manually
- ✅ All-in-one tool (no need Termux for basic tasks)
- ✅ Easier debugging with APK Editor UI

**Key Points:**
1. **Merge properly** → Use MTManager APK Merger
2. **Preserve metadata** → Don't remove Google Services tags
3. **Sign consistently** → Use same keystore
4. **Register SHA-1** → Add to Google Console
5. **Test thoroughly** → Verify login before distributing

---

## 🎯 Quick Reference Commands

**MTManager Shortcuts:**
```
Long press APK → APK Editor → Decompile
Long press folder → APK Editor → Build
Long press APK → Sign APK
Long press APK → View → APK Info (get SHA-1)
```

**Verify APK:**
```bash
# Get SHA-1
keytool -list -printcert -jarfile app.apk | grep SHA1

# Check package name
aapt dump badging app.apk | grep package

# List files
unzip -l app.apk | grep -i "network\|google"
```

---

## 🙏 Credits

- **MTManager:** Powerful APK editor for Android
- **ApkPatcher:** SSL bypass tool with Google OAuth fix
- **Guide Author:** baretoaldo

---

**Need Help?**
- Check logcat for errors
- Verify SHA-1 registration
- Ensure metadata preserved
- Test with non-split APK first (baseline)

**Good luck!** 🚀
