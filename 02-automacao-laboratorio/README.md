# Tema 02 — Script de automação do SRE LAB 3.0

> **SRE LAB 3.0 · Documentação do orquestrador Python, comandos e fluxo de operação.**

Este tema documenta como o arquivo [**sre-lab/scripts/lab.py**](sre-lab/scripts/lab.py) gerencia a fundação do laboratório. A automação é executada no **host Ubuntu**, interage com Vagrant/VirtualBox e coordena Ansible/Kubespray e o Kubernetes local. A intenção é estudar **cada etapa**, validar o estado e praticar troubleshooting, sem executar comandos às cegas.

**Importante sobre esta publicação:** o código acima é a versão revisada do orquestrador, baseada no arquivo enviado após a instalação real. Ele é disponibilizado para estudo e versionamento; **não é um projeto executável isoladamente**. Para executar os comandos abaixo, é necessário o **pacote completo do SRE LAB** (Makefile, config, vagrant, ansible, addons, scripts, testes e dependências) já existente no Ubuntu. Copiar somente este lab.py para uma pasta vazia não instala o laboratório. **A publicação no GitHub não altera o cluster local.**

## 1. O que o script faz

- **Valida o host e a configuração:** Linux Ubuntu x86_64, Python compatível, VirtualBox, Vagrant, RAM, disco, redes e endereços.
- **Protege o ambiente existente:** identifica VMs próprias por UUID, valida a identidade do cluster, compara host keys e não assume VMs desconhecidas.
- **Orquestra a instalação inicial:** bootstrap → VMs → preparação Linux → Kubespray → kubeconfig → add-ons.
- **Gerencia a rotina:** status, start, stop e SSH, sem reinstalar o cluster.
- **Audita saúde:** nós, API, etcd, DNS, MetalLB, Traefik e armazenamento.
- **Suporta estudos de incidentes:** scripts de validação e simulador offline incluídos no pacote completo.

### Fluxo do orquestrador

~~~mermaid
flowchart TD
    A["Ubuntu host: Makefile / lab.py"] --> B["Preflight: recursos, rede, identidades"]
    B --> C["Bootstrap: dependências locais"]
    C --> D["Vagrant + VirtualBox: 5 VMs"]
    D --> E["SSH + Ansible: preparar e validar"]
    E --> F["Kubespray: Kubernetes"]
    F --> G["Kubeconfig isolado"]
    G --> H["Add-ons: MetalLB, Traefik, storage"]
    H --> I["Auditoria e operação SRE"]
    I --> J["make status / start / stop / validate"]
~~~

Topologia prevista no script: **3 control planes/etcd (master-1, master-2, master-3)** e **2 workers (worker-1, worker-2)**. O projeto usa rede privada local; nenhum serviço externo deve ser presumido como alvo.

## 2. Arquivos envolvidos

| Arquivo ou diretório (no pacote completo) | Responsabilidade |
| --- | --- |
| [scripts/lab.py](sre-lab/scripts/lab.py) | Orquestrador central em Python (código revisado publicado aqui). |
| Makefile | Atalhos para chamar as ações do orquestrador. |
| config/lab.example.yml | Modelo de configuração de recursos, IPs, rede, box e margens. |
| config/lab.yml | Configuração efetiva e local; não deve ser publicada. |
| config/versions.json | Versões e referências de dependências. |
| vagrant/Vagrantfile | Definição das cinco VMs. |
| ansible/ | Preflight remoto, preparação e verificação de hosts. |
| addons/ | Configuração do Ingress, LoadBalancer e storage. |
| scripts/validate.sh | Interface para auditorias e testes funcionais. |
| scripts/incident.sh | Simulador offline de incidentes (sem injetar falhas reais). |
| tests/test_lab.py | Testes automatizados do orquestrador. |
| .local/ | Identidades, fingerprints, inventário, binários e kubeconfig locais. **Nunca publicar ou apagar para corrigir erros.** |

O GitHub deste tema contém o **[pacote-fonte completo](sre-lab/)**, com o orquestrador, testes e documentação. A pasta privada .local e os recursos em execução no computador permanecem fora do repositório.

## 3. Pré-requisitos

No host: Ubuntu x86_64, VirtualBox funcional, Vagrant, Git, Make, OpenSSH, iproute2, curl, internet para bootstrap e uma versão Python admitida pela configuração do laboratório (**3.11, 3.12 ou 3.13**). A versão do box e as dependências do Kubespray devem ser revisadas antes de uma instalação nova.

Antes de uma **primeira instalação**, confira também: conflito de redes host-only/VPN, IPs dos nós, VIP da API, pool MetalLB, RAM e espaço em disco. O exemplo de configuração usa mínimo de **60 GiB livres para provisionamento**; isso não é garantia de espaço total suficiente. A instalação exige autorização interativa.

### No laboratório **já instalado e funcionando**

Trabalhe **na pasta local que contém o Makefile e o estado .local**; não substitua arquivos só para acompanhar esta documentação:

~~~bash
cd ~/Downloads/sre-lab
make help
make status
~~~

**make status** consulta o estado registrado das VMs e dos add-ons. Não recria recursos nem reinicia o cluster. Se o projeto estiver em outro diretório, ajuste o caminho.

## 4. Rotina de uso diário — passo a passo

### 4.1. Consultar o estado antes de agir

~~~bash
cd ~/Downloads/sre-lab
make status
~~~

Mostra as máquinas registradas e se cluster/add-ons constam na identidade local. Se ocorrer divergência de UUID ou falta de .local, **pare**: não tente adotar VMs ou recriar a identidade automaticamente.

### 4.2. Iniciar as cinco VMs existentes

~~~bash
make start
~~~

Liga as VMs próprias, sem reprovisioná-las. A lógica inicia os control planes antes dos workers. A versão revisada utiliza **15 GiB livres como piso operacional de retomada**; já a primeira instalação continua sujeita ao mínimo configurado. A verificação de RAM também pode impedir a inicialização se não houver margem.

### 4.3. Apontar o kubectl para o laboratório

No **mesmo terminal**:

~~~bash
export KUBECONFIG="$PWD/.local/sre-lab.kubeconfig"
export PATH="$PWD/.local/bin:$PATH"
kubectl --context sre-lab get nodes -o wide
kubectl --context sre-lab get pods -A
~~~

Se o campo name em config/lab.yml não for sre-lab, use o nome de contexto correspondente. O script **não substitui** o kubeconfig global automaticamente.

### 4.4. Auditar o cluster

~~~bash
make validate
~~~

Executa verificações passivas de saúde, incluindo host, VMs, SSH, rede, cluster e add-ons. **Não injeta falhas reais**. Para relatórios e testes ativos, o pacote completo também oferece:

~~~bash
./scripts/validate.sh --all --report
# Somente quando quiser testes funcionais com recursos efêmeros no cluster:
./scripts/validate.sh --all --active --report
~~~

O modo ativo solicita autorização, cria objetos temporários em um namespace dedicado e tenta removê-los após verificar a identidade. Não equivale a testar failover de control plane. Se ocorrer erro na limpeza, investigue o estado antes de apagar qualquer recurso.

### 4.5. Acessar uma VM

~~~bash
make ssh NODE=master-1
# Dentro da VM, ao finalizar:
exit
~~~

Também é possível selecionar master-2, master-3, worker-1 ou worker-2. A conexão deve respeitar o inventário, as chaves e a identidade SSH previamente confirmados.

### 4.6. Desligar preservando os discos

~~~bash
make stop
~~~

Encerra as VMs do projeto (workers antes dos control planes). **Não é o mesmo que vagrant destroy**. Antes de desligar, finalize operações e testes em andamento. Para voltar outro dia, use **make start**, não **make install**.

## 5. Instalação inicial — entender cada fase, sem executá-la no cluster já pronto

O fluxo abaixo é **para um ambiente novo e revisado**, com o pacote completo e sem VMs conflitantes. **Não execute make install, provision, cluster ou addons por curiosidade em um ambiente que já funciona.**

| Etapa | Comando | O que acontece |
| --- | --- | --- |
| 0 | make help | Lista os comandos sem modificar infraestrutura. |
| 1 | make test | Executa testes unitários do código. |
| 2 | make preflight | Verifica host, dependências, recursos e redes; não cria VMs. |
| 3 | make bootstrap | Prepara dependências isoladas, Kubespray, ferramentas e artefatos. |
| 4 | make provision | Cria/inicia **apenas VMs identificadas como pertencentes ao projeto**. |
| 5 | make prepare | Verifica host keys por console; executa Ansible nas VMs do laboratório. |
| 6 | make cluster | Instala Kubernetes pelo Kubespray e verifica o estado da API. |
| 7 | make kubeconfig | Obtém kubeconfig isolado e registra a identidade do cluster. |
| 8 | make addons | Configura MetalLB, Traefik e armazenamento local. |
| 9 | make validate | Confere a saúde do ambiente. |
| Alternativa | make install | Encadeia as fases anteriores, com confirmações; **apenas primeira instalação controlada**. |

A preparação pressupõe configurar o arquivo local a partir de config/lab.example.yml, preencher a versão real da box, conferir a compatibilidade, revisar rede/sub-rede e marcar as flags de revisão somente após a checagem. O projeto guarda checkpoints locais, mas eles **não substituem** a verificação do estado real após falhas.

### Confirmação de fingerprint SSH

Durante a primeira execução de **make prepare**, a identidade de cada VM deve ser confrontada com o console da VM própria. Exemplo de comando **dentro do console**:

~~~bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
~~~

A revisão aceita o fingerprint SHA256 ou a linha ED25519 completa. **Não aceite uma chave apenas porque foi apresentada pelo ssh-keyscan**.

## 6. Principais funções do lab.py

| Bloco do código | Responsabilidade |
| --- | --- |
| config_validate / config | Validação de esquema JSON/YAML, nós, IPs, recursos e redes. |
| state / owned | Identidade da instalação e verificação de VMs por UUID. |
| host_check | Driver VirtualBox, Python, RAM, disco, rotas e host-only. |
| authorize | Confirmação humana antes das operações que modificam estado. |
| bootstrap / bootstrap_check | Dependências e verificações de integridade dos artefatos. |
| provision | Criação ou retomada das cinco VMs registradas. |
| trust_ssh / ssh / network_check | Fingerprints, acesso remoto e conectividade entre nós. |
| generate_inventory / prepare | Inventários, Ansible, preflight e configuração Linux. |
| deploy_cluster / register / guard | Kubespray, registro e proteção da identidade Kubernetes. |
| addons / apply_objects | MetalLB, Ingress e provisionador de armazenamento. |
| audit / active_tests | Diagnósticos, relatórios e validação funcional efêmera. |
| main / parser | Interface de linha de comando, bloqueios e tratamento de erros. |

## 7. Problemas reais encontrados e melhorias

| Sintoma observado durante a implantação | Causa ou melhoria |
| --- | --- |
| Preflight de VirtualBox bloqueava indevidamente | A verificação do dispositivo de usuário foi corrigida para /dev/vboxdrvu. |
| Problema ao gerar known_hosts | Tratamento das linhas de ssh-keyscan e verificação de fingerprints corrigidos. |
| make start falhava com piso de 60 GiB | Piso operacional separado: **15 GiB na retomada**, mínimo configurado no provisionamento. |
| Entrada do fingerprint difícil de copiar | Aceita a linha completa do ssh-keygen -lf, sem dispensar a validação. |
| Mensagem de pouco disco não explicava o motivo | Informa margem usada e espaço disponível. |
| Interrupção com Ctrl+C | Orienta conferir status e validação; sem rollback automático. |
| VirtualBox não suporta encolher VDI existente | Aviso do hypervisor; não autoriza excluir/recriar discos. |
| Guest Additions divergentes | Aviso a investigar se recursos dependentes falharem; não presume erro do cluster. |
| Clock skew detected | Investigar horário e timestamps; não alterar relógio automaticamente. |

**Qualidade do código:** a revisão publicada teve **29 testes unitários aprovados** e verificação de sintaxe Python/Bash no ambiente de geração. Isso não é certificação de uma nova instalação real; o cluster já existente foi validado separadamente durante os estudos.

## 8. Troubleshooting e diagnóstico

~~~bash
cd ~/Downloads/sre-lab

# Identidades e estado das VMs (consulta):
make status

# Testes de código, sem alterar infraestrutura:
make test
python3 -m py_compile scripts/lab.py

# Conferência passiva do ambiente:
make validate

# Consultas independentes ao host:
df -h /
free -h
VBoxManage list vms
ip -4 route
~~~

Se o erro indicar **identidade divergente**, **host key diferente**, **configuração alterada após o registro** ou **cluster pré-existente**, interrompa a automação. Nunca remova .local ou desabilite verificações de SSH para tentar prosseguir.

Códigos de saída do orquestrador: **0 = aprovado**, **1 = falha de saúde**, **2 = bloqueio/configuração**, **3 = auditoria incompleta**, **130 = interrompido**. Leia o erro específico antes de repetir uma fase.

## 9. Prática SRE: investigar incidentes

O pacote completo inclui um **simulador offline**; ele não derruba workloads:

~~~bash
./scripts/incident.sh list
./scripts/incident.sh random
./scripts/incident.sh evidence 1
./scripts/incident.sh diagnosis 'Minha hipótese'
./scripts/incident.sh mitigation 'Minha mitigação'
./scripts/incident.sh verify
./scripts/incident.sh close
./scripts/incident.sh report
~~~

A ideia é exercitar **evidências → hipótese → causa → mitigação → verificação → post-mortem**. Recriar ambientes de laboratório é aceitável, mas código, documentação e configurações não sensíveis devem permanecer versionados.

## 10. Segurança e manutenção

- **Não publicar:** .local/, kubeconfigs, chaves, tokens, inventários privados, config/lab.yml ou relatórios com dados sensíveis.
- **Não executar:** vagrant destroy, kubeadm reset ou make install em um cluster saudável apenas para atualizar documentação.
- **Versionamento:** o script nesta pasta é uma **referência revisada**. O arquivo no Ubuntu permanece independente; mudanças no GitHub não são aplicadas automaticamente.
- **Limites:** este script provisiona **a fundação Kubernetes**. Jenkins, Argo CD, Prometheus, Grafana, Datadog, Zabbix, Terraform/Terragrunt e bancos são etapas posteriores do roadmap; sua presença no diagrama principal não significa instalação por este script.

---

[← Voltar à visão geral do SRE LAB 3.0](../README.md) · [Tema 01 — Iniciar o laboratório](../01-iniciar-laboratorio/README.md)
