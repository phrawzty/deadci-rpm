%global go_import_path github.com/phrawzty/deadci
%global rev 2bc162f673dcd5028c272c91e463fde3fbf65a8d
%global shortrev %(r=%{rev}; echo ${r:0:12})

Name:           deadci
Version:	0
Release:        1.git%{shortrev}%{?dist}
Summary:        DeadCI is a lightweight continuous integration and testing web server.
Group:          System Environment/Daemons
License:        BSD
URL:            https://deadci.com
Source0:	https://github.com/phrawzty/%{name}/archive/%{rev}/%{name}-%{rev}.tar.gz
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units, golang >= 1.3.0, mercurial
Requires:       systemd
%endif
Requires(pre): shadow-utils

%description
DeadCI is a lightweight continuous integration and testing web server that
integrates seamlessly with GitHub (other platforms coming). As the name implies
it is dead easy to use. DeadCI works by running a command of your choice at the
root of the repository being built. It's easy to run TravisCI jobs from a
.travis.yml locally. It also integrates nicely with JoliCI to run yours tests
inside a Docker container. 

%prep

%setup -qn %{name}-%{rev}

%build
export GOPATH=`pwd`
go get %{go_import_path}
go build %{go_import_path}

%install
mkdir -p %{buildroot}/%{_bindir}
cp bin/%{name} %{buildroot}/%{_bindir}
cp travis-local/travis-local %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
cp %{name}.ini %{buildroot}/%{_sharedstatedir}/%{name}/%{name}.ini-DIST
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
cp %{SOURCE3} %{buildroot}/%{_initrddir}/deadci
%endif

%pre
getent group deadci >/dev/null || groupadd -r deadci
getent passwd deadci >/dev/null || \
    useradd -r -g deadci -d /var/lib/deadci -s /sbin/nologin \
    -c "deadci user" deadci
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/sysconfig/%{name}
%dir %attr(750, deadci, deadci) %{_sharedstatedir}/%{name}
%attr(660, deadci, deadci) %{_sharedstatedir}/%{name}/%{name}.ini-DIST
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%attr(755, root, root) %{_bindir}/%{name}
%attr(755, root, root) %{_bindir}/travis-local

%doc


%changelog
* Tue Mar 17 2015 Dan Phrawzty <phrawzty@mozilla.com>
- Switch to new upstream.
* Fri Mar 13 2015 Dan Phrawzty <phrawzty@mozilla.com>
- release 2 (fix sysconfig)
* Mon Feb 23 2015 Dan Phrawzty <phrawzty@mozilla.com>
- release 1 (upstream has no versioning)
