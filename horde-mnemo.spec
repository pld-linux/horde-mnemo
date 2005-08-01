%include	/usr/lib/rpm/macros.php
Summary:	Nag Task List Manager
Name:		mnemo
Version:	2.0.1
Release:	0.1
License:	GPL
Vendor:		The Horde Project
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/mnemo/%{name}-h3-%{version}.tar.gz
# Source0-md5:	eca23463b7340b8bc1e7b5be2353bdc9
Source1:	%{name}.conf
URL:		http://www.horde.org/mnemo/
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir		/usr/share/horde
%define		_sysconfdir		/etc/horde.org
%define		_appdir			%{hordedir}/%{name}

%description
Mnemo is the Horde notes and memos application. It lets users keep
free-text notes and other bits of information which doesn't fit as a
contact, a todo item, an event, etc. It is very similar in
functionality to the Palm Memo application.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Gollem) please visit <http://www.horde.org/>.

%prep
%setup -q -n %{name}-h3-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.daily,%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
install  config/conf.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You may need to
create the Mnemo database tables. To do so run:
zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{name}.sql.gz | mysql horde
EOF
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
