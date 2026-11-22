# Troubleshooting e retomada

| Sintoma | Investigação não destrutiva |
|---|---|
| Bloqueio no preflight | `ip -4 route`, `VBoxManage list hostonlyifs`, `VBoxManage list dhcpservers`, `VBoxManage list vms`, memória e disco. Verifique arquivos de configuração. Não altere rede existente para forçar. |
| SSH não confiável | Compare fingerprint ED25519 pelo console da VM própria; confirme endereços/UUID. Não ignore StrictHostKeyChecking. |
| Bootstrap falha | Verifique DNS/Internet, Python/venv, commit, versões oficiais e hashes. Não troque versões silenciosamente. |
| VM parcial | Compare UUID local e Vagrant/VirtualBox. Se divergir, pare; não adote pelo nome. |
| Ansible falha | Revise playbook e pré-requisitos; reexecutar `make prepare` somente nas VMs registradas. |
| Cluster parcial | `make status`, `./scripts/validate.sh --stage cluster`, console das VMs próprias. Se a API e cinco nós estiverem saudáveis, `make cluster` tenta registrar/validar sem reinstalar; se incompleto, bloqueia. Analise logs e consulte upstream. Não há reset automatizado. |
| Add-ons parciais | `./scripts/validate.sh --metallb --ingress --storage`. Analise eventos e estado das releases com kubeconfig exclusivo. Não apagar namespace de ferramenta nem editar marcadores de estado para contornar a proteção. Retomada de instalação parcial exige revisão manual de propriedade e procedimento de manutenção específico. |
| PVC Pending | Verifique StorageClass e consumidor; WaitForFirstConsumer aguarda agendamento. Confira espaço real e eventos. |
| API inacessível | Confira IP VIP, certificados, rota host-only e saúde dos CP usando console/SSH verificado. Failover real não é executado automaticamente. |

Para qualquer investigação Kubernetes, exporte o kubeconfig exclusivo e contexto do projeto conforme README; consulte `kubectl get nodes`, `kubectl get pods -A`, `kubectl get events -A`, `kubectl describe` somente em objetos do laboratório. Não executar ações em contexto global. Não use comandos destrutivos como método genérico de recuperação. Os casos do Incident Lab são offline, sem alteração de infraestrutura.
