#! /bin/bash
set -eo pipefail

rm -rf build
mkdir -p build
cp build-aux/py.spec build/py.spec
cp build-aux/inno.iss build/inno.iss

cd build

pacman -Sy --noconfirm --needed \
    mingw-w64-x86_64-meson \
    mingw-w64-x86_64-gtk3 \
    mingw-w64-x86_64-python3-gobject \
    mingw-w64-x86_64-gtk-update-icon-cache \
    mingw-w64-x86_64-desktop-file-utils \
    tar \
    mingw-w64-x86_64-python-pip \
    mingw-w64-x86_64-innoextract
wget -O inno.exe https://jrsoftware.org/download.php/is.exe
innoextract -m inno.exe
pip install pyinstaller CurrencyConverter

meson .. ../build
meson install

wget -O fluent-icon.tar.xz \
    https://github.com/vinceliuice/Fluent-icon-theme/raw/3d0eadd0da82893c763284137179b2c31716863b/release/Fluent.tar.xz

set +e
/bin/tar -xf fluent-icon.tar.xz \
    'Fluent/symbolic/actions' 'Fluent/symbolic/mimetypes' \
    'Fluent/symbolic/status/process-working-symbolic.svg' \
    'Fluent/icon-theme.cache' 'Fluent/index.theme' \
    'Fluent/scalable/apps/appointment-soon.svg'
set -e

mv 'Fluent' 'fluent-icon'
rm -rf /mingw64/share/icons/Fluent
mkdir -p /mingw64/share/icons/Fluent
cp -rf fluent-icon/* /mingw64/share/icons/Fluent

wget -O fluent-theme.tar.xz \
    https://github.com/vinceliuice/Fluent-gtk-theme/raw/f929b7e2c8e4e18b3e23af90bae8a1a345beaafb/release/Fluent.tar.xz

set +e
/bin/tar -xf fluent-theme.tar.xz 'Fluent-light-compact'
set -e

mv 'Fluent-light-compact' 'fluent-theme'
rm -rf /mingw64/share/themes/Fluent
mkdir -p /mingw64/share/themes/Fluent
cp -rf fluent-theme/* /mingw64/share/themes/Fluent

mkdir -p /mingw64/etc/gtk-3.0
echo -e "[Settings]\ngtk-theme-name=Fluent\ngtk-icon-theme-name=Fluent" > /mingw64/etc/gtk-3.0/settings.ini
glib-compile-schemas /mingw64/share/glib-2.0/schemas

pyinstaller py.spec --clean
./app/iscc inno.iss
