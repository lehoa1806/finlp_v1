---
include:
  - packages

create a temporary workspace for lambda:
  cmd.run:
    - names:
        - rm -rf /tmp/workspace
        - mkdir -p /tmp/workspace
        - git clone https://github.com/lehoa1806/finlp.git /tmp/workspace/finlp
        - cd /tmp/workspace/finlp && git submodule update --init --recursive
        - pip3 install -r /tmp/workspace/finlp/requirements.txt -t /tmp/workspace/finlp
    - runas: {{ pillar.user_name }}

zip the repo:
  module.run:
    - name: archive.cmd_zip
    - zip_file: /tmp/workspace/{{ pillar.lambda_s3_object }}
    - sources: .
    - cwd: /tmp/workspace/finlp/

copy to S3:
  cmd.run:
    - name: aws s3 cp /tmp/workspace/{{ pillar.lambda_s3_object }} s3://{{ pillar.s3_workspace_bucket }}/{{ pillar.lambda_s3_object }}
