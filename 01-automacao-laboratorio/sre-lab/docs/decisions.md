# Decisões de implementação

- Configuração JSON (subconjunto YAML) para evitar instalar parser antes do preflight; schema validado em Python com chaves exatas. Os endereços são exemplos, não valores reservados. Vagrant e inventários derivam da mesma fonte.
- Bash como wrappers e Python 3 como orquestrador. Makefile tem alvos não paralelos; mutações pedem autorização, lock local, estado UUID e verificação do cluster por CA e UID.
- Kubespray upstream intacto, tag/commit fixados e ambiente Python separado. Ansible próprio prepara Linux apenas. Kubespray cuida do runtime, swap, módulos e sysctl.
- Calico VXLAN e kube-proxy iptables para simplicidade; interface interna detectada pelo IP em todas as VMs. Kube-vip somente CP. MetalLB externo mais recente que o nativo da tag; não duplicar instalação. Traefik em vez de ingress-nginx descontinuado; dashboard desativado. Helm só privado para bootstrap.
- Local Path externo em vez da versão nativa anterior; `Retain` para estudos e `Delete` para testes. Storage sem replicação, sem garantia de limite físico por PVC. Não instalar storage distribuído.
- Não executar novamente cluster/add-ons parciais sem revisão: resiliência conservadora, com bloqueio de estado ambíguo. Não destruir VMs nem redefinir Kubernetes. Retomada automática de todas as falhas não implementada.
- Incident Lab offline e dados sintéticos; não instalar mecanismos de falhas, não utilizar kubeconfig. Testes funcionais benignos separados do treinamento.
- Ferramentas futuras e ambientes ficam no roadmap, sem criação antecipada.
