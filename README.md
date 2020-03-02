# mip-deployment

This is the MIP6 ready **local** deployment script.

* Once you get it, you may move the script to use it later the easy way
```bash
mv mip-deployment/local_deployment.sh /usr/local/bin/mip
```
* Then, you may change the install path in the script, to /opt (it's $(pwd) by default, which means that the setup is done in the directory where you are when you call the command. Changing it to /opt may be a better idea then). As the script is now supposed to be in */usr/local/bin* and be named *mip*, you may call this command:
```bash
sed --in-place 's/^INSTALL_PATH.*/INSTALL_PATH="\/opt"/' /usr/local/bin/mip
```
* Then, just call *mip* with its option to auto-do the setup, start, stop, status, whatever required
```bash
mip check-required
```
```bash
mip install
```
```bash
mip status
```
* If you have issues, sometimes, doing it may save you
```bash
mip restart
```
* Or even, in case of real problems
```bash
mip stop --force
mip start
```
