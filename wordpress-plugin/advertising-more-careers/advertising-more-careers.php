<?php
/**
 * Plugin Name: Advertising & More — Careers Page
 * Description: Bespoke agency careers page with an accessible application form and secure email delivery.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * Author: Custom concept for Advertising & More
 * Text Domain: am-careers
 */
if (!defined('ABSPATH')) { exit; }

final class AM_Careers_Plugin {
    const OPTION = 'am_careers_recipient_email';
    const TEMPLATE = 'am-careers-canvas.php';
    const MAX_BYTES = 5242880;

    public static function init() {
        add_shortcode('am_careers', [__CLASS__, 'render']);
        add_filter('theme_page_templates', [__CLASS__, 'page_templates']);
        add_filter('template_include', [__CLASS__, 'template_include'], 99);
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue']);
        add_action('admin_menu', [__CLASS__, 'menu']);
        add_action('admin_init', [__CLASS__, 'settings']);
        add_action('wp_ajax_nopriv_am_careers_submit', [__CLASS__, 'submit']);
        add_action('wp_ajax_am_careers_submit', [__CLASS__, 'submit']);
    }

    public static function page_templates($templates) {
        $templates[self::TEMPLATE] = 'Advertising & More — Careers (full width)';
        return $templates;
    }
    private static function is_careers_page() {
        return is_singular('page') && get_page_template_slug(get_queried_object_id()) === self::TEMPLATE;
    }
    public static function template_include($template) {
        if (self::is_careers_page()) {
            return plugin_dir_path(__FILE__) . 'templates/canvas.php';
        }
        return $template;
    }
    public static function enqueue() {
        if (!self::is_careers_page()) { return; }
        $url = plugin_dir_url(__FILE__);
        wp_enqueue_style('am-careers-style', $url . 'assets/styles.css', [], '1.0.0');
        wp_enqueue_script('am-careers-script', $url . 'assets/script.js', [], '1.0.0', true);
        wp_add_inline_script('am-careers-script', 'window.amCareersConfig=' . wp_json_encode([
            'endpoint' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('am_careers_submit')
        ]) . ';', 'before');
    }
    public static function render() {
        $path = plugin_dir_path(__FILE__) . 'templates/content.html';
        if (!is_readable($path)) { return '<p>Careers page asset missing.</p>'; }
        $markup = file_get_contents($path);
        $markup = str_replace('assets/careers-3d.png', esc_url(plugin_dir_url(__FILE__) . 'assets/careers-3d.png'), $markup);
        return $markup;
    }

    public static function menu() {
        add_options_page('Careers Applications', 'Careers Applications', 'manage_options', 'am-careers-settings', [__CLASS__, 'settings_page']);
    }
    public static function settings() {
        register_setting('am_careers_settings', self::OPTION, [
            'type' => 'string', 'sanitize_callback' => 'sanitize_email', 'default' => ''
        ]);
    }
    public static function settings_page() {
        if (!current_user_can('manage_options')) { return; }
        echo '<div class="wrap"><h1>Careers Application Settings</h1>';
        echo '<p>Configure the recruitment inbox before enabling applications. This plugin emails the form details and CV; it does not save submitted CVs to public media uploads or a WordPress database.</p>';
        echo '<form action="options.php" method="post">';
        settings_fields('am_careers_settings');
        echo '<table class="form-table"><tr><th><label for="am_recipient">Recruitment email address</label></th><td><input class="regular-text" type="email" id="am_recipient" name="' . esc_attr(self::OPTION) . '" value="' . esc_attr(get_option(self::OPTION, '')) . '" required /><p class="description">Only applicants should use the public form. Ensure SMTP is configured and send a test application using dummy details.</p></td></tr></table>';
        submit_button('Save recruitment email');
        echo '</form></div>';
    }
    private static function fail($message, $code = 400) {
        wp_send_json_error(['message' => $message], $code);
    }
    private static function value($key) {
        $v = isset($_POST[$key]) && is_scalar($_POST[$key]) ? wp_unslash($_POST[$key]) : '';
        return sanitize_text_field((string) $v);
    }
    private static function valid_date($date) {
        $d = DateTimeImmutable::createFromFormat('!Y-m-d', $date);
        return $d && $d->format('Y-m-d') === $date;
    }
    private static function valid_linkedin($url) {
        if (!filter_var($url, FILTER_VALIDATE_URL) || strtolower((string) wp_parse_url($url, PHP_URL_SCHEME)) !== 'https') { return false; }
        $host = strtolower((string) wp_parse_url($url, PHP_URL_HOST));
        if (!in_array($host, ['www.linkedin.com', 'linkedin.com'], true) && !preg_match('/^[a-z]{2}\.linkedin\.com$/', $host)) { return false; }
        return (bool) preg_match('~^/(in|pub)/[^/]+~i', (string) wp_parse_url($url, PHP_URL_PATH));
    }
    private static function valid_cv($file) {
        if (!isset($file['error'], $file['size'], $file['name'], $file['tmp_name']) || $file['error'] !== UPLOAD_ERR_OK) { return false; }
        if ($file['size'] <= 0 || $file['size'] > self::MAX_BYTES || !is_uploaded_file($file['tmp_name'])) { return false; }
        $name = sanitize_file_name($file['name']);
        $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));
        if (!in_array($ext, ['pdf','doc','docx'], true)) { return false; }
        $handle = fopen($file['tmp_name'], 'rb');
        if (!$handle) { return false; }
        $header = fread($handle, 8);
        fclose($handle);
        if ($ext === 'pdf') { return strncmp($header, '%PDF-', 5) === 0; }
        if ($ext === 'doc') { return strncmp($header, "\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1", 8) === 0; }
        if (strncmp($header, 'PK', 2) !== 0 || !class_exists('ZipArchive')) { return false; }
        $zip = new ZipArchive();
        if ($zip->open($file['tmp_name']) !== true) { return false; }
        $is_docx = $zip->locateName('word/document.xml') !== false && $zip->locateName('[Content_Types].xml') !== false;
        $zip->close();
        return $is_docx;
    }
    public static function submit() {
        if (!check_ajax_referer('am_careers_submit', 'nonce', false)) { self::fail('Please reload the page and try again.', 403); }
        if (self::value('website') !== '') { wp_send_json_success(['message' => 'Thank you.']); }
        $remote = isset($_SERVER['REMOTE_ADDR']) ? (string) $_SERVER['REMOTE_ADDR'] : 'unknown';
        $rate_key = 'am_careers_rate_' . md5($remote);
        $count = (int) get_transient($rate_key);
        if ($count >= 6) { self::fail('Too many attempts. Please try again later.', 429); }
        set_transient($rate_key, $count + 1, HOUR_IN_SECONDS);

        $recipient = sanitize_email(get_option(self::OPTION, ''));
        if (!$recipient || !is_email($recipient)) { self::fail('The recruitment inbox is not configured. Please contact the agency.', 503); }
        $name = self::value('full_name');
        $email = sanitize_email(self::value('email'));
        $type = self::value('applicant_type');
        $passport = self::value('passport_number');
        $dob = self::value('dob');
        $phone = self::value('mobile');
        $employer = self::value('employer');
        $start = self::value('start_date');
        $linkedin = esc_url_raw(self::value('linkedin'));
        $interest = self::value('interest');
        $consent = self::value('consent');
        $today = wp_date('Y-m-d');

        if (strlen($name) < 2 || strlen($name) > 150 || !is_email($email)) { self::fail('Please enter a valid full name and email address.'); }
        if (!in_array($type, ['malaysian','foreigner'], true)) { self::fail('Please choose your applicant type.'); }
        if ($type === 'foreigner' && !preg_match('/^[\p{L}\p{N} -]{4,30}$/u', $passport)) { self::fail('Please enter a valid passport number.'); }
        if (!self::valid_date($dob) || $dob > $today || !self::valid_date($start) || $start < $today) { self::fail('Please check your date of birth and earliest starting date.'); }
        if (!preg_match('/^\+?[0-9() .-]{7,25}$/', $phone) || !$employer || strlen($employer) > 150) { self::fail('Please enter a valid phone number and current employer.'); }
        if (!self::valid_linkedin($linkedin) || $consent !== 'on') { self::fail('Please enter a valid LinkedIn URL and provide recruitment data consent.'); }
        if (!isset($_FILES['cv']) || !self::valid_cv($_FILES['cv'])) { self::fail('Please attach a genuine PDF, DOC, or DOCX file up to 5 MB.'); }

        $upload = $_FILES['cv'];
        $original = sanitize_file_name($upload['name']);
        $temp_file = trailingslashit(get_temp_dir()) . 'am-careers-' . wp_generate_uuid4() . '-' . $original;
        if (!copy($upload['tmp_name'], $temp_file)) { self::fail('We could not prepare your CV. Please try again.', 500); }
        @chmod($temp_file, 0600);
        $lines = [
            'Advertising & More — Careers Application',
            '',
            'Full name (as per IC): ' . $name,
            'Email: ' . $email,
            'Applicant type: ' . $type,
            'Passport number (foreign applicants): ' . ($type === 'foreigner' ? $passport : 'Not applicable'),
            'Date of birth: ' . $dob,
            'Mobile phone number: ' . $phone,
            'Name of current employer: ' . $employer,
            'Earliest starting date: ' . $start,
            'LinkedIn profile: ' . $linkedin,
            'Area of interest (optional): ' . ($interest ?: 'Not provided'),
            'Consent: Given on submission',
            '',
            'CV is attached. Handle applicant identity information confidentially and delete it when no longer necessary.'
        ];
        $sent = wp_mail($recipient, 'New careers application — ' . $name, implode("\n", $lines), [
            'Content-Type: text/plain; charset=UTF-8',
            'Reply-To: ' . $email
        ], [$temp_file]);
        @unlink($temp_file);
        if (!$sent) { self::fail('Your application was not delivered. Please try again or contact the agency.', 502); }
        wp_send_json_success(['message' => 'Application sent successfully.']);
    }
}
AM_Careers_Plugin::init();
