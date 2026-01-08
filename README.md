
# 🏷️ Venttos Electronics. Venttos Trace

O **Venttos Trace** é uma plataforma interna desenvolvida para controlar, monitorar e registrar toda a movimentação de placas/peças dentro do fluxo produtivo. Ele utiliza **QR Codes**, etiquetas individuais por lote e pontos de rastreio (terminais) instalados nos setores para garantir que cada item seja rastreado desde a produção até a expedição.

É um sistema **automatizado em tempo real**, que substitui controles manuais (planilhas, papéis, anotações), reduz falhas humanas e aumenta a confiabilidade da informação.

Visualize a aplicação real através do link no final deste README.md.

---

## 📁 Estrutura do Projeto

```
label-tracking-system-venttos/venttos-trace
├─ static/
│     ├─ icons/
│     │     └─ config.jpeg, dashboard.jpeg, home-hero.png, home.jpeg, live.jpeg,
│     │         logo-page-dashboard.png, logo-page-live.png, logo-page-ops.png,
│     │         logo-page-ordens.png, menu.jpeg, movimentar.jpeg, ops.jpeg, ordens.jpeg  
│     ├─ logos/
│     │     └─ logo-name.jpeg, logo.jpeg, logo.png
│     ├─ qrcodes/
│     │     └─ da.png
│     ├─ users/
│     │     └─ eduardo.jpeg
│     └─ style.css      
│   
├─ templates/
│     ├─ base.html
│     ├─ dashboard.html    
│     ├─ etiqueta_view.html
│     ├─ form.html
│     ├─ history.html
│     ├─ home.html
│     ├─ index.html
│     ├─ label.html
│     ├─ live.html
│     ├─ live_consultar.html
│     ├─ menu.html
│     ├─ movimentar.html
│     ├─ ops.html
│     └─ setores.html
│
├─ app.py
├─ models.db
├─ ping.py
├─ Profile
├─ README.EN.md
├─ README.md
└─ requirements.txt
```

---

## 🚀 Funcionalidades

* Cadastro de modelos/produtos (cliente, linha, lote, OP, processo, CQ etc.)
* Geração automática de **QR Codes**
* Impressão de etiquetas individuais por lote
* Controle de quantidade produzida e saldo disponível
* Histórico completo de movimentações por setor
* Controle de Ordens de Produção (OPs) em tempo real
* Consulta detalhada de produção por OP
* Indicadores por setor, turno, fase e horário
* Dashboard dinâmico de produção
* Interface HTML responsiva com **Bootstrap**
* Experiência otimizada para desktop e mobile

---


## 🧾 Controle de Ordens de Produção (OP)

Além da rastreabilidade por etiquetas, o Venttos Trace possui um módulo completo de controle de OPs, permitindo acompanhar a produção em tempo real, diretamente do chão de fábrica ou do escritório.

---

## 📌 Visão Geral de OPs (Produção em Tempo Real)

A tela de produção ao vivo apresenta:
* Lista consolidada de OPs ativas
* Modelo e cliente
* Quantidade já produzida
* Setor atual da produção

Filtros por:
* Data inicial e final
* Setor (PTH, SMT, IM, PA, Estoque)
* Busca por modelo, cliente ou OP

Tudo é atualizado dinamicamente conforme os registros são lançados no sistema.

---

## 🔍 Consulta Detalhada de OP

### Ao acessar uma OP específica, o sistema exibe uma visão detalhada da produção:

* Total produzido
* Produção filtrada por fase
* Consolidação automática dos dados
* Produção Hora a Hora
* Quantidade produzida por faixa de horário
* Separação por turno
* Visualização clara de ritmo produtivo

### Registros Detalhados. Cada apontamento contém:

* Data e hora
* Turno
* Fase (TOP / BOTTOM)
* Setor
* Quantidade produzida
* Operador responsável

Além disso, é possível aplicar filtros dinâmicos por:

* Turno (1º, 2º ou todos)
 Fase (TOP, BOTTOM ou todas)

---

## 📱 Experiência Desktop e Mobile (UX Diferenciada)

O Venttos Trace foi desenvolvido como um sistema web completo para uso em computadores, porém com um cuidado especial para a experiência mobile.

💻 Desktop

No acesso via computador:
* Layout tradicional de sistema corporativo
* Tabelas completas
* Dashboards amplos
* Ideal para supervisão, gestão e análise

---

## 📲 Mobile (Experiência tipo Aplicativo)

### Ao acessar pelo celular, o sistema:
* Detecta o tamanho da tela
* Ativa layouts específicos para mobile
* Utiliza navegação simplificada
* Botões grandes e acessíveis
* Menus otimizados para toque
* Filtros reorganizados para uso rápido

Mesmo sem ser um aplicativo nativo, a experiência no celular se comporta como um app industrial, facilitando o uso direto no chão de fábrica, terminais ou dispositivos móveis.

---

## 📊 Fluxo de Dados e Pontos de Controle

| Ponto        | Setor   | Função                  |
| ------------ | ------- | ----------------------- |
| **Ponto-01** | PTH     | Produção e Recebimento  |
| **Ponto-02** | SMT     | Produção e Recebimento  |
| **Ponto-03** | SMT     | Inspeção de Qualidade   |
| **Ponto-04** | IM/PA   | Produção e Recebimento  |
| **Ponto-05** | IM/PA   | Inspeção de Qualidade   |
| **Ponto-06** | IM/PA   | Inspeção de Qualidade   |
| **Ponto-07** | Estoque | Expedição (saída final) |

---

## ⚙️ Como o Sistema Funciona

### 1. Cadastro de Modelos

Cada produto/modelo recebe um cadastro contendo:

* Código, Nome, Cliente
* Linha e setor inicial
* Lote e produção prevista
* PO/OP, processo e CQ
* Revisora/Operadora
* Data e horário

Este cadastro gera o registro-mestre que será rastreado.

---

### 2. Geração de Etiquetas e Lotes

Após cadastrar o modelo:

1. O sistema calcula o número de etiquetas necessárias com base em **produção total** e **capacidade por magazine/caixa**.
2. Cada etiqueta recebe:

   * Lote individual (Ex.: "08 / 504")
   * QR Code próprio
   * Relação com o modelo original
3. Cada etiqueta possui:

   * Quantidade original e restante
   * Setor atual
   * Fase (aguardando, disponível, expedido, etc.)
   * Histórico de movimentações

---

### 3. Rastreabilidade com QR Code

Nos terminais, o colaborador escaneia o QR Code. O sistema identifica:

* Modelo, lote, setor, terminal (Ponto-01, 02, …)
* Ação (produção, recebimento, inspeção, expedição)

Cada registro contém:

* Data e hora
* Quantidade
* Setor de origem e destino
* Usuário e equipamento

Isso garante **trilha completa e detalhada** do processo.

---

### 4. Regras de Produção e Movimentação

O sistema impede erros como:

* Registro duplicado de produção
* Entrada repetida em um setor
* Movimentação acima do disponível
* Pular etapas do fluxo
* Mistura de lotes incorretos
* Confusão de modelos com fluxos diferentes (SMT-FIRST)

---

### 5. Histórico Completo

Para cada modelo, é possível visualizar:

* Etiquetas criadas
* Movimentações por setor
* Baixas de produção
* Saldo atual por fase
* Histórico de edição
* Registro cronológico completo com data/hora

---

### 6. Dashboard e Indicadores

O dashboard mostra:

* Saldo por setor (PTH, SMT, IM, PA, Estoque)
* Fase (Aguardando, Disponível, Expedido, etc.)
* Quantidade disponível por lote
* Identificação de gargalos
* Situação atualizada em tempo real

---

## ✅ Benefícios para a Empresa

**Produtividade:**

* Reduz erros manuais
* Elimina retrabalhos
* Aumenta eficiência no chão de fábrica

**Segurança:**

* Registro imutável de cada ação
* Histórico completo para auditoria

---

## 📁 Como Rodar

```bash
pip install -r requirements.txt
python app.py
```

---

## 🔗 Acesso ao Sistema (Deploy)

O sistema está disponível online pelo Render:
Uso contramedidas até na versão free para a página não fechar por inatividade, caso feche, aguarde 50 segundos.

➡️ **https://label-tracking-system-venttos.onrender.com**

---

## 👨‍💻 Autor

* Desenvolvido por **Eduardo Libório**
* 📧 [eduardosoleno@protonmail.com](mailto:eduardosoleno@protonmail.com)

---


