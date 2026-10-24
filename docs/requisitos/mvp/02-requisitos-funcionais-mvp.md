# MVP: Requisitos Funcionais

Prioridade: **A** = Alta, **M** = Média, **B** = Baixa

| ID | Requisito | Ator | Prioridade |
|----|-----------|------|-----------|
| RF01 | O sistema deve permitir o registo de utilizadores com email e palavra-passe. | Visitante | A |
| RF02 | O sistema deve permitir login e logout. | Candidato, Admin | A |
| RF03 | O sistema deve listar as bolsas disponíveis. | Todos | A |
| RF04 | O sistema deve permitir pesquisar e filtrar bolsas por país, tipo (interna ou externa), cobertura (integral ou parcial), nível de estudo, área e prazo. | Todos | A |
| RF05 | O sistema deve mostrar os detalhes de cada bolsa (descrição, tipo, cobertura, custos a cargo do bolseiro, requisitos, documentos, prazo, link oficial). | Todos | A |
| RF06 | O sistema só deve publicar bolsas marcadas como elegíveis para angolanos (campo obrigatório no registo da bolsa). | Admin | A |
| RF07 | O sistema deve redirecionar o candidato para a página oficial de candidatura da bolsa. | Candidato | A |
| RF08 | O administrador deve poder criar, editar e remover bolsas. | Admin | A |
| RF09 | O administrador deve classificar cada bolsa como interna (em Angola) ou externa (no estrangeiro) ao registá-la. | Admin | A |
| RF10 | O administrador deve indicar a cobertura da bolsa (integral ou parcial) e os itens cobertos (propinas, alojamento, alimentação, passagens, seguro de saúde, outros). | Admin | A |
| RF11 | Nas bolsas de cobertura parcial, o administrador deve indicar os custos a cargo do bolseiro (descrição e valor estimado, quando conhecido). | Admin | A |
| RF12 | O sistema deve destacar visualmente as bolsas 100% comparticipadas na listagem e nos detalhes. | Sistema | M |
| RF13 | O sistema deve arquivar automaticamente bolsas com prazo expirado. | Sistema | B |
| RF14 | O administrador deve poder cadastrar, editar e remover perfis de bolseiros voluntários (nome, situação, bolsa, país, universidade, curso, ano, apresentação e relato), e só pode marcar um perfil como verificado depois de confirmar que o voluntário tem ou teve uma bolsa, ou que estuda fora de Angola. | Admin | A |
| RF15 | O sistema deve ter uma secção "Comunidade de bolseiros" com os perfis e relatos de bolseiros verificados, filtrável por país e bolsa. | Todos | A |
| RF16 | A página de cada bolsa deve mostrar os bolseiros que a obtiveram. | Todos | M |
| RF17 | O candidato autenticado deve poder pedir contacto com um bolseiro, escrevendo a sua pergunta; o pedido fica guardado. | Candidato | A |
| RF18 | O administrador deve poder consultar os pedidos de contacto e encaminhá-los ao bolseiro, atualizando o estado do pedido (Pendente, Encaminhado ou Respondido). | Admin | A |
| RF19 | O sistema deve disponibilizar um catálogo público de mentorias pagas (título, descrição, duração, preço em Kz). | Todos | A |
| RF20 | O administrador deve poder criar, editar e remover mentorias do catálogo. | Admin | A |
| RF21 | O candidato autenticado deve poder contratar uma mentoria, indicando a data e hora preferidas. | Candidato | A |
| RF22 | O sistema deve registar o pagamento da mentoria contratada, com os estados Pendente e Pago (pagamento simulado nesta versão). | Candidato, Sistema | A |
| RF23 | O candidato e o administrador devem poder consultar as mentorias contratadas e o estado de pagamento (cada candidato vê as suas; o administrador vê todas). | Candidato, Admin | M |
| RF24 | O sistema deve incluir um chatbot, baseado em regras e palavras-chave, que responda a perguntas frequentes sobre bolsas, candidatura e mentorias. | Todos | A |
| RF25 | O chatbot deve consultar a base de dados para indicar bolsas disponíveis (ex.: bolsas 100% comparticipadas ou por tipo). | Todos | M |
