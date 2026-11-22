# Auditoria e aceite

`validate.sh --help` lista opções. `--stage preflight|bootstrap|provision|prepare|cluster|kubeconfig|addons|install` delimita fases; flags individuais `--host --vms --ssh --network --ansible --kubernetes --etcd --dns --metallb --ingress --storage` podem ser combinadas. `--all` consulta toda base. Relatórios locais texto, JSON e Markdown com escopo e tempos por check. PASS significa apenas o check executado; FAIL indica falha ou bloqueio, SKIP incapacidade de concluir; WARN reservado para avisos não bloqueantes. Códigos: 2 > 1 > 3 > 0. Modo passivo não cria recursos; usa consultas e SSH, pode gerar arquivos de relatório quando solicitado.

`--active` exige auditoria completa aprovada, identidade verificada e autorização. Cria namespace exclusivo com label/UID, quota, pods não privilegiados em dois workers, serviço/ingress e PVC `sre-test`. Verifica HTTP pelo host com header Host, sem alterar DNS; prova persistência somente local. Limpeza confirma UID e labels, para se encontrar objetos inesperados. Falhas ou interrupções podem deixar recursos próprios pendentes; não há limpeza genérica. O teste ativo não exercita falha de nós nem etcd. Não executar contra sistema externo.

| Aceite | Evidência esperada | Status na geração |
|---|---|---|
| AC-01–02 | 5 VMs próprias, 5 Ready | Pendente |
| AC-03 | 3 membros etcd saudáveis | Pendente |
| AC-04–05 | API TLS VIP, redundância CP; failover real em manutenção separada | Pendente; failover não automatizado |
| AC-06–10 | Teste ativo inter-worker, DNS, HTTP LB/Ingress, PVC e persistência | Pendente |
| AC-11–12 | Reexecução segura, ausência de alteração em outros ambientes | Pendente no host; nenhum acesso a VMs na geração |
| AC-13–14 | Auditoria, documentação e instalação reproduzível | Código entregue, execução pendente |
| AC-15 | Guardas, start/stop e isolamento | Testes unitários parciais; integração pendente |
| AC-16 | Catálogo, seleção, evidências, dicas, verificação e recuperação sintética | Teste local, ver relatório |
