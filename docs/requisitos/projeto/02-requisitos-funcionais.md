# 2. Requisitos Funcionais

Prioridade: **A** = Alta, **M** = Média, **B** = Baixa

Fase: **MVP** = entrega de 25 de outubro; **V2** = versão seguinte.

| ID | Requisito | Ator | Prioridade | Fase |
|----|-----------|------|-----------|------|
| RF01 | O sistema deve permitir o registo de utilizadores com email e palavra-passe. | Visitante | A | MVP |
| RF02 | O sistema deve permitir login e logout. | Candidato, Admin | A | MVP |
| RF03 | O sistema deve permitir recuperar a palavra-passe por email. | Candidato | M | V2 |
| RF04 | O candidato deve poder gerir o perfil (nome, província, nível académico, área de interesse). | Candidato | M | V2 |
| RF05 | O sistema deve listar as bolsas disponíveis. | Todos | A | MVP |
| RF06 | O sistema deve permitir pesquisar e filtrar bolsas por país, tipo (interna ou externa), cobertura (integral ou parcial), nível de estudo, área e prazo. | Todos | A | MVP |
| RF07 | O sistema deve mostrar os detalhes de cada bolsa (descrição, tipo, cobertura, custos a cargo do bolseiro, requisitos, documentos, prazo, link oficial). | Todos | A | MVP |
| RF08 | O sistema só deve publicar bolsas marcadas como elegíveis para angolanos (campo obrigatório no registo da bolsa). | Admin | A | MVP |
| RF09 | O sistema deve redirecionar o candidato para a página oficial de candidatura da bolsa. | Candidato | A | MVP |
| RF10 | O candidato deve poder registar e atualizar o estado da sua candidatura (Quero candidatar-me, Em curso, Submetida, Aprovada, Rejeitada). | Candidato | M | V2 |
| RF11 | O candidato deve poder guardar bolsas como favoritas. | Candidato | M | V2 |
| RF12 | O sistema deve enviar alertas quando o prazo de uma bolsa favorita ou em acompanhamento estiver a terminar. | Sistema | M | V2 |
| RF13 | O administrador deve poder criar, editar e remover bolsas. | Admin | A | MVP |
| RF14 | O administrador deve poder gerir utilizadores (consultar, bloquear, remover). | Admin | M | V2 |
| RF15 | O sistema deve arquivar automaticamente bolsas com prazo expirado. | Sistema | B | MVP |
| RF16 | O sistema deve disponibilizar uma secção de mentoria com guias sobre a preparação de candidaturas (documentos necessários, onde e como tratá-los, carta de motivação, CV, tradução e autenticação). | Todos | A | V2 |
| RF17 | O administrador e os mentores devem poder criar, editar e remover guias. | Admin, Mentor | M | V2 |
| RF18 | A página de cada bolsa deve ligar os documentos exigidos aos guias de mentoria correspondentes. | Todos | M | V2 |
| RF19 | O candidato deve poder manter uma checklist de documentos por bolsa e marcar o que já tratou. | Candidato | M | V2 |
| RF20 | O candidato deve poder enviar um pedido de ajuda a um mentor, indicando a bolsa e a dúvida. | Candidato | A | V2 |
| RF21 | O mentor deve poder consultar os pedidos recebidos e responder-lhes. | Mentor | A | V2 |
| RF22 | O candidato deve poder consultar o histórico dos seus pedidos e respostas. | Candidato | M | V2 |
| RF23 | O sistema deve notificar por email o candidato quando o pedido for respondido e o mentor quando receber um pedido. | Sistema | M | V2 |
| RF24 | O administrador deve poder aprovar, bloquear e remover mentores. | Admin | M | V2 |
| RF25 | O candidato deve poder avaliar a ajuda recebida. | Candidato | B | V2 |
| RF26 | O administrador deve classificar cada bolsa como interna (em Angola) ou externa (no estrangeiro) ao registá-la. | Admin | A | MVP |
| RF27 | O administrador deve indicar a cobertura da bolsa (integral ou parcial) e os itens cobertos (propinas, alojamento, alimentação, passagens, seguro de saúde, outros). | Admin | A | MVP |
| RF28 | Nas bolsas de cobertura parcial, o administrador deve indicar os custos a cargo do bolseiro (descrição e valor estimado, quando conhecido). | Admin | A | MVP |
| RF29 | O sistema deve destacar visualmente as bolsas 100% comparticipadas na listagem e nos detalhes. | Sistema | M | MVP |
| RF30 | O utilizador registado deve poder pedir verificação como bolseiro (bolsa, país, instituição, ano). | Candidato | M | V2 |
| RF31 | O administrador deve poder verificar, rejeitar e remover bolseiros. | Admin | M | V2 |
| RF32 | O bolseiro deve poder gerir o seu perfil público (bolsa, país, instituição, curso, ano, apresentação). | Bolseiro | A | V2 |
| RF33 | O bolseiro deve poder publicar relatos sobre a bolsa e o país (como funciona, custo de vida, alojamento, clima, cultura). | Bolseiro | M | V2 |
| RF34 | O sistema deve ter uma secção "Comunidade de bolseiros" com os perfis e relatos de bolseiros verificados, filtrável por país e bolsa. | Todos | A | MVP |
| RF35 | A página de cada bolsa deve mostrar os bolseiros que a obtiveram. | Todos | M | MVP |
| RF36 | O candidato deve poder enviar uma pergunta ou pedido de conversa a um bolseiro, por mensagem escrita. | Candidato | A | V2 |
| RF37 | O bolseiro deve poder consultar e responder às perguntas recebidas, e o candidato deve poder ver o histórico. | Bolseiro, Candidato | A | V2 |
| RF38 | O sistema deve notificar por email quando uma pergunta for recebida ou respondida. | Sistema | M | V2 |
| RF39 | Os utilizadores devem poder denunciar conteúdo inadequado, e o administrador deve poder remover conteúdo e bloquear utilizadores. | Todos, Admin | M | V2 |
| RF40 | O sistema deve disponibilizar um catálogo público de mentorias pagas (título, descrição, duração, preço em Kz). | Todos | A | MVP |
| RF41 | O administrador deve poder criar, editar e remover mentorias do catálogo. | Admin | A | MVP |
| RF42 | O candidato autenticado deve poder contratar uma mentoria, indicando a data e hora preferidas. | Candidato | A | MVP |
| RF43 | O sistema deve registar o pagamento da mentoria contratada, com os estados Pendente e Pago (pagamento simulado nesta versão). | Candidato, Sistema | A | MVP |
| RF44 | O candidato e o administrador devem poder consultar as mentorias contratadas e o estado de pagamento (cada candidato vê as suas; o administrador vê todas). | Candidato, Admin | M | MVP |
| RF45 | O sistema deve incluir um chatbot, baseado em regras e palavras-chave, que responda a perguntas frequentes sobre bolsas, candidatura e mentorias. | Todos | A | MVP |
| RF46 | O chatbot deve consultar a base de dados para indicar bolsas disponíveis (ex.: bolsas 100% comparticipadas ou por tipo). | Todos | M | MVP |
| RF47 | O administrador deve poder cadastrar, editar e remover perfis de bolseiros voluntários (nome, situação, bolsa, país, universidade, curso, ano, apresentação e relato), e só pode marcar um perfil como verificado depois de confirmar que o voluntário tem ou teve uma bolsa, ou que estuda fora de Angola. | Admin | A | MVP |
| RF48 | O candidato autenticado deve poder pedir contacto com um bolseiro, escrevendo a sua pergunta; o pedido fica guardado. | Candidato | A | MVP |
| RF49 | O administrador deve poder consultar os pedidos de contacto e encaminhá-los ao bolseiro, atualizando o estado do pedido (Pendente, Encaminhado ou Respondido). | Admin | A | MVP |
