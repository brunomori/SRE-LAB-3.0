# SRE LAB 3.0

Documentação incremental de um laboratório prático de **Site Reliability Engineering (SRE)**, focado em Kubernetes, automação, CI/CD, infraestrutura como código, GitOps e observabilidade.

## Guias

| Tema | Conteúdo | Status |
| --- | --- | --- |
| [01 — Iniciar o laboratório](01-iniciar-laboratorio/README.md) | Subir VMs, configurar kubectl, validar o cluster e desligar o ambiente | ✅ Documentado |


## Como documentar novos temas

Use a [Skill — Documentação do SRE LAB](../.github/skills/sre-lab-documentacao/SKILL.md) como procedimento para registrar cada nova prática no GitHub. Basta pedir: **“Documenta o que fizemos no SRE LAB e atualiza o índice no GitHub.”**

## Próximos temas (conforme evolução do laboratório)

- Aplicação web e banco de dados no Kubernetes
- Jenkins: primeiro pipeline de CI/CD
- Helm: empacotamento da aplicação e configurações DEV/UAT/PROD
- Argo CD e GitOps
- Terraform/Terragrunt para IaC
- Observabilidade com Prometheus, Grafana e Zabbix
- Troubleshooting, incidentes e runbooks

> **Organização:** cada novo tema terá sua própria pasta e um `README.md` com objetivo, comandos testados, validações e problemas encontrados. Este repositório documenta as práticas; não contém necessariamente todo o estado do laboratório local.

[← Voltar ao repositório](../README.md)
