%define date 20091001

Summary:	An open source first-person shooter
Name:		nexuiz
Version:	2.5.2
Release:	%mkrel 3
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
BuildRequires:	libjpeg-devel
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
%setup_compile_flags
%serverbuild

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
%make -j1 release CPUOPTIMIZATIONS="%{optflags}" UNIX_X11LIBPATH=%{_libdir} DP_FS_BASEDIR=%{_gamesdatadir}/%{name} LDFLAGS_UNIXCOMMON="%{ldflags} -lm" DP_LINK_TO_LIBJPEG="1"

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


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-3mdv2011.0
+ Revision: 613042
- the mass rebuild of 2010.1 packages

* Sat Jun 05 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.2-2mdv2010.1
+ Revision: 547133
- link against symstem libjpeg
- export %%serverbuild and %%setup_compile_flags macros

* Sun Nov 15 2009 Funda Wang <fwang@mandriva.org> 2.5.2-1mdv2010.1
+ Revision: 466288
- New version 2.5.2

* Sun Jul 19 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.1-1mdv2010.0
+ Revision: 397782
- build with %%ldflags
- update to new version 2.5.1

* Fri May 15 2009 Samuel Verschelde <stormi@mandriva.org> 2.5-2mdv2010.0
+ Revision: 376217
- change Group to Arcade like the other FPS and like it's desktop file

* Fri May 01 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5-1mdv2010.0
+ Revision: 369300
- update to new version 2.5

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 2.4.2-4mdv2009.0
+ Revision: 268266
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu May 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.2-3mdv2009.0
+ Revision: 207684
- disable -mmmx

* Wed May 14 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.2-2mdv2009.0
+ Revision: 207210
- enable mmx support

* Tue May 13 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.2-1mdv2009.0
+ Revision: 206528
- new version

* Sat May 03 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4-3mdv2009.0
+ Revision: 200541
- fix the wrapper script one more time

* Fri May 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4-2mdv2009.0
+ Revision: 200500
- fix wrapper script

* Fri May 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4-1mdv2009.0
+ Revision: 199946
- add few missing buildrequires
- extract only needed files from the upstream all-in-one zip file
- license is GPLv2+
- add docs
- new version
- drop patch0
- fix compilation
- drop useless hacks
- spec file clean
- drop X-MandrivaLinux from desktop files

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.3-1mdv2008.1
+ Revision: 148291
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Jun 02 2007 Eskild Hustvedt <eskild@mandriva.org> 2.3-1mdv2008.0
+ Revision: 34431
- New version 2.3
- Now uses exec to start the game


* Thu Feb 08 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.2.3-2mdv2007.0
+ Revision: 118044
- bump release in order to force upload

  + Eskild Hustvedt <eskild@mandriva.org>
    - New version 2.2.3 (security fixes)

* Thu Dec 14 2006 Eskild Hustvedt <eskild@mandriva.org> 2.2.1-1mdv2007.1
+ Revision: 97147
- Added notice about glx client instability
- New version 2.2.1

* Sat Dec 02 2006 Olivier Blin <oblin@mandriva.com> 2.1-2mdv2007.1
+ Revision: 90094
- buildrequire libxxf86dga-devel
- buildrequire GL-devel
- fix XDG menu
- Import nexuiz

* Thu Sep 14 2006 Eskild Hustvedt <eskild@mandriva.org> 2.1-1mdv
- New version 2.1
- XDG menu

* Fri Jun 16 2006 Eskild Hustvedt <eskild@mandriva.org> 2.0-1mdv
- New version 2.0

* Thu Feb 16 2006 Eskild Hustvedt <eskild@mandriva.org> 1.5-1mdk
- New version 1.5

* Wed Nov 02 2005 Eskild Hustvedt <eskild@mandriva.org> 1.2.1-4mdk
- Minor fixes to the menu entries *sigh*

* Wed Nov 02 2005 Eskild Hustvedt <eskild@mandriva.org> 1.2.1-3mdk
- Really really fixed the launch script (I hope)

* Tue Nov 01 2005 Eskild Hustvedt <eskild@mandriva.org> 1.2.1-2mdk
- Fixed the launchscript (bah)

* Sun Oct 30 2005 Eskild Hustvedt <eskild@mandriva.org> 1.2.1-1mdk
- Now defaults to 800x600 instead of 1024x768
- New version 1.2.1

* Wed Aug 31 2005 Couriousous <couriousous@mandriva.org> 1.2-2mdk
- Disable fortify ( ie won't build if enabled )
- Fix Geforce FX detection

* Wed Aug 31 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2-1mdk
- 1.2

* Tue Jul 12 2005 Eskild Hustvedt <eskild@mandriva.org> 1.1-2mdk
- Added a hack for GeForce FX cards in the startup script(s)

* Wed Jul 06 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.1-1mdk
- 1.1
- split out data package
- compile with optimizations
- fix requires & provides
- added dedicated server

* Fri Jun 10 2005 Eskild Hustvedt <eskild@mandrake.org> 1.0-1mdk
- Initial Mandriva Linux package
- Patch0: fix compile (thanks Michael Scherer)

