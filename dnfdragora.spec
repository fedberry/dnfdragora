# No proper release-tags, yet.  :(
%global commit 4d872aba86f3988f3bc052d70dee7db1cf6b3dff
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20170202
%global git_ver -git%{shortcommit}.%{gitdate}
%global git_rel .git%{shortcommit}.%{gitdate}

# CMake builds out of tree.
%global _cmake_build_subdir %{_target_platform}

Name:		dnfdragora
Version:	0.0.0
Release:	0.102%{?git_rel}%{?dist}
Summary:	DNF package-manager based on libYui abstraction

License:	GPLv3+
URL:		https://github.com/manatools/%{name}
Source0:	%{url}/archive/%{commit}.tar.gz#/%{name}-%{version}%{?git_ver}.tar.gz

BuildArch:	noarch

BuildRequires:	cmake			>= 3.4.0
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	help2man
BuildRequires:	libappstream-glib
BuildRequires:	pkgconfig
BuildRequires:	python3-devel		>= 3.4.0
BuildRequires:	python3-dnfdaemon
BuildRequires:	python3-PyYAML
BuildRequires:	python3-yui

Requires:	dnf			>= 1.0.9
Requires:	filesystem
Requires:	hicolor-icon-theme
Requires:	python3-dnfdaemon
Requires:	python3-PyYAML
Requires:	python3-yui		>= 1.1.1-10

# Provide functionality with least dependencies on every system.
Requires:	libyui-mga-ncurses

%description
%{name} is a DNF frontend, based on rpmdragora from Mageia
(originally rpmdrake) Perl code.

%{name} is written in Python 3 and uses libYui, the widget
abstraction library written by SUSE, so that it can be run
using Qt 5, GTK+ 3, or ncurses interfaces.


%prep
%autosetup -n %{name}-%{commit} -p 1
%{__mkdir_p} %{_cmake_build_subdir}


%build
pushd %{_cmake_build_subdir}
%cmake								\
	-DCHECK_RUNTIME_DEPENDENCIES=ON				\
	-DENABLE_COMPS=ON					\
	..
popd
%make_build -C %{_cmake_build_subdir}
tools/po-compile.sh


%install
%make_install -C %{_cmake_build_subdir}

# Create man-page.
%{__mkdir_p} %{buildroot}%{_mandir}/man1
export PYTHONPATH='%{buildroot}%{python3_sitelib}'
%{_bindir}/help2man -s 1 -N					\
	--version-string='%{version}%{?git_ver}'		\
	-o %{buildroot}%{_mandir}/man1/%{name}.1		\
	%{buildroot}%{_bindir}/%{name}
unset PYTHONPATH

# Install locales.
%{__cp} -pr share/locale %{buildroot}%{_datadir}
%find_lang %{name}


%check
# Validate desktop-files.
%{_bindir}/desktop-file-validate				\
	%{buildroot}%{_datadir}/applications/*.desktop

# Validate AppData-files.
%{_bindir}/appstream-util validate-relax --nonet		\
	%{buildroot}%{_datadir}/appdata/*.appdata.xml


%post
/bin/touch --no-create						\
	%{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	/bin/touch --no-create					\
		%{_datadir}/icons/hicolor &>/dev/null
	%{_bindir}/gtk-update-icon-cache			\
		%{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache				\
	%{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yaml
%dir %{_sysconfdir}/%{name}
%doc README.md TODO %{name}.yaml.example
%license AUTHORS LICENSE
%{_bindir}/%{name}
%{_datadir}/appdata/*%{name}.appdata.xml
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_mandir}/man1/%{name}.1*
%{python3_sitelib}/%{name}


%changelog
* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.102.git4d872ab.20170202
- New snapshot

* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.101.gitcc4e556.20170202
- Add Requires: libyui-mga-ncurses for functionality with low dependencies

* Thu Feb 02 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.100.gitcc4e556.20170202
- Initial import (rhbz#1418788)
- Bump to 0.100 to superseed builds from COPR

* Thu Feb 02 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.1.gitcc4e556.20170202
- Initial rpm-release (rhbz#1418788)