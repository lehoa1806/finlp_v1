---

apt-get update:
  cmd.wait:
    - name: apt-get update

install packages:
  pkg.installed:
    - pkgs:
      - salt-minion
      - python3
      - python3-pip
      - awscli
