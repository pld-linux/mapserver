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
BuildRequires:	freetype-devel
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

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz */*.gz
%attr(755,root,root) %{_bindir}/*
