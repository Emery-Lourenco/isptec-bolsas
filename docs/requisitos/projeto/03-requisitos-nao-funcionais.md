# 3. Requisitos Não Funcionais

No MVP, a equipa dá prioridade a RNF01, RNF02, RNF03, RNF05 (senhas encriptadas; HTTPS quando o site for publicado), RNF07 (cuidado básico com dados pessoais), RNF14, RNF15 e RNF17 a RNF22. Os restantes aplicam-se a partir da versão 2.

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Desempenho | As páginas devem carregar em menos de 3 segundos em condições normais de rede. |
| RNF02 | Usabilidade | O site deve estar em português e ser simples de usar, sem necessidade de formação. |
| RNF03 | Compatibilidade | O site deve ser responsivo (telemóvel, tablet e PC) e funcionar nos principais navegadores. |
| RNF04 | Eficiência | O site deve ser leve (imagens otimizadas, poucas dependências), para funcionar com dados móveis lentos. |
| RNF05 | Segurança | As palavras-passe devem ser guardadas encriptadas (hash) e toda a comunicação deve usar HTTPS. |
| RNF06 | Disponibilidade | O sistema deve estar disponível pelo menos 99% do tempo. |
| RNF07 | Privacidade | Os dados pessoais devem ser tratados conforme a lei angolana de proteção de dados pessoais (confirmar referência exata). |
| RNF08 | Manutenibilidade | O código e a documentação devem estar organizados no repositório para facilitar o trabalho em equipa. |
| RNF09 | Confiabilidade | Os links oficiais das bolsas devem ser verificados pelo administrador antes da publicação. |
| RNF10 | Privacidade | Os pedidos e respostas de mentoria só devem ser visíveis ao candidato, ao mentor envolvido e ao administrador. |
| RNF11 | Qualidade | Apenas mentores aprovados pelo administrador podem responder a pedidos e publicar guias. |
| RNF12 | Usabilidade | Os guias de mentoria devem usar linguagem simples e passos numerados. |
| RNF13 | Segurança | O sistema não deve pedir nem guardar documentos pessoais sensíveis (passaporte, BI, certificados) nos pedidos de mentoria. |
| RNF14 | Privacidade | Os contactos pessoais dos bolseiros (telefone, email) não devem ser públicos; o contacto entre candidato e bolseiro deve ser intermediado pela plataforma. |
| RNF15 | Confiança | Os perfis de bolseiros devem ser verificados pelo administrador e mostrar um selo de verificação. |
| RNF16 | Atualidade | As páginas das bolsas devem mostrar a data da última verificação da informação de cobertura e custos. |
| RNF17 | Tecnologia | O sistema deve ser desenvolvido em Python com o framework Flask. |
| RNF18 | Dados | Os dados devem ser guardados numa base de dados PostgreSQL na nuvem (Neon), partilhada pela equipa. |
| RNF19 | Segurança | As credenciais da base de dados e outras chaves devem ficar em variáveis de ambiente (ficheiro `.env`), fora do repositório. |
| RNF20 | Acessibilidade | O sistema deve funcionar nos browsers web atuais, sem instalação. |
| RNF21 | Privacidade | O perfil de um bolseiro só pode ser publicado com o consentimento do próprio. |
| RNF22 | Segurança | Os comprovativos usados para verificar um bolseiro não devem ser guardados na plataforma depois da verificação. |
