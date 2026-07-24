#!/bin/bash

cd U-Fanctl/ || exit 1

# 从 pyproject.toml 提取版本号
VERSION=$(grep -Po '^version = "\K[^"]+' pyproject.toml)
if [ -z "$VERSION" ]; then
    echo "Error: unable to extract version from pyproject.toml"
    exit 1
fi
echo "Current version: $VERSION"

# 更新 manifest 文件
MANIFEST="../Fpk/manifest"
if [ -f "$MANIFEST" ]; then
    sed -i "s/^version\s*=\s*.*/version               = $VERSION/" "$MANIFEST"
    echo "Manifest version updated to $VERSION"
else
    echo "Warning: manifest file not found ($MANIFEST)"
fi

rm -rf dist/
uv run pyinstaller --add-data "./pyproject.toml:." -n "u-fanctl" main.py
cp -r wwwroot/ dist/u-fanctl/
cd ..
rm -rf Fpk/app/server/
cp -r U-Fanctl/dist/u-fanctl/ Fpk/app/server/
cd Fpk/
rm -rf *.fpk
fnpack build
mv u-fanctl.fpk u-fanctl_$VERSION.fpk
echo "🎉Build complete🎉"
