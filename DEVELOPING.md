# Developing ansible-role-netbox

Thanks for you interest and help in developing this role.  

## Steps

1. Fork https://github.com/lae/ansible-role-netbox/
2. checkout locally and create a feature/issue branch locally
3. Make required changes and test locally
4. Regularly push branch changes back to github and make sure CI tests pass on Travis-CI
5. Squash and Rebase as required.
6. Create Pull Request.

## Setting up the local development environment

Minimium requirements are:

- git
- vagrant <https://www.vagrantup.com/>
- virtualbox <https://www.virtualbox.org/>
- molecule <https://molecule.readthedocs.io/en/latest/>

### Setup Vagrant additions

Vagrant when working with molecule requires python-vagrant installed

```cli
$ sudo pip install python-vagrant
```

## Molecule
Molecule is used to run tests locally (these can be integrated into the CI pipeline however not  done for this project at this point in time), currently this project only implements vagrant/virtualbox testing.

Under the molecule directory contains testing scenarios, in this case there is a single default senario using vagrant and virtualbox, howver you may want to add your own in addition to the defaul, i.e. if you use parallels vm or you want to use docker.  Please see molecule documentaton for more details.

```
molecule
└── default
    ├── INSTALL.rst
    ├── molecule.yml
    ├── playbook.yml
    ├── prepare.yml
    ├── requirements.yml
    └── tests
        └── test_default.py
```

**molecule.yml** - defines how the tests are run, linting is enabled/disabled from here, what images are used etc.

**playbook.yml** - actual playbook that gets run during converge

**prepare.yml** - any setups here that get executed as part of the prepare stage, do not modify when vagrant is used as the scenarios method as there are known issues.

**requirements.yml** - any external role dependancey go here.

**tests** - all tests live under here

### Running tests locally

NOTE: please note that all molecule commands listed are executed from the root of the project directory.

Mostly you will (or should be doing):

1. define a test
2. make changes to your code 
3. run the suite of tests under the default scenario to make sure everything passes

Tests are written using testinfra <https://testinfra.readthedocs.io/en/latest/modules.html> and are locally in test_default.py file.

below is an example testing required services are running and enabled.  If either of the two assets fail for any of the three services the test will fail.

```python
def test_services(host):
    services = [
        "netbox.socket",
        "netbox.service",
        "netbox-rqworker.service"
    ]
    for service in services:
        s = host.service(service)
        assert s.is_enabled
        assert s.is_running
```

Easiest way to perform all the required steps and tests is: 

```cli
molecule test
```

This will perform all the correct sequences

However you may want to manually run indiviual stages to troubleshoot the code changes.

### Troubleshooting the role under test

To troublshoot a failed molecule test you can first start with a clean slate

```cli
molecule destroy
```

Then converge the environment via `molecule converge` command.  

The converge will provision the test machine and then apply the role, but will not run any tests beside lint (if enabled), however unlike the `molecule test` command, when it completes it will still keep the vagrant environment up and running so you can:

1.  execute the suite of default tests via the `molecule verify` or `molecule indempotent`
2.  allows you to log into the vagrant machine and poke around. `molecule login`

To re-setup/reprovision the test environment, first perform `molecule destroy` then `molecule converge`

#### What tests can you do locally?

(Please refer to molecule documentation for more details)

**Self Check molecule scenario**

helpful if you make changes to anything under the scenario

```cli
molecule check
```

**Lint**

YAML Lint checking
Ansible Lint checking

These can be enabled/disabled in molecule.yml (currently disabled)

```cli
molecule lint
```

**Syntax**

```cli
molecule syntax
```

**Indempotence**

```cli
molecule indempotence
```

**Side effects**

```cli
molecule side-effect
```
