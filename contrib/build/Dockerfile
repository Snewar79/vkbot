FROM centos:7.9.2009

WORKDIR /
RUN mkdir build

# install OpenSSL 1.1.x
WORKDIR /build
RUN yum -y install openssl openssl-devel
RUN openssl version
RUN yum -y remove openssl openssl-devel
RUN openssl version || true

RUN yum -y groupinstall "Development Tools"
RUN yum install which -y

RUN yum install wget -y

RUN wget https://www.openssl.org/source/openssl-1.1.1t.tar.gz --no-check-certificate
RUN tar xvf openssl-1.1.1t.tar.gz
WORKDIR /build/openssl-1.1.1t

RUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
RUN make -j $(nproc)
RUN make install
RUN ldconfig

ENV PATH="${PATH}:/usr/local/openssl/bin"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/openssl/lib"
RUN  which openssl

# build python3.11.4
WORKDIR /build
RUN yum -y install epel-release
RUN yum -y install wget make cmake gcc bzip2-devel libffi-devel zlib-devel
RUN gcc --version

WORKDIR /build
RUN yum install rpm-build -y
RUN yum install centos-release-scl -y

RUN mkdir /tmp/builds/python/BUILDROOT/python-build-root -p
WORKDIR /tmp/builds/python/BUILDROOT/python-build-root
RUN wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz
RUN mkdir SOURCES
RUN mv Python-3.11.4.tgz SOURCES

COPY python3.11.4-c7x64.spec /tmp/builds/python/BUILDROOT/python-build-root

RUN yum-builddep -y \
      --define "_topdir `pwd`"  \
      --define "name python3"  \
      --define "version 3.11.4"  \
      --define "release 1"  \
      --define "buildthreads 8"  \
      --define "openssl11 yes"  \
      python3.11.4-c7x64.spec

RUN rpmbuild -bb \
      --clean \
      --define "_topdir `pwd`"  \
      --define "name python3"  \
      --define "version 3.11.4"  \
      --define "release 1"  \
      --define "buildthreads 8"  \
      --define "openssl11 yes"  \
      python3.11.4-c7x64.spec

RUN yum localinstall /tmp/builds/python/BUILDROOT/python-build-root/RPMS/x86_64/python3-3.11.4-1.el7.x86_64.rpm -y

WORKDIR /build

RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash -
RUN yum install -y nodejs

RUN yum install postgresql postgresql-devel python-devel -y
