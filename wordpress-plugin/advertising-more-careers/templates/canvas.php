<?php
if (!defined('ABSPATH')) { exit; }
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class('am-careers-full-canvas'); ?>>
<?php wp_body_open(); ?>
<?php echo AM_Careers_Plugin::render(); // Trusted local plugin template. ?>
<?php wp_footer(); ?>
</body>
</html>
