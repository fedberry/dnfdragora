# For release builds set to 1, for snapshots set to 0
%global relbuild 1

%if !0%{?relbuild}
%global commit 3662635626599923d196e8b8a28fe8ec4510a17a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20170411
%global git_ver -git%{gitdate}.%{shortcommit}
%global git_rel .git%{gitdate}.%{shortcommit}
%endif # !0%%{?relbuild}

# CMake builds out of tree.
%global _cmake_build_subdir %{_target_platform}

Name:		dnfdragora
Version:	1.0.1
Release:	1%{?git_rel}%{?dist}
Summary:	DNF package-manager based on libYui abstraction

License:	GPLv3+
URL:		https://github.com/manatools/%{name}
%if 0%{?relbuild}
Source0:	%{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else  # 0%%{?relbuild}
Source0:	%{url}/archive/%{commit}.tar.gz#/%{name}-%{version}%{?git_ver}.tar.gz
%endif # 0%%{?relbuild}

BuildArch:	noarch

BuildRequires:	cmake			>= 3.4.0
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	libappstream-glib
BuildRequires:	pkgconfig
BuildRequires:	python3-devel		>= 3.4.0
BuildRequires:	python3-dnfdaemon
BuildRequires:	python3-PyYAML
BuildRequires:	python3-sphinx
BuildRequires:	python3-yui

Requires:	dnf			>= 1.0.9
Requires:	filesystem
Requires:	hicolor-icon-theme
Requires:	libyui-mga-ncurses
Requires:	python3-dnfdaemon
Requires:	python3-PyYAML
Requires:	python3-yui		>= 1.1.1-10

%description
%{name} is a DNF frontend, based on rpmdragora from Mageia
(originally rpmdrake) Perl code.

%{name} is written in Python 3 and uses libYui, the widget
abstraction library written by SUSE, so that it can be run
using Qt 5, GTK+ 3, or ncurses interfaces.


%package gui
Summary:	Meta-package to pull the needed dependencies for %{name} GUI-mode

Requires:	%{name}			== %{version}-%{release}

# Yumex-DNF is dead.  Let's use dnfdragora-gui as drop-in replacement.
# See:  https://pagure.io/fesco/issue/1690#comment-434558
%if (0%{?fedora} >= 27 && 0%{?fedora} <= 30)
Obsoletes:	yumex-dnf		< 4.3.3-5
Provides:	yumex-dnf		= 4.3.3-5
%endif # (0%%{?fedora} >= 27 && 0%%{?fedora} <= 30)

%description gui
%{name} is a DNF frontend, based on rpmdragora from Mageia
(originally rpmdrake) Perl code.

%{name} is written in Python 3 and uses libYui, the widget
abstraction library written by SUSE, so that it can be run
using Qt 5, GTK+ 3, or ncurses interfaces.

Meta-package to pull the needed dependencies for %{name} GUI-mode.


%prep
%if 0%{?relbuild}
%autosetup -p 1
%else  # 0%%{?relbuild}
%autosetup -n %{name}-%{commit} -p 1
%endif # 0%%{?relbuild}
%{__mkdir_p} %{_cmake_build_subdir}


%build
pushd %{_cmake_build_subdir}
%cmake								\
	-DCHECK_RUNTIME_DEPENDENCIES=ON				\
	-DENABLE_COMPS=ON					\
	..
popd
%make_build -C %{_cmake_build_subdir}


%install
%make_install -C %{_cmake_build_subdir}
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
%{_datadir}/applications/*%{name}*.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_mandir}/man5/%{name}*.5*
%{_mandir}/man8/%{name}*.8*
%{python3_sitelib}/%{name}

%files gui
# Empty meta-package.


%changelog
* Sat Apr 15 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.1-1
- New upstream release

* Wed Apr 12 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-19.git20170411.3662635
- Updated to new snapshot obsoleting patches
- Fixed dependency on libyui-mga-ncurses

* Tue Apr 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-18.git20170411.6098816
- Add fix from anaselli: `RecursionError: maximum recursion depth exceeded`
  (rhbz#1439247, #1436508, #1436451, #1440570, #1440565, #1440174)

* Mon Apr 10 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-17.git20170409.6138805
- Updated to snapshot fixing several translations
- Use rich-dependencies instead of requiring a virtual package

* Mon Apr 10 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-16.git20170407.769c37d
- Adjusted Obsoletes for Yumex-DNF

* Fri Apr 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-15.git20170407.769c37d
- Updated to snapshot fixing several translations

* Wed Apr 05 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-14.git20170405.cca9412
- Updated to snapshot fixing rhbz#1436451

* Wed Apr 05 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-13.git20170404.63fe191
- Updated to snapshot fixing several translations

* Sun Apr 02 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-12.git20170402.f3ca28b
- Updated to snapshot with improved icons and some fixed translations

* Sat Apr 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-11.git20170401.b97db68
- Updated to snapshot fixing some issues with the build-system

* Sat Apr 01 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-10.git20170401.d018d08
- Updated to snapshot adding manpages and fixing some translations

* Fri Mar 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-9.git20170330.f30c75c
- Replace and obsolete Yumex-DNF
  See:  https://pagure.io/fesco/issue/1690#comment-434558

* Thu Mar 30 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-8.git20170330.f30c75c
- Updated to snapshot fixing a missing comma
- Pick up desktop-file for installing local rpms

* Thu Mar 30 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-7.git20170330.6f50912
- Updated to snapshot fixing new dbus-signal with dnf >= 2.2.0

* Tue Mar 28 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-6.git20170325.b8545aa
- Updated to snapshot fixing several translations

* Thu Mar 23 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-5.git20170322.798975a
- Add gui-subpkg
- Prepare obsoletion of Yumex-DNF

* Thu Mar 23 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-4.git20170322.798975a
- Updated to snapshot fixing an issue with the ncurses interface

* Sun Feb 26 2017 Christian Dersch <lupinix@mailbox.org> - 1.0.0-3.git20170226.ae5163e
- updated to snapshot fixing behaviour on start without network

* Sun Feb 26 2017 Christian Dersch <lupinix@mailbox.org> - 1.0.0-2.git20170226.b0b2c9a
- updated to snapshot fixing some minor issues

* Sun Feb 19 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-1
- New upstream release (rhbz#1424827)

* Sun Feb 19 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.114.git20170218.58bd424
- New snapshot

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.0.0-0.113.git20170213.289d170
- Rebuild for brp-python-bytecompile

* Tue Feb 14 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.112.git20170213.289d170
- New snapshot

* Wed Feb 08 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.111.git20170207.783aede
- New snapshot

* Sun Feb 05 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.110.git20170205.d929620
- New snapshot

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.109.git20170204.2c34e52
- New snapshot
- Drop patch, upstreamed
- Run CMake with '-Wno-dev'-flag

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.108.git20170204.f2bb4da
- Swap date and commit-sha in release-tag

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.107.gitf2bb4da.20170204
- Add patch to build and install translations with CMake

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.106.gitf2bb4da.20170204
- New snapshot

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.105.git708a8a8.20170204
- Drop Requires: libyui-mga-ncurses, dnf should be smart enough
  to select the MGA-UI with the least deps during installation

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.104.git708a8a8.20170204
- New snapshot

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.103.gita3492da.20170204
- New snapshot

* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.102.git4d872ab.20170202
- New snapshot

* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.101.gitcc4e556.20170202
- Add Requires: libyui-mga-ncurses for functionality with low dependencies

* Thu Feb 02 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.100.gitcc4e556.20170202
- Initial import (rhbz#1418788)
- Bump to 0.100 to superseed builds from COPR

* Thu Feb 02 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0-0.1.gitcc4e556.20170202
- Initial rpm-release (rhbz#1418788)
