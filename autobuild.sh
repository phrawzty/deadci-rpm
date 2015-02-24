#!/usr/bin/env bash
# This script automatically builds copies over the systemd unit files, spec files and builds the rpm.

RPM_BUILD_DIR="$HOME/rpmbuild"

if [ ! -d "RPM_BUILD_DIR" ]; then
    echo "$HOME/rpmbuild doesn't exist, creating"
    mkdir -p $HOME/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp ./SPECS/deadci.spec $HOME/rpmbuild/SPECS/
    cp ./SOURCES/deadci.* $HOME/rpmbuild/SOURCES/
fi

# Upstream doesn't use versioning (grr), so get the epoch stamp for the most
# recent build. There's no guarantee that the released archive matches up
# with the last commit, but this is the best we've got.
commit_date=`curl -s https://api.github.com/repos/phayes/deadci/commits?per_page=1 | grep -m 1 date | cut -d '"' -f 4`
export EPOCH=`date --date="${commit_date}" +%s`

spectool -g -R $HOME/rpmbuild/SPECS/deadci.spec
rpmbuild -ba $HOME/rpmbuild/SPECS/deadci.spec
