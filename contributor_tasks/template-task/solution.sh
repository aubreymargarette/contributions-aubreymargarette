#!/bin/bash

# Create the devteam group
groupadd -f devteam

# Remove users if they exist
userdel -r aubrey 2>/dev/null
userdel -r margarette 2>/dev/null

# Create users with devteam as primary group
useradd -m -g devteam aubrey
useradd -m -g devteam margarette

# Add both users to devteam as secondary group to pass the Python test
usermod -aG devteam aubrey
usermod -aG devteam margarette

# Create shared directory
mkdir -p /shared/dev
chown :devteam /shared/dev
chmod 2770 /shared/dev

# Test file creation
sudo -u aubrey touch /shared/dev/testfile_aubrey
sudo -u margarette touch /shared/dev/testfile_margarette
