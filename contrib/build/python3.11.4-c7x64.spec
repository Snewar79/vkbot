%global __python python3.6

Name: %{name}
Version: %{version}
Release: %{release}%{dist}
Group: Internet
Summary: reup
License: reup
URL: https://python.org


%if "%{openssl11}" == "yes"
BuildRequires: openssl11-devel >= 1.1.1
%else
BuildRequires: openssl-devel >= 1.0.2
%endif

BuildRequires: devtoolset-8-gcc >= 8.2.1
BuildRequires: devtoolset-8-gcc-c++ >= 8.2.1
BuildRequires: rh-python36-python >= 3.6.3-1
BuildRequires: bzip2-devel >= 1.0.6
BuildRequires: libffi-devel >= 3.0.13
BuildRequires: make >= 3.82-24
BuildRequires: xz-devel >= 5.2.2

%if "%{openssl11}" == "yes"
Requires: openssl11 >= 1.1.1
%endif

Autoreq: no

Source: Python-%{version}.tgz

%description
reup

%prep

%setup -qc

%build
export PATH="/opt/rh/devtoolset-8/root/usr/bin:${PATH}"

ln -sf /opt/rh/devtoolset-8/root/bin/gcc /usr/bin/gcc
ln -sf /opt/rh/devtoolset-8/root/bin/g++ /usr/bin/g++

%if "%{openssl11}" == "yes"
sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' Python-%{version}/configure
%endif

Python-%{version}/configure --enable-optimizations

%install
make -j %{buildthreads}
make install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
/usr/local/
