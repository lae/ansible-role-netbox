[![Build Status](https://travis-ci.org/lae/ansible-role-netbox.svg?branch=master)](https://travis-ci.org/lae/ansible-role-netbox)
[![Galaxy Role](https://img.shields.io/badge/ansible--galaxy-netbox-blue.svg)](https://galaxy.ansible.com/lae/netbox/)

lae.netbox
=========

Deploys and configures DigitalOcean's [NetBox].

This role will deploy NetBox within its own virtualenv either by release tarball
or via git using Python 3 (or 2 if you're so inclined) and uWSGI as an HTTP
server/frontend (default) or as a backend for a load balancer.

Tested and supported against CentOS 7/Debian 8/Ubuntu 16.

Note that this role is slightly opinionated and differs from installation
instructions from the NetBox documentation. The main differences are:

* Uses distro-provided systemd instead of supervisord
* Uses uWSGI as an application server instead of gunicorn
* Hardens the NetBox/uWSGI service (see `templates/netbox.service.j2`)
* Will hot reload on upgrades and configuration changes

Quickstart
----------

Provided you have Ansible installed and are using defaults:

```
ansible-galaxy install geerlingguy.postgresql lae.netbox
ansible-playbook -i your.server.fqdn, /etc/ansible/roles/lae.netbox/examples/playbook_single_host_deploy.yml -K
```

Modify accordingly. Read below for more insight.

Prerequisites
-------------

### Database

This role does not setup a PostgreSQL server (but will create a database if
needed), so you'll need to setup a PostgreSQL server and create a database user
separate from this role. Take a look at the *Example Playbook* section.

Role Variables
--------------

See `examples/` for some playbooks you could write for different scenarios.
Note that some variables below **must** be defined in your playbook.

    netbox_stable: false
    netbox_git: false

It's **required** to set one of the above variables to `true`. `netbox_stable`
tells the role to deploy by extracting tarball releases from GitHub, while
`netbox_git` tells the role to clone a NetBox git repository - they're mutually
exclusive.

    netbox_stable_version: 2.0.6
    netbox_stable_uri: "https://github.com/digitalocean/netbox/archive/v{{ netbox_stable_version }}.tar.gz"

These can be configured to pin a version (e.g. increment to trigger an upgrade)
or deploy using a tarball located somewhere else. Useful for when you need to
modify something in a release or are deploying while firewalled in your local network.

    netbox_git_version: develop
    netbox_git_uri: "https://github.com/digitalocean/netbox.git"

`netbox_git_version` can be any valid ref within a git repository.
`netbox_git_uri` can be used to point to e.g. an on-premise repo or a fork.

    netbox_behind_load_balancer: false

uWSGI, *by default*, will be configured to act as its own HTTP server/load
balancer for the NetBox application. By setting this to `true`, this role will
configure uWSGI to act as just an application server listening over WSGI.
Toggle this when you're deploying multiple instances of NetBox.

    netbox_superuser_username: admin
    #netbox_superuser_password: changeme
    netbox_superuser_email: admin@localhost

It is **required** to set the superuser password. This role will create a new
superuser if the user does not exist, or will modify an existing user if they're
not a superuser/have a different email or password. (Yes, you can use this to 
reset your superuser password if you forget it.)

    netbox_database: netbox
    netbox_database_user: netbox
    #netbox_database_password: changeme
    #netbox_database_host: localhost
    netbox_database_port: 5432
    #netbox_database_socket: /var/run/postgresql

It is **required** to configure either a socket directory (to communicate over
UNIX sockets) or a host/password (to use TCP/IP). See the **Example Playbook**
section for more information on configuring the database.

Note that these are used to configure `DATABASE` in `configuration.py`.

    netbox_config:
      #SECRET_KEY:
      ALLOWED_HOSTS:
        - localhost
        - 127.0.0.1

This is a dictionary of settings used to template NetBox's `configuration.py`.
See [Mandatory Settings] and [Optional Settings] from the NetBox documentation
for more details, as well as `examples/netbox_config.yml` in this repository.

It is not necessary to define `SECRET_KEY` here - this role will automatically
create one for you and store it in `{{ netbox_shared_path }}/generated_secret_key`.
The `SECRET_KEY` will then be read from this file on subsequent runs, unless you
later do set this in your playbook. Note that you should define the `SECRET_KEY`
if you are deploying multiple NetBox instances behind one load balancer.

    netbox_user: netbox
    netbox_group: netbox
    netbox_home: /srv/netbox
    netbox_releases_path: "{{ netbox_home }}/releases"
    netbox_git_path: "{{ netbox_releases_path }}/git"
    netbox_stable_path: "{{ netbox_releases_path }}/netbox-{{ netbox_stable_version }}"
    netbox_current_path: "{{ netbox_home }}/current"
    netbox_shared_path: "{{ netbox_home }}/shared"

These are all deployment details that you can modify to change the application
user and application storage locations. `netbox_releases_path` stores all NetBox
releases you've ever deployed. `netbox_git_path` is where the Git repository
will be cloned to, and `netbox_stable_path` is the extracted folder from a
tarball. `netbox_current_path` will be symlinked to the selected release and
used in service/configuration files as the location NetBox is installed.
`netbox_shared_path` is intended to store configuration files and other "shared"
content, like logs.

    netbox_python: 3

If you wish to deploy using Python 2, set this to `2`.

    netbox_uwsgi_socket: "127.0.0.1:8000"
    netbox_uwsgi_protocol: uwsgi
    netbox_uwsgi_processes: "{{ ansible_processor_vcpus }}"

Configure `netbox_uwsgi_socket` to either be a TCP address or UNIX socket to
bind to. If behind a load balancer, `netbox_uwsgi_protocol` defines what
language the uWSGI application server speaks; set to `http` to configure
uWSGI to use an HTTP-speaking socket instead.

    netbox_uwsgi_logger: "file:{{ netbox_shared_path }}/application.log"
    netbox_uwsgi_req_logger: "file:{{ netbox_shared_path }}/requests.log"

These define where logs will be stored. You can use external logging facilities
instead of local files if you wish.

    netbox_load_initial_data: false

To load the initial data shipped by NetBox, set this to `true`.

    netbox_ldap_enabled: false
    netbox_ldap_config_template: netbox_ldap_config.py.j2

Toggle `netbox_ldap_enabled` to `true` to configure LDAP authentication for
NetBox. `netbox_ldap_config_template` should be the path to your template - by
default, Ansible will search your playbook's `templates/` directory for this.
You can find an example in `examples/`.

Example Playbook
----------------

The following installs PostgreSQL and creates a user with @geerlingguy's robust
Postgres role, then proceeds to deploy and configure NetBox using a local unix
socket to talk to the Postgres server with the default netbox database user.

    - hosts: netbox.idolactiviti.es
      become: yes
      roles:
        - geerlingguy.postgresql
        - lae.netbox
      vars:
        netbox_stable: true
        netbox_database_socket: "{{ postgresql_unix_socket_directories[0] }}"
        netbox_superuser_password: netbox
        netbox_uwsgi_socket: "0.0.0.0:80"
        netbox_config:
          ALLOWED_HOSTS:
            - netbox.idolactiviti.es
        postgresql_users:
          - name: "{{ netbox_database_user }}"
            role_attr_flags: CREATEDB,NOSUPERUSER

Note the `CREATEDB` attribute.

Assuming you have a PG server already running with the user `netbox_prod_user`
created, it owns a database called `netbox_prod`, and it allows the host you're
installing NetBox on to authenticate with it over TCP:

    - hosts: netbox.idolactiviti.es
      become: yes
      roles:
        - lae.netbox
      vars:
        netbox_stable: true
        netbox_superuser_password: netbox
        netbox_uwsgi_socket: "0.0.0.0:80"
        netbox_config:
          ALLOWED_HOSTS:
            - "{{ inventory_hostname }}"
        netbox_database_host: pg-netbox.idolactiviti.es
        netbox_database_port: 15432
        netbox_database_name: netbox_prod
        netbox_database_user: netbox_prod_user
        netbox_database_password: "very_secure_password_for_prod"

See `examples/` for more.

[NetBox]: https://github.com/digitalocean/netbox
[Mandatory Settings]: http://netbox.readthedocs.io/en/stable/configuration/mandatory-settings/
[Optional Settings]: http://netbox.readthedocs.io/en/stable/configuration/optional-settings/
