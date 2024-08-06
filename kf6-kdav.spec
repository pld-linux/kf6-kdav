#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.4
%define		qtver		5.15.2
%define		kfname		kdav
Summary:	Kdav
Name:		kf6-%{kfname}
Version:	6.4.0
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	22d430f8c3c0a1ea87cc4c0900948893
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6Test-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kdeframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kdeframever}
BuildRequires:	kf6-ki18n-devel >= %{kdeframever}
BuildRequires:	kf6-kio-devel >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A DAV protocoll implemention with KJobs.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.


%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories6/kdav.categories
%ghost %{_libdir}/libKF6DAV.so.6
%attr(755,root,root) %{_libdir}/libKF6DAV.so.*.*
%{_datadir}/qlogging-categories6/kdav.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KDAV
%{_libdir}/cmake/KF6DAV
%{_libdir}/libKF6DAV.so
