{{{$version := printf "%s.%s.%s" .major .minor .patch }}}
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global golang_version 1.22.5
%global _buildhost  build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           flannel-cni-plugin
Version:        {{{ $version }}}
Release:        1%{dist}
Summary:        This plugin is designed to work in conjunction with flannel, a network fabric for containers.
Vendor:         Oracle America
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/flannel-io/cni-plugin
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  golang >= %{golang_version}

%description
This plugin is designed to work in conjunction with flannel,
a network fabric for containers. When flannel daemon is
started, it outputs a /run/flannel/subnet.env file. This
information reflects the attributes of flannel network on
the host. The flannel CNI plugin uses this information to
configure another CNI plugin, such as bridge plugin.

%prep
%setup -q -n %{name}-%{version}

%build
chmod +x scripts/build_flannel.sh
go mod tidy
go mod vendor
scripts/build_flannel.sh
source ./scripts/version.sh
cp ${OUTPUT_DIR}/flannel* dist/

%install
install -m 755 -d %{buildroot}/opt/cni/bin
cp dist/flannel* %{buildroot}/opt/cni/bin/flannel

%files
%license THIRD_PARTY_LICENSES.txt
/opt/cni/bin

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle specific build files for Flannel CNI Plugins
