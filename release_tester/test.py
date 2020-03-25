import sys
import installers.installer as installer
import installers.arangosh as arangosh
import installers.log as loglog
log = loglog.log

# python test.py 3.6.2 enterprise c:/Users/willi/Downloads

# python3 test.py 3.6.2 enterprise /home/willi/Downloads

if len(sys.argv) != 4:
    print("usage: version enterprise|community packageDir ")
print(sys.argv)

(selffile, version, enterprise, packagedir) = sys.argv
if enterprise == 'enterprise':
    enterprise = True
else:
    enterprise = False

jsVersionCheck = (
    "if (db._version()!='%s') { throw 'fail'}" % (version),
    'check version')

myInstaller = installer.get(version, enterprise, packagedir)

myInstaller.calculatePackageNames()
myInstaller.installPackage()
myInstaller.stopService()
myInstaller.broadcastBind()
myInstaller.startService()
myInstaller.checkInstalledPaths()
myInstaller.checkEngineFile()

systemInstallArangosh = arangosh.arangoshExecutor(myInstaller.cfg)

if not systemInstallArangosh.runCommand(jsVersionCheck):
    log("Version Check failed!")
input("Press Enter to continue")

myInstaller.unInstallPackage()

myInstaller.checkUninstallCleanup()
