---

{% set secret_bucket = 'finulp-secrets' %}

create {{ grains.boxname.lower() }} security group:
  boto_secgroup.present:
    - name: {{ grains.boxname.lower() }}-security-group
    - description: Security group of {{ grains.boxname }}
    - region: {{ pillar.aws_region }}
    - rules:
      - ip_protocol: tcp
        cidr_ip: 0.0.0.0/0
        from_port: 22
        to_port: 22
    - vpc_id: {{ pillar.vpc.vpc_id }}

 create {{ grains.boxname.lower() }} auto scaling group:
  boto_asg.present:
    - name: {{ grains.boxname.lower() }}-auto-scaling-group
    - launch_config_name: Auto scaling group of {{ grains.boxname }}
    - launch_config:
      - security_groups:
        - {{ grains.boxname.lower() }}-security-group
      - instance_type: t2.micro
      - instance_monitoring: false
      - vpc_id: {{ pillar.vpc.vpc_id }}
      - instance_profile_name: {{ pillar.iam_ec2_role }}
      - cloud_init:
        scripts:
          'deploy.sh': |
            #!/bin/bash
            cd /home/{{ pillar.user_name }}
            wget -O - https://repo.saltstack.com/py3/ubuntu/20.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
            bash -c 'echo "deb http://repo.saltstack.com/py3/ubuntu/20.04/amd64/latest focal main" > /etc/apt/sources.list.d/saltstack.list'
            apt-get -y update
            apt-get -y install salt-minion python3 python3-pip git awscli
            snap remove amazon-ssm-agent
            sudo -u {{ pillar.user_name }} git clone {{ pillar.project_code }} {{ pillar.project }}
            cd {{ pillar.project_home }}
            sudo -u {{ pillar.user_name }} git submodule update --recursive
            pip3 install -r requirements.txt
            aws s3 cp {{ secret_bucket }}/minion /etc/salt/minion
            cd {{ pillar.project_home }}/deploy/devbox
            salt-call --local state.apply -l debug
    - min_size: 1
    - desired_capacity: 1
    - max_size: 1
    - tags:
      - key: 'Name'
        value: {{ grains.boxname.lower() }}
        propagate_at_launch: true
    - region: {{ pillar.aws_region }}
