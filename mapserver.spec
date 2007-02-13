#
# TODO:
# - add conditional builds for all mapscript variants
# - fix tcl mapscript (maybe rel > 4.6.1 will include pre-swig'ed mapscript_wrap.c)
#
# Contitional build:
%bcond_with	ms_tcl			# Tcl mapscript module
#
#%%define	apxs	/usr/sbin/apxs1
%include	/usr/lib/rpm/macros.perl
Summary:	Web-enabled mapping application development
Summary(pl.UTF-8):	Generowanie map poprzez WWW
Name:		mapserver
Version:	4.10.0
Release:	0.1
License:	BSD-like
Group:		Applications
Source0:	http://cvs.gis.umn.edu/dist/%{name}-%{version}.tar.gz
# Source0-md5:	4668bbd017c20c251e962a5cd09c8f31
Patch0:		%{name}-fastcgi-include.patch
URL:		http://mapserver.gis.umn.edu/
BuildRequires:	apache-devel
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	curl-devel >= 7.10.1
BuildRequires:	fcgi-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gd-devel >= 2.0.16
BuildRequires:	gdal-devel >= 1.3.0
BuildRequires:	geos-devel >= 2.0.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	ming-devel
BuildRequires:	pdflib-devel
BuildRequires:	perl-devel
BuildRequires:	php-devel >= 3:4.2.3
BuildRequires:	proj-devel >= 4
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.344
%{?with_ms_tcl:BuildRequires:	tcl-devel}
BuildRequires:	zlib-devel
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
%requires_eq	perl

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

%build
%{__autoconf}
%configure \
	--with-eppl \
	--with-php=$(php-config --include-dir) \
	--with-proj \
	--with-geos \
	--with-gdal \
	--with-postgis \
	--with-ogr \
	--with-wfs \
	--with-wcs \
	--with-wmsclient \
	--with-fastcgi \
	--with-ming \
	--with-pdf \
	--with-wfsclient

%{__make} \
	REGEX_OBJ=

cd mapscript/perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"
%if %{with ms_tcl}
# tcl currently disables - swig problems and mapscript_wrap.c not included!
cd ../tcl
touch ../../perlvars
./configure \
	--with-tcl=/usr
%{__make} \
	TCL_CC="%{__cc} %{rpmcflags} -pipe" \
	TCL_SHLIB_CC="%{__cc} %{rpmcflags} -pipe -shared"
%endif
# mapscript/python - TODO? but no Makefile nor README...

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/php,%{php_sysconfdir}/conf.d,%{_includedir}/mapserver}

install legend mapserv scalebar tile4ms \
	shp2img shp2pdf shptree shptreetst sortshp \
	$RPM_BUILD_ROOT%{_bindir}
install libmap.a $RPM_BUILD_ROOT%{_libdir}
install map.h $RPM_BUILD_ROOT%{_includedir}/mapserver

install mapscript/php3/php_mapscript.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/mapscript.ini
; Enable mapscript extension module
extension=php_mapscript.so
EOF

%{__make} -C mapscript/perl install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with ms_tcl}
%{__make} -C mapscript/tcl install \
	TCL_EXEC_PREFIX=$RPM_BUILD_ROOT%{_prefix}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n php-mapscript
%php_webserver_restart

%postun -n php-mapscript
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%triggerpostun -n php-mapscript -- php-mapscript < 4.6.1-1.1
/usr/sbin/php-module-install remove php_mapscript /etc/php/php.ini

%files
%defattr(644,root,root,755)
%doc README HISTORY.TXT
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/mapserver

%files -n perl-mapscript
%defattr(644,root,root,755)
%doc mapscript/perl/examples/*.pl
%{perl_vendorarch}/mapscript.pm
%dir %{perl_vendorarch}/auto/mapscript
%{perl_vendorarch}/auto/mapscript/mapscript.bs
%attr(755,root,root) %{perl_vendorarch}/auto/mapscript/mapscript.so

%files -n php-mapscript
%defattr(644,root,root,755)
%doc mapscript/php3/README mapscript/php3/examples/*.phtml
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/mapscript.ini
%attr(755,root,root) %{php_extensiondir}/php/php_mapscript.so

%if %{with ms_tcl}
%files -n tcl-mapscript
%defattr(644,root,root,755)
%doc mapscript/tcl/README mapscript/tcl/examples/*.tcl
%dir %{_libdir}/MapscriptTcl1.1
%attr(755,root,root) %{_libdir}/MapscriptTcl1.1/*.so
%{_libdir}/MapscriptTcl1.1/*.tcl
%{_libdir}/MapscriptTcl1.1/*.html
%endif
