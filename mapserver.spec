%include	/usr/lib/rpm/macros.perl
Summary:	Web-enabled mapping application development
Summary(pl):	Generowanie map poprzez www
Name:		mapserver
Version:	3.6.0
Release:	4
License:	BSD-like
Group:		Applications
Source0:	http://mapserver.gis.umn.edu/dist/%{name}-%{version}.tar.gz
Patch0:		%{name}-php.patch
URL:		http://mapserver.gis.umn.edu/
BuildRequires:	apache-devel < 2.0.0
BuildRequires:	apache-devel >= 1.3.0
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pdflib-devel
BuildRequires:	perl-devel
BuildRequires:	php-devel >= 4.2.3
BuildRequires:	rpm-perlprov
BuildRequires:	tcl-devel
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

%description -l pl
MapServer to narzêdzie do tworzenia aplikacji z mapami dostêpnymi
przez WWW bazuj±cych na CGI. Przetwarza zdefiniowane przez u¿ytkownika
pliki konfiguracyjne i wzorce, pozwalaj±c na tworzenie du¿ego zakresu
aplikacji, w tym interaktywne mapy oraz definicje i przetwarzanie
zapytañ przestrzennych. Obs³uguje kilka formatów danych. Podstawowe
mo¿liwo¶ci to renderowanie map w zale¿no¶ci od skali, automatyczny
suwak skaluj±cy i tworzenie legendy, nanoszenie nazw z unikaniem
kolizji, klasyfikacja logiczna i tematyczna oraz tworzone w locie
rzuty danych rastrowych i wektorowych. Aplikacja mo¿e tak¿e korzystaæ
z innych serwerów WMS jako kaskadowy serwer map.

%package devel
Summary:	MapServer development package
Summary(pl):	Pakiet programistyczny MapServer
Group:		Development/Libraries

%description devel
This package contains static library and header file for developing
programs that use libmap.

%description devel -l pl
Ten pakiet zawiera bibliotekê statyczn± i plik nag³ówkowy do tworzenia
programów u¿ywaj±cych libmap.

%package -n perl-mapscript
Summary:	Perl MapScript module
Summary(pl):	Modu³ perla MapScript
Group:		Development/Languages/Perl
%requires_eq	perl

%description -n perl-mapscript
Perl MapScript module.

%description -n perl-mapscript -l pl
Modu³ perla MapScript.

%package -n php-mapscript
Summary:	MapScript module for PHP
Summary(pl):	Modu³ MapScript dla PHP
Group:		Libraries
PreReq:		php-common = %(rpm -q --qf '%%{EPOCH}:%%{VERSION}' php-common)

%description -n php-mapscript
MapScript extension module for PHP.

%description -n php-mapscript -l pl
Modu³ MapScript dla PHP.

%package -n tcl-mapscript
Summary:	Tcl MapScript module
Summary(pl):	Modu³ Tcl MapScript
Group:		Development/Languages/Tcl

%description -n tcl-mapscript
Tcl MapScript module.

%description -n tcl-mapscript -l pl
Modu³ Tcl MapScript.

%prep
%setup -q
%patch -p1

%build
autoconf
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
        CPPFLAGS="`pkg-config libpng12 --cflags`"; export CPPFLAGS
fi
%configure \
	--with-eppl \
	--with-apxs=%{_sbindir}/apxs \
	--with-php=/usr/include/php
%{__make} REGEX_OBJ=

cd mapscript/perl
perl Makefile.PL
%{__make} \
	OPTIMIZE="%{rpmcflags}"

cd ../tcl
./configure --with-tcl=/usr
%{__make} \
	TCL_CC="%{__cc} %{rpmcflags} -pipe" \
	TCL_SHLIB_CC="%{__cc} %{rpmcflags} -pipe -shared"

# mapscript/python - TODO? but no Makefile nor README...

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/php,%{_includedir}/mapserver}

install legend mapserv scalebar tile4ms \
	shp2img shp2pdf shptree shptreetst sortshp \
	$RPM_BUILD_ROOT%{_bindir}
install libmap.a $RPM_BUILD_ROOT%{_libdir}
install map.h $RPM_BUILD_ROOT%{_includedir}/mapserver

install mapscript/php3/php_mapscript.so $RPM_BUILD_ROOT%{_libdir}/php

cd mapscript/perl
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ../tcl
%{__make} install \
	TCL_EXEC_PREFIX=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n php-mapscript
/usr/sbin/php-module-install install php_mapscript /etc/php/php.ini

%preun -n php-mapscript
if [ "$1" = "0" ]; then
	/usr/sbin/php-module-install remove php_mapscript /etc/php/php.ini
fi

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
%{perl_sitearch}/mapscript.pm
%dir %{perl_sitearch}/auto/mapscript
%{perl_sitearch}/auto/mapscript/mapscript.bs
%attr(755,root,root) %{perl_sitearch}/auto/mapscript/mapscript.so

%files -n php-mapscript
%defattr(644,root,root,755)
%doc mapscript/php3/README mapscript/php3/examples/*.phtml
%attr(755,root,root) %{_libdir}/php/php_mapscript.so

%files -n tcl-mapscript
%defattr(644,root,root,755)
%doc mapscript/tcl/README mapscript/tcl/examples/*.tcl
%dir %{_libdir}/MapscriptTcl1.1
%attr(755,root,root) %{_libdir}/MapscriptTcl1.1/*.so
%{_libdir}/MapscriptTcl1.1/*.tcl
%{_libdir}/MapscriptTcl1.1/*.html
