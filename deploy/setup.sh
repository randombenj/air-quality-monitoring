#!/bin/sh
# setup script for the 'air quality monitoring' raspi
# ------------------------------------

# prepare workdir
WORKDIR=$(mktemp -d)
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "Creating deployment"

CURDIR=$(pwd)
cd $WORKDIR

# download and extract the image
wget https://downloads.raspberrypi.org/raspios_lite_armhf_latest --trust-server-names --timestamping --quiet --output-document raspios-lite.zip
unzip raspios-lite.zip
mv *.img raspios-lite.img

# create requirements.txt for the imstallation
type poetry >/dev/null 2>&1 || { echo >&2 "Please install poetry: https://python-poetry.org/docs/#installation"; exit 1; }

cd $SCRIPT_DIR/../qualitair/
poetry export --without-hashes -f requirements.txt --output requirements.txt
cd -

# configure the image
sudo $SCRIPT_DIR/lib/prepare.sh raspios-lite.img $SCRIPT_DIR/lib/setup.sh
sudo $SCRIPT_DIR/lib/chroot.sh raspios-lite.img
sudo $SCRIPT_DIR/lib/grow.sh raspios-lite.img

cd $CURDIR
mv $WORKDIR/raspios-lite.img .

echo "Done! To flash the deployment run:"
echo "  sudo dd if=raspios-lite.img of=/dev/YOUR_DISK"

