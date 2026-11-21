# DevOps Automation Workspace

Laboratório de estudos em automação DevOps e integração contínua com GitHub Actions.

## Estado atual

O workflow [`hello.yml`](.github/workflows/hello.yml) executa uma mensagem de teste em um runner Ubuntu quando ocorre um push na branch `main`. É um primeiro exercício de CI, não um pipeline de produção.

## Como verificar

1. Consulte a aba **Actions** do repositório.
2. Abra uma execução de **Hello GitHub Actions**.
3. Confira o resultado do job `say-hello` e o log da etapa.

## Roadmap

- [ ] Validar arquivos YAML e documentação em pull requests.
- [ ] Adicionar testes para scripts e manifestos de laboratório.
- [ ] Documentar permissões mínimas e troubleshooting dos workflows.
- [ ] Integrar exemplos de CI aos laboratórios de infraestrutura.

## Projetos relacionados

- [Kubernetes — exercícios](https://github.com/brunomori/Exercicio-Kubernets-)
- [Terraform](https://github.com/brunomori/Terraform)
- [Docker](https://github.com/brunomori/Docker)

Documentação em português; nomes de workflows e commits podem utilizar inglês técnico.

## SRE LAB 3.0

- [Acessar índice dos temas](sre-lab-3.0/README.md)
- [Tema 01 — Iniciar o laboratório](sre-lab-3.0/01-iniciar-laboratorio/README.md)
