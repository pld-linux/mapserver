#
# TODO:
# - add conditional builds for all mapscript variants
# - test php mapscript
# - fix perl mapscript
# - fix tcl mapscript
#
# Contitional build:
%bcond_with	ms_php			# PHP mapscript module
%bcond_with	ms_perl			# Perl mapscript module
%bcond_with	ms_tcl			# Tcl mapscript module
#
#%%define	apxs	/usr/sbin/apxs1
Summary:	Web-enabled mapping application development
Summary(pl.UTF-8):	Generowanie map poprzez WWW
Name:		mapserver
Version:	7.0.0
Release:	0.6
License:	BSD-like
Group:		Applications
Source0:	http://download.osgeo.org/mapserver/%{name}-%{version}.tar.gz
# Source0-md5:	e39360006e668ae2ba3560ed37a43e9b
#git diff rel-7-0-0..>mapserver-branch.patch
Patch0:		%{name}-branch.patch
Patch1:		%{name}-fastcgi-cmake.patch
Patch2:		%{name}-fribidi-cmake.patch
URL:		http://mapserver.org/
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	cmake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gdal-devel >= 1.3.0
BuildRequires:	giflib-devel
BuildRequires:	fribidi-devel
BuildRequires:	harfbuzz-devel
BuildRequires:	proj-devel >= 4
BuildRequires:	fcgi-devel
%{?with_ms_php:BuildRequires:	php-devel}
%if %{with ms_perl}
BuildRequires:	perl-devel
BuildRequires:	swig-perl
%endif

#BuildRequires:	apache-devel
#BuildRequires:	bison
#BuildRequires:	curl-devel >= 7.10.1
#BuildRequires:	gd-devel >= 2.0.16
#BuildRequires:	geos-devel >= 2.0.0
#BuildRequires:	libtiff-devel
#BuildRequires:	ming-devel
#BuildRequires:	pdflib-devel
#BuildRequires:	rpm-perlprov
#%{?with_ms_tcl:BuildRequires:	tcl-devel}
#BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MapServer is a CGI based Web mapping application development tool. It
processes user defined configuration files and templates to allow for
a wide variety of applications to be developed, including interactive
mapping, and spatial query definition and processing. It supports
several data formats. Key features include scale dependent map
rendering, automatic scalebar and legend building, feature labeling
with collision avoidance, logical and thematic classifications, and
on-the-fly projection of raster and vector data. The application can
also access other WMS servers as a cascading map server.

%description -l pl.UTF-8
MapServer to narzędzie do tworzenia aplikacji z mapami dostępnymi
przez WWW bazujących na CGI. Przetwarza zdefiniowane przez użytkownika
pliki konfiguracyjne i wzorce, pozwalając na tworzenie dużego zakresu
aplikacji, w tym interaktywne mapy oraz definicje i przetwarzanie
zapytań przestrzennych. Obsługuje kilka formatów danych. Podstawowe
możliwości to renderowanie map w zależności od skali, automatyczny
suwak skalujący i tworzenie legendy, nanoszenie nazw z unikaniem
kolizji, klasyfikacja logiczna i tematyczna oraz tworzone w locie
rzuty danych rastrowych i wektorowych. Aplikacja może także korzystać
z innych serwerów WMS jako kaskadowy serwer map.

%package devel
Summary:	MapServer development package
Summary(pl.UTF-8):	Pakiet programistyczny MapServer
Group:		Development/Libraries

%description devel
This package contains static library and header file for developing
programs that use libmap.

%description devel -l pl.UTF-8
Ten pakiet zawiera bibliotekę statyczną i plik nagłówkowy do tworzenia
programów używających libmap.

%package -n perl-mapscript
Summary:	Perl MapScript module
Summary(pl.UTF-8):	Moduł Perla MapScript
Group:		Development/Languages/Perl
#%requires_eq	perl

%description -n perl-mapscript
Perl MapScript module.

%description -n perl-mapscript -l pl.UTF-8
Moduł Perla MapScript.

%package -n php-mapscript
Summary:	MapScript module for PHP
Summary(pl.UTF-8):	Moduł MapScript dla PHP
Group:		Libraries
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4

%description -n php-mapscript
MapScript extension module for PHP.

%description -n php-mapscript -l pl.UTF-8
Moduł MapScript dla PHP.

%package -n tcl-mapscript
Summary:	Tcl MapScript module
Summary(pl.UTF-8):	Moduł Tcl MapScript
Group:		Development/Languages/Tcl

%description -n tcl-mapscript
Tcl MapScript module.

%description -n tcl-mapscript -l pl.UTF-8
Moduł Tcl MapScript.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

install -d build
cd build
%cmake \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DINSTALL_BIN_DIR=%{_bindir} \
	-DINSTALL_INCLUDE_DIR=%{_includedir} \
	-DWITH_PHP=0%{?with_ms_php:1} \
	-DWITH_PERL=0%{?with_ms_perl:1} \
        ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with ms_php}
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/mapscript.ini
; Enable mapscript extension module
extension=php_mapscript.so
EOF
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n php-mapscript
%php_webserver_restart

%postun -n php-mapscript
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README HISTORY.TXT
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libmapserver.so.*.*.*
%ghost %{_libdir}/libmapserver.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmapserver.so
%{_includedir}/mapserver
%dir %{_datadir}/mapserver
%{_datadir}/mapserver/cmake

%if %{with ms_perl}
%files -n perl-mapscript
%defattr(644,root,root,755)
%doc mapscript/perl/examples/*.pl
#%{perl_vendorarch}/mapscript.pm
#%dir %{perl_vendorarch}/auto/mapscript
#%{perl_vendorarch}/auto/mapscript/mapscript.bs
#%attr(755,root,root) %{perl_vendorarch}/auto/mapscript/mapscript.so
%endif

%if %{with ms_php}
%files -n php-mapscript
%defattr(644,root,root,755)
%doc mapscript/php/README mapscript/php/examples/*.phtml
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/mapscript.ini
%attr(755,root,root) %{php_extensiondir}/php_mapscript.so
%endif

%if %{with ms_tcl}
%files -n tcl-mapscript
%defattr(644,root,root,755)
%doc mapscript/tcl/README mapscript/tcl/examples/*.tcl
%dir %{_libdir}/MapscriptTcl1.1
%attr(755,root,root) %{_libdir}/MapscriptTcl1.1/*.so
%{_libdir}/MapscriptTcl1.1/*.tcl
%{_libdir}/MapscriptTcl1.1/*.html
%endif
