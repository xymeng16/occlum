%define centos_base_release 1

%define _unpackaged_files_terminate_build 0
%define sgxsdk_install_dir /opt/intel

Name: occlum
Version: %{_version}
Release: %{centos_base_release}%{?dist}
Summary: Memory-safe, multi-process library OS (LibOS) for Intel SGX
Group: Development/Libraries
License: BSD License
URL: https://github.com/occlum/occlum
Source0: https://github.com/occlum/occlum/archive/%{_version}.tar.gz
Source10: occlum-pal.sh
Source11: occlum-filelist
Source12: occlum-pal-filelist
Source13: occlum-platform-filelist
SOURCE14: occlum-platform.sh

ExclusiveArch: x86_64

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cmake
BuildRequires: libtool
BuildRequires: ocaml
BuildRequires: ocaml-ocamlbuild
BuildRequires: python
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: git
BuildRequires: fuse-devel
BuildRequires: fuse-libs

%description
Occlum is a memory-safe, multi-process library OS (LibOS) for Intel SGX.
As a LibOS, it enables legacy applications to run on SGX with little or even no modifications of source code,
thus protecting the confidentiality and integrity of user workloads transparently.

%package pal
Summary: Platform Abstraction Layer of Occlum enclave

%description pal
occlum-pal is the Platform Abstraction Layer of Occlum enclave.
It provides interfaces to execute trused applications inside enclave.

%package platform
Summary: Platform Abstraction Layer command for occlum enclave

%description platform
occlum-platform contains command for occlum enclave.

%prep
%setup -q -c -n %{name}-%{_version}

%build
# build occlum
cd %{?_builddir}/%{name}-%{_version}/occlum-%{_version}
NOT_GIT=true make submodule

%install
# set sgxsdk env
source %{sgxsdk_install_dir}/sgxsdk/environment

cd occlum-%{_version}
OCCLUM_RELEASE_BUILD=1 make
OCCLUM_PREFIX=%{?buildroot}/opt/occlum make install

# install occlum-pal.sh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

%files -f %{SOURCE11}

%files pal -f %{SOURCE12}
/etc/profile.d/occlum-pal.sh

%files platform -f %{SOURCE13}
/etc/profile.d/occlum-platform.sh

%post pal
echo 'Please execute command "source /etc/profile" to validate envs immediately'

%post platform
echo 'Please execute command "source /etc/profile" to validate envs immediately'

%changelog
* Mon Aug 03 2020 Chunyang Hui <sanqian.hcy@antfin.com> - 0.14.0-1
- Integrate with Occlum
- Remove sgxsdk installation

* Mon Jul 20 2020 Chunmei Xu <xuchunmei@linux.alibaba.com> - 0.14.0-0
- Initial commit