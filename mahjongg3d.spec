%define	name		mahjongg3d
%define	version	0.96
%define	release	1mdk

Summary:	MahJongg 3D Solitaire
Name:	%{name}
Version:	%{version}
Release:	%{release}
BuildRequires:	qt3-devel
Source:	http://www.reto-schoelly.de/mahjongg3d/%{name}-%{version}.tar.bz2
Source10:	http://www.reto-schoelly.de/mahjongg3d/hieroglyph_tileset.tar.bz2
Source11:	http://www.reto-schoelly.de/mahjongg3d/lab_layout.tar.bz2
Source20: 	%{name}-16.png
Source21: 	%{name}-32.png
Source22: 	%{name}-48.png
Group:	Games/Boards
License:	GPL
URL:		http://www.reto-schoelly.de/mahjongg3d/
BuildRoot:	%_tmppath/%{name}-build

%description
MahJongg 3D Solitaire

%prep

%setup -n mahjongg3d.release
pushd bin
tar xvjf %{SOURCE10}
tar xvjf %{SOURCE11}
popd

%build

qmake
cat > src/gamedata_path.h <<EOF
#define GAMEDATA_BASE_PATH "/usr/share/games/mahjongg3d"
EOF

%make PREFIX=/usr GAMEDATA_PREFIX=/usr/share/games

%install
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
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): needs="x11" \
 section="More Applications/Games/Boards" \
 title="%{summary}" \
 longtitle="%{summary} - A board game using OpenGL, with several themes" \
 command="%{_gamesbindir}/%{name}" \
 icon="%{name}.png"
EOF

%files
%defattr(-,root,root)
%doc Changelog COPYING INSTALL_CUSTOM README
%attr(0755,root,games) %{_gamesbindir}/%{name}
%{_mandir}/man6/%{name}.6*
%{_gamesdatadir}/%{name}
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}
