# Info
This is a subordinate charm for the Sojobo-api which enables the use of Manual-clouds

# Installation
The required charms can be found in the qrama-charms repo. In order to install these using the following commands, one must be in the topdir of the cloned qrama-charms repo.  
```
juju deploy ./controller-manual
juju add-relation sojobo-api controller-manual

```
To disable GCE-clouds, just remove the application
**Warning: Removing this will prevent the use of existing GCE-clouds!**

# Bugs
Report bugs on <a href="https://github.com/tengu-team/layer-controller-manual/issues">Github</a>

# Authors
- Sébastien Pattyn <sebastien.pattyn@tengu.io>
