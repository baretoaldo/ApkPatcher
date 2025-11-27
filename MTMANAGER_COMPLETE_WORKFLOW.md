# 🎯 MTManager Complete Workflow - Google OAuth Fix

## Masalah yang Anda Alami

Dari log Anda, masalah terjadi di tahap **Anti-Split Merge**:

```
03.199 I: [MERGE] Removed-element : <meta-data> name="com.android.vending.splits.required"
03.211 I: [MERGE] Removed-element : <meta-data> name="com.android.vending.derived.apk.id"
```

**APKEditor menghapus metadata yang DIPERLUKAN oleh Google Play Services!**

Plus, APK di-sign ulang dengan debug keystore:
```
SHA256: 1e08a903aef9c3a721510b64ec764d01d3d094eb954161b62544ea8f187b5953
```

---

## ✅ Solusi Lengkap

### WORKFLOW 1: Automated Fix (RECOMMENDED)

**Step 1: Merge dengan ApkPatcher (Seperti Biasa)**
```bash
cd /sdcard/MT2/apks/
ApkPatcher -i robox.apks -skip getAcceptedIssuers
```

**Step 2: Fix Google OAuth Metadata (SETELAH Decompile, SEBELUM Recompile)**

Modifikasi workflow ApkPatcher untuk inject fix script.

**Step 3: Register SHA-1 Baru**
```bash
# Get SHA-1 dari APK yang sudah di-sign
keytool -list -printcert -jarfile robox_Patched.apk | grep SHA1

# Register di Google Console
# https://console.cloud.google.com/apis/credentials
```

---

### WORKFLOW 2: Manual Fix dengan Script

**Step 1: Patch APK Seperti Biasa**
```bash
ApkPatcher -i robox.apks -skip getAcceptedIssuers
```

Ini akan:
1. Merge split APK → `robox.apk`
2. Decompile → `robox_decompiled/`
3. Patch SSL bypass
4. **STOP HERE!** (Jangan recompile dulu)

**Step 2: Run Fix Script**
```bash
# Transfer script ke Termux
cd ~
python3 fix_merged_apk_google_oauth.py robox_decompiled/
```

Script akan:
- ✅ Restore `com.google.android.gms.version` metadata
- ✅ Restore `com.google.android.gms.games.APP_ID` (jika perlu)
- ✅ Create missing resources
- ✅ Verify AndroidManifest

**Step 3: Recompile & Sign**
```bash
# Recompile
apktool b robox_decompiled -o robox_fixed.apk

# Sign (gunakan keystore yang KONSISTEN!)
jarsigner -keystore your.keystore robox_fixed.apk your_alias

# Or dengan uber-apk-signer
java -jar Uber-Apk-Signer.jar -a robox_fixed.apk
```

**Step 4: Register SHA-1**
```bash
# Get SHA-1
keytool -list -printcert -jarfile robox_fixed.apk | grep SHA1

# Output example:
# SHA1: 1E:08:A9:03:AE:F9:C3:A7:21:51:0B:64:EC:76:4D:01:D3:D0:94:EB

# Register di Google Console (lihat panduan di bawah)
```

---

### WORKFLOW 3: MTManager Manual (Full Control)

**Step 1: Merge dengan MTManager**
```
1. Open MTManager
2. Long press robox.apks
3. "Extract" → Extract all files
4. "APK Editor" → "Merge Split APKs"
5. Output: robox_merged.apk
```

**Step 2: Decompile dengan MTManager**
```
1. Long press robox_merged.apk
2. "APK Editor" → "Decompile (Apktool)"
3. Output: robox_merged/ folder
```

**Step 3: Manual Fix AndroidManifest**

Buka `robox_merged/AndroidManifest.xml` dengan text editor:

**BEFORE (APKEditor removed these):**
```xml
<application ...>
    <!-- ❌ MISSING after merge! -->
</application>
```

**AFTER (Add these back):**
```xml
<application ...>
    <!-- ✅ ADD THESE for Google OAuth -->
    <meta-data 
        android:name="com.google.android.gms.version"
        android:value="@integer/google_play_services_version" />
    
    <!-- If app uses Google Play Games -->
    <meta-data 
        android:name="com.google.android.gms.games.APP_ID"
        android:value="@string/app_id" />
</application>
```

**Step 4: Check res/values/integers.xml**

Buka `robox_merged/res/values/integers.xml` (atau `values.xml`):

**Add if missing:**
```xml
<resources>
    <!-- Add this -->
    <integer name="google_play_services_version">12451000</integer>
</resources>
```

**Step 5: Inject Certificate & Network Config**

```
1. Copy certificate.pem → robox_merged/res/raw/Techno_India.pem
2. Create robox_merged/res/xml/network_security_config.xml
   (gunakan template dari guide sebelumnya dengan Google OAuth fix)
3. Edit AndroidManifest.xml:
   <application
       android:networkSecurityConfig="@xml/network_security_config"
       android:usesCleartextTraffic="true"
       ...>
```

**Step 6: Rebuild dengan MTManager**
```
1. Long press robox_merged/ folder
2. "APK Editor" → "Build (Apktool)"
3. Output: robox_merged_rebuilt.apk
```

**Step 7: Sign dengan MTManager**
```
1. Long press robox_merged_rebuilt.apk
2. "Sign APK"
3. Select your keystore (IMPORTANT: Use consistent keystore!)
4. Output: robox_merged_rebuilt_signed.apk
```

**Step 8: Register SHA-1**
```
1. MTManager → View APK → APK Info
2. Copy SHA-1 fingerprint
3. Register di Google Console
```

---

## 📋 SHA-1 Registration Guide

### Option A: You Are the App Developer

```
1. Go to: https://console.cloud.google.com/
2. Select your project
3. APIs & Services → Credentials
4. OAuth 2.0 Client IDs → Android
5. Click "Edit"
6. Add new SHA-1:
   Name: "Patched APK"
   SHA-1: [paste dari command keytool]
7. Save
8. Wait 5-10 minutes
9. Test login
```

### Option B: You Are NOT the Developer

**Problem:** Anda tidak bisa register SHA-1 di project developer lain!

**Solutions:**

**1. Create Your Own OAuth Client (For Testing)**
```
1. Create new Google Cloud project
2. Enable Google Sign-In API
3. Create OAuth 2.0 Client ID (Android)
4. Add your APK's SHA-1
5. Modify APK to use your OAuth Client ID (advanced!)
```

**2. Use Same Keystore as Original**
```
Problem: Anda biasanya TIDAK punya original keystore!
Solution: Hubungi developer untuk:
- Register SHA-1 Anda, OR
- Provide original keystore (unlikely)
```

**3. Use Non-Google OAuth Apps**
```
Test dengan apps yang TIDAK pakai Google OAuth dulu
Untuk verify SSL bypass works
```

**4. Root Device + System Certificate**
```
If device rooted:
1. Install your cert as system certificate
2. Some apps might accept this
3. But Google OAuth might still fail (depends on app implementation)
```

---

## 🧪 Testing Checklist

### Before Install:
- [ ] Merged APK created successfully
- [ ] Google Services metadata restored in AndroidManifest
- [ ] `google_play_services_version` resource exists
- [ ] Certificate injected (res/raw/)
- [ ] network_security_config.xml created
- [ ] APK signed with consistent keystore
- [ ] SHA-1 extracted and noted down
- [ ] SHA-1 registered in Google Console (wait 5-10 min)

### After Install:
- [ ] App launches without crash
- [ ] No "App not installed" error
- [ ] Click "Login via Google"
- [ ] Google account selector appears
- [ ] Select account
- [ ] ✅ Login SUCCESS (not blank screen!)
- [ ] App loads user data
- [ ] Test HttpCanary capture (non-OAuth endpoints)

---

## 🐛 Troubleshooting

### Problem 1: Still Login Failed

**Check 1: SHA-1 Registered?**
```bash
# Verify SHA-1
keytool -list -printcert -jarfile your_app.apk | grep SHA1

# Compare dengan yang di Google Console
# Must MATCH exactly!
```

**Check 2: Metadata Present?**
```bash
# Decompile and check
apktool d your_app.apk
grep -r "google_play_services_version" your_app/
grep -r "com.google.android.gms" your_app/AndroidManifest.xml
```

**Check 3: Logcat Errors**
```bash
adb logcat | grep -i "oauth\|google\|signature\|developer_error"

Common errors:
- DEVELOPER_ERROR → SHA-1 not registered
- API_DISABLED → OAuth not enabled in project  
- SIGN_IN_FAILED → Package name mismatch
```

### Problem 2: App Crashes

**Check:** Missing resources
```bash
adb logcat | grep -i "resourcenotfound\|integer\|google_play_services"
```

**Fix:** Verify integers.xml has `google_play_services_version`

### Problem 3: "App Not Installed"

**Causes:**
- Signature mismatch with previous installation
- Missing native libraries
- Corrupted APK

**Fix:**
```bash
# Uninstall completely
adb uninstall com.your.package

# Clear data
adb shell pm clear com.your.package

# Reinstall
adb install your_app.apk
```

---

## 📊 Success Indicators

**✅ Everything Working:**
```
1. App installs successfully
2. App launches without crash
3. Click "Login via Google"
4. Account selector appears (not blank!)
5. Select account
6. Brief loading screen
7. ✅ Logged in! (User data loads)
8. HttpCanary shows API captures (non-OAuth)
```

**❌ Still Failing:**
```
1. Click "Login via Google"
2. Account selector appears
3. Select account
4. Blank screen / Loading forever / "Failed to sign in"
5. Back to login screen
```

If this happens:
1. **Wait 10-15 minutes** (SHA-1 propagation)
2. **Clear app data** and test again
3. **Check logcat** for specific error
4. **Verify SHA-1** registration

---

## 🎯 Quick Command Reference

```bash
# Get SHA-1 from APK
keytool -list -printcert -jarfile app.apk | grep SHA1

# Get SHA-1 from keystore
keytool -list -v -keystore my.keystore -alias myalias

# Decompile APK
apktool d app.apk

# Build APK
apktool b app_decompiled -o app_rebuilt.apk

# Sign APK (uber-apk-signer)
java -jar Uber-Apk-Signer.jar -a app.apk

# Install APK
adb install app.apk

# Uninstall APK
adb uninstall com.package.name

# Watch logcat for errors
adb logcat | grep -i "oauth\|google"

# Fix merged APK
python3 fix_merged_apk_google_oauth.py app_decompiled/
```

---

## 💡 Pro Tips

1. **Use Consistent Keystore**
   - Create ONE keystore for all your patched APKs
   - Register its SHA-1 once in Google Console
   - Reuse for all future patches

2. **Backup Original Split APK**
   - Keep `.apks` file before merge
   - If something goes wrong, start fresh

3. **Test Non-OAuth First**
   - Verify SSL bypass works on non-Google login
   - Then tackle Google OAuth

4. **Document Your SHA-1**
   - Save SHA-1 somewhere safe
   - You'll need it for every APK you patch

5. **Wait for Propagation**
   - After registering SHA-1, wait 10-15 minutes
   - Don't assume instant activation

---

## 📝 Summary

**Root Cause:**
- APKEditor merge removes Google Services metadata
- APK re-signing changes SHA-1 certificate

**Solution:**
1. Restore metadata in AndroidManifest
2. Ensure resources exist (integers.xml)
3. Sign with consistent keystore
4. Register SHA-1 in Google Console
5. Wait for propagation
6. Test

**Key Files:**
- `AndroidManifest.xml` → Add `<meta-data>` for Google Services
- `res/values/integers.xml` → Add `google_play_services_version`
- `res/raw/Techno_India.pem` → Your certificate
- `res/xml/network_security_config.xml` → SSL bypass config

---

**Good luck! Semoga berhasil!** 🚀

If masih gagal, share:
1. Logcat output saat login
2. SHA-1 dari APK
3. Screenshot error (jika ada)
