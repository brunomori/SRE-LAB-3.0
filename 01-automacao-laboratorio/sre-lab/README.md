# SRE LAB v3.0 — Kubernetes Platform Engineering

Laboratório local para aprofundar Kubernetes, IaC, GitOps e confiabilidade. A geração inicial do pacote ocorreu sem execução de VMs; posteriormente o laboratório foi instalado e **13 verificações passaram no host em 17/11/2026**, conforme [registro de validação prática](docs/validacao-pratica-2026-11-17.md). O orquestrador foi revisado em 21/11/2026 e aprovado em **29 testes unitários isolados**. Essa revisão no GitHub **não foi aplicada automaticamente ao Ubuntu**. Consulte [o relatório inicial (histórico)](docs/validation-report.md) e os requisitos de compatibilidade antes de uma instalação nova.

## Arquitetura

- Ubuntu Desktop x86_64, VirtualBox e Vagrant; cinco VMs novas Ubuntu 22.04 (3 control planes/etcd e 2 workers).
- Kubespray v2.32.0 / Kubernetes 1.36.4 / containerd, Calico VXLAN, CoreDNS, kube-vip para VIP da API, MetalLB L2, Traefik e Local Path Provisioner.
- 10 vCPU, 21 GiB de RAM e 190 GiB de capacidade virtual de disco sugeridos. O espaço real depende da alocação e do crescimento; 60 GiB livres é apenas piso inicial configurável, não garantia de capacidade. Desligue manualmente cargas não utilizadas antes de começar, sem destruir o laboratório anterior.
- StorageClass `sre-local` (padrão, Retain) e `sre-test` (Delete, somente testes); volumes locais sem replicação nem quota física efetiva.
- Git, Jenkins, Argo CD, Terraform, Helm de estudos, bancos e observabilidade não são instalados. O Helm privado é usado somente para o add-on Traefik.

## Pré-requisitos e revisão obrigatória

Tenha VirtualBox/Vagrant compatíveis com seu kernel, make, git, curl, OpenSSH (ssh/ssh-keyscan/ssh-keygen), iproute2, Python 3.11–3.13 com venv e internet para fontes oficiais. Não são instalados drivers nem pacotes globais automaticamente. Ubuntu 26.04 pode ter Python padrão fora dessa faixa: selecione um interpretador suportado já instalado. Consulte os links em `docs/compatibility.md`. Revise o fim do suporte do Ansible 12/Core 2.19 e disponibilidade de versões; não use este laboratório como produção. O pacote não confirma a versão do box ou a compatibilidade de seu host. Se houver bloqueio, não prossiga.

```bash
unzip sre-lab-v3.0.zip
cd sre-lab
make help
cp config/lab.example.yml config/lab.yml
# Edite config/lab.yml em seu editor
make test
make preflight
```

`lab.yml` usa o subconjunto JSON de YAML (aspas duplas, sem comentários). Isso permite validação com biblioteca padrão Python, sem dependência antes do bootstrap. Escolha a versão exata publicada do box `ubuntu/jammy64` com provider virtualbox/amd64, preencha `box_version`; ajuste o Python e os IPs conforme necessário. A rede exemplo é 192.168.57.0/24, distinta do exemplo anterior 192.168.56.0/24, mas **não se presume livre**. Confira `ip -4 route`, `VBoxManage list hostonlyifs`, `VBoxManage list dhcpservers`, `VBoxManage list vms`, VPNs e os CIDRs de clusters anteriores, inclusive rotas não visíveis. Reserve a faixa do MetalLB e VIP fora de DHCP. A rede deve ser nova/dedicada, /24, permitida no host-only do VirtualBox. Somente após revisão explícita marque `network_reviewed` e `compatibility_reviewed` como true. Não altere regras globais do VirtualBox para contornar conflito. A automação bloqueia rotas/VMs conflitantes visíveis; não detecta todos os conflitos possíveis.

## Instalação por etapas (recomendado na primeira vez)

Cada etapa mutável pede que digite o nome do projeto para confirmar; nenhuma é executada neste pacote automaticamente.

```bash
make bootstrap
make provision
make prepare
make cluster
make kubeconfig
make addons
make validate
./scripts/validate.sh --all --report
```

Durante `make prepare`, confirme os fingerprints ED25519 exibidos pelo console VirtualBox de cada VM recém-provisionada (`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`). Não copie a chave pública do resultado de uma conexão desconhecida para confiar nela. A automação compara o fingerprint da chave obtida na rede host-only; o Vagrant fornece as chaves de acesso privadas próprias. Sem confirmação, a fase para. Essa interação deliberada protege contra adoção de hosts errados. O próprio bootstrap Vagrant usa o mecanismo de SSH da box; não equivale à verificação posterior do Ansible.

Alternativa encadeada, após revisar os requisitos: `make install`. Ainda exige as confirmações de SSH e bloqueia se uma etapa falhar. Para retomar, execute a etapa pertinente após revisar o estado; instalação parcial do cluster/add-ons não é reaplicada cegamente. Consulte `docs/troubleshooting.md`. Não apague `.local` nem modifique identidades para contornar bloqueios.

## Acesso e rotina diária

```bash
# Apenas nesta sessão, não altera ~/.kube/config:
export KUBECONFIG="$PWD/.local/sre-lab.kubeconfig"
export PATH="$PWD/.local/bin:$PATH"
kubectl --context sre-lab get nodes
kubectl --context sre-lab get pods -A
kubectl --context sre-lab get storageclass,ingressclass
make status
make ssh NODE=worker-1
```

Se mudou `name`, use esse contexto. Freelens pode importar o arquivo exclusivo quando instalado. Não publique kubeconfig, credenciais ou `.local`. Para desligar, salve trabalhos e faça `make stop` (workers primeiro, CP por último). Para retornar, `make start` (CP primeiro) e `make validate`. Não é necessário reinstalar. Nenhuma sexta VM ou rede pública é criada.

## Auditoria

```bash
./scripts/validate.sh --stage provision
./scripts/validate.sh --stage prepare
./scripts/validate.sh --etcd
./scripts/validate.sh --network
./scripts/validate.sh --all --report
# Após revisão e com base saudável, autorize testes benignos no laboratório:
./scripts/validate.sh --all --active --report
```

Modo passivo consulta estado real; testes ativos criam namespace efêmero próprio, testam dois workers, DNS, HTTP via LB/Ingress, PVC com dado fictício e persistência no mesmo nó, depois removem somente seu namespace verificado. Não testam queda de CP. Se a limpeza falhar, investigue sem remover recursos alheios. `reports/` contém resultados locais sem dados sensíveis deliberadamente incluídos. Exit codes: 0 aprovado no escopo, 1 erro de saúde/comando, 2 configuração/destino bloqueado, 3 incompleto. Leia `docs/validation.md`.

## Incident Lab (já utilizável offline)

```bash
./scripts/incident.sh list
./scripts/incident.sh random
./scripts/incident.sh evidence 1
./scripts/incident.sh diagnosis 'Minha hipótese...'
./scripts/incident.sh mitigation 'Meu plano de mitigação...'
./scripts/incident.sh verify
./scripts/incident.sh hint
./scripts/incident.sh solution
./scripts/incident.sh close
./scripts/incident.sh report
```

O simulador usa dados fictícios e nunca modifica o cluster. `./scripts/recovery.sh` inicia nova sessão do mesmo caso, preservando histórico. Ele não é uma plataforma de injeção de falhas. Veja `incident-lab/README.md`.

## Próximos estudos

Siga `ROADMAP.md`: administração Kubernetes, Helm/Terraform, Git/GitHub, aplicação e SQL, Jenkins, Argo CD, observabilidade, performance, troubleshooting e SRE. AWS fora do escopo; multi-cluster e storage avançado ficam para depois.

## Verificações locais da fonte

`./scripts/static-check.sh` executa compilação Python, sintaxe Bash/Ruby, testes unitários e dry-run Makefile. Não acessa VMs. A revisão atual passou em **29 testes unitários** fora do host. A [validação real de 17/11/2026](docs/validacao-pratica-2026-11-17.md) é um registro pontual, não prova de idempotência nem homologação para instalações futuras.
