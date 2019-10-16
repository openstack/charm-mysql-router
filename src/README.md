# Overview

This charm provides a MySQL 8 Router. The charm proxies database requests from
the principle application charm to a MySQL 8 InnoDB Cluster. MySQL Router
handles cluster communication and understands the cluster schema.

Ubuntu 19.10 or above is required.

# Usage

The charm is intended to be deployed as a subordinate charm on the
application server and related to the mysql-innodb-cluster charm.

## Cluster deployment

```
juju deploy mysql-router
```

The charm is related to a principle application charm via the
[shared-db relation](https://github.com/openstack/charm-interface-mysql-shared):

```
juju add-relation keystone:shared-db mysql-router:shared-db
```

The charm is then related to the [MySQL 8 InnoDB cluster charm](https://github.com/openstack-charmers/charm-mysql-innodb-cluster) via the
[db-router relation](https://github.com/openstack-charmers/charm-interface-mysql-router):

```
juju add-relation msyql-router:db-router mysql-innodb-cluster:db-router
```

## Scale out Usage

Scale out is accomplished by adding units to the principle charm:

```
juju add-unit keystone
```

## Known Limitations and Issues

> **Warning**: This charm is in preview state.

The charm is under active development and is not yet production ready. Its
current intended use is for validation of MySQL 8 InnoDB cluster for use with
OpenStack.

# Contact Information

OpenStack Charmers <openstack-charmers@lists.ubuntu.com>

## Upstream MySQL

  - [Upstream documentation](https://dev.mysql.com/doc/mysql-router/8.0/en/)

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/charm-mysql-router/+filebug).

For general questions please refer to the OpenStack [Charm Guide](https://docs.openstack.org/charm-guide/latest/).
