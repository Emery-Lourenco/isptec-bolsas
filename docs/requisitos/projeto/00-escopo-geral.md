# 0. Escopo Geral do Projeto

## 0.1 Visão
**[Nome do Site]** é uma plataforma web que reúne bolsas de estudo a que angolanos podem candidatar-se (internas e externas, com cobertura integral ou parcial), liga os candidatos a **bolseiros voluntários verificados** que partilham a sua experiência sobre a bolsa, o país e a universidade, e oferece **mentorias pagas** a quem se quer candidatar, com um **chatbot** que orienta o candidato.

## 0.2 Tema oficial e como o projeto o cobre
| O tema pede | Como respondemos |
|-------------|------------------|
| Publicar bolsas de estudo | O administrador publica bolsas elegíveis para angolanos; o público vê a lista com filtros por tipo (interna/externa), cobertura (integral/parcial) e país. |
| Oferecer mentorias pagas | Catálogo de mentorias com preço em Kz; o candidato contrata e paga (pagamento simulado no MVP). |
| A quem se quer candidatar | Redirecionamento para a página oficial de candidatura de cada bolsa, comunidade de bolseiros e chatbot que responde às dúvidas. |

**Diferencial do projeto:** a comunidade de bolseiros. Estudantes que têm ou tiveram uma bolsa, ou que estudam fora de Angola, partilham de forma voluntária como funciona a bolsa, como é o país e como é a universidade. A equipa recruta os voluntários e garante que cada um realmente faz parte de uma bolsa ou estuda fora antes de publicar o perfil.

## 0.3 Estratégia em três fases
| Fase | Quando | Objetivo |
|------|--------|----------|
| **MVP** | Até 25 de outubro | Fluxo completo de ponta a ponta, simples e funcional |
| **Versão 2** | Depois do MVP | Bolseiros com conta própria, guias, alertas e mentores com conta |
| **Futuro** | A definir | Pagamento real, videochamadas, app móvel, entre outros |

Regra de ouro do MVP: fazer só o necessário, mas fazê-lo funcionar de ponta a ponta.

## 0.4 Atores
| Ator | MVP | Versão 2 |
|------|-----|----------|
| Visitante | Vê bolsas, bolseiros e mentorias e usa o chatbot | |
| Candidato | Regista-se, vai ao site oficial da bolsa, pede contacto com bolseiros e contrata mentorias | Favoritos, alertas, conversa com bolseiros pela plataforma |
| Administrador | Publica bolsas, verifica e cadastra bolseiros, encaminha pedidos de contacto e gere mentorias | Gere utilizadores e modera conteúdo |
| Bolseiro voluntário | Perfil cadastrado e verificado pelo administrador, sem conta | Conta própria, relatos publicados por ele e respostas pela plataforma |
| Chatbot | Responde a perguntas frequentes | |
| Mentor | | Conta própria; responde a pedidos de ajuda |

## 0.5 Módulos por fase
| Módulo | MVP | Versão 2 | Futuro |
|--------|-----|----------|--------|
| Bolsas | Publicar, listar, filtrar (tipo, cobertura, país), detalhe e link oficial | Favoritos, alertas de prazo, acompanhamento do estado da candidatura | Recomendação personalizada, importação semiautomática |
| Contas | Registo e login | Recuperar palavra-passe, perfil, gestão de utilizadores | |
| Comunidade de bolseiros | Perfis verificados, relatos, bolseiros por bolsa e pedido de contacto encaminhado pelo administrador | Bolseiros com conta, relatos próprios, perguntas e respostas pela plataforma, denúncia e moderação | |
| Mentorias | Catálogo pago e pagamento simulado | Guias, checklist de documentos, pedidos de ajuda a mentores, mentores com conta, avaliações | Pagamento real, videochamadas, chat em tempo real, alertas por WhatsApp ou SMS |
| Chatbot | Perguntas frequentes por palavras-chave e consulta de bolsas | | |
| Plataforma | Flask, PostgreSQL (Neon), Bootstrap | Emails automáticos | App móvel, versão em inglês |

## 0.6 Documentação
| Ficheiro | Conteúdo |
|----------|----------|
| `00-escopo-geral.md` | Visão completa e fases |
| `01-introducao.md` | Propósito, âmbito, atores, glossário |
| `02-requisitos-funcionais.md` | Todos os RF, com a fase (MVP ou V2) |
| `03-requisitos-nao-funcionais.md` | Todos os RNF |
| `04-casos-de-uso.md` | Todos os casos de uso e descrições |
| `05-documentacao-teorica.md` | Estrutura da parte teórica |
| `06-requisitos-futuros.md` | O que fica para depois |
| `07-metodo-recolha-bolsas.md` | Como encontrar e verificar as bolsas |
| `08-recrutamento-verificacao-bolseiros.md` | Como encontrar e verificar os bolseiros voluntários |
| `diagramas/casos-de-uso.puml` | Diagrama completo |
