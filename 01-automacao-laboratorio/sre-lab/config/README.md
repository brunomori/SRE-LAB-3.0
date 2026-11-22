# Configuração central

Copie `lab.example.yml` para `lab.yml`; o formato é JSON válido, também aceito como YAML. O schema executável é `config_validate()` em `scripts/lab.py`, com validação de chaves exatas, tipos, CIDRs, IPs, pool, topologia, timezone, recursos e revisão explícita. O `lab.yml` nunca é versionado. `versions.json` fixa referências do upstream e add-ons; alteração de versão/configuração depois do registro bloqueia a automação. Não há arquivos de credenciais nesta pasta.
