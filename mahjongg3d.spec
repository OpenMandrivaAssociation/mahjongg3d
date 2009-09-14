Name:			mahjongg3d
Version:		0.96
Release:		%mkrel 7

Summary:	MahJongg 3D Solitaire
License:        GPLv2+
Group:		Games/Boards
URL:            http://www.reto-schoelly.de/mahjongg3d/
Source:		http://www.reto-schoelly.de/mahjongg3d/%{name}-%{version}.tar.bz2
Source1:	http://www.reto-schoelly.de/mahjongg3d/%{name}-0.96-patch2.tar.bz2
Source10:	http://www.reto-schoelly.de/mahjongg3d/hieroglyph_tileset.tar.bz2
Source11:	http://www.reto-schoelly.de/mahjongg3d/lab_layout.tar.bz2
Source20:	%{name}-16.png
Source21:	%{name}-32.png
Source22:	%{name}-48.png
Patch:		mahjongg3d-0.96-mdv-64bit-fix.patch

BuildRequires:	qt3-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
MahJongg Solitaire 3D is an OpenGL enhanced solitaire version of the ancient
chinese board game "Mah Jongg".

%prep
%setup -q -n mahjongg3d.release -a 1
%patch -p1 -b .build+x64-fix

pushd bin
tar xvjf %{SOURCE10}
tar xvjf %{SOURCE11}
popd

cp -fr patch2/* .
rm -fr patch2
sed -i -e 's/openglwidget.h/OpenGLWidget.h/' src/MainDialogBase.ui

%build
export QTDIR=%{qt3dir}
%{qt3dir}/bin/qmake
%{qt3dir}/bin/qmake src/src.pro -o src/Makefile
cat > src/gamedata_path.h <<EOF
#define GAMEDATA_BASE_PATH "/usr/share/games/mahjongg3d"
EOF

%make PREFIX=%{_prefix} GAMEDATA_PREFIX=%_gamesdatadir

%install
rm -rf %buildroot
install -d %buildroot%{_gamesdatadir}/%{name}/backgrounds
install -d %buildroot%{_gamesdatadir}/%{name}/gra
install -d %buildroot%{_gamesdatadir}/%{name}/layouts
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets/default
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets/flowers
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets/hiero
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets/runes
install -d %buildroot%{_gamesdatadir}/%{name}/tilesets/traditional

install -d %buildroot%{_gamesbindir}
install -d %buildroot%{_mandir}/man6
install -m 0755 bin/%{name} %buildroot%{_gamesbindir}/
install -m 0644 bin/backgrounds/* %buildroot%{_gamesdatadir}/%{name}/backgrounds/
install -m 0644 bin/gra/* %buildroot%{_gamesdatadir}/%{name}/gra/
install -m 0644 bin/layouts/* %buildroot%{_gamesdatadir}/%{name}/layouts/
install -m 0644 bin/tilesets/*.tileset %buildroot%{_gamesdatadir}/%{name}/tilesets/
install -m 0644 bin/tilesets/default/* %buildroot%{_gamesdatadir}/%{name}/tilesets/default/
install -m 0644 bin/tilesets/flowers/* %buildroot%{_gamesdatadir}/%{name}/tilesets/flowers/
install -m 0644 bin/tilesets/hiero/* %buildroot%{_gamesdatadir}/%{name}/tilesets/hiero/
install -m 0644 bin/tilesets/runes/* %buildroot%{_gamesdatadir}/%{name}/tilesets/runes/
install -m 0644 bin/tilesets/traditional/* %buildroot%{_gamesdatadir}/%{name}/tilesets/traditional/
install -m 0644 %{name}.6 %buildroot%{_mandir}/man6/

install -m 644 -D %{SOURCE20} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m 644 -D %{SOURCE21} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m 644 -D %{SOURCE22} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=MahJongg 3D Solitaire
Comment=MahJongg 3D Solitaire - A board game using OpenGL, with several themes
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Boards;Game;BoardGame;Qt;
EOF

%files
%defattr(-,root,root)
%doc Changelog COPYING INSTALL_CUSTOM README
%attr(0755,root,games) %{_gamesbindir}/%{name}
%{_mandir}/man6/%{name}.6*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/*.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post
%{update_menus}

%postun
%{clean_menus}
%endif
