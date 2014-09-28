%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Summary:    CentOS Package Update Tool
Name:       centos-package-cron
Version:    1.0
License:    Public Domain
Release:    0.4%{?dist}

Source0:    *
Requires:   python >= 2.7.5
Requires:   yum >= 3.4.3
Requires:   yum-plugin-changelog >= 1.1.31
Requires:   mailx

%description
Notifies about updates similar to Apticron for Ubuntu.

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%files
%{_bindir}/centos-package-cron
%{python_sitelib}/centos_package_cron*
