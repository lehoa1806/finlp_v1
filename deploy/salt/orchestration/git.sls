---
install git:
  pkg.installed:
    - pkgs:
      - git
      - git-core

finpl-project:
  git.latest:
    - name: {{ pillar.project_code }}
    - target: /home/{{ pillar.user_name }}/{{ pillar.project }}
    - user: {{ pillar.user_name }}
    - branch: {{ pillar.project_branch }}
    - submodules: true
    - force_reset: true
