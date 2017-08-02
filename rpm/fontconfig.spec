%global freetype_version 2.1.4

Name:       fontconfig
Summary:    Font configuration and customization library
Version:    2.12.4
Release:    1
Group:      System/Libraries
License:    MIT
URL:        http://fontconfig.org
Source0:    http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Source1:    10-antialias.conf
Source2:    10-hinted.conf
Source3:    25-no-bitmap-fedora.conf
Source4:    fcblanks.h
Requires(post): freetype >= %{freetype_version}
Requires(post): coreutils
Requires(post): /bin/grep
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  gawk
BuildRequires:  expat-devel
BuildRequires:  perl
BuildRequires:  python
BuildRequires:  python-lxml
BuildRequires:  gperf
Conflicts:   fonts-hebrew < 0.100
Conflicts:   fonts-xorg-base
Conflicts:   fonts-xorg-syriac


%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.



%package devel
Summary:    Font configuration and customization library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   fontconfig = %{version}-%{release}
Requires:   freetype-devel >= %{freetype_version}
Requires:   pkgconfig

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.



%prep
%setup -q -n %{name}-%{version}


%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

# avoid build time network dependency
cp %{SOURCE4} fontconfig/fc-blanks/fcblanks.h

pushd fontconfig
sh autogen.sh
%configure --disable-static \
    --with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts

make %{?jobs:-j%jobs}
# appears to run tests against already installed fontconfig with mb2, likely something similar on obs too.
# test set is quite small so just omit for now
#make check
popd

%install
rm -rf %{buildroot}

pushd fontconfig
%make_install

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
ln -s %{_datadir}/fontconfig/conf.avail/10-autohint.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/10-antialias.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/10-hinted.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/25-no-bitmap-fedora.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
popd


%post
/sbin/ldconfig
umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig
# Remove stale caches
rm -f %{_localstatedir}/cache/fontconfig/????????????????????????????????.cache-2
rm -f %{_localstatedir}/cache/fontconfig/stamp

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-pattern
%{_bindir}/fc-validate
%dir %{_datadir}/fontconfig/conf.avail
%dir %{_datadir}/fonts
%{_datadir}/xml/fontconfig/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf
%doc %{_sysconfdir}/fonts/conf.d/README
%{_datadir}/fontconfig/conf.avail/*.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig


%files devel
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig

