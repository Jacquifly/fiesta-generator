<?php

/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'carevets_carevets');

/** MySQL database username */
define('DB_USER', 'carevets_careadm');

/** MySQL database password */
define('DB_PASSWORD', 'Green23grass!');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'OlN>ljL$n-44.4JUvuBH|&@;EiI(.je$RWP9lmU2V3k4v<Du;!9$*{WFQRxg?0B:');
define('SECURE_AUTH_KEY',  'n*(|me~?e2G&^3bwyTtf<nn<+a huaAnwOvi9i3=J`{(8|/3b>e@PMgURB.u+U(-');
define('LOGGED_IN_KEY',    ';%^nZ~0Qz0:n]AuQWWGS_^vBAcT+<J@lfd|z-+S 3fN^y%Ju#-^fkd:ap!<2<#nf');
define('NONCE_KEY',        'BM>.w*TW,hTpYvbKhi`~]moy{(Rf5C:rqTWh2suD,)D!|p*kMy0;3+jzg:pv7J f');
define('AUTH_SALT',        '-aL6<+XF!?vAq+|mV1G1s~G!lT,J_rX2jxKZq%N6@<--p@.1J@<)2B@U_ 4Gvwr2');
define('SECURE_AUTH_SALT', '.w0S@}rTdi-%=Bz|G[-<Z|{AJ7r-cHW+-lT0#mNUv91(;-Gb{`5 X+/Woc U%_RG');
define('LOGGED_IN_SALT',   'cm{c>@~Y=z}+q/6*4MKp&%&~|@B}T 4M/he Nvpe-Eh^e8ai>5e62;4LQ[Dg2s);');
define('NONCE_SALT',       'q|jS0B}=W(i>0i![|C@s*Ib0%[Vev[K|v0L=r9#D:.^*!`SycWAKv>U69L^AuvNH');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wpcv_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress. A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de_DE.mo to wp-content/languages and set WPLANG to 'de_DE' to enable German
 * language support.
 */
define('WPLANG', '');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* Multisite */
define('MULTISITE', false);


/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');
/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

import random
import string
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Code Generator", layout="centered")

st.title("🔐 16-Digit Code Generator")

# ✏️ Input for the prefix
prefix = st.text_input("Enter a 6-letter prefix for your codes", max_chars=6).upper()

# 🧮 Input for number of codes
num_codes = st.number_input("How many codes would you like to generate?", min_value=1, max_value=1000, value=300)

# Only show the button if a valid prefix is entered
if len(prefix) != 6 or not prefix.isalpha():
    st.warning("Please enter exactly **6 letters** as your prefix.")
    st.stop()

# ✅ Generate codes button
if st.button("🚀 Generate Codes"):

    def generate_codes(prefix, num, length=10):
        codes = set()
        while len(codes) < num:
            numeric_part = ''.join(random.choices(string.digits, k=length))
            codes.add(f"{prefix}{numeric_part}")
        return list(codes)

    codes = generate_codes(prefix, num_codes)

    df = pd.DataFrame(codes, columns=["Code"])
    st.success(f"🎉 Generated {len(codes)} codes with prefix: {prefix}")

    # Show preview
    st.dataframe(df)

    # 📥 Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{prefix}_generated_codes.csv",
        mime='text/csv'
    )
