%define		mod_name	auth_pgsql
Summary:	This is the PgSQL authentication module for Apache
Summary(pl):	Modu³ autentykacji PgSQL dla Apache
Summary(pt_BR):	Autenticação via PostgreSQL para o Apache
Name:		apache-mod_%{mod_name}
Version:	0.9.10
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.giuseppetanzilli.it/mod_%{mod_name}/dist/mod_%{mod_name}-%{version}.tar.gz
Patch0:		%{name}-version.patch
BuildRequires:	postgresql-devel
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using postgresql RDBMS.

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem bazy danych postgresql.

%description -l pt_BR
Com o mod_auth_pgsql você pode fazer autenticação no Apache usando o
PostgreSQL.

%prep 
%setup -q -n "mod_%{mod_name}-%{version}"
%patch0 -p1

%build
/usr/sbin/apxs \
	-I %{_includedir}/postgresql \
	-l pq \
	-c mod_%{mod_name}.c \
	-o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n auth_pgsql %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n auth_pgsql %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_pkglibdir}/*
