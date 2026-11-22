# Relatório de validação — SRE LAB v3.0 (geração inicial)

> **Registro histórico:** este relatório descreve a geração inicial sem infraestrutura real. Posteriormente, houve [13 verificações de integração aprovadas no host](validacao-pratica-2026-11-17.md) e a revisão do orquestrador passou em 29 testes unitários. São escopos e momentos diferentes.

**Resultado:** código gerado e verificações estáticas/unitárias executadas; **não homologado para instalação real**. Nenhuma VM, cluster, conta GitHub ou infraestrutura externa foi acessada ou alterada. O ambiente de geração não dispõe de VirtualBox, Vagrant, Ansible, Helm, kubectl ou ShellCheck; a tentativa de acesso direto a raw.githubusercontent.com falhou por DNS. A documentação oficial foi consultada pelo navegador de pesquisa, não houve download real de dependências.

## Testes executados nesta geração

| Teste | Comando | Resultado | Evidência |
|---|---|---|---|
| Python | `python -m py_compile scripts/*.py` | APROVADO | Dois módulos compilados sem erro |
| Bash | `bash -n scripts/*.sh` (um por arquivo) | APROVADO | Todos os wrappers passaram |
| Ruby | `ruby -c vagrant/Vagrantfile` | APROVADO | Syntax OK |
| YAML/JSON | PyYAML `safe_load_all` e `json.loads` para arquivos do projeto | APROVADO | 9 YAML e 33 JSON interpretados; não valida schema Kubernetes |
| Unitários | `make test` | APROVADO | 21 testes, 0 falhas |
| Makefile | `make -n install validate start stop ssh NODE=master-1` | APROVADO | Alvos apontam ao orquestrador, sem executar |
| Interface auditoria | `./scripts/validate.sh --help` | APROVADO | Flags e stages listados |
| Catálogo Incident Lab | `./scripts/incident.sh list` | APROVADO | 16 casos |

Os testes unitários incluem fixture válida e inválida, duplicação de IP, sobreposição de CIDR/pool, chaves desconhecidas, confirmação manual, prioridade de exit codes, VM alheia, alteração de configuração, identidade de cluster divergente, modo passivo sem criação de recursos, bloqueio de testes ativos após falha, autorização ao chamar script diretamente, argumentos inválidos, grupos de inventário, bootstrap incompleto, catálogo, sessões separadas, recuperação sintética e revelação explícita de soluções. São mocks/fixtures locais, não prova de segurança ou comportamento real do hypervisor/cluster.

## Testes não executados e bloqueios

| Verificação | Status | Motivo / como verificar no host |
|---|---|---|
| ShellCheck | NÃO EXECUTADO | ferramenta ausente; `shellcheck scripts/*.sh` |
| Ansible syntax-check/lint/inventory | NÃO EXECUTADO | Ansible e upstream não baixados; após bootstrap, verificar com venvs e inventário gerado, sem conexão às VMs para syntax-check |
| Vagrant validate | NÃO EXECUTADO | Vagrant ausente; após preencher config, validar no host com ambiente do projeto |
| Helm template e download | NÃO EXECUTADO | Helm ausente / rede direta indisponível; `make bootstrap` renderiza antes de provisionar |
| Schema manifestos/Kubernetes | NÃO EXECUTADO | kubectl/chart/CRDs ausentes; testes de integração no cluster de laboratório |
| Assinaturas de manifests/chart e imagem por digest | NÃO EXECUTADO | dependências não baixadas; fontes HTTPS/tag verificadas documentalmente; hashes locais de artefatos não são prova criptográfica independente |
| Compatibilidade host, box, hypervisor, kernel, L2/VIP | NÃO EXECUTADO | host real não acessado; versão box a preencher, revisar capacidade, DHCP, rotas e drivers |
| Ansible Core e demais dependências | BLOQUEIO DE REVISÃO | Ansible 12 fora de manutenção e Core 2.19 EOL nov/2026; revisar explicitamente antes de executar; não trocar tag silenciosamente |
| Instalação, idempotência, HA, etcd, rede, Ingress, PVC | NÃO EXECUTADO | não autorizado na geração, execução posterior pelo estudante |
| Concorrência, sinais, retomada após falha e limpeza ativa em cluster real | NÃO EXECUTADO | mocks não cobrem todos os caminhos; guarda conservadora bloqueia estados parciais; nenhum reset automático |
| Auditoria integrada no cluster | NÃO EXECUTADO | ausência de infraestrutura local disponível |

## Lacunas e desvios da especificação

- Configuração inicial usa JSON como subconjunto YAML; `box_version` exige preenchimento e revisão explícita. Nenhuma versão inventada do box. A configuração exemplo não é pronta para executar sem revisão. A matriz de versões é uma seleção documentada, não uma homologação cruzada.
- O projeto fixa versões diretas, mas ainda não congela integralmente as dependências transitivas nem valida assinaturas de todos os artefatos. O bootstrap grava o `pip freeze` local para inspeção. Requer revisão de segurança na data de execução.
- A instalação é encadeada, com checkpoints conservadores. Se Vagrant, cluster ou add-ons ficarem parcialmente instalados sem identidade/aceite, a automação bloqueia; a retomada de toda falha parcial não é automática. Não há prova de idempotência operacional.
- Preflight analisa rotas e redes host-only visíveis e exige revisão manual de VPN/DHCP/CIDRs existentes; não garante descoberta de todo IP ocupado. O bootstrap SSH inicial é responsabilidade do Vagrant; Ansible usa host key conferida pelo console.
- O modo ativo testa funcionalidades benignas em namespace isolado. Failover real, recuperação de componentes críticos e injeção de falhas não fazem parte dos scripts. A confirmação de redundância é apenas inspeção de saúde dos backends até um teste de manutenção separado.
- Incident Lab é offline (16 casos, evidências e avaliação por termos); não fornece sabotagem real nem recuperação de infraestrutura. Pontuação de termos é didática, não avaliação semântica completa.
- Não foi feita homologação de suporte do Traefik/MetalLB/Local Path com todas as versões selecionadas, nem testes de capacidade do host. Relatório de runtime e aceites AC-01–16 devem ser produzidos após revisão e execução autorizada.

**Recomendação:** use a instalação por etapas, não execute `make install` antes de resolver as pendências de compatibilidade. Este pacote é uma primeira implementação auditável para revisão, não uma garantia de instalação funcional. Para critérios de aceite reais, consulte `docs/validation.md`.
