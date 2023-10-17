%define __prefix /usr/local

# workaround for sum missmatch
%define __prelink_undo_cmd %{nil}

%define debug_package %{nil}
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name: %{_name}
Version: %{_version}
Release: %{_release}%{dist}
Summary: vkbot.market
Group: vkbot.market
License: Python and LGPLv2
Url: https://vk.com/snewar

Source: %{_tarballname}.tar

BuildRequires: python3 = 3.11.4
Requires: python3 = 3.11.4

%description
vkbot.market
See <link on some confluence>

%prep


%setup -qc


%build


%install
# creating virtual environment
virtualenv %{buildroot}%{__prefix}/%{name}

# install requirements
%{buildroot}%{__prefix}/%{name}/bin/python -m pip install pip==20.3.4
%{buildroot}%{__prefix}/%{name}/bin/python -m pip install -r requirements.txt
%{buildroot}%{__prefix}/%{name}/bin/python -m pip install .

# remove setuptools and pip while keeping pkg_resource
SETUPTOOLS_RECORD=`find %{buildroot}%{__prefix}/%{name} -type f -name RECORD | grep setuptools`
sed -i '/^pkg_resources.py/d' $SETUPTOOLS_RECORD
sed -i '/^_markerlib/d' $SETUPTOOLS_RECORD
%{buildroot}%{__prefix}/%{name}/bin/python -m pip uninstall pip setuptools --yes

# do not include *.pyc in rpm
# .pyc may be link too
find %{buildroot}%{__prefix}/%{name}/ -name "*.py[co]" -delete

# fix python path
find %{buildroot}%{__prefix}/%{name}/bin -type f \
    -exec sed -i 's:%{buildroot}::' {} \;

# compile py files
%{buildroot}%{__prefix}/%{name}/bin/python \
    -m compileall -qf %{buildroot}%{__prefix}/%{name}/

# init.d scripts
%{__mkdir_p} %{buildroot}/usr/local/etc/vkbot

%{__install} -D -m 644 -p contrib/log.ini \
    %{buildroot}/usr/local/etc/vkbot/log.ini

%{__install} -D -m 644 -p contrib/conf.sample.env \
    %{buildroot}/usr/local/etc/vkbot/conf.sample.env

%{__install} -D -m 644 -p contrib/config.sample.yaml \
    %{buildroot}/usr/local/etc/vkbot/config.sample.yaml

%{__install} -D -m 755 contrib/vkbot.service %{buildroot}/%{_unitdir}/vkbot.service

# logs
%{__mkdir_p} %{buildroot}/var/log/vkbot/
%{__mkdir_p} %{buildroot}/var/lib/vkbot/
%{__mkdir_p} %{buildroot}/var/run/vkbot/
%{__mkdir_p} %{buildroot}/var/www/vkbot/

%pre
getent group vkbot >/dev/null || groupadd -r vkbot
getent passwd vkbot >/dev/null || \
    useradd -r -g vkbot -d /home/vkbot -s /sbin/nologin \
    -c "this account to run vkbot applications" vkbot

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%{__prefix}/%{name}/
%{__prefix}/etc/%{name}/
%{_unitdir}/vkbot.service

%attr(-, vkbot, vkbot) /var/log/vkbot
%attr(-, vkbot, vkbot) /var/lib/vkbot
%attr(-, vkbot, vkbot) /var/run/vkbot
%attr(-, vkbot, vkbot) /var/www/vkbot
