#!/usr/bin/env python3
"""
Fix Merged Split APK for Google OAuth
Author: baretoaldo
Purpose: Restore Google Services metadata after APKEditor merge
"""

import os
import sys
import re
import xml.etree.ElementTree as ET

def fix_manifest_for_google_oauth(decompiled_dir):
    """
    Restore Google Services metadata that was removed by APKEditor merge
    """
    manifest_path = os.path.join(decompiled_dir, 'AndroidManifest.xml')
    
    if not os.path.exists(manifest_path):
        print(f"❌ AndroidManifest.xml not found: {manifest_path}")
        return False
    
    print(f"\n🔍 Analyzing: {manifest_path}")
    
    # Read manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Google Services metadata exists
    has_gms_version = 'com.google.android.gms.version' in content
    has_app_id = 'com.google.android.gms.games.APP_ID' in content
    
    print(f"   Google Play Services version metadata: {'✅ Found' if has_gms_version else '❌ Missing'}")
    print(f"   Google Play Games APP_ID metadata: {'✅ Found' if has_app_id else '❌ Missing'}")
    
    # Find application tag
    application_match = re.search(r'(<application[^>]*>)', content)
    if not application_match:
        print("❌ <application> tag not found")
        return False
    
    application_tag = application_match.group(1)
    
    # Prepare metadata to inject
    metadata_to_inject = []
    
    # Always add Google Play Services version (required for OAuth)
    if not has_gms_version:
        metadata_to_inject.append(
            '    <meta-data android:name="com.google.android.gms.version" '
            'android:value="@integer/google_play_services_version"/>'
        )
        print("   ➕ Will add: com.google.android.gms.version")
    
    # Check if app uses Google Play Games
    if 'com.google.android.gms.games' in content and not has_app_id:
        metadata_to_inject.append(
            '    <meta-data android:name="com.google.android.gms.games.APP_ID" '
            'android:value="@string/app_id"/>'
        )
        print("   ➕ Will add: com.google.android.gms.games.APP_ID")
    
    # Inject metadata after <application> tag
    if metadata_to_inject:
        injection_point = content.find('>', content.find('<application'))
        if injection_point != -1:
            injection = '\n' + '\n'.join(metadata_to_inject) + '\n'
            content = content[:injection_point+1] + injection + content[injection_point+1:]
            
            # Write back
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n✅ Manifest updated with {len(metadata_to_inject)} metadata entries")
            return True
    else:
        print("\n✅ All required metadata already present")
        return True
    
    return False


def check_resources(decompiled_dir):
    """
    Check if required resources exist
    """
    print("\n🔍 Checking required resources...")
    
    # Check res/values/integers.xml for google_play_services_version
    integers_files = [
        'res/values/integers.xml',
        'res/values/values.xml',
    ]
    
    has_gps_version = False
    for integers_file in integers_files:
        path = os.path.join(decompiled_dir, integers_file)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'google_play_services_version' in content:
                    has_gps_version = True
                    print(f"   ✅ Found google_play_services_version in {integers_file}")
                    break
    
    if not has_gps_version:
        print("   ⚠️  google_play_services_version not found")
        print("      This might cause issues. Checking if Google Play Services is used...")
        
        # Check if app uses Google Play Services
        manifest_path = os.path.join(decompiled_dir, 'AndroidManifest.xml')
        with open(manifest_path, 'r', encoding='utf-8') as f:
            if 'com.google.android.gms' in f.read():
                print("   ❌ App uses Google Play Services but version resource missing!")
                print("      Creating fallback resource...")
                create_gps_version_resource(decompiled_dir)
    
    return True


def create_gps_version_resource(decompiled_dir):
    """
    Create google_play_services_version resource if missing
    """
    integers_path = os.path.join(decompiled_dir, 'res/values/integers.xml')
    
    # Default Google Play Services version (use latest stable)
    gps_version = 12451000  # Google Play Services 12.4.51
    
    if os.path.exists(integers_path):
        # Append to existing file
        with open(integers_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has google_play_services_version
        if 'google_play_services_version' in content:
            return
        
        # Insert before </resources>
        injection = f'    <integer name="google_play_services_version">{gps_version}</integer>\n'
        content = content.replace('</resources>', injection + '</resources>')
        
        with open(integers_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Added google_play_services_version = {gps_version} to integers.xml")
    else:
        # Create new integers.xml
        os.makedirs(os.path.join(decompiled_dir, 'res/values'), exist_ok=True)
        
        content = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <integer name="google_play_services_version">{gps_version}</integer>
</resources>
'''
        with open(integers_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Created integers.xml with google_play_services_version = {gps_version}")


def print_sha1_info():
    """
    Print info about SHA-1 registration
    """
    print("\n" + "="*60)
    print("📋 IMPORTANT: SHA-1 Certificate Registration")
    print("="*60)
    print("""
When APK is re-signed, the SHA-1 certificate fingerprint changes.
You MUST register the new SHA-1 in Google Cloud Console:

1. Get SHA-1 from signed APK:
   keytool -list -printcert -jarfile your_app_Patched.apk | grep SHA1

2. Or from keystore:
   keytool -list -v -keystore your.keystore -alias your_alias

3. Register in Google Cloud Console:
   https://console.cloud.google.com/apis/credentials
   → OAuth 2.0 Client IDs → Android → Add SHA-1

4. Wait 5-10 minutes for propagation

5. Test Google OAuth login

⚠️  Without proper SHA-1 registration, Google OAuth will FAIL!
""")


def main():
    if len(sys.argv) < 2:
        print("""
Usage: python3 fix_merged_apk_google_oauth.py <decompiled_apk_dir>

Example:
    python3 fix_merged_apk_google_oauth.py robox_decompiled/

This script will:
1. Restore Google Services metadata removed by APKEditor merge
2. Check and fix required resources
3. Ensure Google OAuth compatibility

After running this script:
1. Recompile APK with apktool
2. Sign with your certificate
3. Register SHA-1 in Google Console
4. Install and test
""")
        sys.exit(1)
    
    decompiled_dir = sys.argv[1]
    
    if not os.path.exists(decompiled_dir):
        print(f"❌ Directory not found: {decompiled_dir}")
        sys.exit(1)
    
    print("="*60)
    print("🔧 Fix Merged Split APK for Google OAuth")
    print("="*60)
    print(f"Target: {decompiled_dir}")
    
    # Step 1: Fix manifest
    success = fix_manifest_for_google_oauth(decompiled_dir)
    
    # Step 2: Check resources
    check_resources(decompiled_dir)
    
    # Step 3: Print SHA-1 info
    print_sha1_info()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("\nNext steps:")
        print("1. Recompile: apktool b " + decompiled_dir)
        print("2. Sign APK with your certificate")
        print("3. Register SHA-1 in Google Console")
        print("4. Install and test Google OAuth login")
    else:
        print("\n❌ Fix failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
