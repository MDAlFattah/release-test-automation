PYTHON='python3'

switch (TARGET) {
    case 'windows': 
        PYTHON='python'
        TARGET_HOST='bruecktendo'
        SUDO=''
        break

    case 'linux_deb':
        TARGET_HOST='willi-test-release'
        SUDO='sudo'
        break
    case 'linux_rpm': // TODO
        SUDO='sudo'
        break
    case 'macos':// TODO
        break
}

PACKAGE_DIR = '/home/jenkins/Downloads/'

ENTERPRISE_PARAM = '--no-enterprise'
if (params['ENTERPRISE']) {
    ENTERPRISE_PARAM = '--enterprise'
}

FORCE_PARAM_OLD = ''
if (params['FORCE_OLD']) {
    FORCE_PARAM_OLD = '--force'
}

FORCE_PARAM_NEW = ''
if (params['FORCE_NEW']) {
    FORCE_PARAM_NEW = '--force'
}

ZIP = ''
if (params['ZIP']) {
    ZIP = '--zip'
}

node(TARGET_HOST)  {

    checkout([$class: 'GitSCM',
              branches: [[name: "master"]],
              /*
         doGenerateSubmoduleConfigurations: false,
         extensions: [[$class: 'SubmoduleOption',
         disableSubmodules: false,
         parentCredentials: false,
         recursiveSubmodules: true,
         reference: '',
         trackingSubmodules: false]],
         submoduleCfg: [],
         */
              extensions: [
            [$class: 'CheckoutOption', timeout: 20],
            [$class: 'CloneOption', timeout: 20]
        ],
              userRemoteConfigs:
              [[url: 'https://github.com/arangodb/release-test-automation.git']]])

    sh 'pwd'
    
    if (params['VERSION_OLD'] != "") {
        ACQUIRE_COMMAND = """
${PYTHON} release_tester/acquire_packages.py ${ENTERPRISE_PARAM} --enterprise-magic ${params['ENTERPRISE_KEY']} --package-dir ${PACKAGE_DIR} ${FORCE_PARAM_OLD} --source ${params['PACKAGE_SOURCE_OLD']} --version '${params['VERSION_OLD']}' --httpuser dothebart --httppassvoid '${params['HTTP_PASSVOID']}' ${ZIP}
"""
        print("downloading old package(s) using:")
        print(ACQUIRE_COMMAND)
        sh ACQUIRE_COMMAND
    }
    ACQUIRE_COMMAND = """
${PYTHON} release_tester/acquire_packages.py ${ENTERPRISE_PARAM} --enterprise-magic ${params['ENTERPRISE_KEY']} --package-dir ${PACKAGE_DIR} ${FORCE_PARAM_NEW} --source ${params['PACKAGE_SOURCE_NEW']} --version '${params['VERSION_NEW']}' --httpuser dothebart --httppassvoid '${params['HTTP_PASSVOID']}' ${ZIP}
"""
    print("downloading new package(s) using:")
    print(ACQUIRE_COMMAND)
    sh ACQUIRE_COMMAND

    if File('/tpm/config.yml').exists() {
        print("cleaning up the system (if):")
        CLEANUP_COMMAND = """
${SUDO} ${PYTHON} release_tester/cleanup.py ${ZIP}
"""
        print(CLEANUP_COMMAND)
        sh CLEANUP_COMMAND
    } else {
        print("no old install detected; not cleaning up")
    }

    if (params['VERSION_OLD'] != "") {
        print("Running upgrade test")
        UPGRADE_COMMAND = """
${SUDO} ${PYTHON} release_tester/upgrade.py ${ENTERPRISE_PARAM} --old-version ${params['VERSION_OLD']} --version ${params['VERSION_NEW']} --package-dir ${PACKAGE_DIR} --publicip 192.168.173.88 ${ZIP} --no-interactive
"""
        print(UPGRADE_COMMAND)
        sh UPGRADE_COMMAND

    } else {
        print("Running plain install test")
        TEST_COMMAND = """
${SUDO} ${PYTHON} release_tester/test.py ${ENTERPRISE_PARAM} --version ${params['VERSION_NEW']} --package-dir ${PACKAGE_DIR} --publicip 192.168.173.88 ${ZIP} --no-interactive
"""
        print(TEST_COMMAND)
        sh TEST_COMMAND

    }
}
