[![Build Status](https://travis-ci.org/lae/ansible-role-netbox.svg?branch=master)](https://travis-ci.org/lae/ansible-role-netbox)
[![Galaxy Role](https://img.shields.io/badge/ansible--galaxy-netbox-blue.svg)](https://galaxy.ansible.com/lae/netbox/)

lae.netbox
=========

Installs and configures DigitalOcean's [NetBox]().

This role deploys NetBox inside of a virtualenv, uses uWSGI as its frontend
(can be used standalone or behind a load balancer), works with both Python 2/3
and has been tested across CentOS 7/Debian 8/Ubuntu 16.

Requirements
------------

### Database

You'll need to setup a PostgreSQL server and create a database user separately
from this role. This role will check and attempt to create a database itself if
it doesn't already exist. The example playbook provides an excellent, tested
example of deploying Postgres locally with this role, giving the database user
CREATEDB permissions (which aren't needed if you create the database yourself).

Role Variables
--------------

To enable a stable release, set `netbox_stable` to `true` (mutually exclusive
with `netbox_git` - only one can be set to `true`). You can also pin a specific
version with `netbox_stable_version`, or download a different NetBox tarball
with `netbox_stable_uri`.

To deploy NetBox via git, set `netbox_git` to `true`. You can select a specific
commit, branch or tag by setting `netbox_git_version` to a valid ref, and you
can use a different git repository by defining `netbox_git_uri`.

By default, Python 3 will be used for deployment. Set `netbox_python` to 2 in
order to use Python 2.

See the *Example Playbook* section for more information on configuring the DB.

`netbox_config` should contain a dictionary of of settings to configure
NetBox with. See [Mandatory Settings]() and [Optional Settings]() from the
NetBox documentation for more information, as well as `examples/netbox_config.yml`
in this repository.

If `netbox_config.SECRET_KEY` is left undefined, this role will automatically
generate one for you and store it in `/srv/netbox/shared/generated_secret_key`
(by default). The SECRET_KEY will be read from this file on subsequent runs,
unless you override it by defining `netbox_config.SECRET_KEY`.

To load the initial data shipped by NetBox, set `netbox_load_initial_data` to
true. Otherwise, this role will deploy NetBox with an empty slate.

Configure `netbox_uwsgi_socket` to either be a TCP address or UNIX socket to
bind to. By default, this role will configure uWSGI to serve a full uWSGI HTTP
web server. You can set `netbox_behind_load_balancer` to `true` to use an uWSGI
socket (and you can also set `netbox_uwsgi_protocol` to `http` to configure
uWSGI to use an HTTP-speaking socket instead).

By default, NetBox will be configured to output to `/srv/netbox/shared/application.log`
and `/srv/netbox/shared/requests.log`. You can override these with a valid
uWSGI logger by setting `netbox_uwsgi_logger` and `netbox_uwsgi_req_logger`.

Toggle `netbox_ldap_enabled` to `true` to configure LDAP authentication for
NetBox. By default, Ansible will look for `netbox_ldap_config.py.j2` in your
playbook's `templates/` directory - which you can find an example of in this
role's `templates/` directory. You can set `netbox_ldap_config_template` to a
different location if you have your template located somewhere else.

Example Playbook
----------------

The following installs PostgreSQL and creates a user with @geerlingguy's robust
Postgres role, then proceeds to deploy and configure NetBox using a local unix
socket to authenticate with the Postgres server.

    - hosts: netbox.idolactiviti.es
      become: yes
      roles:
         - geerlingguy.postgresql
         - lae.netbox
      vars:
         netbox_stable: true
         netbox_database_socket: "{{ postgresql_unix_socket_directories[0] }}"
         netbox_uwsgi_socket: "0.0.0.0:80"
         netbox_config:
           ALLOWED_HOSTS:
             - netbox.idolactiviti.es
         postgresql_users:
           - name: "{{ netbox_database_user }}"
             role_attr_flags: CREATEDB,NOSUPERUSER

Assuming you have a PG server already running with the user `netbox_prod_user`
created, it owns a database called `netbox_prod`, and it allows the host you're
installing NetBox on to authenticate with it over TCP:

    - hosts: netbox.idolactiviti.es
      become: yes
      roles:
         - lae.netbox
      vars:
         netbox_stable: true
         netbox_uwsgi_socket: "0.0.0.0:80"
         netbox_config:
           ALLOWED_HOSTS:
             - "{{ inventory_hostname }}"
         netbox_database_host: pg-netbox.idolactiviti.es
         netbox_database_port: 15432
         netbox_database_name: netbox_prod
         netbox_database_user: netbox_prod_user
         netbox_database_password: "very_secure_password_for_prod"

[NetBox]: https://github.com/digitalocean/netbox
[Mandatory Settings]: http://netbox.readthedocs.io/en/stable/configuration/mandatory-settings/
[Optional Settings]: http://netbox.readthedocs.io/en/stable/configuration/optional-settings/
