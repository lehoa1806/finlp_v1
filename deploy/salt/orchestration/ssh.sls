---
copy authorized_keys to local:
  cmd.run:
    - names:
        - /usr/bin/aws s3 cp s3://{{ pillar.secret_bucket }}/authorized_keys /home/{{ pillar.user_name }}/.ssh/authorized_keys
    - runas: {{ pillar.user_name }}

correct .ssh/authorized_keys permissions:
  file.managed:
    - name: /home/{{ pillar.user_name }}/.ssh/authorized_keys
    - mode: '0600'
    - user: {{ pillar.user_name }}
    - group: {{ pillar.user_name }}
