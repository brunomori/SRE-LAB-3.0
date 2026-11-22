# Validação prática do SRE LAB 3.0 — 17/11/2026

Este documento resume o relatório de execução do laboratório de 17/11/2026, anteriormente presente na pasta reports. É um **registro histórico de uma execução real**, não uma medição contínua nem homologação universal.

## Resultado da execução

- Escopo all com testes ativos.
- **13 PASS, 0 WARN, 0 FAIL, 0 SKIP; exit code 0.**
- Cinco VMs próprias e **5/5 nós Kubernetes Ready**.
- API TLS/VIP e três backends, Calico, etcd com três membros, CoreDNS, MetalLB, Traefik e storage.
- Testes funcionais: comunicação entre workers, DNS, HTTP por LoadBalancer/Ingress, PVC e persistência local.

## Verificações registradas

| Verificação | Estado |
| --- | --- |
| Host | PASS |
| Bootstrap | PASS |
| VMs | PASS |
| SSH | PASS |
| Networking | PASS |
| Ansible | PASS |
| Kubernetes | PASS |
| etcd | PASS |
| DNS | PASS |
| MetalLB | PASS |
| Ingress | PASS |
| Storage | PASS |
| Active tests | PASS |

O relatório original informou explicitamente que **não realizou failover real dos control planes**. Este resultado não comprova que qualquer alteração posterior do código foi aplicada no computador. O orquestrador atualizado em 21/11/2026 teve seus **29 testes unitários** executados separadamente em ambiente isolado.

## Como repetir uma validação passiva

~~~bash
cd ~/Downloads/sre-lab
make status
make test
make validate
~~~

O modo ativo cria e remove recursos temporários no cluster e requer autorização:

~~~bash
./scripts/validate.sh --all --active --report
~~~

Não execute esse teste em produção. A documentação aqui não altera as VMs do Ubuntu.

[Voltar ao README do pacote](../README.md)
