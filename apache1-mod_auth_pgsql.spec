%define		mod_name	auth_pgsql
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PostgreSQL authentication module for Apache
Summary(cs):	Základní autentizace pro WWW server Apache pomocí PostgreSQL
Summary(da):	Autenticering for webtjeneren Apache fra en PostgreSQL-database
Summary(de):	Authentifizierung für den Apache Web-Server, der eine PostgreSQL-Datenbank verwendet
Summary(es):	Autenticación vía PostgreSQL para Apache
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant une base de données PostgreSQL
Summary(it):	Autenticazione di base per il server web Apache mediante un database PostgreSQL
Summary(ja):	PostgreSQL ¥Ç¡¼¥¿¥Ù¡¼¥¹¤ò»È¤Ã¤¿ Apache Web ¥µ¡¼¥Ð¡¼¤Ø¤Î´ðËÜÇ§¾Ú
Summary(no):	Autentisering for webtjeneren Apache fra en PostgreSQL-database
Summary(pl):	Modu³ autentykacji PostgreSQL dla Apache
Summary(pt_BR):	Autenticação via PostgreSQL para o Apache
Summary(sv):	Grundläggande autenticering till webbservern Apache med en PostgreSQL-databas
Name:		apache-mod_%{mod_name}
Version:	0.9.12
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.giuseppetanzilli.it/mod_%{mod_name}/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7be403b7487c13cdb023cc526ee2e13a
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
BuildRequires:	postgresql-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	mod_auth_pgsql

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using postgresql RDBMS.

%description -l cs
Balíèek mod_auth_pgsql slou¾í pro omezení pøístupu k dokumentùm, které
poskytuje WWW server Apache. Jména a hesla jsou ulo¾ena v databázi
PostgreSQL.

%description -l de
Mod_auth_pgsql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es die Felder in
einer Tabelle in einer PostgresQL-Datenbank prüft.

%description -l es
Mod_auth_pgsql puede usarse para limitar el acceso a documentos
servidos desde un servidor web verificando datos en una base de datos
PostgreSQL.

%description -l fr
mod_auth_pgsql peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant des champs dans une table d'une
base de données PostgresQL.

%description -l it
Mod_auth_pgsql può essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i campi di una tabella in un
database PostgresQL.

%description -l ja
Mod_auth_pgsql ¤Ï¡¢PostgresQL ¥Ç¡¼¥¿¥Ù¡¼¥¹¤Î¥Æ¡¼¥Ö¥ë¤ÎÃæ¤Î¥Õ¥£¡¼¥ë¥É¤ò
¥Á¥§¥Ã¥¯¤¹¤ë¤³¤È¤Ë¤è¤Ã¤Æ¡¢Web ¥µ¡¼¥Ð¡¼¤¬Äó¶¡¤¹¤ëÊ¸½ñ¤Ø¤Î¥¢¥¯¥»¥¹¤ò
À©¸Â¤Ç¤­¤Þ¤¹¡£

%description -l pl
To jest modu³ autentykacji dla Apache pozwalaj±cy na autentykacjê
klientów HTTP z u¿yciem bazy danych postgresql.

%description -l pt_BR
Com o mod_auth_pgsql você pode fazer autenticação no Apache usando o
PostgreSQL.

%description -l sv
Mod_auth_pgsql kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera data i en
PostgreSQL-databas.

%prep
%setup -q -n "mod_%{mod_name}-%{version}"

%build
%{apxs} \
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
%{apxs} -e -a -n auth_pgsql %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n auth_pgsql %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_pkglibdir}/*
