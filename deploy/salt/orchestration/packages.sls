---

apt-get update:
  cmd.wait:
    - name: apt-get update

install packages:
  pkg.installed:
    - pkgs:
      - awscli
      - memcached
      - python3
      - python3-pip
      - salt-minion
