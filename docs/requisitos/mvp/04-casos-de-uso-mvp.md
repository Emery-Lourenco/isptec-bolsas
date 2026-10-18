# MVP: Casos de Uso

## Diagrama
Ver `diagramas/casos-de-uso-mvp.puml` (PlantUML). Para gerar a imagem: https://www.plantuml.com/plantuml ou extensão PlantUML do VS Code.

## Lista
| ID | Caso de uso | Ator principal | RF relacionados |
|----|-------------|----------------|-----------------|
| UC01 | Registar-se | Visitante | RF01 |
| UC02 | Autenticar-se | Candidato, Admin | RF02 |
| UC03 | Pesquisar e filtrar bolsas | Todos | RF03, RF04 |
| UC04 | Ver detalhes da bolsa | Todos | RF05, RF16 |
| UC05 | Candidatar-se a bolsa | Candidato | RF07 |
| UC06 | Gerir bolsas | Admin | RF06, RF08 a RF13 |
| UC07 | Explorar comunidade de bolseiros | Todos | RF15, RF16 |
| UC08 | Pedir contacto com um bolseiro | Candidato | RF17 |
| UC09 | Gerir bolseiros voluntários | Administrador | RF14 |
| UC10 | Tratar pedidos de contacto | Administrador | RF18 |
| UC11 | Consultar catálogo de mentorias | Todos | RF19 |
| UC12 | Contratar mentoria (pagamento simulado) | Candidato | RF21, RF22 |
| UC13 | Gerir catálogo de mentorias | Admin | RF20 |
| UC14 | Consultar mentorias contratadas | Candidato, Admin | RF23 |
| UC15 | Conversar com o chatbot | Todos, Chatbot | RF24, RF25 |

## Descrições detalhadas

### UC01: Registar-se
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante |
| Pré-condição | O visitante não tem conta. |
| Fluxo principal | 1. Visitante abre a página de registo. 2. Preenche nome, email e palavra-passe. 3. Sistema valida os dados. 4. Sistema cria a conta. |
| Fluxo alternativo | 3a. Email já registado: o sistema informa e sugere login. 3b. Palavra-passe fraca: o sistema pede nova palavra-passe. |
| Pós-condição | Conta criada. |

### UC02: Autenticar-se
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato, Administrador |
| Pré-condição | O utilizador tem conta. |
| Fluxo principal | 1. Utilizador introduz email e palavra-passe. 2. Sistema valida. 3. Sistema inicia sessão. |
| Fluxo alternativo | 2a. Credenciais inválidas: mensagem de erro. |
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
| Fluxo principal | 1. Candidato clica em "Candidatar-me". 2. Sistema abre a página oficial de candidatura da bolsa, num novo separador. |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 2a. Link oficial indisponível: sistema avisa e permite reportar ao administrador. |
| Pós-condição | Candidato encaminhado para o site oficial da bolsa. |

### UC06: Gerir bolsas
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin escolhe criar, editar ou remover bolsa. 2. Preenche os dados (incluindo tipo interna/externa, cobertura integral/parcial e custos a cargo do bolseiro) e confirma que a bolsa é elegível para angolanos. 3. Sistema valida e publica. |
| Fluxo alternativo | 2a. Elegibilidade não confirmada: sistema não permite publicar. 2b. Bolsa parcial sem custos indicados: sistema pede a indicação dos custos. |
| Pós-condição | Bolsa criada, atualizada ou removida. |

### UC07: Explorar comunidade de bolseiros
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Existem bolseiros verificados. |
| Fluxo principal | 1. Utilizador abre "Comunidade de bolseiros". 2. Filtra por país ou bolsa. 3. Abre um perfil ou relato. 4. Sistema mostra a experiência (como funciona a bolsa, o país, a universidade, custo de vida, alojamento, cultura). |
| Fluxo alternativo | 2a. Sem resultados: sistema sugere remover filtros. |
| Pós-condição | Perfil ou relato apresentado. |

### UC08: Pedir contacto com um bolseiro
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; existe pelo menos um bolseiro verificado. |
| Fluxo principal | 1. Candidato abre o perfil de um bolseiro. 2. Escolhe "Quero falar com este bolseiro" e escreve a pergunta (ex.: como é a bolsa, o país, a universidade). 3. Sistema guarda o pedido com o estado Pendente. 4. Sistema informa que o administrador irá encaminhar o pedido. |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 2a. Pergunta vazia: sistema pede preenchimento. 3a. Já existe um pedido pendente para o mesmo bolseiro: sistema informa. |
| Pós-condição | Pedido de contacto registado. |

### UC09: Gerir bolseiros voluntários
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado; o voluntário aceitou participar e consentiu a publicação do perfil. |
| Fluxo principal | 1. Admin escolhe cadastrar, editar ou remover um bolseiro. 2. Preenche nome, situação, bolsa, país, universidade, curso, ano, apresentação e relato. 3. Confirma que o voluntário tem ou teve uma bolsa, ou que estuda fora de Angola, e marca o perfil como verificado. 4. Sistema publica o perfil com o selo de verificado. |
| Fluxo alternativo | 2a. Campos obrigatórios em falta: sistema indica os erros. 3a. Verificação não concluída: o perfil fica em rascunho e não é publicado. |
| Pós-condição | Perfil publicado, atualizado ou removido. |

### UC10: Tratar pedidos de contacto
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado; existem pedidos pendentes. |
| Fluxo principal | 1. Admin consulta os pedidos pendentes. 2. Abre um pedido e envia a pergunta ao bolseiro, sem revelar mais dados do candidato do que o necessário. 3. O bolseiro responde ao administrador ou, se ambos concordarem, o administrador põe-os em contacto direto. 4. Admin atualiza o estado do pedido (Encaminhado ou Respondido). |
| Fluxo alternativo | 3a. Bolseiro sem resposta: admin informa o candidato e sugere outro bolseiro. |
| Pós-condição | Estado do pedido atualizado. |

### UC11: Consultar catálogo de mentorias
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato |
| Pré-condição | Existem mentorias ativas no catálogo. |
| Fluxo principal | 1. Utilizador abre "Mentorias". 2. Sistema lista as mentorias com título, duração e preço em Kz. 3. Utilizador abre uma mentoria e lê a descrição. |
| Fluxo alternativo | 2a. Catálogo vazio: sistema informa que não há mentorias disponíveis. |
| Pós-condição | Catálogo apresentado. |

### UC12: Contratar mentoria (pagamento simulado)
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato |
| Pré-condição | Candidato autenticado; mentoria ativa. |
| Fluxo principal | 1. Candidato escolhe uma mentoria. 2. Indica a data e hora preferidas. 3. Sistema regista a contratação com o estado Pendente. 4. Candidato confirma o pagamento (simulado). 5. Sistema muda o estado para Pago e mostra a confirmação. |
| Fluxo alternativo | 1a. Visitante sem login: sistema pede login. 4a. Candidato não confirma o pagamento: a contratação fica Pendente. |
| Pós-condição | Contratação registada com o estado de pagamento. |

### UC13: Gerir catálogo de mentorias
| Campo | Descrição |
|-------|-----------|
| Ator | Administrador |
| Pré-condição | Administrador autenticado. |
| Fluxo principal | 1. Admin escolhe criar, editar ou remover mentoria. 2. Preenche título, descrição, duração, preço em Kz e nome do mentor. 3. Sistema valida e guarda. |
| Fluxo alternativo | 2a. Preço ou título em falta: sistema indica os erros. |
| Pós-condição | Catálogo atualizado. |

### UC14: Consultar mentorias contratadas
| Campo | Descrição |
|-------|-----------|
| Ator | Candidato, Administrador |
| Pré-condição | Utilizador autenticado. |
| Fluxo principal | 1. O candidato abre "As minhas mentorias" e vê as contratações com o estado de pagamento. 2. O administrador abre o painel com todas as mentorias contratadas e o respetivo estado de pagamento. |
| Fluxo alternativo | 1a. Sem registos: sistema informa que ainda não há mentorias contratadas. |
| Pós-condição | Listas apresentadas. |

### UC15: Conversar com o chatbot
| Campo | Descrição |
|-------|-----------|
| Ator | Visitante, Candidato; Chatbot (ator secundário) |
| Pré-condição | Nenhuma. |
| Fluxo principal | 1. Utilizador abre a janela do chatbot. 2. Escreve uma pergunta. 3. Chatbot identifica palavras-chave e responde. 4. Se a pergunta for sobre bolsas, o chatbot consulta a base de dados e lista as bolsas correspondentes. |
| Fluxo alternativo | 3a. Sem correspondência: chatbot responde com uma mensagem padrão e sugere perguntas possíveis. |
| Pós-condição | Pergunta respondida. |
