%define		mod_name	auth_pgsql
%define 	apxs		/usr/sbin/apxs1
Summary:	This is the PostgreSQL authentication module for Apache
Summary(cs.UTF-8):	Základní autentizace pro WWW server Apache pomocí PostgreSQL
Summary(da.UTF-8):	Autenticering for webtjeneren Apache fra en PostgreSQL-database
Summary(de.UTF-8):	Authentifizierung für den Apache Web-Server, der eine PostgreSQL-Datenbank verwendet
Summary(es.UTF-8):	Autenticación vía PostgreSQL para Apache
Summary(fr.UTF-8):	Authentification de base pour le serveur Web Apache utilisant une base de données PostgreSQL
Summary(it.UTF-8):	Autenticazione di base per il server web Apache mediante un database PostgreSQL
Summary(ja.UTF-8):	PostgreSQL データベースを使った Apache Web サーバーへの基本認証
Summary(nb.UTF-8):	Autentisering for webtjeneren Apache fra en PostgreSQL-database
Summary(pl.UTF-8):	Moduł uwierzytelnienia PostgreSQL dla Apache
Summary(pt_BR.UTF-8):	Autenticação via PostgreSQL para o Apache
Summary(sv.UTF-8):	Grundläggande autenticering till webbservern Apache med en PostgreSQL-databas
Name:		apache1-mod_%{mod_name}
Version:	0.9.12
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.giuseppetanzilli.it/mod_%{mod_name}/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7be403b7487c13cdb023cc526ee2e13a
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql/
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	postgresql-devel >= 7
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_auth_pgsql <= 0.9.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using PostgreSQL RDBMS.

%description -l cs.UTF-8
Balíček mod_auth_pgsql slouží pro omezení přístupu k dokumentům, které
poskytuje WWW server Apache. Jména a hesla jsou uložena v databázi
PostgreSQL.

%description -l de.UTF-8
Mod_auth_pgsql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es die Felder in
einer Tabelle in einer PostgresQL-Datenbank prüft.

%description -l es.UTF-8
Mod_auth_pgsql puede usarse para limitar el acceso a documentos
servidos desde un servidor web verificando datos en una base de datos
PostgreSQL.

%description -l fr.UTF-8
mod_auth_pgsql peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant des champs dans une table d'une
base de données PostgresQL.

%description -l it.UTF-8
Mod_auth_pgsql può essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i campi di una tabella in un
database PostgresQL.

%description -l ja.UTF-8
Mod_auth_pgsql は、PostgresQL データベースのテーブルの中のフィールドを
チェックすることによって、Web サーバーが提供する文書へのアクセスを
制限できます。

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem bazy danych PostgreSQL.

%description -l pt_BR.UTF-8
Com o mod_auth_pgsql você pode fazer autenticação no Apache usando o
PostgreSQL.

%description -l sv.UTF-8
Mod_auth_pgsql kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera data i en
PostgreSQL-databas.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} \
	-I%{_includedir}/postgresql \
	-lpq \
	-c mod_%{mod_name}.c \
	-o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 0.9.12-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
