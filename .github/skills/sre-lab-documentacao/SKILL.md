---
name: sre-lab-documentacao
description: Documentar incrementalmente os temas do SRE LAB 3.0 no GitHub, com README.md prático, links no índice e validação após publicação. Use quando o usuário pedir para registrar, documentar, adicionar ou continuar um tema do SRE LAB.
---

# Skill — Documentação incremental do SRE LAB 3.0

## Objetivo

Transformar cada atividade prática do laboratório SRE em documentação Markdown clara, reutilizável e organizada no GitHub, sem apagar o histórico anterior.

## Repositório e convenções

- **Repositório:** `brunomori/workspace-devops-automation`
- **Branch padrão:** `main` (verificar antes de gravar).
- **Índice:** `sre-lab-3.0/README.md`
- **Temas:** `sre-lab-3.0/NN-nome-do-tema/README.md`
- **Tema inicial existente:** `sre-lab-3.0/01-iniciar-laboratorio/README.md`
- **Idioma:** português (Brasil), preservando nomes técnicos, comandos e arquivos.
- **Estilo:** didático, objetivo, mãos na massa, Markdown válido e comandos em blocos de código `bash`/`yaml` quando relevante.

## Gatilhos (pedidos equivalentes)

- "Documenta isso no SRE LAB."
- "Adiciona o Tema 02 ao GitHub."
- "Vamos continuar o SRE LAB 3.0."
- "Cria o README desse laboratório."
- "Usa a skill do SRE LAB."

## Fluxo obrigatório

1. **Entender o tema atual.** Utilizar o que foi efetivamente informado/feito na conversa. Se faltar um detalhe essencial para comandos corretos, consultar arquivos relevantes ou perguntar apenas o necessário. Não inventar saídas ou etapas validadas.
2. **Conferir o GitHub.** Ler o índice do SRE LAB, localizar a próxima numeração e conferir se já existe tema com mesmo assunto. Evitar duplicatas.
3. **Preparar o README.** Registrar objetivo, pré-requisitos, comandos, verificação de sucesso, troubleshooting e referências quando úteis. Indicar claramente o que foi *testado* versus *sugerido*.
4. **Criar ou atualizar o arquivo do tema.** Para tema novo, criar `NN-slug/README.md`. Para continuação do mesmo tema, atualizar o README correspondente com base na versão mais recente, sem apagar notas úteis.
5. **Atualizar o índice.** Adicionar link, descrição de uma linha e status real no `sre-lab-3.0/README.md`. Evitar editar a raiz do repositório sem necessidade.
6. **Verificar a publicação.** Buscar de volta os arquivos no GitHub e confirmar os links e conteúdo publicado.
7. **Responder com resultado.** Informar quais arquivos mudaram, incluir links diretos e destacar o próximo passo no laboratório.

## Estrutura sugerida para cada tema

```markdown
# Tema NN — Nome do tema

> SRE LAB 3.0 · objetivo em uma frase.

## Objetivo
Por que e o que será praticado.

## Pré-requisitos
Ferramentas, ambiente e dependências relevantes.

## Passo a passo
Comandos e explicações curtas.

## Validação
O que verificar e qual é o resultado esperado.

## Troubleshooting
Problemas observados e como investigá-los.

## Próximos passos
Como continuar o laboratório.

[← Índice do SRE LAB 3.0](../README.md)
```

Adaptar as seções: um guia de consulta rápida pode ser bem menor.

## Regras de segurança e qualidade

- **Nunca publicar** segredos, tokens, kubeconfig, credenciais, IPs sensíveis, dados pessoais, arquivos `.env`, IDs privados ou saídas com informações confidenciais. Sanitizar exemplos e revisar conteúdo antes de publicar.
- Não executar comandos destrutivos (`vagrant destroy`, `terraform destroy`, exclusões AWS etc.) apenas para documentar.
- Nunca confundir documentação com execução: publicar um comando **não significa** que foi executado nem validado no host.
- Preservar projetos e arquivos existentes; preferir pequenas alterações e commits descritivos.
- Conferir caminhos, nomes e versões quando houver alterações no laboratório.
- Publicar diretamente quando o usuário pedir a documentação no GitHub e houver acesso autorizado; caso contrário, entregar o Markdown pronto para commit.
- Se a conexão GitHub não estiver disponível, explicar e entregar o arquivo Markdown completo; não afirmar que houve publicação.

## Contexto do laboratório (confirmar a cada etapa)

Ambiente local Ubuntu com Vagrant, VirtualBox, Kubespray e Kubernetes. Estudos planejados: aplicação web e banco de dados, Jenkins/CI-CD, Helm, Argo CD/GitOps, Terraform/Terragrunt, observabilidade (Prometheus, Grafana, Zabbix), troubleshooting e runbooks. A topologia do cluster, as versões e os comandos locais podem mudar: validar antes de descrever como atuais.

## Atalho de uso

**Pedido curto:** "Documenta o que fizemos hoje no SRE LAB, seguindo a skill `sre-lab-documentacao` e atualiza o índice no GitHub."

Este arquivo é a fonte persistente das instruções. Assistentes devem consultar a versão atual no repositório quando forem solicitados a usar a skill; ela não é automaticamente carregada em toda conversa do ChatGPT.
