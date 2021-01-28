---
set up environment variables:
  cmd.run:
    - names:
        - echo "PYTHONPATH=\"{{ pillar.project_home }}\"" >> /etc/environment
