# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.23
# 
# >> macros
%global freetype_version 2.1.4
# << macros

Name:       fontconfig
Summary:    Font configuration and customization library
Version:    2.8.0
Release:    1
Group:      System/Libraries
License:    MIT
URL:        http://fontconfig.org
Source0:    http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Source1:    25-no-bitmap-fedora.conf
Source2:    10-antialias.conf
Source3:    10-hinted.conf
Source100:  fontconfig.yaml
Requires(post): freetype >= %{freetype_version}
Requires(post): coreutils
Requires(post): /bin/grep
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  gawk
BuildRequires:  expat-devel
BuildRequires:  perl
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

# >> setup
# << setup

%build
# >> build pre
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no
# << build pre

%configure --disable-static \
    --with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts

make %{?jobs:-j%jobs}

# >> build post
make check
# << build post
%install
rm -rf %{buildroot}
# >> install pre

# << install pre
%make_install

# >> install post
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.avail
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.avail
ln -s ../conf.avail/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s ../conf.avail/10-autohint.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s ../conf.avail/10-antialias.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s ../conf.avail/10-hinted.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# move installed doc files back to build directory to package themm
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
# << install post



%post
/sbin/ldconfig
# >> post
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
# << post

%postun -p /sbin/ldconfig





%files
%defattr(-,root,root,-)
# >> files
%defattr(-, root, root)
%doc README AUTHORS COPYING
%doc fontconfig-user.txt fontconfig-user.html
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-query
%{_bindir}/fc-scan
%dir %{_sysconfdir}/fonts/conf.avail
%dir %{_datadir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf
%doc %{_sysconfdir}/fonts/conf.d/README
%config %{_sysconfdir}/fonts/conf.avail/*.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
# << files


%files devel
%defattr(-,root,root,-)
# >> files devel
%defattr(-, root, root)
%doc fontconfig-devel.txt fontconfig-devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*
# << files devel

