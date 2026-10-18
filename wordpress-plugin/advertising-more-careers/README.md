# Advertising & More — Careers Page (Optional WordPress Adapter)

A custom, agency-specific careers landing page with a refined header and footer and secure application delivery using WordPress AJAX. This is an **optional integration** for WordPress installations; the agency's production platform has **not been verified** from public access. Confirm the existing site's CMS/framework and apply this design within that stack if it is not WordPress.

## Install (only if the site runs on WordPress)

1. Back up the live site, then upload `advertising-more-careers.zip` from the WordPress **Plugins → Add New → Upload Plugin** screen and activate it.
2. Navigate to **Settings → Careers Applications** and enter a real recruitment inbox. Configure/test the site's transactional SMTP mail service before accepting live applicants.
3. Create a new WordPress **Page** titled `Careers` or `Job Vacancy`. Under the page template options, select **Advertising & More — Careers (full width)**. Publish. The custom canvas replaces the theme's default page header/footer **on this page only**, avoiding duplicates; other pages remain unaffected.
4. Open the published page, review desktop/tablet/mobile, and send a test application using fictional information and an innocuous sample PDF. Confirm the email arrives with CV attached before announcing the page.
5. Add the new Careers link to the agency's global primary navigation using the existing site's header editor/theme (this plugin does not modify other pages' header or footer). Review regional privacy/retention wording and accessibility with the site owner.

## Form

Fields: full name as per IC/legal identity, email, Malaysian/foreign applicant type, passport number (required for foreign nationals only), date of birth, mobile, current employer, earliest start date, LinkedIn URL, optional area of interest, CV file upload, data processing consent.

Client/server checks: mandatory fields; valid dates (DOB no later than today, start date no earlier than today); verified HTTPS LinkedIn profile; file-size limit 5 MiB; accepted PDF/DOC/DOCX *file signatures*; consent; nonce; honeypot; rate limiting per IP. ZIP-based DOCX signature checks require the PHP ZipArchive extension. Uploaded files are **not left in public WordPress uploads**; email attachments are copied into server temporary storage and deleted after `wp_mail` returns. No permanent database of applicants is made by the plugin.

**Important**: Server-side acceptance and attachment handling have been code-reviewed and PHP-linted, but live `wp_mail` transmission, SMTP deliverability, CAPTCHA/WAF and real WordPress environment compatibility cannot be tested without access to the agency site. WordPress AJAX nonces do not replace anti-spam/WAF protection. For highly sensitive identity data, a restricted-access recruitment portal with explicit retention/deletion policies may be preferable to email attachments. Obtain the owner's approval for exact passport/DOB handling, privacy wording and storage/retention.

## Styling

The design uses a unique, generated 3D coffee + careers illustration, warm brand palette, bold oversized typography, animated ticker, responsive form, accessible reduced-motion treatment and a reimagined navigation/footer. Artwork and brandwordmark are concept assets; use the company's original approved brand files for final production.

## Files

- `advertising-more-careers.php`: plugin controller, admin settings, secure AJAX handler.
- `templates/canvas.php`: full-width page with WordPress asset hooks.
- `templates/content.html`: on-page markup.
- `assets/styles.css`: layout/typography/responsive CSS.
- `assets/script.js`: interactions, conditional passport field, validation, upload UI, AJAX.
- `assets/careers-3d.png`: commissioned concept illustration.
