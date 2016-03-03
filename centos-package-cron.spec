%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%global  db_path          %{_var}/lib/centos-package-cron/

Summary:    CentOS Package Update Tool
Name:       centos-package-cron
Version:    1.0.6
License:    Public Domain
Release:    0.2%{?dist}

Source0:    *
BuildRequires:  python-setuptools >= 0.9.8
Requires:       python >= 2.6
Requires:       yum >= 3.2
Requires:       yum-plugin-changelog >= 1.1.31
Requires:       MTA
Requires:       python-sqlalchemy >= 0.5.5
Requires:       sqlite >= 3.6

%description
Notifies about updates similar to Apticron for Ubuntu.

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{db_path}

%files
%{_bindir}/centos-package-cron
%{python_sitelib}/centos_package_cron*
%{db_path}
