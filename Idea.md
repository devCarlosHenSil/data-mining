# Documento de Contexto para Codex  
**Gerar Aplicação Exata “Mila-Bot Data Mining”**

## Objetivo
Gerar **100% fiel** a aplicação Rails 8 headless descrita no artigo “Eu Fiz um Sistema de Data Mining pra Minha Namorada Influencer” (04/03/2026).https://akitaonrails.com/2026/03/04/eu-fiz-um-sistema-de-data-mining-pra-minha-namorada-influencer-dicas-e-truques/
O sistema deve funcionar **exatamente** como mostrado: coleta automática Instagram/YouTube/X, Oracle de eventos, chatbot Discord com tool calling, 5 digests diários, idempotência total, SQLite em produção, Docker Compose com 4 serviços.

## Requisitos Funcionais (IDEA.md original)
- Responder em linguagem natural (português) via Discord:  
  “quais animes devem estrear em breve?”, “como foram meus posts essa semana?”, “quanto cobrar por publi?”, “melhor horário para postar”, etc.
- Calcular performance de posts (viral / above-average / etc.) e sentimento de comentários.
- Sugerir conteúdo baseado em tendências + calendário de eventos.
- Calcular preços de publicidade com base em engajamento, concorrentes e eventos.
- Gerar conteúdo pago que não parece propaganda.
- **Exemplo real de output** (Discord):
  - Release that Witch (hoje)  
  - NEEDY GIRL OVERDOSE (em 3 dias)  
  - Rooster Fighter (em 12 dias)  
  - Agents of the Four Seasons: Dance of Spring (em 26 dias)  
  - Pared de Gelo (em 30 dias)  
  com tag “Alta relevância” e botão “Ótimo pra conteúdos de hype”.

## Stack Exata
- Rails 8.1 (headless – sem views, sem controllers exceto `/up`)
- SQLite3 (WAL mode, bind mount `./data/storage`)
- Solid Queue + Solid Cache
- RubyLLM (Claude Sonnet via OpenRouter + Grok)
- Ferrum + chromedp/headless-shell
- Discordrb
- Docker Compose (4 serviços: app, jobs, discord, chrome)

## docker-compose.yml (copiar exatamente)
```yaml
x-app: &app
  build: .
  env_file: .env
  restart: unless-stopped
  volumes:
    - ./data/storage:/rails/storage

services:
  app:
    <<: *app
    ports: ["127.0.0.1:3000:80"]
    healthcheck: ["CMD", "curl", "-f", "http://localhost:80/up"]
    deploy: { resources: { limits: { memory: 512M } } }

  jobs:
    <<: *app
    command: bundle exec rake solid_queue:start
    depends_on: { app: { condition: service_healthy } }
    deploy: { resources: { limits: { memory: 1G } } }

  discord:
    <<: *app
    command: bundle exec rake discord:start
    depends_on: { app: { condition: service_healthy } }

  chrome:
    image: chromedp/headless-shell:stable
    deploy: { resources: { limits: { memory: 1G } } }
Estrutura de Pastas Obrigatória
text/config/prompts/          # 23 arquivos YAML
/config/prompts/snippets/ # null_vs_zero.yml, never_invent.yml, json_only.yml, etc.
/config/recurring.yml     # 25+ jobs agendados
/app/models/              # 17 models
/app/jobs/                # Collection::*, Analysis::*, Oracle::*, Discovery::*
/app/tools/               # 40+ RubyLLM::Tool
/app/services/llm/        # PromptBuilder
/lib/discord_bot.rb
Padrão Idempotente (obrigatório em TODOS jobs)
Copiar exatamente o BaseCollectorJob:
RubySNAPSHOT_DEDUP_WINDOW = 1.hour
# find_or_initialize_by(platform_post_id)
# record_snapshot com where captured_at > SNAPSHOT_DEDUP_WINDOW.ago
PromptBuilder (obrigatório)
Rubymodule Llm
  class PromptBuilder
    # carrega YAML + _base_context + snippets listados em "includes"
  end
end
Tool Calling (exemplo obrigatório)
Copiar exatamente PostPerformanceTool com clamping:
Ruby[[val.to_i, 1].max, 50].min
Chrome Headless Bypass (obrigatório)
Copiar exatamente:
Rubydef discover_ws_url(chrome_url)
  # Host: localhost + rewrite ws_url
end
nil vs Zero (snippet YAML obrigatório)
YAMLQuando um campo é null: Não diga “0 likes” — diga “dado não disponível para esta plataforma”.
Quando é zero: reporte normalmente.
Jobs Agendados (recurring.yml – estrutura exata)

youtube_collection: every day at 3am
instagram_collection: every day at 4am
x_collection: every 2 days at 5am
oracle_events: every Monday at 2am
convention_monitor: every day at 5am
discovery_pipeline: every Friday at 2am
comment_sentiment: every Sunday at 5am
digests: Monday–Friday 9am (5 temas)

Digests Diários (exato)

Segunda: Recap Performance
Terça: Radar Concorrentes
Quarta: Playbook Conteúdo
Quinta: Oportunidades e Preços
Sexta: Semana que Vem
(com botões de feedback)

Regras Rígidas para Codex

Sem interface web (exceto /up).
Todo job idempotente.
Clamping + normalização em todas tools.
Injetar current_datetime (UTC-3) em prompts de tempo.
Split automático Discord (2000 chars).
Apify primário Instagram, Ferrum fallback.
Tools retornam sempre Hash/Array.
SQLite WAL + bind mount.
916 testes (0 falhas).
Prompts YAML composable (nunca strings hardcoded).

Instrução final ao Codex:
Gere a aplicação completa (Gemfile, config, models, jobs, tools, prompts, rake tasks, docker-compose, .env.example) seguindo exatamente esses padrões. Comece pelo scaffold Rails 8 e siga a ordem: models → jobs base → prompt builder → tools → discord bot → oracle → recurring jobs.
595msconsegue me devolver o arquivo em .md para downloadMarkdown# Documento de Contexto para Codex  
**Gerar Aplicação Exata “Mila-Bot Data Mining”**

## Objetivo
Gerar **100% fiel** a aplicação Rails 8 headless descrita no artigo “Eu Fiz um Sistema de Data Mining pra Minha Namorada Influencer” (04/03/2026).  
O sistema deve funcionar **exatamente** como mostrado: coleta automática Instagram/YouTube/X, Oracle de eventos, chatbot Discord com tool calling, 5 digests diários, idempotência total, SQLite em produção, Docker Compose com 4 serviços.

## Requisitos Funcionais (IDEA.md original)
- Responder em linguagem natural (português) via Discord:  
  “quais animes devem estrear em breve?”, “como foram meus posts essa semana?”, “quanto cobrar por publi?”, “melhor horário para postar”, etc.
- Calcular performance de posts (viral / above-average / etc.) e sentimento de comentários.
- Sugerir conteúdo baseado em tendências + calendário de eventos.
- Calcular preços de publicidade com base em engajamento, concorrentes e eventos.
- Gerar conteúdo pago que não parece propaganda.
- **Exemplo real de output** (Discord):
  - Release that Witch (hoje)  
  - NEEDY GIRL OVERDOSE (em 3 dias)  
  - Rooster Fighter (em 12 dias)  
  - Agents of the Four Seasons: Dance of Spring (em 26 dias)  
  - Pared de Gelo (em 30 dias)  
  com tag “Alta relevância” e botão “Ótimo pra conteúdos de hype”.

## Stack Exata
- Rails 8.1 (headless – sem views, sem controllers exceto `/up`)
- SQLite3 (WAL mode, bind mount `./data/storage`)
- Solid Queue + Solid Cache
- RubyLLM (Claude Sonnet via OpenRouter + Grok)
- Ferrum + chromedp/headless-shell
- Discordrb
- Docker Compose (4 serviços: app, jobs, discord, chrome)

## docker-compose.yml (copiar exatamente)
```yaml
x-app: &app
  build: .
  env_file: .env
  restart: unless-stopped
  volumes:
    - ./data/storage:/rails/storage

services:
  app:
    <<: *app
    ports: ["127.0.0.1:3000:80"]
    healthcheck: ["CMD", "curl", "-f", "http://localhost:80/up"]
    deploy: { resources: { limits: { memory: 512M } } }

  jobs:
    <<: *app
    command: bundle exec rake solid_queue:start
    depends_on: { app: { condition: service_healthy } }
    deploy: { resources: { limits: { memory: 1G } } }

  discord:
    <<: *app
    command: bundle exec rake discord:start
    depends_on: { app: { condition: service_healthy } }

  chrome:
    image: chromedp/headless-shell:stable
    deploy: { resources: { limits: { memory: 1G } } }
Estrutura de Pastas Obrigatória
text/config/prompts/          # 23 arquivos YAML
/config/prompts/snippets/ # null_vs_zero.yml, never_invent.yml, json_only.yml, etc.
/config/recurring.yml     # 25+ jobs agendados
/app/models/              # 17 models
/app/jobs/                # Collection::*, Analysis::*, Oracle::*, Discovery::*
/app/tools/               # 40+ RubyLLM::Tool
/app/services/llm/        # PromptBuilder
/lib/discord_bot.rb
Padrão Idempotente (obrigatório em TODOS jobs)
Copiar exatamente o BaseCollectorJob:
RubySNAPSHOT_DEDUP_WINDOW = 1.hour
# find_or_initialize_by(platform_post_id)
# record_snapshot com where captured_at > SNAPSHOT_DEDUP_WINDOW.ago
PromptBuilder (obrigatório)
Rubymodule Llm
  class PromptBuilder
    # carrega YAML + _base_context + snippets listados em "includes"
  end
end
Tool Calling (exemplo obrigatório)
Copiar exatamente PostPerformanceTool com clamping:
Ruby[[val.to_i, 1].max, 50].min
Chrome Headless Bypass (obrigatório)
Copiar exatamente:
Rubydef discover_ws_url(chrome_url)
  # Host: localhost + rewrite ws_url
end
nil vs Zero (snippet YAML obrigatório)
YAMLQuando um campo é null: Não diga “0 likes” — diga “dado não disponível para esta plataforma”.
Quando é zero: reporte normalmente.
Jobs Agendados (recurring.yml – estrutura exata)

youtube_collection: every day at 3am
instagram_collection: every day at 4am
x_collection: every 2 days at 5am
oracle_events: every Monday at 2am
convention_monitor: every day at 5am
discovery_pipeline: every Friday at 2am
comment_sentiment: every Sunday at 5am
digests: Monday–Friday 9am (5 temas)

Digests Diários (exato)

Segunda: Recap Performance
Terça: Radar Concorrentes
Quarta: Playbook Conteúdo
Quinta: Oportunidades e Preços
Sexta: Semana que Vem
(com botões de feedback)

Regras Rígidas para Codex

Sem interface web (exceto /up).
Todo job idempotente.
Clamping + normalização em todas tools.
Injetar current_datetime (UTC-3) em prompts de tempo.
Split automático Discord (2000 chars).
Apify primário Instagram, Ferrum fallback.
Tools retornam sempre Hash/Array.
SQLite WAL + bind mount.
916 testes (0 falhas).
Prompts YAML composable (nunca strings hardcoded).

Instrução final ao Codex:
Gere a aplicação completa (Gemfile, config, models, jobs, tools, prompts, rake tasks, docker-compose, .env.example) seguindo exatamente esses padrões. Comece pelo scaffold Rails 8 e siga a ordem: models → jobs base → prompt builder → tools → discord bot → oracle → recurring jobs.