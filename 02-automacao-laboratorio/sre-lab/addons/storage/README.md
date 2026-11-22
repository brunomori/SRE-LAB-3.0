# Storage local

O manifesto Local Path v0.0.37 é obtido do upstream; o script fixa a imagem do helper no manifesto derivado. As classes próprias usam WaitForFirstConsumer; `sre-local` padrão Retain e `sre-test` Delete. A classe upstream `local-path` permanece não padrão. Não há quota física garantida nem replicação; o espaço disponível depende do disco da VM. Backups são necessários.
