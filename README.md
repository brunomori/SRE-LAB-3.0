# SRE LAB 3.0

**Laboratório prático de Site Reliability Engineering (SRE) e Platform Engineering.**

Um ambiente de estudos progressivo para construir, operar, automatizar e evoluir uma plataforma de aplicações — do provisionamento da infraestrutura ao deploy contínuo, à observabilidade e à resposta a incidentes.

> **Proposta:** aprender fazendo, com um cenário integrado que se aproxima das tarefas de uma operação real. O objetivo não é apenas instalar ferramentas, mas entender **por que usá-las, como se relacionam e como diagnosticar falhas**.

## 🎯 Objetivos do projeto

- **Infraestrutura reproduzível:** preparar e administrar ambientes Linux e máquinas virtuais.
- **Orquestração de aplicações:** operar Kubernetes, seus recursos, armazenamento, rede e políticas de acesso.
- **Automação e entrega:** construir pipelines de CI/CD, empacotar aplicações e adotar GitOps.
- **Confiabilidade:** observar métricas, logs e alertas; investigar incidentes; validar recuperação e resiliência.
- **Portfólio técnico:** registrar decisões, comandos testados, problemas e aprendizados em documentação pública, sem expor informações sensíveis.

## 🗺️ Mapa de estudos e arquitetura

O laboratório foi planejado para conectar infraestrutura, aplicações, dados, entrega e operação em um **único ambiente de prática**.

![Mapa de estudos, arquitetura e roadmap do SRE LAB 3.0](assets/mapa-estudos-sre-lab-3.0.jpg)

*Mapa de estudos e prática: arquitetura, stack de ferramentas, etapas e evolução planejada do laboratório.*

### Visão geral da solução

```mermaid
flowchart TD
    H[Host Ubuntu / Vagrant + VirtualBox] --> I[Ansible + Kubespray]
    I --> K[Cluster Kubernetes]
    G[GitHub: código e configuração] --> C[CI/CD: Jenkins e GitHub Actions]
    C --> D[Helm e Argo CD]
    D --> K
    K --> A[Aplicação em DEV / UAT / PROD]
    A --> B[(Bancos de dados e armazenamento)]
    K --> O[Prometheus / Grafana / Zabbix / Datadog]
    O --> R[Alertas, diagnóstico e runbooks]
```

**Fluxo de trabalho proposto:** código e configuração versionados no Git; build e testes em pipeline; imagem de contêiner; implantação no Kubernetes; sincronização declarativa; monitoramento e investigação de problemas.

## 🧰 Tecnologias previstas

| Área | Ferramentas e conceitos |
| --- | --- |
| Base do laboratório | Linux, Git, Shell, Vagrant, VirtualBox |
| Contêineres e orquestração | Docker, Kubernetes, Helm |
| Provisionamento e configuração | Ansible, Kubespray, Terraform, Terragrunt |
| Entrega contínua | Jenkins, GitHub Actions, Argo CD, GitOps |
| Dados | PostgreSQL como banco principal e MySQL para estudos SQL; PV/PVC no Kubernetes |
| Observabilidade | Prometheus, Grafana, Zabbix e Datadog |
| Operação e confiabilidade | Troubleshooting, testes, falhas controladas, rollback, runbooks, SLOs e análise de incidentes |

A presença de uma ferramenta neste mapa **não significa que ela já está instalada ou integrada**: a implementação ocorre por etapas, conforme os exercícios avançam.

## 📐 Abordagem de estudo

Cada etapa segue um ciclo simples:

1. **Entender:** conceito, motivação e problema que a ferramenta resolve.
2. **Implementar:** aplicar no ambiente, com configuração e comandos explicados.
3. **Validar:** observar o resultado, investigar erros e confirmar o funcionamento.
4. **Revisar:** comparar alternativas e fixar os comandos essenciais.
5. **Repetir:** realizar um exercício curto para consolidar o aprendizado.

O laboratório evolui **progressivamente**: primeiro o deploy manual; depois, padronização com Helm; em seguida, automação com Jenkins; adoção de GitOps com Argo CD; e ampliação do CI/CD com GitHub Actions. Observabilidade e troubleshooting acompanham essa evolução.

## 🧭 Roadmap de alto nível

| Fase | Foco | Resultado esperado |
| --- | --- | --- |
| **01 · Fundamentos** | Linux, Git, Docker e Kubernetes | Ambiente operacional e domínio dos recursos básicos |
| **02 · Aplicação e infraestrutura** | Helm, SQL, Terraform/Terragrunt e Ansible | Aplicação implantável e infraestrutura documentada |
| **03 · Entrega e automação** | Jenkins, Argo CD e GitHub Actions | Pipeline de build, testes, deploy e recuperação |
| **04 · Confiabilidade** | Prometheus, Grafana, Zabbix, Datadog, testes e incidentes | Operação observável, resposta a falhas e melhoria contínua |

**Ambientes lógicos:** `dev`, `uat` e `prod` serão usados para praticar isolamento e promoção de versões. São ambientes de laboratório, não serviços reais de produção.

## 🏗️ Estado do laboratório

**Base já preparada e documentada:** Ubuntu, Vagrant/VirtualBox e Kubernetes provisionado via Kubespray. As demais integrações fazem parte do roadmap e terão o status atualizado conforme forem realmente implantadas e verificadas.

A topologia, os endereços, as versões e o estado das VMs podem mudar ao longo do projeto. A documentação de cada etapa deve registrar o que foi **executado e validado**, separadamente do que está **planejado**.

## 📚 Documentação prática

O README principal descreve a **visão e os objetivos**. Os procedimentos executáveis ficam nas pastas numeradas e serão adicionados gradualmente, sem transformar esta apresentação em um manual de comandos.

- [**Tema 01 — Iniciar o laboratório**](01-iniciar-laboratorio/README.md): guia de inicialização, acesso ao cluster, validação e desligamento.
- **Próximos temas:** serão publicados conforme os estudos e as práticas evoluírem.

O padrão de organização e publicação está em [SKILL.md](SKILL.md).

## ✅ Resultado esperado

Ao final do roadmap, o projeto deverá demonstrar um fluxo integrado de **infraestrutura → aplicação → entrega → observabilidade → resposta a incidentes**, com exemplos reproduzíveis, decisões explicadas e evidências de aprendizado.

---

*Projeto de estudos em evolução. Documentação em português, com terminologia técnica em inglês quando aplicável.*