#!/bin/bash

cd src/ || exit 1

# 从 pyproject.toml 提取版本号
VERSION=$(grep -Po '^version = "\K[^"]+' pyproject.toml)
if [ -z "$VERSION" ]; then
    echo "Error: unable to extract version from pyproject.toml"
    exit 1
fi
echo "Current version: $VERSION"

# 更新 manifest 文件
MANIFEST="../fnos-package/manifest"
if [ -f "$MANIFEST" ]; then
    sed -i "s/^version\s*=\s*.*/version               = $VERSION/" "$MANIFEST"
    echo "Manifest version updated to $VERSION"
else
    echo "Warning: manifest file not found ($MANIFEST)"
fi

# 构建前端代码
read -r -p "是否构建前端代码? [Y/n] " BUILD_WEBUI
if [ -z "$BUILD_WEBUI" ] || [[ "$BUILD_WEBUI" =~ ^[Yy]$ ]]; then
    echo "Building webui..."
    (cd ../webui && npm run build) || exit 1
else
    echo "Skipped webui build"
fi

rm -rf dist/
uv run pyinstaller --add-data "./pyproject.toml:." -n "u-fanctl" main.py
cp -r wwwroot/ dist/u-fanctl/
cd ..
rm -rf fnos-package/app/server/
cp -r src/dist/u-fanctl/ fnos-package/app/server/
cd fnos-package/
rm -rf *.fpk
fnpack build || exit 1
mv u-fanctl.fpk u-fanctl_$VERSION.fpk
echo "🎉Build complete🎉"
