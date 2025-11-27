# 🔍 Analisis: Split APK + Google OAuth Problem

## 🎯 Problem Statement

**Scenario:**
```
1. Download split APK (.apks / .apkm / .xapk)
2. Merge dengan Anti-Split tool → base.apk
3. Patch dengan ApkPatcher → base_patched.apk
4. Install & test → ❌ Google OAuth login GAGAL
```

**Observation:**
- APK non-split → Google OAuth works ✅
- APK yang di-merge dari split → Google OAuth fails ❌

---

## 🐛 Root Cause Analysis

### 1. Google OAuth Requirements

Google OAuth memerlukan:
1. **Correct Package Name**
2. **Valid SHA-1 Certificate Fingerprint** (registered di Google Console)
3. **Proper signature verification**
4. **Complete AndroidManifest metadata**

### 2. Apa yang Rusak Saat Merge Split APK?

**A. Signature Mismatch**
```
Original Split APK:
- base.apk (signature A)
- config.arm64_v8a.apk (signature A)
- config.xxhdpi.apk (signature A)
→ All signed with SAME certificate

Merged APK (Anti-Split):
- merged.apk (RE-SIGNED with different certificate!)
→ SHA-1 fingerprint BERUBAH!
```

**Result:** Google OAuth server reject karena SHA-1 tidak match dengan yang registered!

**B. Missing Metadata**
```xml
<!-- Split APK biasanya punya metadata ini di AndroidManifest -->
<meta-data 
    android:name="com.google.android.gms.version"
    android:value="@integer/google_play_services_version" />

<meta-data
    android:name="com.google.android.gms.games.APP_ID"
    android:value="@string/app_id" />
```

Saat merge, beberapa metadata ini **hilang** atau **corrupted**.

**C. Split Configuration Info**
```xml
<!-- Original split APK metadata -->
<meta-data
    android:name="com.android.vending.splits"
    android:value="..." />
```

ApkPatcher **menghapus** tag ini (untuk anti-detection), tapi Google Play Services **memerlukan** info ini untuk proper initialization!

---

## 💡 Solutions

### Solution 1: Preserve Google OAuth Metadata (RECOMMENDED)

Modifikasi `Manifest_Patch.py` untuk **TIDAK menghapus** Google OAuth specific metadata:

```python
# DON'T remove these for Google OAuth compatibility
patterns = [
    (
        r'\s+android:(splitTypes|requiredSplitTypes)="[^"]*?"',
        r'',
        'Splits'  # Keep removing this (OK)
    ),
    (
        r'(isSplitRequired=)"true"',
        r'\1"false"',
        'isSplitRequired'  # Keep this fix (OK)
    ),
    (
        # ❌ OLD (too aggressive):
        r'\s+<meta-data[^>]*"com.android.(vending.|stamp.|dynamic.apk.)[^"]*"[^>]*/>',
        
        # ✅ NEW (selective):
        r'\s+<meta-data[^>]*"com.android.(vending.derived.apk|stamp.source|dynamic.apk.)[^"]*"[^>]*/>',
        '<meta-data>'
    ),
]
```

**Preserve these tags:**
- `com.google.android.gms.*` (Google Play Services)
- `com.google.android.games.*` (Google Play Games)
- Package signature verification metadata

---

### Solution 2: Use Original SHA-1 Certificate

**Problem:** Merged APK di-sign ulang → SHA-1 berubah → Google reject

**Fix:**

1. **Extract original certificate** dari split APK:
```bash
# Extract cert from original split APK
unzip base.apk -d temp/
cp temp/META-INF/CERT.RSA original_cert.rsa
keytool -printcert -file original_cert.rsa
# Note SHA-1: XX:XX:XX:...
```

2. **Sign merged APK dengan certificate yang SAMA**:
```bash
# If you have original keystore
jarsigner -keystore original.keystore merged.apk alias_name

# Or use uber-apk-signer with original key
java -jar uber-apk-signer.jar \
  --ks original.keystore \
  --ksPass password \
  --ksAlias alias_name \
  -a merged.apk
```

3. **Register SHA-1 di Google Console**:
   - Go to: https://console.cloud.google.com/apis/credentials
   - Add **NEW** SHA-1 fingerprint dari merged APK
   - Wait 5-10 minutes untuk propagation

**⚠️ Problem:** Anda biasanya TIDAK punya original keystore!

---

### Solution 3: MTManager Workflow (PRACTICAL)

Karena Anda punya MTManager, gunakan workflow ini:

**Step 1: Merge dengan MTManager (Better Control)**
```
1. Open MTManager
2. Select .apks / .apkm file
3. Choose "Merge & Install" atau "Extract & Merge"
4. MTManager akan merge TANPA re-sign (lebih baik!)
```

**Step 2: Patch dengan ApkPatcher MODIFIED**

Kita perlu modifikasi `Manifest_Patch.py` untuk preserve Google metadata:

```python
# File: ApkPatcher/Patch/Manifest_Patch.py

def Fix_Manifest(manifest_path, smali_folders, isPKG, preserveGoogleOAuth=True):
    
    # ... existing code ...
    
    # MODIFIED: Preserve Google OAuth metadata
    patterns = [
        (
            r'\s+android:(splitTypes|requiredSplitTypes)="[^"]*?"',
            r'',
            'Splits'
        ),
        (
            r'(isSplitRequired=)"true"',
            r'\1"false"',
            'isSplitRequired'
        ),
    ]
    
    # Only remove non-Google metadata
    if not preserveGoogleOAuth:
        patterns.append(
            (
                r'\s+<meta-data[^>]*"com.android.(vending.|stamp.|dynamic.apk.)[^"]*"[^>]*/>',
                r'',
                '<meta-data>'
            )
        )
    else:
        # Selective removal (keep Google-related)
        patterns.append(
            (
                # Only remove split-specific metadata, NOT Google services
                r'\s+<meta-data[^>]*"com.android.(vending.derived.apk.splits|stamp.source|dynamic.apk.)[^"]*"[^>]*/>',
                r'',
                '<meta-data> (Google OAuth Safe)'
            )
        )
    
    # ... rest of code ...
```

**Step 3: Re-sign dengan Proper Certificate**

MTManager biasanya punya built-in signing tool yang lebih baik preserve metadata.

---

### Solution 4: Alternative Merge Tool

**Gunakan SAI (Split APKs Installer):**

```bash
# Install SAI from GitHub
# https://github.com/Aefyr/SAI

# SAI merge lebih "clean" untuk OAuth apps
1. Open SAI
2. Import .apks / .xapk
3. Export as single APK
4. Patch dengan ApkPatcher
```

**Atau APKTool Manual Merge:**

```bash
# Merge manual (preserve metadata)
apktool d base.apk -o merged
apktool d config.arm64_v8a.apk -o config_arm

# Copy libraries
cp -r config_arm/lib/* merged/lib/

# Copy resources
cp -r config_arm/res/* merged/res/

# Rebuild
apktool b merged -o merged.apk

# Patch
ApkPatcher -i merged.apk
```

---

## 🛠️ Recommended Fix Implementation

Mari saya modifikasi kode ApkPatcher untuk handle merged split APK dengan benar:

### File to Modify: `Manifest_Patch.py`

**Add flag untuk preserve Google metadata:**

```python
def Fix_Manifest(manifest_path, smali_folders, isPKG, preserveGoogleServices=True):
    
    isPC = bool(M.re.search('piracychecker', open(manifest_path).read(), M.re.I))
    
    # Base patterns (always apply)
    patterns = [
        (
            r'\s+android:(splitTypes|requiredSplitTypes)="[^"]*?"',
            r'',
            'Splits'
        ),
        (
            r'(isSplitRequired=)"true"',
            r'\1"false"',
            'isSplitRequired'
        ),
    ]
    
    # Selective metadata removal
    if preserveGoogleServices:
        # Only remove app bundle specific metadata
        # KEEP: com.google.android.gms.* (Google Play Services)
        # KEEP: com.google.android.games.* (Google Games)
        patterns.append(
            (
                r'\s+<meta-data[^>]*"com.android.(vending.derived.apk.splits|stamp.source|stamp.type|dynamic.apk.distribution.status)[^"]*"[^>]*/>',
                r'',
                '<meta-data> (Selective - Google Services Protected)'
            )
        )
    else:
        # Aggressive removal (original behavior)
        patterns.append(
            (
                r'\s+<meta-data[^>]*"com.android.(vending.|stamp.|dynamic.apk.)[^"]*"[^>]*/>',
                r'',
                '<meta-data> (Aggressive)'
            )
        )
    
    # License check removal
    patterns.append(
        (
            r'\s+<[^>]*"(com.pairip.licensecheck)[^"]*"[^>]*/>' if isPC else r'\s+<[^>]*"com.(pairip.licensecheck|android.vending.CHECK_LICENSE)[^"]*"[^>]*/>',
            r'',
            'CHECK_LICENSE'
        )
    )
    
    # ... rest of code stays the same ...
```

**Add CLI flag:**

```python
# In CLI.py
parser.add_argument(
    '--preserve-google',
    action='store_true',
    help='Preserve Google Services metadata (needed for OAuth in merged split APKs)'
)
```

**Usage:**
```bash
# For merged split APK with Google OAuth
ApkPatcher -i merged.apk --preserve-google
```

---

## 🧪 Testing Checklist

### Test Case 1: Non-Split APK (Baseline)
```bash
ApkPatcher -i regular_app.apk
# Expected: ✅ Google OAuth works
```

### Test Case 2: Merged Split APK (Original Issue)
```bash
# Merge split APK first
java -jar APKEditor.jar m -i app.apks

# Patch without --preserve-google
ApkPatcher -i app.apk

# Expected: ❌ Google OAuth fails (original problem)
```

### Test Case 3: Merged Split APK (With Fix)
```bash
# Patch WITH --preserve-google
ApkPatcher -i app.apk --preserve-google

# Expected: ✅ Google OAuth works!
```

---

## 📊 Comparison

| Method | Google OAuth | API Capture | Complexity |
|--------|--------------|-------------|------------|
| Original ApkPatcher | ✅ | ✅ | Low |
| Merged Split (current) | ❌ | ✅ | Low |
| Merged Split (--preserve-google) | ✅ | ✅ | Low |
| MTManager custom sign | ✅ | ✅ | Medium |
| Register new SHA-1 | ✅ | ✅ | High |

---

## 🎯 Action Items

1. **Modify `Manifest_Patch.py`** → Add selective metadata removal
2. **Add CLI flag** `--preserve-google` 
3. **Update documentation** → Explain split APK handling
4. **Test dengan real merged split APK**
5. **Push update ke GitHub**

Apakah Anda ingin saya implementasikan fix ini sekarang?
