# TODO:
# - Fix tests (a few fail)
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define		module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python3-%{module}
Version:	7.0.0
Release:	3
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/psutil/
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	5ad9868e9f36604f8164ba7bf53550f2
URL:		https://github.com/giampaolo/psutil
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-ipaddress
BuildRequires:	python3-mock
%endif
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Module providing an interface for retrieving information on all
running processes and system utilization (CPU, disk, memory, network)
in a portable way by using Python, implementing many functionalities
offered by command line tools.

%description -l pl.UTF-8
Moduł dostarczający interfejs do informacji o działających procesach
oraz zużyciu systemu (procesor, dyski, pamięć, sieć) w przenośny
sposób używjąc Pythona. Implementuje wiele funkcjonalności oferowanych
przez narzędzia linii komend.

%package apidocs
Summary:	API documentation for Python psutil module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona psutil
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python psutil module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona psutil.

%prep
%setup -q -n %{module}-release-%{version}

%build
%py3_build

%if %{with tests}
cd build-3/lib.*
ln -sf ../../scripts .
ln -sf ../../setup.py .
PYTHONPATH=$(pwd) \
%{__python3} -m psutil.tests
%{__rm} scripts setup.py
cd ../..
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/psutil/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst LICENSE README.rst
%dir %{py3_sitedir}/psutil
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_linux.*.so
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_posix.*.so
%{py3_sitedir}/psutil/*.py
%{py3_sitedir}/psutil/__pycache__
%{py3_sitedir}/psutil-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
