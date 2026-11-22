# Tema 02 — Iniciar o laboratório

> **SRE LAB 3.0** · Guia rápido para subir o ambiente local no Ubuntu.

## 1. Entrar na pasta do laboratório

```bash
cd ~/Downloads/sre-lab
```

> Se você moveu o projeto, ajuste o caminho para a pasta que contém o `Makefile` e o `Vagrantfile`.

## 2. Iniciar as máquinas virtuais

```bash
make start
```

O ambiente utiliza **Vagrant + VirtualBox** e um cluster **Kubernetes provisionado com Kubespray**. Este comando pressupõe que o alvo `start` esteja definido no `Makefile` local.

## 3. Configurar o acesso ao Kubernetes

No **mesmo terminal** e na pasta do laboratório:

```bash
export KUBECONFIG="$PWD/.local/sre-lab.kubeconfig"
export PATH="$PWD/.local/bin:$PATH"
```

> Os `export` valem para a sessão atual do terminal; repita-os ao abrir um novo terminal.

## 4. Validar se tudo subiu

```bash
vagrant status
kubectl config current-context
kubectl get nodes -o wide
kubectl get pods -A
```

**Resultado esperado:** VMs em execução, nós Kubernetes em `Ready` e os componentes principais do cluster saudáveis. Se algo não estiver `Ready`, investigue antes de instalar aplicações.

## 5. Acessar uma VM (opcional)

```bash
make ssh NODE=master-1
```

Para sair da VM:

```bash
exit
```

## 6. Encerrar o laboratório

Na máquina **host**, dentro da pasta do Vagrantfile:

```bash
vagrant halt
```

Esse comando desliga as VMs gerenciadas pelo Vagrant sem destruí-las. **Não use `vagrant destroy` para encerrar a sessão**, pois ele remove as VMs.

## Checagens rápidas

| Situação | O que conferir |
| --- | --- |
| `make start` não existe | Verifique se está na pasta correta e confira os alvos do `Makefile`. |
| `kubectl` não conecta | Confira o arquivo `$KUBECONFIG`, o contexto atual e o status das VMs. |
| Nó em `NotReady` | Verifique `kubectl describe node <nome-do-node>` e os Pods de `kube-system`. |
| Comando funciona só em um terminal | Repita os `export` da etapa 3. |

---

[← Índice do SRE LAB 3.0](../README.md) · [Tema 01 — Automação do laboratório](../01-automacao-laboratorio/README.md)

**Observação:** este documento registra o procedimento de inicialização utilizado no laboratório local. Os caminhos e alvos do `Makefile` devem ser conferidos caso a estrutura local mude.
