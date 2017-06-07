[![Build Status](https://travis-ci.org/lae/ansible-role-netbox.svg?branch=master)](https://travis-ci.org/lae/ansible-role-netbox)
[![Galaxy Role](https://img.shields.io/badge/ansible--galaxy-netbox-blue.svg)](https://galaxy.ansible.com/lae/netbox/)

lae.netbox
=========

Installs and configures DigitalOcean's NetBox.

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

TBD


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
         netbox_database_host: pg-netbox.idolactiviti.es
         netbox_database_port: 15432
         netbox_database_name: netbox_prod
         netbox_database_user: netbox_prod_user
         netbox_database_password: "very_secure_password_for_prod"

