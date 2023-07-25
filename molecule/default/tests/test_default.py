import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services(host):
    services = [
        "netbox.socket",
        "netbox.service",
        "netbox-rqworker@1.service"
        "netbox-rqworker@2.service"
    ]
    for service in services:
        s = host.service(service)
        assert s.is_enabled
        assert s.is_running


def test_sockets(host):
    assert host.socket("tcp://0.0.0.0:80")


def test_files(host):
    files = [
        "/srv/netbox/shared/application.log",
        "/srv/netbox/shared/configuration.py"
    ]
    for file in files:
        assert host.file(file)
