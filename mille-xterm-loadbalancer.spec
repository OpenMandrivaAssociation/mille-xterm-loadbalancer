%define svn 2137

Summary:	Load balancer for the MILLE-XTERM project
Name:		mille-xterm-loadbalancer
Version:	1.0
Release:	%mkrel 0.%{svn}.4
License:	GPL
Group:		System/Servers
URL:		http://www.revolutionlinux.com/mille-xterm
Source:		mille-xterm-loadbalancer-%{version}.tar.bz2
Patch0:		mille-xterm-loadbalancer-1.0-initscript.patch
%py_requires -d
BuildRequires:	perl
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-buildroot

%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%%d.%%d'%%v" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_prefix %(python -c "import sys; print sys.prefix" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_libdir %{py_prefix}/lib/python%{py_ver}

%description
Load balancer for the MILLE-XTERM project.


%package -n	%{name}-common
Summary:	Documentation and common files
Group:		System/Servers

%description -n	%{name}-common
Load balancer of the MILLE-XTERM project.

Documentation and common files

%package -n	%{name}-lbagent
Summary:	Monitoring agent
Group:		System/Servers
Requires:	%{name}-common

%description -n	%{name}-lbagent
Load balancer of the MILLE-XTERM project.

Monitoring agent

%package -n	%{name}-lbserver
Summary:	Load balancer server
Group:		System/Servers
Requires:	%{name}-common

%description -n	%{name}-lbserver
Load balancer of the MILLE-XTERM project.

Load balancer server

%prep

%setup -q
%patch0 -p1
find -type f|xargs perl -pi -e "s|\015||g;"

%build 

%install
rm -fr %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/lib/python%{py_ver}/site-packages

pushd src/lbagent
    python setup.py install --prefix=%{buildroot}
popd

pushd src/lbserver
    python setup.py install --prefix=%{buildroot}
popd

chmod 755 %{buildroot}%{_datadir}/mille-xterm/lb*/*

install -m0755 src/lbagent/lbagent %{buildroot}%{_initrddir}/lbagent
install -m0755 src/lbserver/lbserver %{buildroot}%{_initrddir}/lbserver

# cleanup
rm -rf %{buildroot}%{_sysconfdir}/init.d
rm -rf %{buildroot}/lib/python%{py_ver}/site-packages

%post -n %{name}-lbserver
chkconfig --add lbserver

%preun -n %{name}-lbserver
chkconfig --del lbserver

%post -n %{name}-lbagent
chkconfig --add lbagent

%preun -n %{name}-lbagent
chkconfig --del lbagent

%clean
rm -rf %{buildroot}

%files -n %{name}-common
%defattr(-,root,root)
%doc AUTHORS Changelog COPYING doc/LoadBalancer_fr.odt doc/examples/v07_lbaconfig.xml doc/examples/v07_lbsconfig.xml INSTALL README

%files -n %{name}-lbagent
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mille-xterm/lbaconfig.xml
%{_initrddir}/lbagent
%{_datadir}/mille-xterm/lbagent/*

%files -n %{name}-lbserver
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mille-xterm/lbsconfig.xml
%{_initrddir}/lbserver
%{_datadir}/mille-xterm/lbserver/*


