# RPM Spec for DeadCI

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/deadci`
* Config: `/etc/deadci/`
* Sysconfig: `/etc/sysconfig/deadci`

# Build (automated)

* Ensure that `rpmdevtools` and `mock` are available:

    ```
    sudo yum install rpmdevtools mock
    ```

* Run `autobuild.sh`:

    ```
    cd ${repo}/
    chmod u+x autobuild.sh
    ./autobuild.sh
    ```

# Build (manual)

To build the RPM (non-root user):

1. Check out this repo
2. Install rpmdevtools and mock 

    ```
    sudo yum install rpmdevtools mock
    ```
3. Set up your rpmbuild directory tree

    ```
    rpmdev-setuptree
    ```
4. Link the spec file and sources from the repository into your rpmbuild/SOURCES directory

    ```
    ln -s ${repo}/SPECS/deadci.spec rpmbuild/SPECS/
    ln -s ${repo}/SOURCES/* rpmbuild/SOURCES/
    ```
5. Download remote source files

    ```
    spectool -g -R rpmbuild/SPECS/deadci.spec
    ```
6. Build the RPM

    ```
    rpmbuild -ba rpmbuild/SPECS/deadci.spec
    ```

# Run

1. Install the rpm
2. Put config files in `/etc/deadci/`
3. Change command line arguments to deadci in `/etc/sysconfig/deadci`. 
4. Start the service and tail the logs `systemctl start deadci.service` and `journalctl -f`
  * To enable at reboot `systemctl enable deadci.service`

# More info

See the [deadci.com](https://deadci.com) website.
