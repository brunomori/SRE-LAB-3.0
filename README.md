# SRE LAB 3.0 — Laboratório Prático de SRE

Laboratório pessoal de **Site Reliability Engineering (SRE)** para estudar infraestrutura, Kubernetes, CI/CD, GitOps e observabilidade com práticas documentadas e reproduzíveis.

## Ambiente do laboratório

- **Host:** Ubuntu Linux
- **Virtualização:** Vagrant + VirtualBox
- **Cluster:** Kubernetes instalado com Kubespray
- **Objetivo:** evoluir de fundamentos até deploys, pipelines, automação, monitoramento e troubleshooting.

> Este repositório contém **documentação**. As máquinas virtuais, credenciais, configurações locais e artefatos sensíveis não são versionados aqui.

## 📚 Temas documentados

| Tema | Assunto | Situação |
| --- | --- | --- |
| [01 — Iniciar o laboratório](01-iniciar-laboratorio/README.md) | Iniciar as VMs, configurar `kubectl`, verificar o cluster e desligar o ambiente | Guia publicado |

## 🚀 Começar rapidamente

No Ubuntu, considerando o caminho local utilizado no laboratório:

```bash
cd ~/Downloads/sre-lab
make start

export KUBECONFIG="$PWD/.local/sre-lab.kubeconfig"
export PATH="$PWD/.local/bin:$PATH"

kubectl get nodes -o wide
kubectl get pods -A
```

Os comandos acima são um **guia de consulta**: confirme os caminhos e os alvos disponíveis no `Makefile` local antes de executar.

**Guia completo:** [Tema 01 — Iniciar o laboratório](01-iniciar-laboratorio/README.md).

## 🧭 Roadmap

- [x] Documentar a inicialização do ambiente Kubernetes
- [ ] Aplicação web e banco de dados
- [ ] Jenkins e CI/CD
- [ ] Helm e configurações DEV/UAT/PROD
- [ ] Argo CD e GitOps
- [ ] Terraform e Terragrunt
- [ ] Observabilidade: Prometheus, Grafana e Zabbix
- [ ] Runbooks e troubleshooting de incidentes

## 📝 Padrão de documentação

Cada tema ganha uma pasta `NN-nome-do-tema/` com `README.md` prático, comandos, validações e troubleshooting. A numeração cresce conforme o laboratório evolui.

A referência do processo está em [SKILL.md](SKILL.md). Para solicitar a documentação de um novo tema: **“Documenta o que fizemos no SRE LAB e atualiza o GitHub.”**

---

*Projeto em evolução — documentação técnica em português.*
