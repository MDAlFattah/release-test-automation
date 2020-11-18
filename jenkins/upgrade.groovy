PYTHON='python3'
PACKAGE_DIR = '/home/jenkins/Downloads/'
WINDOWS = false

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

VERBOSE=''
if (params['VERBOSE']) {
    VERBOSE='--verbose'
}

DISTRO=""
if (pararams['DISTRO'] != "") {
    DISTRO="""-${params['DISTRO']}"""
}
OSVERSION=""
if (pararams['OSVERSION'] != "") {
    OSVERSION="""-${params['OSVERSION']}"""
}
switch (TARGET) {
    case 'windows': 
        PYTHON='python'
        TARGET_HOST=TARGET
        SUDO=''
        TARGET_HOST = """windows${DISTRO}${OSVERSION}"""
        PACKAGE_DIR = 'c:/jenkins/downloads'
        WINDOWS = true
        break

    case 'linux_deb':
        TARGET_HOST="""linux_deb${DISTRO}${OSVERSION}"""
        if (params['ZIP']) {
            SUDO='' // no root needed for zip testing
        } else {
            SUDO='sudo'
        }
        PYTHON='' // Lean on shebang!
        break
    case 'linux_rpm':
        TARGET_HOST="""linux_deb${DISTRO}${OSVERSION}"""
        if (params['ZIP']) {
            SUDO='' // no root needed for zip testing
        } else {
            SUDO='sudo'
        }
        PYTHON='' // Lean on shebang!
        break
    case 'macos':
        TARGET_HOST="""mac${DISTRO}${OSVERSION}"""
        if (params['ZIP']) {
            SUDO='' // no root needed for zip testing
        } else {
            SUDO='sudo'
        }
        PYTHON='' // Lean on shebang!
        break
}

print("""going to work on '${TARGET_HOST}'""")

node(TARGET_HOST)  {
    stage('checkout') {
        checkout([$class: 'GitSCM',
                  branches: [[name: params['GIT_BRANCH']]],
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
    }
    stage('fetch old') {
        if (params['VERSION_OLD'] != "") {
            ACQUIRE_COMMAND = """
${PYTHON} ${WORKSPACE}/release_tester/acquire_packages.py ${ENTERPRISE_PARAM} --enterprise-magic ${params['ENTERPRISE_KEY']} --package-dir ${PACKAGE_DIR} ${FORCE_PARAM_OLD} --source ${params['PACKAGE_SOURCE_OLD']} --version "${params['VERSION_OLD']}" --httpuser dothebart --httppassvoid "${params['HTTP_PASSVOID']}" ${ZIP} ${VERBOSE}
"""
            print("downloading old package(s) using:")
            print(ACQUIRE_COMMAND)
            if (WINDOWS) {
                powershell ACQUIRE_COMMAND
            } else {
                sh ACQUIRE_COMMAND
            }
        }
    }

    stage('fetch new') {
        ACQUIRE_COMMAND = """
${PYTHON} ${WORKSPACE}/release_tester/acquire_packages.py ${ENTERPRISE_PARAM} --enterprise-magic ${params['ENTERPRISE_KEY']} --package-dir ${PACKAGE_DIR} ${FORCE_PARAM_NEW} --source ${params['PACKAGE_SOURCE_NEW']} --version '${params['VERSION_NEW']}' --httpuser dothebart --httppassvoid '${params['HTTP_PASSVOID']}' ${ZIP} ${VERBOSE}
"""
        print("downloading new package(s) using:")
        print(ACQUIRE_COMMAND)
        if (WINDOWS) {
            powershell ACQUIRE_COMMAND
        } else {
            sh ACQUIRE_COMMAND
        }
    }

    stage('cleanup') {
        if (fileExists('/tmp/config.yml')) {
            print("cleaning up the system (if):")
            CLEANUP_COMMAND = """
${SUDO} ${PYTHON} ${WORKSPACE}/release_tester/cleanup.py ${ZIP}
"""
            print(CLEANUP_COMMAND)
            if (WINDOWS) {
                powershell CLEANUP_COMMAND
            } else {
                sh CLEANUP_COMMAND
            }
        } else {
            print("no old install detected; not cleaning up")
        }
    }

    if (params['VERSION_OLD'] != "") {
        stage('upgrade') {
            print("Running upgrade test")
            UPGRADE_COMMAND = """
${SUDO} ${PYTHON} ${WORKSPACE}/release_tester/upgrade.py ${ENTERPRISE_PARAM} --old-version ${params['VERSION_OLD']} --version ${params['VERSION_NEW']} --package-dir ${PACKAGE_DIR} --publicip 127.0.0.1 ${ZIP} --no-interactive ${VERBOSE} --starter-mode ${params['STARTER_MODE']}
"""
            print(UPGRADE_COMMAND)
            if (WINDOWS) {
                powershell UPGRADE_COMMAND
            } else {
                sh UPGRADE_COMMAND
            }
        }
        stage('plain test'){}
    } else {
        stage('upgrade'){}
        stage('plain test') {
            print("Running plain install test")
            TEST_COMMAND = """
${SUDO} ${PYTHON} ${WORKSPACE}/release_tester/test.py ${ENTERPRISE_PARAM} --version ${params['VERSION_NEW']} --package-dir ${PACKAGE_DIR} --publicip 127.0.0.1 ${ZIP} --no-interactive ${VERBOSE} --starter-mode ${params['STARTER_MODE']}
"""
            print(TEST_COMMAND)
            if (WINDOWS) {
                powershell TEST_COMMAND
            } else {
                sh TEST_COMMAND
            }
        }
    }
}
