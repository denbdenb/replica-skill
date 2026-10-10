# Platform Deployment and Distribution Reference

Reference material for `replica-deploy`. Load this reference only when preparing
final production deployment or app store distribution for your specific platform.

## 1. Web Hosting and DNS Configuration

Connect Git repository to Vercel, Cloudflare Pages, Netlify, or Fly.io.

Configure DNS at domain registrar:
| Record | Name | Value / Target | Purpose |
|---|---|---|---|
| A | @ | Host apex IP address | Root domain routing |
| CNAME | www | Host alias (e.g. `cname.vercel-dns.com`) | Subdomain routing |
| TXT | @ | Host verification token | Domain ownership verification |

Email Authentication Records:
- **SPF (TXT)**: `v=spf1 include:_spf.provider.com ~all`
- **DKIM (CNAME or TXT)**: Provider-specified public key selector
- **DMARC (TXT)**: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`

## 2. Desktop Application Distribution

- **Windows**: Package with MSIX or create self-contained executable with `dotnet publish -c Release -r win-x64 --self-contained`. Sign with certificate.
- **macOS**: Bundle `.app`, sign with Apple Developer ID, notarize via `xcrun notarytool`, and package `.dmg`.
- **Linux**: Build AppImage or `.tar.gz` binary release assets.

## 3. Mobile Store Distribution

- **Android (Google Play)**: Build signed Android App Bundle (`./gradlew bundleRelease`). Upload to Google Play Console Internal Testing track.
- **iOS (Apple App Store)**: Archive in Xcode, upload to App Store Connect, distribute to TestFlight beta group.
