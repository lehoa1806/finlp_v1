---

install supervisor:
  cmd.run:
    - name: /usr/bin/python3 -m pip install supervisor

supervisor conf:
  file.copy:
    - name: /etc/supervisord.conf
    - source: {{ pillar.supervisord_conf }}
    - user: root
    - group: root
    - mode: '0644'
    - force: true

start supervisor:
  cmd.run:
    - name: sudo `which supervisord`
    - cwd: /home/{{ pillar.user_name }}/{{ pillar.project }}
    - runas: root
    - bg: true
