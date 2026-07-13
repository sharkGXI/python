# Instagram Post Scheduler

Programa em Python para logar no Instagram (conta pessoal) e publicar posts
automaticamente em datas e horários agendados.

## ⚠️ Avisos importantes

- Este projeto usa a biblioteca **não-oficial** `instagrapi`, que automatiza
  login/postagem imitando o app oficial. **O Instagram não aprova esse tipo
  de automação** para contas pessoais, então existe risco real de:
  - Pedido de verificação extra (challenge) ao logar de um novo local/IP;
  - Bloqueio temporário por atividade suspeita, especialmente se você
    postar com muita frequência ou rodar o script de vários lugares;
  - Em casos raros, suspensão da conta.
- Use por sua conta e risco, e apenas para publicar **seu próprio conteúdo**.
- Recomendações para reduzir risco:
  - Não poste mais que 1–3 vezes por dia;
  - Sempre rode o script do mesmo computador/rede (o script salva a sessão
    em `session.json` para evitar logins repetidos);
  - Evite rodar o script imediatamente após trocar a senha ou ativar 2FA.

**Alternativa mais segura:** se você puder converter sua conta para
Business ou Creator (gratuito, direto no app do Instagram), é possível usar
a API oficial da Meta (Graph API), que é sancionada e não tem esse risco de
bloqueio. Posso te ajudar a montar essa versão também, se preferir.

## Instalação

```bash
cd insta_scheduler
pip install -r requirements.txt
```

## Configuração

1. Copie `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edite `.env` e preencha `IG_USERNAME` e `IG_PASSWORD` com seus dados.
3. Coloque as imagens/vídeos que você quer postar na pasta `posts/`.
4. Edite `schedule_config.json` com os posts desejados:

```json
{
  "posts": [
    {
      "id": "post_001",
      "media_path": "posts/exemplo1.jpg",
      "caption": "Legenda do post aqui #hashtag",
      "date": "2026-07-10",
      "time": "09:00",
      "type": "photo",
      "posted": false
    }
  ]
}
```

- `type` pode ser `"photo"`, `"video"` ou `"reel"`.
- `date` no formato `AAAA-MM-DD`, `time` no formato `HH:MM` (24h).
- Não mude o campo `"posted"` manualmente — o script marca como `true`
  automaticamente após publicar.

## Rodando

```bash
python main.py
```

O script vai:
1. Logar no Instagram (na primeira vez pode pedir código de verificação,
   se você tiver 2FA ativado);
2. Salvar a sessão em `session.json` para não precisar logar toda vez;
3. Ficar rodando em segundo plano, checando a cada 60 segundos se chegou
   a hora de publicar algum post da lista;
4. Registrar tudo em `scheduler.log`.

Deixe o terminal aberto (ou rode com `nohup python main.py &` no Linux/Mac,
ou como uma tarefa agendada no Windows) para que ele continue funcionando.

## Estrutura de arquivos

```
insta_scheduler/
├── main.py                 # script principal
├── schedule_config.json    # lista de posts agendados
├── requirements.txt
├── .env                     # suas credenciais (não compartilhar!)
├── posts/                   # suas imagens/vídeos
├── session.json             # sessão salva (gerado automaticamente)
└── scheduler.log            # log de execução
```
