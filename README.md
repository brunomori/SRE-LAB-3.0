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

A arquitetura é dividida em **três fluxos complementares**: (1) provisionar o cluster, (2) entregar versões da aplicação e (3) operar os ambientes com bancos de dados e observabilidade. O diagrama abaixo representa a **arquitetura-alvo**, não a confirmação de que todas as ferramentas já foram implantadas.

```mermaid
flowchart TB
    subgraph INFRA["1. Provisionamento da infraestrutura local"]
        direction LR
        HOST["Host Ubuntu"] --> VAGRANT["Vagrant + VirtualBox<br/>Criar e gerenciar VMs"]
        VAGRANT --> VMS["VMs Linux<br/>Control planes e workers"]
        VMS --> ANSIBLE["Ansible<br/>Preparar e configurar as VMs"]
        ANSIBLE --> KUBESPRAY["Kubespray<br/>Instalar e configurar Kubernetes<br/>com Ansible"]
    end

    subgraph ENTREGA["2. Código, CI/CD e artefatos"]
        direction LR
        GITHUB["GitHub<br/>Código, Dockerfile, charts Helm<br/>e configuração GitOps"] --> CI["Jenkins / GitHub Actions<br/>Build e testes"]
        CI --> REGISTRY["Registry<br/>Imagens Docker versionadas"]
        GITHUB --> HELM["Helm charts + values<br/>DEV / UAT / PROD"]
    end

    subgraph CLUSTER["3. Cluster Kubernetes"]
        direction TB
        ARGO["Argo CD<br/>Sincronização declarativa com Helm"]

        subgraph AMBIENTES["Aplicações e bancos isolados por namespace"]
            direction LR
            subgraph DEV["Namespace dev"]
                direction TB
                APP_DEV["Aplicação DEV"] <--> DB_DEV[("Banco DEV<br/>PVC separado")]
            end
            subgraph UAT["Namespace uat"]
                direction TB
                APP_UAT["Aplicação UAT"] <--> DB_UAT[("Banco UAT<br/>PVC separado")]
            end
            subgraph PROD["Namespace prod"]
                direction TB
                APP_PROD["Aplicação PROD"] <--> DB_PROD[("Banco PROD<br/>PVC separado")]
            end
        end

        MONITORING["Namespace monitoring<br/>Prometheus + Grafana"]
    end

    OUTROS["Zabbix / Datadog<br/>Integrações de observabilidade"]
    OPERACAO["Alertas, dashboards, troubleshooting<br/>runbooks e resposta a incidentes"]

    KUBESPRAY --> CLUSTER
    HELM --> ARGO
    ARGO --> APP_DEV
    ARGO --> APP_UAT
    ARGO --> APP_PROD
    REGISTRY -.-> APP_DEV
    REGISTRY -.-> APP_UAT
    REGISTRY -.-> APP_PROD

    APP_DEV -.-> MONITORING
    APP_UAT -.-> MONITORING
    APP_PROD -.-> MONITORING
    DB_DEV -.-> MONITORING
    DB_UAT -.-> MONITORING
    DB_PROD -.-> MONITORING
    CLUSTER -.-> OUTROS

    MONITORING --> OPERACAO
    OUTROS --> OPERACAO
```

#### Como interpretar o fluxo

1. **Provisionamento:** o **host Ubuntu** executa o Vagrant, que utiliza o **VirtualBox** para criar e gerenciar as VMs. O **Ansible** automatiza sua preparação; o **Kubespray** usa playbooks Ansible para instalar e configurar o **cluster Kubernetes**.
2. **CI (integração contínua):** o código fica no **GitHub**. **Jenkins** e, numa etapa futura, **GitHub Actions**, executam build e testes e publicam imagens versionadas em um **registry**.
3. **CD e GitOps (entrega):** os **charts Helm** e os valores por ambiente ficam versionados. O **Argo CD**, executando no Kubernetes, sincroniza o estado desejado e instala/atualiza os releases. **Helm é o mecanismo de empacotamento e implantação**, e não um servidor de pipeline.
4. **Aplicação e banco:** cada namespace (`dev`, `uat`, `prod`) possui **sua aplicação conectada ao respectivo banco**, com persistência isolada por **PVC**. Nenhum ambiente deve usar o banco de outro.
5. **Observabilidade transversal:** **Prometheus e Grafana** formam a camada compartilhada de métricas e dashboards (por exemplo, em `monitoring`); **Zabbix e Datadog** serão integrados progressivamente. O monitoramento abrange aplicações, bancos, Pods, nós e infraestrutura e alimenta alertas, diagnóstico e runbooks.

**Limites do desenho:** GitHub, registry e pipelines não precisam executar dentro do cluster. O Argo CD e os workloads podem rodar no cluster. Os ambientes `dev`, `uat` e `prod` são **namespaces de um cluster de laboratório**, sem equivalência automática com o isolamento de clusters independentes em produção. **Terraform/Terragrunt** entram em práticas de IaC à parte; não substituem o Vagrant no provisionamento local atualmente planejado.

> **Nota sobre a imagem acima:** o mapa de estudos é uma visão didática do roadmap. Este fluxograma descreve com mais precisão as dependências e os limites entre infraestrutura, pipeline de entrega, workloads e monitoramento.

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