# Roadmap SRE LAB — estudos

Todas as fases começam pendentes. Metodologia: instalar → entender → automatizar → integrar → diagnosticar → recuperar → documentar. Trabalhe apenas em dados fictícios, clusters próprios e ferramentas gratuitas. Registre commits, evidências e runbooks.

| Fase | Pré-requisito | Entregável/evidência |
|---|---|---|
| 0 Fundação | Host compatível | Auditoria passiva, ativa e relatório de aceite |
| 1 Kubernetes | Cluster acessível | Manifestos e exercícios, explicar ciclo de vida |
| 2 Helm/IaC | Fase 1 | Módulos versionados e plan revisado |
| 3 Git/GitHub | Git local | PR, review, merge, tag |
| 4 Aplicação/SQL | Namespace e storage | CRUD, testes, imagem e migration |
| 5 Jenkins | Git + app | Pipelines CI e IaC com aprovação |
| 6 GitOps | CI + Helm | Promoção da mesma imagem DEV/UAT/PROD |
| 7 Observabilidade | App operacional | Dashboard, alerta e runbook |
| 8 Performance | Métricas | Requests/limits, probes, HPA e evidências |
| 9 Incident Lab | Nenhum para modo offline | Sessões e RCAs fictícios |
| 10 Confiabilidade | App e métricas | SLO, backup/restore e post-mortem |

## 0 — Fundação
- [ ] Revisar compatibilidade e configuração; provisionar cinco VMs e validar acesso, rede, API, DNS, storage.
- [ ] Rodar auditoria passiva e testes ativos benignos; registrar pendências e limitações.

## 1 — Kubernetes operacional
- [ ] kubectl, YAML, namespaces, labels/selectors, Deployments/StatefulSets, Services e Ingress.
- [ ] ConfigMaps, Secrets, RBAC/ServiceAccounts, ResourceQuota, LimitRange, NetworkPolicy, PV/PVC.
- [ ] Probes e rollouts; distinguir readiness e liveness. Documentar como investigar eventos.

## 2 — Helm e Terraform/Terragrunt
- [ ] Instalar Helm e Terraform pessoalmente; entender charts/releases/values e Kubernetes/Helm Providers.
- [ ] Criar módulos namespace, RBAC, SA, quota, limit-range, network-policy e plataforma (Jenkins etc.). Inputs, outputs, constraints, README e exemplos.
- [ ] State protegido, plan/apply com revisão, import de recursos criados manualmente, drift; Terragrunt após dominar módulos. Não compartilhar propriedade de release com Argo CD.
- [ ] Estrutura futura: `modules/{namespace,rbac,jenkins,...}`, `live/{platform,dev,uat,prod}`. Não criar esses módulos agora.

## 3 — Git e GitHub Free
- [ ] Criar repositórios gradualmente: infrastructure, kubernetes, terraform, webapp, gitops, observability; Helm separado somente se útil.
- [ ] Feature branch, commit, push, PR, revisão, merge, tag e resolução de conflitos. Não publicar credenciais, state ou dados do trabalho. Verificar limites e política do GHCR.

## 4 — Aplicação web + PostgreSQL
- [ ] Criar CRUD de chamados (sugestão Flask + HTML + PostgreSQL), testes, Dockerfile e configuração por ambiente.
- [ ] Aprender SELECT/INSERT/UPDATE/DELETE, constraints, índices, migrations versionadas com dados fictícios, backup/restore e compatibilidade de schema.
- [ ] Empacotar imagem versionada e publicar GHCR conforme limites gratuitos. Adicionar health endpoints, logs estruturados e métricas gradualmente.

## 5 — Jenkins
- [ ] Instalar manualmente; entender agentes, credenciais de escopo mínimo e PVC; criar módulo Terraform/Helm depois. Bootstrap independente do próprio pipeline.
- [ ] CI: checkout → teste → build → publicação da imagem → atualização do GitOps. Não depender de webhook público; polling ou manual no laboratório.
- [ ] IaC: fmt/check → init → validate → plan → aprovação explícita → apply → auditoria. Identidade de cluster explícita; sem destroy automático.

## 6 — Argo CD e GitOps
- [ ] Instalar pessoalmente; entender reconciliação, health, sync e diferença entre CI e CD.
- [ ] Criar DEV/UAT/PROD como namespaces simulados com isolamento, recursos e bancos/credenciais próprios. Namespaces platform/cicd/gitops/monitoring separados quando necessário.
- [ ] Promover a mesma imagem imutável DEV → UAT → PROD via mudanças Git e aprovação. Validar migrations; rollback de imagem não reverte schema.

## 7 — Observabilidade
- [ ] Zabbix (infra/serviços), Prometheus (métricas e alertas), Grafana (dashboards); instalar manualmente e automatizar depois.
- [ ] Latência, tráfego, erros e saturação; métricas de nodes, app, DB e pipelines. Alertas acionáveis, logs e runbooks. Loki/Alertmanager quando úteis.

## 8 — Performance
- [ ] Requests/limits, HPA com fonte de métricas (Metrics Server a instalar), PDB, affinity/anti-affinity, taints/tolerations, scheduling.
- [ ] Medir consumo e capacidade sem esgotar host ou sistemas; comparar métricas de referência e resultados em app descartável.

## 9 — Incident Lab
- [ ] Resolver os 16 casos sintéticos; registrar hipótese, evidências, mitigação, validação e medidas preventivas.
- [ ] Comparar investigação de Kubernetes, IaC, banco e CI/CD; registrar MTTD/MTTR didáticos. Nenhum mecanismo que derrube infraestrutura.

## 10 — Engenharia de confiabilidade
- [ ] SLIs/SLOs/error budgets, alertas, capacidade, backups e restauração de dados fictícios, post-mortem sem culpabilização, RCA, runbooks e redução de toil.
- [ ] Documentar decisões, evidências e limitações, evitando confundir HA de VMs no mesmo host com HA física.

Futuro opcional: multi-cluster, Cluster Mesh, storage distribuído, networking/TLS avançado e DR. Chaos Engineering avançado apenas planejamento conceitual separado. AWS fora do escopo.
