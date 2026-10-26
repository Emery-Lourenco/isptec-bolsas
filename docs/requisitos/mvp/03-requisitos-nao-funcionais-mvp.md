# MVP: Requisitos Não Funcionais

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Desempenho | As páginas devem carregar em menos de 3 segundos em condições normais de rede. |
| RNF02 | Usabilidade | O site deve estar em português e ser simples de usar, sem necessidade de formação. |
| RNF03 | Compatibilidade | O site deve ser responsivo (telemóvel, tablet e PC) e funcionar nos principais navegadores. |
| RNF04 | Segurança | As palavras-passe devem ser guardadas encriptadas (hash) e toda a comunicação deve usar HTTPS. |
| RNF05 | Privacidade | Os dados pessoais devem ser tratados conforme a lei angolana de proteção de dados pessoais (confirmar referência exata). |
| RNF06 | Privacidade | Os contactos pessoais dos bolseiros (telefone, email) não devem ser públicos; o contacto entre candidato e bolseiro deve ser intermediado pela plataforma. |
| RNF07 | Confiança | Os perfis de bolseiros devem ser verificados pelo administrador e mostrar um selo de verificação. |
| RNF08 | Privacidade | O perfil de um bolseiro só pode ser publicado com o consentimento do próprio. |
| RNF09 | Segurança | Os comprovativos usados para verificar um bolseiro não devem ser guardados na plataforma depois da verificação. |
| RNF10 | Tecnologia | O sistema deve ser desenvolvido em Python com o framework Flask. |
| RNF11 | Dados | Os dados devem ser guardados numa base de dados PostgreSQL na nuvem (Neon), partilhada pela equipa. |
| RNF12 | Segurança | As credenciais da base de dados e outras chaves devem ficar em variáveis de ambiente (ficheiro `.env`), fora do repositório. |
| RNF13 | Acessibilidade | O sistema deve funcionar nos browsers web atuais, sem instalação. |

O HTTPS aplica-se quando o site for publicado; em ambiente local, basta guardar as palavras-passe encriptadas.
