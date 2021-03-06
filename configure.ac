dnl Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
 
m4_define(gedit_plugins_major_version,  3)
m4_define(gedit_plugins_minor_version,  12)
m4_define(gedit_plugins_micro_version,  1)
m4_define(gedit_plugins_version, gedit_plugins_major_version.gedit_plugins_minor_version.gedit_plugins_micro_version)

AC_INIT([gedit-plugins],
        [gedit_plugins_version],
        [http://bugzilla.gnome.org/enter_bug.cgi?product=gedit],
        [gedit-plugins])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_SRCDIR([plugins])
AC_CONFIG_MACRO_DIR([m4])
AC_PREFIX_PROGRAM([gedit])

AM_INIT_AUTOMAKE([1.11 tar-ustar dist-xz no-dist-gzip subdir-objects -Wno-portability])
AM_MAINTAINER_MODE([enable])

AM_SILENT_RULES([yes])

# Check for programs
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_MAKE_SET

AM_PATH_PYTHON

# Initialize libtool
LT_PREREQ([2.2])
LT_INIT([disable-static])

dnl check for win32 platform
AC_MSG_CHECKING([for some Win32 platform])
case "$host" in
  *-*-mingw*|*-*-cygwin*)
    platform_win32=yes
    ;;
  *)
    platform_win32=no
    ;;
esac
AC_MSG_RESULT([$platform_win32])
AM_CONDITIONAL(PLATFORM_WIN32, test "$platform_win32" = "yes")

# ================================================================
# Gettext stuff.
# ================================================================
IT_PROG_INTLTOOL([0.40.0])

AM_GNU_GETTEXT_VERSION([0.17])
AM_GNU_GETTEXT([external])

GETTEXT_PACKAGE=gedit-plugins
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package])

# ================================================================
# Start of pkg-config checks
# ================================================================

PKG_CHECK_MODULES(GEDIT, [
	glib-2.0 >= 2.32.0
	gio-2.0 >= 2.32.0
	gtk+-3.0 >= 3.9.0
	gtksourceview-3.0 >= 3.9.2
	libpeas-1.0 >= 1.7.0
	libpeas-gtk-1.0 >= 1.7.0
	gedit >= 3.11.3
])

dnl ================================================================
dnl GSettings stuff
dnl ================================================================
GLIB_GSETTINGS

# ================================================================
# Plugins
# ================================================================

AC_ARG_ENABLE([verify-all],
              AC_HELP_STRING([--enable-verify-all], [verify that all plugins are enabled]),
              [enable_verify_all=$enableval],
              [enable_verify_all="no"])

# C plugins that don't need special dependencies
C_PLUGINS="bookmarks drawspaces wordcompletion"

# Python plugins that don't need special dependencies, besides python
PY_PLUGINS="bracketcompletion charmap codecomment colorpicker colorschemer commander dashboard joinlines multiedit smartspaces textsize"

PLUGINS="$C_PLUGINS"
disabled_plugins=""

# ================================================================
# Python
# ================================================================
AC_MSG_CHECKING([whether Python support is requested])
AC_ARG_ENABLE([python],
              AS_HELP_STRING([--enable-python], [Enable python support]),
              [enable_python=$enableval],
              [enable_python="yes"])

AM_CONDITIONAL([ENABLE_PYTHON], [test "x$enable_python" = "xyes"])

# ================================================================
# disable all python plugins if there is no python support
# ================================================================
if test "x$enable_python" = "xyes"
then
	PLUGINS="$PLUGINS $PY_PLUGINS"

	# ================================================================
	# Synctex (dbus-python)
	# ================================================================
	DBUSPYTHON_REQUIRED=0.82
	PKG_CHECK_MODULES([DBUSPYTHON],
		[dbus-python >= $DBUSPYTHON_REQUIRED],
		[have_synctex=yes],
		[have_synctex=no])

	AC_SUBST([DBUS_PYTHON_CFLAGS])
	AC_SUBST([DBUS_PYTHON_LIBS])

	if test "x$have_synctex" = "xyes"; then
		PLUGINS="$PLUGINS synctex"
	else
		disabled_plugins="$disabled_plugins synctex (dbus-python not found)"
	fi

	# ================================================================
	# Terminal (vte)
	# ================================================================
	if `$PYTHON -c "import gi; gi.require_version('Vte', '2.90')" 2>/dev/null`;
	then
		have_vte=yes
		PLUGINS="$PLUGINS terminal"
	else
		have_vte=no
		disabled_plugins="$disabled_plugins terminal (vte not found)"
	fi

	# ================================================================
	# Git (libgit2-glib)
	# ================================================================
	LIBGIT2_GLIB_REQUIRED=0.0.6
	PKG_CHECK_MODULES([GIT2_GLIB],
		[libgit2-glib-1.0 >= $LIBGIT2_GLIB_REQUIRED],
		[have_git2=yes],
		[have_git2=no])

	if test "x$have_git2" = "xyes"; then
		PLUGINS="$PLUGINS git"
	else
		disabled_plugins="$disabled_plugins git"
	fi
else
	disabled_plugins="$disabled_plugins $PY_PLUGINS synctex vte git (python not found)"
fi

AM_CONDITIONAL([ENABLE_SYNCTEX], test "x$have_synctex" = "xyes")
AM_CONDITIONAL([ENABLE_TERMINAL], test "x$have_vte" = "xyes")
AM_CONDITIONAL([ENABLE_GIT], test "x$have_git2" = "xyes")

AC_SUBST(PLUGINS)

# ================================================================
# Misc
# ================================================================
AC_PATH_PROG(GLIB_COMPILE_RESOURCES, glib-compile-resources)
AC_PATH_PROG(GLIB_GENMARSHAL, glib-genmarshal)

AC_DEFINE(GDK_VERSION_MIN_REQUIRED, GDK_VERSION_3_8, [minimum gdk version])

YELP_HELP_INIT

AC_ARG_ENABLE(deprecations,
              [AS_HELP_STRING([--enable-deprecations],
                              [warn about deprecated usages [default=no]])],,
              [enable_deprecations=no])

if test "x$enable_deprecations" = "xyes"
then
	DISABLE_DEPRECATED_CFLAGS="\
		-DG_DISABLE_DEPRECATED		\
		-DGDK_DISABLE_DEPRECATED	\
		-DGTK_DISABLE_DEPRECATED	\
		-DGDK_PIXBUF_DISABLE_DEPRECATED	\
		-DGNOME_DISABLE_DEPRECATED"
	AC_SUBST(DISABLE_DEPRECATED_CFLAGS)
fi

if test "$platform_win32" = yes; then
	PLUGIN_LIBTOOL_FLAGS="-module -avoid-version -no-undefined"
else
	PLUGIN_LIBTOOL_FLAGS="-module -avoid-version"
fi
AC_SUBST(PLUGIN_LIBTOOL_FLAGS)

GEDIT_PLUGINS_LIBS_DIR="$libdir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_LIBS_DIR)

GEDIT_PLUGINS_DATA_DIR="$datadir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_DATA_DIR)

if test "x$enable_verify_all" != "xno" && test ! -z "$disabled_plugins"; then
AC_MSG_ERROR([some plugins are not being built: $disabled_plugins])
fi

AC_CONFIG_FILES([
Makefile
help/Makefile
plugins/gpdefs.py
plugins/bookmarks/bookmarks.plugin.desktop.in
plugins/bracketcompletion/bracketcompletion.plugin.desktop.in
plugins/charmap/charmap.plugin.desktop.in
plugins/codecomment/codecomment.plugin.desktop.in
plugins/colorpicker/colorpicker.plugin.desktop.in
plugins/colorschemer/colorschemer.plugin.desktop.in
plugins/commander/commander.plugin.desktop.in
plugins/dashboard/dashboard.plugin.desktop.in
plugins/drawspaces/drawspaces.plugin.desktop.in
plugins/drawspaces/org.gnome.gedit.plugins.drawspaces.gschema.xml.in
plugins/git/git.plugin.desktop.in
plugins/joinlines/joinlines.plugin.desktop.in
plugins/multiedit/multiedit.plugin.desktop.in
plugins/smartspaces/smartspaces.plugin.desktop.in
plugins/synctex/synctex.plugin.desktop.in
plugins/terminal/org.gnome.gedit.plugins.terminal.gschema.xml.in
plugins/terminal/terminal.plugin.desktop.in
plugins/textsize/textsize.plugin.desktop.in
plugins/wordcompletion/org.gnome.gedit.plugins.wordcompletion.gschema.xml.in
plugins/wordcompletion/wordcompletion.plugin.desktop.in
po/Makefile.in])

AC_OUTPUT

echo "

Configuration:

	Source code location:   ${srcdir}
	Compiler:               ${CC}
	Prefix:			${prefix}
	Python Plugins Support: $enable_python
	Plugins:
	  $PLUGINS

	Disabled plugins:       $disabled_plugins

Note: you have to install these plugins into the same prefix as your gedit
installation (probably /usr if you're using your distro packages, /usr/local
if you have compiled it on your own).
"

