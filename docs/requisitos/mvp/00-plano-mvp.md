# MVP: Plano de Entrega (até 25 de outubro)

## 1. Objetivo
Entregar até 25 de outubro um sistema que funciona de ponta a ponta: o administrador publica bolsas, o candidato consulta e é encaminhado para o site oficial, conhece bolseiros voluntários verificados, contrata uma mentoria e usa o chatbot. Regra de ouro: só o necessário, mas a funcionar.

## 2. Atores no MVP
| Ator | O que faz |
|------|-----------|
| Visitante | Vê bolsas, bolseiros e mentorias e usa o chatbot |
| Candidato | Regista-se, vai ao site oficial da bolsa para se candidatar, pede contacto com bolseiros e contrata mentorias |
| Administrador | Publica bolsas, verifica e cadastra bolseiros, encaminha pedidos de contacto e gere o catálogo de mentorias |
| Chatbot | Responde a perguntas frequentes (ator secundário) |
| Bolseiro voluntário | Não tem conta no MVP; o perfil é cadastrado pelo administrador depois da verificação |

## 3. O que entra no MVP
| Módulo | Funcionalidade | RF |
|--------|----------------|----|
| Contas | Registo e login do candidato; login do administrador | RF01, RF02 |
| Bolsas | O administrador cria, edita e remove bolsas | RF08 |
| Bolsas | Cada bolsa tem tipo (interna/externa), cobertura (integral/parcial), custos a cargo do bolseiro, prazo, requisitos, documentos, link oficial e confirmação de elegibilidade para angolanos | RF06, RF09, RF10, RF11 |
| Bolsas | Lista pública com filtros simples (tipo, cobertura, país) e selo "100% comparticipada" | RF03, RF04, RF12 |
| Bolsas | Detalhe da bolsa com botão "Candidatar-me" que leva à página oficial de candidatura; bolsas com prazo expirado deixam de aparecer na lista pública | RF05, RF07, RF13 |
| Bolseiros | O administrador cadastra perfis de bolseiros voluntários (bolsa, país, universidade, curso, apresentação, relato) e só os verifica depois de confirmar a situação | RF14 |
| Bolseiros | Secção "Comunidade de bolseiros" com filtro por país e bolsa, e bolseiros mostrados na página de cada bolsa | RF15, RF16 |
| Bolseiros | O candidato pede contacto com um bolseiro e o administrador encaminha o pedido | RF17, RF18 |
| Mentorias | Catálogo público (título, descrição, duração, preço em Kz) gerido pelo administrador | RF19, RF20 |
| Mentorias | O candidato contrata, indicando data e hora preferidas, e faz o pagamento simulado (Pendente ou Pago) | RF21, RF22 |
| Mentorias | Candidato e administrador veem as mentorias contratadas | RF23 |
| Chatbot | Responde por palavras-chave a perguntas sobre bolsas, candidatura, bolseiros e mentorias | RF24 |
| Chatbot | Consulta a base de dados para indicar bolsas (ex.: as 100% comparticipadas) | RF25 |

### O que NÃO fazer no MVP (para não exagerar)
Candidatura dentro da plataforma (a candidatura é sempre feita no site oficial da bolsa), envio de documentos, emails automáticos, recuperação de palavra-passe, favoritos, bolseiros com conta própria e conversa direta pela plataforma, guias de mentoria, checklist de documentos, moderação e pagamentos reais.

## 4. Bolseiros voluntários: o diferencial
A comunidade de bolseiros distingue o projeto de um simples agregador de bolsas. No MVP é simples e controlada:
- O administrador cadastra os perfis depois de confirmar que o voluntário tem ou teve uma bolsa, ou que estuda fora de Angola, e de ter o seu consentimento.
- Os perfis verificados mostram o selo "Bolseiro verificado" e o relato sobre a bolsa, o país e a universidade.
- O candidato pede contacto e o administrador encaminha o pedido, para proteger os contactos dos voluntários.
- Meta: pelo menos 5 perfis verificados até 23 de outubro.
- Plano B: se faltar tempo, cortar o pedido de contacto (RF17 e RF18) e manter a comunidade.

O método para encontrar e verificar os voluntários está no ficheiro `05-bolseiros-voluntarios-mvp.md`.

## 5. Regras de negócio assumidas (confirmar com o professor)
| # | Dúvida | Proposta para o MVP |
|---|--------|---------------------|
| 1 | Como se paga a mentoria? | Pagamento simulado (Pendente/Pago). Pagamento real fica para o futuro. |
| 2 | Que moeda? | Kwanza (Kz). |
| 3 | Campos obrigatórios da bolsa? | Título, entidade, tipo, cobertura, prazo, link oficial e confirmação de elegibilidade para angolanos; custos a cargo do bolseiro se a cobertura for parcial. |
| 4 | O que acontece depois do prazo? | A bolsa deixa de aparecer na lista pública; o administrador continua a vê-la. |
| 5 | Como se faz a candidatura? | Sempre no site oficial da bolsa; o nosso site redireciona o candidato. |
| 6 | O site acompanha o estado das candidaturas? | Não no MVP; fica para a versão 2. |
| 7 | Quem são os mentores? | O administrador regista as mentorias no catálogo (nome do mentor como texto). Conta própria para mentores fica na versão 2. |
| 8 | Como se agenda a mentoria? | O candidato indica data e hora preferidas; a confirmação é feita pelo administrador fora do sistema. |
| 9 | Quem publica bolsas? | Só o administrador. |
| 10 | Que idioma? | Português. |
| 11 | Quem são os bolseiros e como entram no site? | Voluntários que tenham ou tenham tido uma bolsa, ou que estudem fora de Angola. Só entram depois de verificados e de darem o consentimento. |
| 12 | Como fala o candidato com um bolseiro? | Faz um pedido de contacto; o administrador encaminha-o ao bolseiro, sem revelar contactos pessoais. |

## 6. Fluxo de demonstração
1. O administrador faz login e publica uma bolsa (tipo, cobertura e custos preenchidos).
2. O visitante vê a lista, filtra pelas bolsas 100% comparticipadas e abre o detalhe.
3. Na página da bolsa, vê os bolseiros que a obtiveram e abre o perfil de um bolseiro verificado.
4. O candidato regista-se e faz login.
5. O candidato pede contacto com o bolseiro, escrevendo a sua pergunta.
6. O candidato clica em "Candidatar-me" e é encaminhado para a página oficial da bolsa.
7. O candidato pergunta ao chatbot como funciona a mentoria e que bolsas integrais existem.
8. O candidato contrata uma mentoria e faz o pagamento simulado.
9. O administrador consulta os pedidos de contacto e as mentorias contratadas.

## 7. Dados mínimos (proposta para a Domingas e o Emery ajustarem)
A tabela `bolsas` já existe na nuvem; falta acrescentar `tipo`, `cobertura` e `custos_bolseiro`.

| Tabela | Campos principais |
|--------|-------------------|
| `utilizadores` | id, nome, email, senha (encriptada), papel (admin/candidato) |
| `bolsas` | id, titulo, entidade, pais, tipo, cobertura, custos_bolseiro, nivel_estudo, requisitos, documentos, prazo, link_oficial, elegivel_angola |
| `bolseiros` | id, nome, situacao (atual/antigo/estudante no estrangeiro), bolsa_id (opcional), bolsa_nome, pais, universidade, curso, ano, apresentacao, relato, email_contacto_privado, verificado, verificado_em, consentimento_em |
| `pedidos_contacto` | id, utilizador_id, bolseiro_id, pergunta, estado (Pendente/Encaminhado/Respondido), criado_em |
| `mentorias` | id, titulo, descricao, duracao_min, preco_kz, mentor_nome, ativa |
| `contratacoes_mentoria` | id, utilizador_id, mentoria_id, data_hora_preferida, estado_pagamento, criada_em |

O chatbot não precisa de tabela: as regras ficam no código Python. O campo `email_contacto_privado` nunca aparece nas páginas públicas.

## 8. Tecnologia e organização
| Aspeto | Escolha |
|--------|---------|
| Linguagem e framework | Python com Flask |
| Base de dados | PostgreSQL na nuvem (Neon), partilhada pela equipa |
| Interface | HTML e Bootstrap |
| Segredos | Ficheiro `.env`, fora do repositório |
| Versões | Git e GitHub: uma branch por membro e Pull Request para a `main` |

## 9. Quem faz o quê
| Membro | Branch | Entrega |
|--------|--------|---------|
| Emery | `feature/backend-python` | Rotas Flask: login, bolsas, bolseiros, pedidos de contacto, mentorias, contratações e lógica do chatbot |
| Domingas | `feature/database` | Scripts SQL das tabelas (incluindo `bolseiros` e `pedidos_contacto`), ajuste da tabela `bolsas` e dados de exemplo |
| Luciano | `feature/frontend` | Telas: lista e detalhe de bolsas, login e registo, comunidade e perfil de bolseiro, pedido de contacto, mentorias, painel do administrador e janela do chatbot |
| Josenilson | `docs/requisitos` | Requisitos, casos de uso e diagrama; coordena a verificação dos bolseiros voluntários; guião da apresentação |
| Toda a equipa | | Cada membro traz pelo menos 2 contactos de possíveis bolseiros voluntários |

## 10. Calendário sugerido
| Data | Foco |
|------|------|
| 18 de outubro | Fechar escopo e regras com a equipa; modelo de dados; wireframes; começar a contactar voluntários |
| 19 a 21 de outubro | Implementar em paralelo: bolsas e login, bolseiros, mentorias e chatbot; verificar os primeiros bolseiros |
| 22 de outubro | Juntar as branches na `main` e testar o fluxo completo (sem novas funcionalidades depois deste dia) |
| 23 de outubro | Corrigir erros, carregar dados de exemplo e perfis verificados, fechar a documentação |
| 24 de outubro | Ensaio da apresentação |
| 25 de outubro | Entrega (domingo; confirmar a hora limite) |

## 11. O MVP está concluído quando
- [ ] O administrador faz login e publica, edita e remove bolsas.
- [ ] O visitante vê a lista, filtra por tipo e cobertura e abre o detalhe.
- [ ] O candidato regista-se, faz login e é encaminhado para o site oficial da bolsa.
- [ ] Existem pelo menos 3 perfis de bolseiros verificados publicados (se não houver, perfis de exemplo marcados como "Exemplo").
- [ ] O candidato pede contacto com um bolseiro e o administrador vê o pedido.
- [ ] O catálogo de mentorias funciona e a contratação fica registada com estado de pagamento.
- [ ] O chatbot responde a, pelo menos, as perguntas frequentes definidas pela equipa.
- [ ] O administrador vê os pedidos de contacto e as mentorias contratadas.
- [ ] O fluxo da secção 6 corre do princípio ao fim sem erros.
- [ ] A documentação (RF, RNF, casos de uso e diagrama) está entregue.

## 12. Guião da apresentação (5 a 7 minutos)
1. O problema: informação dispersa sobre bolsas e dúvidas sobre a candidatura e a vida no estrangeiro.
2. A solução e as três fases do projeto.
3. O diferencial: bolseiros voluntários verificados que partilham a sua experiência.
4. Requisitos e diagrama de casos de uso do MVP.
5. Demonstração ao vivo (fluxo da secção 6).
6. Próximos passos: versão 2 e futuro.

## 13. Correspondência com a lista inicial da equipa
| Lista inicial | Nesta documentação |
|---------------|--------------------|
| RF01 Admin faz login e cria bolsas | RF02, RF08, RF09 a RF11 |
| RF02 Visitante vê lista de bolsas | RF03, RF04, RF05 |
| RF03 Candidato submete candidatura | RF07 (redireciona para o site oficial) |
| RF04 Catálogo de mentorias pagas | RF19, RF21, RF22 |
| RF05 Chatbot | RF24, RF25 |
| RNF01 Browser web | RNF13 |
| RNF02 Python com Flask | RNF10 |
| RNF03 Dados numa base de dados | RNF11 |

## 14. Documentos do MVP
| Ficheiro | Conteúdo |
|----------|----------|
| `00-plano-mvp.md` | Este documento |
| `01-introducao-mvp.md` | Propósito, âmbito, atores e glossário do MVP |
| `02-requisitos-funcionais-mvp.md` | 25 requisitos funcionais |
| `03-requisitos-nao-funcionais-mvp.md` | 13 requisitos não funcionais |
| `04-casos-de-uso-mvp.md` | 15 casos de uso com descrição |
| `05-bolseiros-voluntarios-mvp.md` | Como encontrar e verificar os primeiros bolseiros |
| `diagramas/casos-de-uso-mvp.puml` | Diagrama de casos de uso |
