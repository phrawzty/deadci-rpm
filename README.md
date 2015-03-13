# RPM Spec for DeadCI

I tried to follow the Fedora [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines);
however, DeadCI expects the config file to be in the working directory, which
means that `/etc/deadci/` is not sufficiently accessible once permissions have
been dropped to the `deadci` user. In short, config is in `/var/lib/deadci/`
whether we like it or not.

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

* Check out this repo. Nice, no?
* Install `rpmdevtools` and `mock`. 
    ```
    sudo yum install rpmdevtools mock
    ```

* Set up your rpmbuild directory tree.
    ```
    rpmdev-setuptree
    ```

* Link the spec file and sources.
    ```
    ln -s $HOME/consul-rpm/SPECS/consul.spec rpmbuild/SPECS/
    find $HOME/consul-rpm/SOURCES -type f -exec ln -s {} rpmbuild/SOURCES/ \;
    ```

* Download remote source files.
    ```
    spectool -g -R rpmbuild/SPECS/deadci.spec
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/deadci.spec
    ```

# Run

* Install the rpm.
* Modify `/var/lib/deadci/deadci.ini` as necessary.
* Start the service and tail the logs `systemctl start deadci.service` and `journalctl -f`
  * To enable at reboot `systemctl enable deadci.service`

# More info

See the [deadci.com](https://deadci.com) website.
