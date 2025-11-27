# Changelog

All notable changes to this ApkPatcher fork will be documented here.

## [2.0.0] - 2025-11-27

### Added - Split APK Google OAuth Fix
- **`fix_merged_apk_google_oauth.py`**: Python script to restore Google Services metadata removed during split APK merge
- **`MTMANAGER_COMPLETE_WORKFLOW.md`**: Complete workflow guide for MTManager users
- **`MTMANAGER_GOOGLE_OAUTH_GUIDE.md`**: Step-by-step guide with 3 different methods
- **`SPLIT_APK_GOOGLE_OAUTH_ANALYSIS.md`**: Technical analysis of the split APK merge problem

### Changed - Google OAuth SSL Bypass
- Modified `Cert_Net_Config.py` to use selective SSL bypass
- Implemented 3-tier priority system:
  1. **Priority 1**: Google OAuth domains (NO BYPASS) - `accounts.google.com`, `oauth2.googleapis.com`
  2. **Priority 2**: Google APIs (USER CERT ALLOWED) - `googleapis.com`, `firebaseio.com`
  3. **Priority 3**: All other domains (FULL BYPASS) - App-specific endpoints

### Fixed
- ✅ Google OAuth login now works in patched APKs
- ✅ Split APK merge no longer breaks Google Services
- ✅ Preserved critical metadata: `com.google.android.gms.version`, `com.google.android.gms.games.APP_ID`
- ✅ API capture still works for non-OAuth endpoints

### Technical Details
**Problem:** 
- APKEditor merge removes Google Play Services metadata
- Re-signing changes SHA-1 certificate fingerprint
- Google OAuth rejects modified certificates

**Solution:**
- Selective SSL bypass excludes Google OAuth domains
- Restore metadata script for merged split APKs
- Comprehensive SHA-1 registration guide

## [1.0.0] - 2025-11-27

### Initial Fork
- Forked from [TechnoIndian/ApkPatcher](https://github.com/TechnoIndian/ApkPatcher)
- Initial Google OAuth fix implementation

---

## Upgrade Guide

### From Original ApkPatcher

If you're using the original ApkPatcher and experiencing Google OAuth login failures:

```bash
# Uninstall original
pip uninstall ApkPatcherX -y

# Install this fixed version
pip install git+https://github.com/baretoaldo/ApkPatcher.git
```

### For Split APK Users

If you're patching merged split APKs (.apks/.apkm/.xapk):

1. **Use the fix script** after decompile:
   ```bash
   python3 fix_merged_apk_google_oauth.py your_app_decompiled/
   ```

2. **Follow the workflow guide**: `MTMANAGER_COMPLETE_WORKFLOW.md`

3. **Register SHA-1** in Google Cloud Console

---

## Known Issues

### Split APK Limitations
- Original keystore not available → Must register new SHA-1
- Some apps detect merged split APKs → May require additional patches
- Native libraries must be properly merged

### Workarounds
- Use MTManager for better merge control
- Sign with consistent keystore
- Always register SHA-1 in Google Console
- Wait 10-15 minutes after SHA-1 registration

---

## Roadmap

### Planned Features
- [ ] Automated SHA-1 extraction and display
- [ ] One-click SHA-1 registration helper
- [ ] Better detection of Google Services dependencies
- [ ] Facebook/Twitter OAuth support
- [ ] Custom OAuth provider configuration

### Under Consideration
- [ ] GUI wrapper for fix script
- [ ] Integration with MTManager workflow
- [ ] Automatic metadata backup before merge
- [ ] Alternative signing methods

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly with real split APKs
4. Submit a pull request with clear description

---

## Credits

- **Original ApkPatcher**: [TechnoIndian](https://github.com/TechnoIndian/ApkPatcher)
- **Google OAuth Fix**: [baretoaldo](https://github.com/baretoaldo)
- **Split APK Analysis**: Community feedback and testing

---

## Support

- **GitHub Issues**: [Report bugs](https://github.com/baretoaldo/ApkPatcher/issues)
- **Original Project**: [TechnoIndian/ApkPatcher](https://github.com/TechnoIndian/ApkPatcher)
- **Community**: [Telegram](https://t.me/rktechnoindians)

---

**For detailed usage instructions, see:**
- `README.md` - General usage
- `GOOGLE_OAUTH_FIX_README.md` - Google OAuth fix details
- `MTMANAGER_COMPLETE_WORKFLOW.md` - MTManager workflow
- `SPLIT_APK_GOOGLE_OAUTH_ANALYSIS.md` - Technical analysis
