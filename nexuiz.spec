%define date 20091001

Summary:	An open source first-person shooter
Name:		nexuiz
Version:	2.5.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Games/Arcade
URL:		http://www.nexuiz.com/
# (tpg) original source is here http://downloads.sourceforge.net/nexuiz/
# extract only needed files
# unzip -j nexuiz-25.zip Nexuiz/sources/enginesource%{date}.zip
Source0:	enginesource%{date}.zip
BuildRequires:	SDL-devel
BuildRequires:	GL-devel
BuildRequires:	libxxf86dga-devel
BuildRequires:	libxext-devel
BuildRequires:	libxpm-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	libalsa-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

WARNING: This game contains violence that is not suitable for children.

%package glx
Summary:	GLX client for the open source first-person shooter Nexuiz
Group:		Games/Arcade
Provides:	nexuiz = %{version}-%{release}
Requires:	nexuiz-data = %{version}

%description glx
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This package contains the glx client.
It is known to be unstable on some systems, if you experience problems
please try the nexuiz-sdl package instead.

WARNING: This game contains violence that is not suitable for children.

%package sdl
Summary:	SDL client for the open source first-person shooter Nexuiz
Group:		Games/Arcade
Provides:	nexuiz = %{version}-%{release}
Requires:	nexuiz-data = %{version}

%description sdl
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This package contains the SDL client.

WARNING: This game contains violence that is not suitable for children.

%package dedicated
Summary:	Dedicated server for Nexuiz
Group:		Games/Arcade
Requires:	nexuiz-data = %{version}

%description dedicated
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This packages contains the dedicated server.

WARNING: This game contains violence that is not suitable for children.

%prep
%setup -q -n darkplaces
sed -i 's/\r//' darkplaces.txt
sed -i 's,/usr/X11R6/,/usr/,g' makefile makefile.inc

%build

# Create main launch script
VARIANTS="sdl glx"
for TYPE in $VARIANTS; do
cat << LAUNCH_END > ./nexuiz-${TYPE}_launch
#!/bin/bash
# Mandriva launch script copyright (C) Eskild Hustvedt 2005, 2006
# Licensed under the GNU General Public License
cd %{_gamesdatadir}/nexuiz/
# Check if the user is running a GeForce FX card and doesn't already have a config file
if [ ! -e \$HOME/.nexuiz/ ]; then
	mkdir -p \$HOME/.nexuiz/data
        if [ "\`lspcidrake | grep -i nvidia | grep -i geforce | grep FX\`" = "" ]; then
                # Don't use GLSL
                echo 'r_glsl "0"' > \$HOME/.nexuiz/data/autoexec.cfg
        fi
# Set default video settings
cat << EOF > \$HOME/.nexuiz/data/config.cfg
vid_fullscreen "1"
vid_height "600"
vid_width "800"
EOF
fi
exec %{_gamesbindir}/nexuiz-${TYPE}.real "\$@"
LAUNCH_END
done

# Create the server launch script
cat << EOF > ./nexuiz-dedicated_launch
#!/bin/bash
cd %{_gamesdatadir}/nexuiz/
exec %{_gamesbindir}/nexuiz-dedicated.real "\$@"
EOF

# (tpg) build with mdv ldflags
sed -i -e 's@LDFLAGS_UNIXCOMMON=@LDFLAGS_UNIXCOMMON+=@g' makefile.inc

# Building breaks when using multiple jobs, so force one.
%make -j1 release CPUOPTIMIZATIONS="%{optflags}" UNIX_X11LIBPATH=%{_libdir} DP_FS_BASEDIR=%{_gamesdatadir}/%{name} LDFLAGS_UNIXCOMMON="%{ldflags} -lm"

%install
rm -rf %{buildroot}
install -m755 darkplaces-glx -D %{buildroot}%{_gamesbindir}/nexuiz-glx.real
install -m755 darkplaces-sdl -D %{buildroot}%{_gamesbindir}/nexuiz-sdl.real
install -m755 darkplaces-dedicated -D %{buildroot}%{_gamesbindir}/nexuiz-dedicated.real

install -m755 nexuiz-glx_launch -D %{buildroot}%{_gamesbindir}/nexuiz-glx
install -m755 nexuiz-sdl_launch -D %{buildroot}%{_gamesbindir}/nexuiz-sdl
install -m755 nexuiz-dedicated_launch -D %{buildroot}%{_gamesbindir}/nexuiz-dedicated

mkdir -p %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}-glx.desktop
[Desktop Entry]
Name=Nexuiz (glx client)
StartupNotify=true
Terminal=false
Type=Application
Icon=%{name}
Exec=%{_gamesbindir}/%{name}-glx
Categories=Game;ArcadeGame;
EOF
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}-sdl.desktop
[Desktop Entry]
Name=Nexuiz (sdl client)
StartupNotify=true
Terminal=false
Type=Application
Icon=%{name}
Exec=%{_gamesbindir}/%{name}-sdl
Categories=Game;ArcadeGame;
EOF

%if %mdkversion < 200900
%post glx
%{update_menus}
%endif

%if %mdkversion < 200900
%post sdl
%{update_menus}
%endif

%if %mdkversion < 200900
%postun glx 
%{clean_menus}
%endif

%if %mdkversion < 200900
%postun sdl
%{clean_menus}
%endif

%clean 
rm -rf %{buildroot} 

%files glx
%defattr(-,root,root)
%doc darkplaces.txt
%{_gamesbindir}/nexuiz-glx
%{_gamesbindir}/nexuiz-glx.real
%{_datadir}/applications/%{name}-glx.desktop

%files sdl
%doc darkplaces.txt
%defattr(-,root,root)
%{_gamesbindir}/nexuiz-sdl
%{_gamesbindir}/nexuiz-sdl.real
%{_datadir}/applications/%{name}-sdl.desktop

%files dedicated
%defattr(-,root,root)
%doc darkplaces.txt
%{_gamesbindir}/nexuiz-dedicated
%{_gamesbindir}/nexuiz-dedicated.real
