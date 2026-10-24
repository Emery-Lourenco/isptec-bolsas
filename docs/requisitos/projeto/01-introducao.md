# 1. Introdução

## 1.1 Propósito
Este documento descreve os requisitos do sistema **[Nome do Site]**, uma plataforma web que reúne e divulga bolsas de estudo a que angolanos podem candidatar-se, liga os candidatos a bolseiros voluntários verificados e oferece mentorias pagas.

## 1.2 Problema
Muitos estudantes angolanos perdem oportunidades porque a informação sobre bolsas está dispersa em vários sites, quase sempre em inglês, e nem sempre é claro se os angolanos são elegíveis nem que custos o bolseiro terá de suportar. Faltam também orientação para preparar a candidatura e contacto com quem já passou pelo processo e pode contar como é a bolsa, o país e a universidade.

## 1.3 Objetivo
Centralizar, filtrar e divulgar bolsas elegíveis para angolanos, e ajudar o candidato a encontrar, escolher e preparar a sua candidatura, com a experiência de bolseiros verificados e com mentoria.

## 1.4 Âmbito
**MVP (entrega de 25 de outubro):**
- Publicação de bolsas pelo administrador e lista pública com filtros (tipo interna/externa, cobertura integral/parcial, país).
- Registo e login de candidatos.
- Redirecionamento para a página oficial de candidatura de cada bolsa.
- Comunidade de bolseiros voluntários verificados, com pedido de contacto encaminhado pelo administrador.
- Catálogo de mentorias pagas, contratação e pagamento simulado.
- Chatbot de perguntas frequentes.

**Versão 2:** bolseiros com conta própria e conversa pela plataforma, guias de mentoria, checklist de documentos, favoritos, alertas de prazo, pedidos de ajuda a mentores, mentores com conta própria e moderação.

**Fora do âmbito por agora:** pagamento real, videochamadas, chat em tempo real e candidatura dentro da plataforma (a candidatura faz-se sempre no site oficial da bolsa).

## 1.5 Atores
| Ator | Descrição |
|------|-----------|
| Visitante | Pessoa sem conta; pode ver e pesquisar bolsas, ver bolseiros e usar o chatbot. |
| Candidato | Angolano registado. |
| Administrador | Publica bolsas, verifica e cadastra bolseiros, encaminha pedidos de contacto, gere o catálogo de mentorias e (V2) os utilizadores. |
| Bolseiro voluntário | Estudante que tem ou teve uma bolsa, ou que estuda fora de Angola, e partilha a sua experiência. É verificado pela equipa antes de aparecer no site. |
| Mentor (V2) | Utilizador aprovado pelo administrador que orienta candidatos sobre documentos e processo de candidatura. |
| Chatbot | Assistente virtual que responde a perguntas frequentes sobre bolsas, candidatura e mentorias (ator secundário). |
| Sistema de notificações (V2) | Ator secundário; envia emails e alertas. |

Nota: um utilizador pode ter mais de um papel (ex.: ser bolseiro e mentor).

## 1.6 Glossário
| Termo | Significado |
|-------|-------------|
| RF | Requisito Funcional |
| RNF | Requisito Não Funcional |
| UC | Caso de Uso |
| MVP | Mínimo Produto Viável: a versão mais simples que funciona de ponta a ponta |
| Bolsa elegível | Bolsa que aceita candidaturas de cidadãos angolanos |
| Bolsa interna | Bolsa para estudar em Angola |
| Bolsa externa | Bolsa para estudar no estrangeiro |
| Cobertura integral | Bolsa 100% comparticipada: o bolseiro não paga nenhum dos custos principais |
| Cobertura parcial | Bolsa que cobre só parte dos custos; o bolseiro paga o restante |
| Bolseiro | Estudante que tem ou teve uma bolsa de estudo, ou que estuda fora de Angola |
| Bolseiro verificado | Bolseiro cuja situação foi confirmada pela equipa e que consentiu a publicação do perfil |
| Mentoria | Serviço pago de orientação sobre a candidatura, oferecido através do catálogo |
| Pagamento simulado | Registo do estado de pagamento (Pendente ou Pago) sem ligação a um meio de pagamento real |
| Chatbot | Programa que responde a perguntas por palavras-chave, sem inteligência artificial |
