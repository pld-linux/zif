# NOTE: no longer developed; some code lives in hawkey backend in PackageKit
#
# Conditional build:
%bcond_with	rpm5	# RPM 5.x instead of rpm.org

Summary:	Simple wrapper for rpm and the Fedora package metadata
Summary(pl.UTF-8):	Proste opakowanie dla rpm-a i metadanych pakietów Fedory
Name:		zif
Version:	0.3.6
Release:	0.2
License:	GPL v2+
Group:		Libraries
Source0:	https://people.freedesktop.org/~hughsient/zif/releases/%{name}-%{version}.tar.xz
# Source0-md5:	fcec454a8d839cfe4aa9ee7b6e20ed15
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-xattr.patch
Patch3:		%{name}-rpm4.14.patch
URL:		https://people.freedesktop.org/~hughsient/zif/
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.9
BuildRequires:	bzip2-devel
BuildRequires:	docbook-utils
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	gpgme-devel
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libtool >= 2:2
BuildRequires:	rpm-devel >= 5
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.16.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zif is a simple yum-compatible library that provides read-write access
to the rpm database and the Fedora metadata for PackageKit.

%description -l pl.UTF-8
Zif to prosta biblioteka kompatybilna z yumem, dająca dostęp w trybie
odczytu i zapisu do bazy danych rpm-a oraz metadanych Fedory dla
PackageKita.

%package devel
Summary:	Header files for Zif library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Zif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bzip2-devel
Requires:	glib2-devel >= 1:2.16.1
Requires:	gpgme-devel
Requires:	zlib-devel

%description devel
Header files for Zif library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Zif.

%package static
Summary:	Static Zif library
Summary(pl.UTF-8):	Statyczna biblioteka Zif
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Zif library.

%description static -l pl.UTF-8
Statyczna biblioteka Zif.

%package apidocs
Summary:	Zif API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Zif
Group:		Documentation

%description apidocs
Zif API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Zif.

%package -n bash-completion-zif
Summary:	Bash completion for zif command
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla polecenia zif
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-zif
Bash completion for zif command.

%description -n bash-completion-zif -l pl.UTF-8
Bashowe dopełnianie parametrów dla polecenia zif.

%prep
%setup -q
%if %{with rpm5}
%patch -P0 -p1
%else
%patch -P3 -p1
%endif
%patch -P1 -p1
%patch -P2 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzif.la

# duplicate of bg (both are empty anyway)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/bg_BG

%find_lang Zif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f Zif.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/zif
%attr(755,root,root) %{_libdir}/libzif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzif.so.5
%{_libdir}/girepository-1.0/Zif-1.0.typelib
%dir %{_sysconfdir}/zif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zif/zif.conf
%dir /var/lib/zif
%ghost /var/lib/zif/history.db
%{_mandir}/man1/zif.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzif.so
%{_includedir}/libzif
%{_datadir}/gir-1.0/Zif-1.0.gir
%{_pkgconfigdir}/zif.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzif.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/zif

%files -n bash-completion-zif
%defattr(644,root,root,755)
/etc/bash_completion.d/zif-completion.bash
