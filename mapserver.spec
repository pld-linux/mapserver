Summary:	Web-enabled mapping application development
Summary(pl):	Generowanie map poprzez www
Name:		mapserver
Version:	3.5
Release:	1
License:	BSD-like
Group:		Applications
Source0:	http://mapserver.gis.umn.edu/dist/ms_%{version}.tar.gz
URL:		http://mapserver.gis.umn.edu/
BuildRequires:	apache-devel < 2.0.0
BuildRequires:	apache-devel >= 1.3.0
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pdflib-devel
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

%prep
%setup -q -n %{name}_%{version}

%build
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
        CPPFLAGS="`pkg-config libpng12 --cflags`"; export CPPFLAGS
fi
%configure2_13 \
	--with-eppl \
	--with-apxs=%{_sbindir}/apxs \
	--with-php
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README */*.gz
%attr(755,root,root) %{_bindir}/*
