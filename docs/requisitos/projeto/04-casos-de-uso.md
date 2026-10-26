# 4. Casos de Uso

## 4.1 Diagrama
Ver `diagramas/casos-de-uso.puml` (PlantUML). Para gerar a imagem: https://www.plantuml.com/plantuml ou extensão PlantUML do VS Code.

## 4.2 Lista
| ID | Caso de uso | Ator principal | RF relacionados | Fase |
|----|-------------|----------------|-----------------|------|
| UC01 | Registar-se | Visitante | RF01 | MVP |
| UC02 | Autenticar-se | Candidato, Admin | RF02, RF03 | MVP |
| UC03 | Pesquisar e filtrar bolsas | Todos | RF05, RF06 | MVP |
| UC04 | Ver detalhes da bolsa | Todos | RF07, RF35 | MVP |
| UC05 | Candidatar-se a bolsa | Candidato | RF09 (RF10 em V2) | MVP |
| UC06 | Guardar bolsa favorita | Candidato | RF11 | V2 |
| UC07 | Gerir perfil | Candidato | RF04 | V2 |
| UC08 | Gerir bolsas | Admin | RF08, RF13, RF15, RF26 a RF29 | MVP |
| UC09 | Gerir utilizadores | Admin | RF14 | V2 |
| UC10 | Receber alertas de prazo | Sistema de notificações | RF12 | V2 |
| UC11 | Consultar guias de mentoria | Todos | RF16, RF18 | V2 |
| UC12 | Pedir ajuda a um mentor | Candidato | RF20, RF22, RF23, RF25 | V2 |
| UC13 | Responder pedido de ajuda | Mentor | RF21, RF23 | V2 |
| UC14 | Gerir guias de mentoria | Admin, Mentor | RF17 | V2 |
| UC15 | Gerir mentores | Admin | RF24 | V2 |
| UC16 | Gerir checklist de documentos | Candidato | RF19 | V2 |
| UC17 | Explorar comunidade de bolseiros | Todos | RF34, RF35 | MVP |
| UC18 | Perguntar a um bolseiro | Candidato | RF36, RF37, RF38 | V2 |
| UC19 | Responder a candidato | Bolseiro | RF37, RF38 | V2 |
| UC20 | Gerir perfil e relatos de bolseiro | Bolseiro | RF32, RF33 | V2 |
| UC21 | Pedir verificação como bolseiro | Candidato | RF30 | V2 |
| UC22 | Verificar bolseiros | Admin | RF31 | V2 |
| UC23 | Denunciar e moderar conteúdo | Todos, Admin | RF39 | V2 |
| UC24 | Consultar catálogo de mentorias | Todos | RF40 | MVP |
| UC25 | Contratar mentoria (pagamento simulado) | Candidato | RF42, RF43 | MVP |
| UC26 | Gerir catálogo de mentorias | Admin | RF41 | MVP |
| UC27 | Conversar com o chatbot | Todos, Chatbot | RF45, RF46 | MVP |
| UC28 | Consultar mentorias contratadas | Candidato, Admin | RF44 | MVP |
| UC29 | Pedir contacto com um bolseiro | Candidato | RF48 | MVP |
| UC30 | Gerir bolseiros voluntários | Administrador | RF47 | MVP |
| UC31 | Tratar pedidos de contacto | Administrador | RF49 | MVP |

## 4.3 Descrições detalhadas

### UC01: Registar-se
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante |
| Pré-condição | O visitante não tem conta. |
| Fluxo principal | 1. Visitante abre a página de registo. 2. Preenche nome, email e palavra-passe. 3. Sistema valida os dados. 4. Sistema cria a conta e envia email de confirmação. |
| Fluxo alternativo | 3a. Email já registado: o sistema informa e sugere login. 3b. Palavra-passe fraca: o sistema pede nova palavra-passe. |
| Pós-condição | Conta criada. |

### UC02: Autenticar-se
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato, Administrador |
| Pré-condição | O utilizador tem conta. |
| Fluxo principal | 1. Utilizador introduz email e palavra-passe. 2. Sistema valida. 3. Sistema inicia sessão. |
| Fluxo alternativo | 2a. Credenciais inválidas: mensagem de erro. 2b. Esqueceu a palavra-passe: sistema envia link de recuperação. |
| Pós-condição | Sessão iniciada. |

### UC03: Pesquisar e filtrar bolsas
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Nenhuma. |
| Fluxo principal | 1. Utilizador abre a lista de bolsas. 2. Aplica filtros (país, tipo interna/externa, cobertura integral/parcial, nível, área, prazo) ou escreve uma pesquisa. 3. Sistema mostra os resultados. |
| Fluxo alternativo | 3a. Sem resultados: sistema sugere remover filtros. |
| Pós-condição | Lista filtrada apresentada. |

### UC04: Ver detalhes da bolsa
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | A bolsa existe e está ativa. |
| Fluxo principal | 1. Utilizador seleciona uma bolsa. 2. Sistema mostra descrição, tipo (interna/externa), cobertura (integral/parcial), custos a cargo do bolseiro, requisitos, documentos, prazo, link oficial e bolseiros que obtiveram a bolsa. |
| Fluxo alternativo | 1a. Bolsa arquivada: sistema indica que o prazo terminou. |
| Pós-condição | Detalhes apresentados. |

### UC05: Candidatar-se a bolsa
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; bolsa ativa. |
| Fluxo principal | 1. Candidato clica em "Candidatar-me". 2. Sistema abre a página oficial de candidatura da bolsa, num novo separador. (Versão 2: ao voltar, o candidato pode marcar o estado da candidatura.) |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 2a. Link oficial indisponível: sistema avisa e permite reportar ao administrador. |
| Pós-condição | Candidato encaminhado para o site oficial da bolsa. |

### UC06: Guardar bolsa favorita
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado. |
| Fluxo principal | 1. Candidato clica em "Guardar". 2. Sistema adiciona a bolsa aos favoritos. |
| Fluxo alternativo | 1a. Bolsa já guardada: sistema remove dos favoritos. |
| Pós-condição | Lista de favoritos atualizada. |

### UC07: Gerir perfil
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado. |
| Fluxo principal | 1. Candidato abre o perfil. 2. Edita dados (nome, província, nível académico, área). 3. Sistema valida e guarda. |
| Fluxo alternativo | 3a. Dados inválidos: sistema indica os erros. |
| Pós-condição | Perfil atualizado. |

### UC08: Gerir bolsas
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin escolhe criar, editar ou remover bolsa. 2. Preenche os dados (incluindo tipo interna/externa, cobertura integral/parcial e custos a cargo do bolseiro) e confirma que a bolsa é elegível para angolanos. 3. Sistema valida e publica. |
| Fluxo alternativo | 2a. Elegibilidade não confirmada: sistema não permite publicar. 2b. Bolsa parcial sem custos indicados: sistema pede a indicação dos custos. |
| Pós-condição | Bolsa criada, atualizada ou removida. |

### UC09: Gerir utilizadores
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin consulta a lista de utilizadores. 2. Seleciona um utilizador. 3. Bloqueia ou remove. 4. Sistema regista a ação. |
| Pós-condição | Estado do utilizador atualizado. |

### UC10: Receber alertas de prazo
| Campo | Descrição |
|-------|-----------|
| Ator | Sistema de notificações |
| Pré-condição | Candidato tem bolsas favoritas ou em acompanhamento. |
| Fluxo principal | 1. Sistema verifica prazos diariamente. 2. Identifica bolsas a terminar (ex.: em 7 dias). 3. Envia email ao candidato. |
| Pós-condição | Alerta enviado. |

### UC11: Consultar guias de mentoria
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Existem guias publicados. |
| Fluxo principal | 1. Utilizador abre a secção de mentoria. 2. Escolhe um tema (ex.: carta de motivação, certificados, tradução, autenticação). 3. Sistema mostra o guia com passos e onde tratar cada documento. |
| Fluxo alternativo | 1a. Utilizador chega ao guia a partir da página de uma bolsa (RF18). 2a. Sem guia para o tema: sistema sugere pedir ajuda a um mentor. |
| Pós-condição | Guia apresentado. |

### UC12: Pedir ajuda a um mentor
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado. |
| Fluxo principal | 1. Candidato abre "Pedir ajuda". 2. Escolhe a bolsa (opcional) e escreve a dúvida. 3. Sistema regista o pedido e notifica os mentores. 4. Mentor responde (UC13). 5. Sistema notifica o candidato. 6. Candidato lê a resposta e pode avaliá-la. |
| Fluxo alternativo | 2a. Dúvida vazia: sistema pede preenchimento. 4a. Sem resposta num prazo definido: sistema reencaminha o pedido para outro mentor ou avisa o administrador. |
| Pós-condição | Pedido respondido e guardado no histórico. |

### UC13: Responder pedido de ajuda
| Campo | Descrição |
|-------|-----------|
| Ator | Mentor |
| Pré-condição | Mentor autenticado e aprovado. |
| Fluxo principal | 1. Mentor consulta os pedidos pendentes. 2. Abre um pedido. 3. Escreve a resposta. 4. Sistema guarda e notifica o candidato. |
| Fluxo alternativo | 2a. Pedido já respondido por outro mentor: sistema informa. |
| Pós-condição | Pedido marcado como respondido. |

### UC14: Gerir guias de mentoria
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador, Mentor |
| Pré-condição | Utilizador autenticado com permissão. |
| Fluxo principal | 1. Escolhe criar, editar ou remover guia. 2. Preenche título, tema e passos. 3. Sistema valida e publica. |
| Fluxo alternativo | 2a. Campos obrigatórios em falta: sistema indica os erros. |
| Pós-condição | Guia criado, atualizado ou removido. |

### UC15: Gerir mentores
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin consulta candidaturas a mentor e mentores existentes. 2. Aprova, bloqueia ou remove. 3. Sistema atualiza permissões. |
| Pós-condição | Estado do mentor atualizado. |

### UC16: Gerir checklist de documentos
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; bolsa guardada ou em acompanhamento. |
| Fluxo principal | 1. Candidato abre a checklist da bolsa. 2. Sistema lista os documentos exigidos com link para o guia. 3. Candidato marca cada documento como tratado. |
| Pós-condição | Progresso guardado. |

### UC17: Explorar comunidade de bolseiros
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Existem bolseiros verificados. |
| Fluxo principal | 1. Utilizador abre "Comunidade de bolseiros". 2. Filtra por país ou bolsa. 3. Abre um perfil ou relato. 4. Sistema mostra a experiência (como funciona a bolsa, o país, a universidade, custo de vida, alojamento, cultura). |
| Fluxo alternativo | 2a. Sem resultados: sistema sugere remover filtros. |
| Pós-condição | Perfil ou relato apresentado. |

### UC18: Perguntar a um bolseiro
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado. |
| Fluxo principal | 1. Candidato abre o perfil de um bolseiro. 2. Escreve a pergunta. 3. Sistema regista e notifica o bolseiro. 4. Bolseiro responde (UC19). 5. Sistema notifica o candidato, que lê a resposta no histórico. |
| Fluxo alternativo | 2a. Pergunta vazia: sistema pede preenchimento. |
| Pós-condição | Pergunta e resposta guardadas no histórico. |

### UC19: Responder a candidato
| Campo | Descrição |
|-------|-----------|
| Ator | Bolseiro |
| Pré-condição | Bolseiro autenticado e verificado. |
| Fluxo principal | 1. Bolseiro consulta as perguntas recebidas. 2. Abre uma pergunta e escreve a resposta. 3. Sistema guarda e notifica o candidato. |
| Fluxo alternativo | 2a. Bolseiro não pode responder: marca como "sem resposta" e o candidato é informado. |
| Pós-condição | Pergunta respondida. |

### UC20: Gerir perfil e relatos de bolseiro
| Campo | Descrição |
|-------|-----------|
| Ator | Bolseiro |
| Pré-condição | Bolseiro autenticado e verificado. |
| Fluxo principal | 1. Bolseiro edita o perfil público (bolsa, país, instituição, curso, apresentação). 2. Cria ou edita relatos sobre a bolsa e o país. 3. Sistema valida e publica. |
| Fluxo alternativo | 3a. Campos obrigatórios em falta: sistema indica os erros. |
| Pós-condição | Perfil ou relato publicado. |

### UC21: Pedir verificação como bolseiro
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Utilizador autenticado. |
| Fluxo principal | 1. Utilizador escolhe "Sou bolseiro". 2. Indica bolsa, país, instituição e ano. 3. Sistema regista o pedido como pendente. |
| Fluxo alternativo | 2a. Pedido já pendente: sistema informa. |
| Pós-condição | Pedido de verificação pendente. |

### UC22: Verificar bolseiros
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin consulta pedidos pendentes. 2. Confirma os dados do bolseiro. 3. Aprova ou rejeita. 4. Sistema atribui o selo de verificação e notifica o utilizador. |
| Fluxo alternativo | 3a. Rejeição: sistema pede motivo e informa o utilizador. |
| Pós-condição | Bolseiro verificado ou pedido rejeitado. |

### UC23: Denunciar e moderar conteúdo
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato, Bolseiro, Mentor, Administrador |
| Pré-condição | Utilizador autenticado. |
| Fluxo principal | 1. Utilizador denuncia um relato, guia ou mensagem. 2. Sistema regista a denúncia. 3. Admin analisa. 4. Admin remove o conteúdo ou arquiva a denúncia. |
| Fluxo alternativo | 4a. Reincidência: admin bloqueia o utilizador. |
| Pós-condição | Denúncia resolvida. |

### UC24: Consultar catálogo de mentorias
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Existem mentorias ativas no catálogo. |
| Fluxo principal | 1. Utilizador abre "Mentorias". 2. Sistema lista as mentorias com título, duração e preço em Kz. 3. Utilizador abre uma mentoria e lê a descrição. |
| Fluxo alternativo | 2a. Catálogo vazio: sistema informa que não há mentorias disponíveis. |
| Pós-condição | Catálogo apresentado. |

### UC25: Contratar mentoria (pagamento simulado)
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; mentoria ativa. |
| Fluxo principal | 1. Candidato escolhe uma mentoria. 2. Indica a data e hora preferidas. 3. Sistema regista a contratação com o estado Pendente. 4. Candidato confirma o pagamento (simulado). 5. Sistema muda o estado para Pago e mostra a confirmação. |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 4a. Candidato não confirma o pagamento: a contratação fica Pendente. |
| Pós-condição | Contratação registada com o estado de pagamento. |

### UC26: Gerir catálogo de mentorias
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin escolhe criar, editar ou remover mentoria. 2. Preenche título, descrição, duração, preço em Kz e nome do mentor. 3. Sistema valida e guarda. |
| Fluxo alternativo | 2a. Preço ou título em falta: sistema indica os erros. |
| Pós-condição | Catálogo atualizado. |

### UC27: Conversar com o chatbot
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato; Chatbot (ator secundário) |
| Pré-condição | Nenhuma. |
| Fluxo principal | 1. Utilizador abre a janela do chatbot. 2. Escreve uma pergunta. 3. Chatbot identifica palavras-chave e responde. 4. Se a pergunta for sobre bolsas, o chatbot consulta a base de dados e lista as bolsas correspondentes. |
| Fluxo alternativo | 3a. Sem correspondência: chatbot responde com uma mensagem padrão e sugere perguntas possíveis. |
| Pós-condição | Pergunta respondida. |

### UC28: Consultar mentorias contratadas
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato, Administrador |
| Pré-condição | Utilizador autenticado. |
| Fluxo principal | 1. O candidato abre "As minhas mentorias" e vê as contratações com o estado de pagamento. 2. O administrador abre o painel com todas as mentorias contratadas e o respetivo estado de pagamento. |
| Fluxo alternativo | 1a. Sem registos: sistema informa que ainda não há mentorias contratadas. |
| Pós-condição | Listas apresentadas. |

### UC29: Pedir contacto com um bolseiro
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; existe pelo menos um bolseiro verificado. |
| Fluxo principal | 1. Candidato abre o perfil de um bolseiro. 2. Escolhe "Quero falar com este bolseiro" e escreve a pergunta (ex.: como é a bolsa, o país, a universidade). 3. Sistema guarda o pedido com o estado Pendente. 4. Sistema informa que o administrador irá encaminhar o pedido. |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 2a. Pergunta vazia: sistema pede preenchimento. 3a. Já existe um pedido pendente para o mesmo bolseiro: sistema informa. |
| Pós-condição | Pedido de contacto registado. |

### UC30: Gerir bolseiros voluntários
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado; o voluntário aceitou participar e consentiu a publicação do perfil. |
| Fluxo principal | 1. Admin escolhe cadastrar, editar ou remover um bolseiro. 2. Preenche nome, situação, bolsa, país, universidade, curso, ano, apresentação e relato. 3. Confirma que o voluntário tem ou teve uma bolsa, ou que estuda fora de Angola, e marca o perfil como verificado. 4. Sistema publica o perfil com o selo de verificado. |
| Fluxo alternativo | 2a. Campos obrigatórios em falta: sistema indica os erros. 3a. Verificação não concluída: o perfil fica em rascunho e não é publicado. |
| Pós-condição | Perfil publicado, atualizado ou removido. |

### UC31: Tratar pedidos de contacto
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado; existem pedidos pendentes. |
| Fluxo principal | 1. Admin consulta os pedidos pendentes. 2. Abre um pedido e envia a pergunta ao bolseiro, sem revelar mais dados do candidato do que o necessário. 3. O bolseiro responde ao administrador ou, se ambos concordarem, o administrador põe-os em contacto direto. 4. Admin atualiza o estado do pedido (Encaminhado ou Respondido). |
| Fluxo alternativo | 3a. Bolseiro sem resposta: admin informa o candidato e sugere outro bolseiro. |
| Pós-condição | Estado do pedido atualizado. |
