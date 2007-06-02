%define	name	nexuiz
%define	version 2.3
%define rel	1
%define	release	%mkrel %{rel}

Name:		%{name} 
Summary:	An open source first-person shooter
Version:	%{version} 
Release:	%{release} 
Source0:	%{name}-%{version}.tar.bz2
# Fixes compiling
Patch0:		nexuiz-1.0-compile.patch
URL:		http://www.nexuiz.com/
Group:		Games/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	SDL-devel GL-devel libxxf86dga-devel

%description
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

WARNING: This game contains violence that is not suitable for children.

%package	glx
Group:		Games/Other
Summary:	GLX client for the open source first-person shooter Nexuiz
Provides:	nexuiz = %{version}-%{release}
Requires:	nexuiz-data = %{version}

%description	glx
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This package contains the glx client.
It is known to be unstable on some systems, if you experience problems
please try the nexuiz-sdl package instead.

WARNING: This game contains violence that is not suitable for children.

%package	sdl
Group:		Games/Other
Summary:	SDL client for the open source first-person shooter Nexuiz
Provides:	nexuiz = %{version}-%{release}
Requires:	nexuiz-data = %{version}

%description	sdl
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This package contains the SDL client.

WARNING: This game contains violence that is not suitable for children.

%package	dedicated
Group:		Games/Other
Summary:	Dedicated server for Nexuiz
Requires:	nexuiz-data = %{version}

%description	dedicated
Nexuiz is a multiplayer 3D first-person shooter based upon a
heavily modified Quake 1 engine.

This packages contains the dedicated server.

WARNING: This game contains violence that is not suitable for children.

%prep
%setup -q
%patch0 -p0

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
        if [ "\`lspcidrake|grep -i nvidia|grep -i geforce |grep FX\`" != "" ]; then
                # Don't use GLSL
                echo 'r_shadow_glsl 0' > \$HOME/.nexuiz/data/autoexec.cfg
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

%(echo %make|perl -pe 's/-j\d+/-j1/g') CPUOPTIMIZATIONS="%(echo %optflags|sed s/-Wp,-D_FORTIFY_SOURCE=2//)" release

%install
rm -rf $RPM_BUILD_ROOT
install -m755 darkplaces-glx -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-glx.real
install -m755 darkplaces-sdl -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-sdl.real
install -m755 darkplaces-dedicated -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-dedicated.real
install -m755 nexuiz-glx_launch -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-glx
install -m755 nexuiz-sdl_launch -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-sdl
install -m755 nexuiz-dedicated_launch -D $RPM_BUILD_ROOT%{_gamesbindir}/nexuiz-dedicated

mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}-sdl
?package(%{name}-sdl):command="%{_gamesbindir}/nexuiz-sdl"\
 icon="%{name}.png" needs="X11" section="More Applications/Games/Other"\
 title="Nexuiz (sdl client)" longtitle="A 3D first person shooter" xdg="true"
EOF
cat << EOF > %{buildroot}%{_menudir}/%{name}-glx
?package(%{name}-glx):command="%{_gamesbindir}/nexuiz-glx"\
 icon="%{name}.png" needs="X11" section="More Applications/Games/Other"\
 title="Nexuiz (glx client)" longtitle="A 3D first person shooter" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat << EOF > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-glx.desktop
[Desktop Entry]
Name=Nexuiz (glx client)
StartupNotify=true
Terminal=false
Type=Application
Icon=%{name}
Exec=%{_gamesbindir}/%{name}-glx
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF
cat << EOF > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-sdl.desktop
[Desktop Entry]
Name=Nexuiz (sdl client)
StartupNotify=true
Terminal=false
Type=Application
Icon=%{name}
Exec=%{_gamesbindir}/%{name}-sdl
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

%post glx
%{update_menus}
%post sdl
%{update_menus}

%postun glx 
%{clean_menus}
%postun sdl
%{clean_menus}

%clean 
rm -rf $RPM_BUILD_ROOT 

%files glx
%defattr(-,root,root)
%{_gamesbindir}/nexuiz-glx
%{_gamesbindir}/nexuiz-glx.real
%{_menudir}/%{name}-glx
%{_datadir}/applications/%{name}-glx.desktop

%files sdl
%defattr(-,root,root)
%{_gamesbindir}/nexuiz-sdl
%{_gamesbindir}/nexuiz-sdl.real
%{_menudir}/%{name}-sdl
%{_datadir}/applications/%{name}-sdl.desktop

%files dedicated
%defattr(-,root,root)
%{_gamesbindir}/nexuiz-dedicated
%{_gamesbindir}/nexuiz-dedicated.real
