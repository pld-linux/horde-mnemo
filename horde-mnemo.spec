%define		hordeapp mnemo
#define		_snap	2005-08-01
%define		subver	rc2
%define		rel	1
#
%include	/usr/lib/rpm/macros.php
Summary:	Horde notes and memos application
Summary(pl.UTF-8):	Aplikacja z notatkami i przypominajkami dla Horde
Name:		horde-%{hordeapp}
Version:	2.2
Release:	%{?subver:0.%{subver}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{rel}
License:	GPL
Group:		Applications/WWW
#Source0:	ftp://ftp.horde.org/pub/mnemo/%{hordeapp}-h3-%{version}.tar.gz
Source0:	ftp://ftp.horde.org/pub/mnemo/%{hordeapp}-h3-%{version}-%{subver}.tar.gz
# Source0-md5:	083febbf8794aa1f82689fd10c2561b4
Source1:	%{hordeapp}.conf
Patch0:		%{hordeapp}-prefs.patch
URL:		http://www.horde.org/mnemo/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.15.1
Requires:	horde >= 3.0
Requires:	webapps
Obsoletes:	%{hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Mnemo is the Horde notes and memos application. It lets users keep
free-text notes and other bits of information which doesn't fit as a
contact, a todo item, an event, etc. It is very similar in
functionality to the Palm Memo application.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Mnemo) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
Mnemo to aplikacja z notatkami i przypominajkami dla Horde. Pozwala
użytkownikom na przechowywanie notatek z dowolnym tekstem oraz innych
informacji, która nie pasuje do określenia kontakt, rzecz do
zrobienia, zdarzenie itp. Jest bardzo podobna w funkcjonalności do
aplikacji Palm Memo.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla
Mnemo) można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -qcT -n %{?_snap:%{hordeapp}-%{_snap}}%{!?_snap:%{hordeapp}-%{version}%{?subver:-%{subver}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1

rm */.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the Mnemo database tables. To do so run:
zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
