# TODO
# - "port" to jbj rpm, sigh
#/usr/include/rpm/hdrinline.h:615:10: error: expected '=', ',', ';', 'asm' or '__attribute__' before 'headerGetStartOff'
#/usr/include/rpm/hdrinline.h:624:10: error: expected '=', ',', ';', 'asm' or '__attribute__' before 'headerSetStartOff'
#/usr/include/rpm/hdrinline.h:632:10: error: expected '=', ',', ';', 'asm' or '__attribute__' before 'headerGetEndOff'
#/usr/include/rpm/hdrinline.h:641:10: error: expected '=', ',', ';', 'asm' or '__attribute__' before 'headerSetEndOff'
Summary:	Simple wrapper for rpm and the Fedora package metadata
Name:		zif
Version:	0.1.5
Release:	0.1
License:	GPL v2+
Group:		Libraries
URL:		http://github.com/hughsie/zif
Source0:	http://www.packagekit.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	7811aae553cb4d1f21648096a7e9a8d0
BuildRequires:	bzip2-devel
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gnome-doc-utils
BuildRequires:	gpgme-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libarchive-devel
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	rpm-devel
BuildRequires:	sqlite-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zif is a simple yum-compatible library that provides read-write access
to the rpm database and the Fedora metadata for PackageKit.

Zif is not designed as a replacement to yum, nor to be used by end
users.

%package devel
Summary:	GLib Libraries and headers for zif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bzip2-devel
Requires:	gpgme-devel
Requires:	zlib-devel

%description devel
GLib headers and libraries for zif.

%prep
%setup -q

%build
%configure \
	--enable-gtk-doc \
	--disable-static \
	--disable-dependency-tracking
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libzif*.la

%find_lang Zif

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f Zif.lang
%defattr(644,root,root,755)
%doc README AUTHORS NEWS
%{_sysconfdir}/bash_completion.d/*-completion.bash
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zif/zif.conf
%attr(755,root,root) %{_bindir}/zif
%{_libdir}/*libzif*.so.*
%{_mandir}/man1/*.1*
%dir %{_sysconfdir}/zif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libzif*.so
%{_pkgconfigdir}/zif.pc
%dir %{_includedir}/libzif
%{_includedir}/libzif/*.h
%{_datadir}/gtk-doc
