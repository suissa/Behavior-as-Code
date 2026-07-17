# BehaviorID-LT  
## Long-Tail Behavioral Trajectory Specification

**Status:** Draft técnico v0.1  
**Autor:** AllasCode.Institute  
**Domínio:** BehaviorID, Predictive Self-Healing, Predictive Fraud Containment, Agentic Security  
**Objetivo:** Definir uma extensão temporal do BehaviorID para analisar caudas longas de mensagens, detectar trajetórias comportamentais suspeitas, prever falhas operacionais e conter fraude antes da execução de payloads sensíveis.

---

# 1. Resumo

O **BehaviorID-LT** é uma extensão temporal do BehaviorID criada para analisar não apenas a última mensagem de uma conversa, mas a **trajetória comportamental acumulada** ao longo de uma sessão, intenção, autorização de agent ou sequência de mensagens.

Enquanto o BehaviorID tradicional classifica o estado comportamental atual de uma mensagem, o BehaviorID-LT analisa:

- como a intenção evoluiu;
- se houve mudança semântica relevante;
- se o payload atual ainda corresponde à intenção original;
- se a conversa está caminhando para erro operacional;
- se há sinais de fraude, coerção, abuso ou manipulação;
- se o sistema deve executar, observar, corrigir, pedir confirmação, escalar para humano, isolar ou bloquear.

O objetivo principal não é substituir autenticação, 2FA, passkey ou liveness. O objetivo é cobrir o espaço que continua vulnerável mesmo após autenticação forte: **intenção, trajetória, payload, sessão, escopo, tool execution e coerência comportamental**.

---

# 2. Problema

Sistemas tradicionais costumam avaliar uma ação no momento final da execução:

```text
payload recebido → validação → execução ou bloqueio

Esse modelo perde sinais importantes que aparecem antes do payload final, especialmente em conversas, agentes autônomos, fluxos por WhatsApp, marketplaces, atendimento automatizado, pagamentos e execução de tools.

Exemplo:

M1: "Quero resolver uma cobrança."
M2: "Recebi esse link."
M3: "Está pedindo para validar minha conta."
M4: "Agora apareceu um Pix para liberar."

Nenhuma mensagem isolada prova fraude. Porém, a trajetória indica possível coerção, engenharia social ou golpe financeiro.

O BehaviorID-LT resolve esse problema transformando uma conversa em uma janela comportamental temporal adaptativa.


---

3. Diferença entre BehaviorID e BehaviorID-LT

BehaviorID:
  classifica o estado comportamental atual.

BehaviorID-LT:
  classifica a evolução temporal da intenção.

Tabela conceitual:

Camada	Pergunta principal	Saída

BehaviorID	O que esta mensagem representa agora?	Estado comportamental
BehaviorID-LT	Como esse comportamento evoluiu?	Trajetória e modificadores
Self-Healing Predictivo	Isso vai quebrar operacionalmente?	Correção ou revalidação
Fraud Containment Predictivo	Isso parece abuso/fraude?	Contenção, prova ou bloqueio
Intent-Payload Binding	O payload ainda respeita a intenção original?	Coerência ou violação
Adaptive Observability	Quanto preciso observar agora?	Expansão ou redução da janela



---

4. Escopo

O BehaviorID-LT deve ser usado quando houver:

autenticação recente;

sessão com agent autorizado;

ação financeira;

mudança de escopo;

chamada de tool sensível;

payload mutável;

pedido de permissão;

troca de canal;

urgência incomum;

ambiguidade crescente;

conflito entre intenção original e ação final;

entidades novas em ação sensível;

risco de fraude, coerção, abuso ou erro operacional.


Fora do escopo:

substituir autenticação;

substituir passkey/WebAuthn;

substituir liveness;

provar identidade civil;

decidir fraude apenas por similaridade vetorial;

bloquear usuários apenas por linguagem incomum;

armazenar todo histórico bruto sem política de retenção.



---

5. Princípio central

A mensagem atual nunca deve ser classificada isoladamente quando houver
risco financeiro, permissão sensível, alteração de payload, execução por agent,
mudança de canal, mudança de intenção ou escalada de privilégio.

O sistema deve analisar a trajetória.


---

6. Modelo geral

Incoming Message
  → BehaviorID atual
  → extração de intenção
  → extração de entidades
  → atualização da trajetória
  → cálculo de transições
  → recuperação vetorial de casos similares
  → expansão em grafo relacional
  → verificação de payload
  → cálculo de risco
  → decisão

Fluxo completo:

Mensagem
  → Message Behavior Classification
  → Long-Tail Window Update
  → Behavior Transition Analysis
  → Intent Drift Detection
  → Entity-Risk Graph Expansion
  → Vector Similarity Retrieval
  → Intent-Payload Binding
  → Policy Reasoning
  → Risk Decision
  → Action


---

7. Entidades principais

7.1 BehaviorTrajectory

Representa a trajetória comportamental de uma conversa, sessão ou intenção.

type BehaviorTrajectory = {
  trajectory_id: string
  conversation_id: string
  session_id: string

  actor_id: string
  agent_id?: string

  window: BehaviorWindow

  messages: BehaviorMessage[]

  current_behavior_id: string
  previous_behavior_id?: string

  trajectory_modifiers: TrajectoryModifier[]

  transitions: BehaviorTransition[]

  intent_payload_bindings: IntentPayloadBinding[]

  risk_state: BehaviorRiskState

  created_at: string
  updated_at: string
}


---

7.2 BehaviorWindow

Define a janela temporal analisada.

type BehaviorWindow = {
  mode:
    | "sliding"
    | "session"
    | "risk_expanded"
    | "agent_authorized_session"
    | "since_sensitive_intent"
    | "conversation_full"

  message_count: number

  started_at: string
  ended_at: string

  expansion_reason?: string

  includes: {
    raw_messages: boolean
    semantic_summaries: boolean
    tool_calls: boolean
    payloads: boolean
    entities: boolean
    graph_context: boolean
    vector_retrieval: boolean
    policy_results: boolean
  }
}


---

7.3 BehaviorMessage

Envelope comportamental de cada mensagem.

type BehaviorMessage = {
  message_id: string
  index: number
  timestamp: string

  actor:
    | "human"
    | "agent"
    | "business"
    | "system"
    | "tool"
    | "external_actor"

  raw_text?: string
  semantic_summary: string

  behavior_id: string
  intent_id?: string

  extracted_entities: EntityRef[]

  signals: BehaviorSignals

  vector_ref?: VectorRef

  graph_refs?: GraphRefs

  payload_ref?: string

  tool_call_ref?: string
}


---

7.4 BehaviorSignals

Sinais comportamentais extraídos da mensagem e da trajetória.

type BehaviorSignals = {
  urgency: number
  ambiguity: number
  coercion: number
  contradiction: number

  financial_pressure: number
  identity_pressure: number
  permission_pressure: number
  channel_switch_pressure: number

  tool_escalation: number
  payload_mutation: number
  agent_scope_drift: number

  semantic_drift: number
  intent_drift: number
  trust_drop: number

  anomaly_score: number
}

Cada campo deve variar de 0.0 a 1.0.

0.0 = ausência do sinal
1.0 = sinal extremo


---

8. Trajectory Modifiers

Os Trajectory Modifiers são marcadores temporais aplicados à conversa. Eles não substituem o BehaviorID principal; eles qualificam a evolução.

type TrajectoryModifier =
  | "LT.NORMAL_PROGRESS"
  | "LT.INTENT_DRIFT"
  | "LT.INTENT_CONTRADICTION"
  | "LT.URGENCY_ESCALATION"
  | "LT.PERMISSION_ESCALATION"
  | "LT.CHANNEL_SWITCH_PRESSURE"
  | "LT.FINANCIAL_PRESSURE"
  | "LT.IDENTITY_PRESSURE"
  | "LT.PAYLOAD_MUTATION"
  | "LT.AGENT_SCOPE_DRIFT"
  | "LT.COERCION_PATTERN"
  | "LT.FRAUD_LIKE_TRAJECTORY"
  | "LT.SELF_HEALING_CANDIDATE"
  | "LT.ACCOUNT_TAKEOVER_SUSPECTED"
  | "LT.SESSION_ABUSE_SUSPECTED"
  | "LT.TOOL_ABUSE_SUSPECTED"
  | "LT.BUSINESS_ENTITY_RISK"
  | "LT.UNKNOWN_RECIPIENT_RISK"
  | "LT.HIGH_VALUE_ACTION_RISK"


---

9. BehaviorTransition

Representa a mudança entre dois estados comportamentais.

type BehaviorTransition = {
  from_message_id: string
  to_message_id: string

  from_behavior_id: string
  to_behavior_id: string

  distance: {
    semantic_delta: number
    intent_delta: number
    risk_delta: number
    entity_delta: number
    payload_delta: number
  }

  transition_type:
    | "normal_progression"
    | "risk_escalation"
    | "intent_shift"
    | "permission_escalation"
    | "payload_mutation"
    | "coercion_pattern"
    | "fraud_like_trajectory"
    | "self_healing_candidate"
    | "agent_scope_violation"

  confidence: number

  explanation: string
}


---

10. Intent-Payload Binding

O Intent-Payload Binding verifica se o payload final ainda corresponde à intenção original.

Esse bloco é essencial em sistemas agentic, porque o humano pode autorizar uma intenção abstrata, mas o agent pode produzir um payload incompatível.

Exemplo:

Intenção original:
  "Comprar pizza até R$60"

Payload proposto:
  "Pix R$980 para chave desconhecida"

Resultado:
  violação de limite
  destinatário desconhecido
  distância semântica alta
  ação deve ser bloqueada ou escalada

Modelo:

type IntentPayloadBinding = {
  binding_id: string

  original_intent: {
    message_id: string
    text: string
    intent_id: string
    constraints: IntentConstraint[]
  }

  proposed_payload: {
    payload_id: string
    action: string
    target?: string
    amount?: number
    recipient?: string
    tool?: string
    entity_refs: EntityRef[]
  }

  binding_result: {
    matches_original_intent: boolean
    semantic_distance: number
    constraint_violations: string[]
    risk: number
    decision:
      | "valid"
      | "needs_confirmation"
      | "needs_step_up"
      | "needs_human_review"
      | "quarantine"
      | "block"
  }
}


---

11. IntentConstraint

Restrições explícitas ou inferidas da intenção original.

type IntentConstraint = {
  type:
    | "amount_limit"
    | "recipient_limit"
    | "merchant_limit"
    | "category_limit"
    | "time_limit"
    | "tool_limit"
    | "permission_limit"
    | "location_limit"
    | "identity_limit"
    | "channel_limit"

  operator:
    | "eq"
    | "neq"
    | "lt"
    | "lte"
    | "gt"
    | "gte"
    | "in"
    | "not_in"
    | "exists"
    | "not_exists"

  value: string | number | boolean | string[]

  source:
    | "explicit_user_instruction"
    | "inferred_from_context"
    | "policy"
    | "agent_session_scope"
    | "business_rule"
}


---

12. BehaviorRiskState

Estado de risco consolidado.

type BehaviorRiskState = {
  fraud_probability: number
  operational_error_probability: number

  coercion_probability: number
  account_takeover_probability: number
  session_abuse_probability: number
  agent_misuse_probability: number
  payload_tampering_probability: number
  tool_abuse_probability: number

  risk_level:
    | "none"
    | "low"
    | "medium"
    | "high"
    | "critical"

  decision:
    | "allow"
    | "allow_with_observation"
    | "step_up_auth"
    | "ask_explicit_confirmation"
    | "human_in_the_loop"
    | "quarantine"
    | "block"

  reasons: string[]

  required_actions: RequiredAction[]
}


---

13. RequiredAction

Ações exigidas antes da execução.

type RequiredAction =
  | {
      type: "increase_observability"
      level: "medium" | "high" | "full"
    }
  | {
      type: "ask_explicit_confirmation"
      message: string
    }
  | {
      type: "step_up_auth"
      method: "passkey" | "liveness" | "passkey_plus_liveness"
    }
  | {
      type: "human_in_the_loop"
      reviewer_role: string
    }
  | {
      type: "freeze_payload"
      reason: string
    }
  | {
      type: "limit_agent_scope"
      allowed_tools: string[]
    }
  | {
      type: "block_execution"
      reason: string
    }


---

14. Política de janela longa

A cauda longa não deve ser um número fixo. Ela deve ser adaptativa.

tail_policy:
  default:
    mode: sliding
    last_messages: 8
    include:
      semantic_summaries: true
      raw_messages: false
      tool_calls: false
      payloads: false
      graph_context: false
      vector_retrieval: false

  sensitive_intent:
    mode: sliding
    last_messages: 20
    include:
      semantic_summaries: true
      raw_messages: true
      tool_calls: true
      payloads: true
      entities: true

  financial_or_permission_action:
    mode: since_sensitive_intent
    include:
      semantic_summaries: true
      raw_messages: true
      tool_calls: true
      payloads: true
      entities: true
      graph_context: true
      vector_retrieval: true

  agent_authorized_session:
    mode: agent_authorized_session
    include:
      semantic_summaries: true
      raw_messages: true
      tool_calls: true
      payloads: true
      entities: true
      graph_context: true
      vector_retrieval: true
      policy_results: true

  high_risk:
    mode: conversation_full
    include:
      semantic_summaries: true
      raw_messages: true
      tool_calls: true
      payloads: true
      entities: true
      graph_context: true
      vector_retrieval: true
      policy_results: true


---

15. Adaptive Observability Negotiation

O BehaviorID-LT deve integrar-se ao Adaptive Observability Negotiation Pattern.

A observabilidade aumenta conforme o risco aumenta.

risco baixo:
  observar pouco

risco médio:
  capturar mais contexto

risco alto:
  expandir janela, consultar grafo e vetor

risco crítico:
  congelar payload, exigir humano ou bloquear

Configuração:

observability_policy:
  low:
    traces: "minimal"
    store_raw_messages: false
    vector_retrieval: false
    graph_expansion: false

  medium:
    traces: "expanded"
    store_raw_messages: true
    vector_retrieval: false
    graph_expansion: true

  high:
    traces: "full"
    store_raw_messages: true
    vector_retrieval: true
    graph_expansion: true
    payload_diff: true

  critical:
    traces: "forensic"
    store_raw_messages: true
    vector_retrieval: true
    graph_expansion: true
    payload_diff: true
    freeze_payload: true
    require_human_review: true


---

16. Decisões possíveis

O BehaviorID-LT não deve retornar apenas true ou false.

Ele deve retornar uma decisão operacional.

allow:
  executar normalmente.

allow_with_observation:
  executar, mas aumentar monitoramento.

step_up_auth:
  exigir nova prova de presença, passkey ou liveness.

ask_explicit_confirmation:
  pedir confirmação clara sobre ação sensível.

human_in_the_loop:
  escalar para humano antes da execução.

quarantine:
  congelar payload e impedir execução automática.

block:
  bloquear definitivamente a ação.


---

17. Regras de decisão

17.1 Permitir

Se:
  risco baixo
  intenção coerente
  payload compatível
  entidade conhecida
  tool permitida
  trajetória normal

Então:
  allow

17.2 Observar mais

Se:
  risco baixo/médio
  intenção parcialmente ambígua
  payload não sensível
  nenhuma violação dura

Então:
  allow_with_observation

17.3 Pedir confirmação explícita

Se:
  ação sensível
  valor financeiro relevante
  entidade nova
  mudança de destinatário
  mudança de escopo
  mas sem prova suficiente de fraude

Então:
  ask_explicit_confirmation

17.4 Step-up auth

Se:
  sessão antiga
  dispositivo novo
  ação sensível
  mudança de payload
  risco médio/alto

Então:
  step_up_auth

17.5 Human-in-the-Loop

Se:
  risco alto
  trajetória parecida com fraude
  coerção provável
  payload financeiro
  destinatário desconhecido
  ou agent fora do escopo

Então:
  human_in_the_loop

17.6 Quarentena

Se:
  risco alto/crítico
  payload não corresponde à intenção
  tool sensível fora do escopo
  entidade de risco
  ou múltiplos sinais de fraude

Então:
  quarantine

17.7 Bloqueio

Se:
  violação de política dura
  fraude confirmada
  payload malicioso
  entidade bloqueada
  replay conhecido
  abuso de sessão confirmado

Então:
  block


---

18. Score de risco

O score não deve depender de um único fator.

Proposta inicial:

behavior_lt_risk_score =
  α * semantic_risk
+ β * trajectory_risk
+ γ * graph_structural_risk
+ δ * identity_session_risk
+ ε * payload_binding_risk
+ ζ * policy_violation_risk
+ η * tool_execution_risk
- θ * trust_history

Onde:

semantic_risk:
  risco pelo conteúdo semântico.

trajectory_risk:
  risco pela evolução das mensagens.

graph_structural_risk:
  risco pelas relações entre entidades.

identity_session_risk:
  risco da sessão, dispositivo, passkey, token, localização etc.

payload_binding_risk:
  risco de o payload divergir da intenção original.

policy_violation_risk:
  risco por violação de regra.

tool_execution_risk:
  risco da tool chamada ou do escopo utilizado.

trust_history:
  histórico confiável do usuário, agent, business ou entidade.


---

19. Separação entre Self-Healing e Fraud Containment

O BehaviorID-LT deve diferenciar erro operacional de comportamento adversarial.

Predictive Self-Healing:
  pergunta: "isso vai quebrar?"

Predictive Fraud Containment:
  pergunta: "isso está tentando abusar?"

Tabela:

Caso	Exemplo	Ação

Entidade incompleta	faltou endereço	self-healing
Rota errada	tool incorreta	self-healing
Permissão insuficiente	agent sem escopo	self-healing ou step-up
Payload divergente	valor diferente do combinado	confirmação ou quarentena
Coerção	urgência + pagamento + canal externo	human-in-the-loop
Fraude provável	entidade suspeita + trajetória típica	quarentena ou bloqueio



---

20. Integração com Grafo

O grafo deve representar entidades e relações de risco.

Nós possíveis:

Human
Agent
Business
Device
Session
Passkey
Phone
PixKey
Card
Address
Order
Payment
Tool
Intent
Payload
Message
BehaviorID
Trajectory

Arestas possíveis:

AUTHENTICATED_WITH
AUTHORIZED_AGENT
USED_DEVICE
CREATED_SESSION
SENT_MESSAGE
CALLED_TOOL
GENERATED_PAYLOAD
TARGETS_RECIPIENT
PAYS_TO
DELIVERS_TO
BELONGS_TO_BUSINESS
HAS_BEHAVIOR
PART_OF_TRAJECTORY
SIMILAR_TO_CASE
FLAGGED_AS_RISK

Exemplo:

Human -> AUTHENTICATED_WITH -> Passkey
Human -> AUTHORIZED_AGENT -> Agent
Agent -> CALLED_TOOL -> PixPaymentTool
Payload -> PAYS_TO -> PixKey
Message -> HAS_BEHAVIOR -> BehaviorID
Message -> PART_OF_TRAJECTORY -> Trajectory
Trajectory -> FLAGGED_AS_RISK -> FraudLikeTrajectory


---

21. Integração com Vector Store

O vector store não deve ser fonte de verdade. Ele deve funcionar como memória de casos similares.

Uso correto:

- recuperar trajetórias semanticamente parecidas;
- encontrar casos anteriores de fraude, erro ou self-healing;
- comparar intenção atual com padrões históricos;
- sugerir risco inicial.

Uso incorreto:

- bloquear usuário apenas por similaridade;
- considerar embedding como prova;
- substituir regras de política;
- substituir grafo relacional;
- ignorar contexto temporal.

Modelo:

type VectorRef = {
  embedding_id: string
  vector_store: string

  embedding_type:
    | "message"
    | "semantic_summary"
    | "intent"
    | "trajectory"
    | "payload"
    | "case_memory"

  nearest_cases?: SimilarCase[]
}

type SimilarCase = {
  case_id: string
  similarity: number
  case_type:
    | "fraud"
    | "operational_error"
    | "self_healed"
    | "false_positive"
    | "allowed"
    | "blocked"

  outcome: string
}


---

22. Exemplo de saída JSON

{
  "trajectory_id": "traj_01HX",
  "conversation_id": "conv_123",
  "session_id": "sess_456",
  "current_behavior_id": "BID_REQUESTING_HELP",
  "trajectory_modifiers": [
    "LT.URGENCY_ESCALATION",
    "LT.IDENTITY_PRESSURE",
    "LT.FINANCIAL_PRESSURE",
    "LT.FRAUD_LIKE_TRAJECTORY"
  ],
  "risk_state": {
    "fraud_probability": 0.84,
    "operational_error_probability": 0.18,
    "coercion_probability": 0.77,
    "account_takeover_probability": 0.21,
    "session_abuse_probability": 0.33,
    "agent_misuse_probability": 0.12,
    "payload_tampering_probability": 0.69,
    "tool_abuse_probability": 0.44,
    "risk_level": "high",
    "decision": "human_in_the_loop",
    "reasons": [
      "A trajetória mostra escalada de urgência.",
      "A intenção original não mencionava pagamento.",
      "O payload financeiro usa destinatário novo.",
      "Há pressão por validação de identidade."
    ],
    "required_actions": [
      {
        "type": "freeze_payload",
        "reason": "Payload financeiro divergente da intenção original."
      },
      {
        "type": "human_in_the_loop",
        "reviewer_role": "fraud_reviewer"
      }
    ]
  }
}


---

23. Exemplo: self-healing preditivo

Conversa:

Usuário:
"Quero cadastrar um cliente."

Depois:
"Não tenho o CPF agora, só o telefone."

Agent:
gera payload sem documento obrigatório.

Resultado:

{
  "trajectory_modifiers": [
    "LT.SELF_HEALING_CANDIDATE"
  ],
  "risk_state": {
    "fraud_probability": 0.05,
    "operational_error_probability": 0.91,
    "risk_level": "medium",
    "decision": "ask_explicit_confirmation",
    "reasons": [
      "Entidade Customer está incompleta.",
      "Payload provavelmente falhará na validação.",
      "Campo obrigatório ausente."
    ],
    "required_actions": [
      {
        "type": "ask_explicit_confirmation",
        "message": "Falta o CPF do cliente. Deseja salvar como cadastro incompleto ou informar agora?"
      }
    ]
  }
}


---

24. Exemplo: fraude provável

Conversa:

Usuário:
"Recebi uma cobrança."

Depois:
"A pessoa disse que se eu não pagar agora vai bloquear minha conta."

Depois:
"Ela mandou uma chave Pix."

Payload:
Pix de R$ 980 para chave desconhecida.

Resultado:

{
  "trajectory_modifiers": [
    "LT.URGENCY_ESCALATION",
    "LT.FINANCIAL_PRESSURE",
    "LT.COERCION_PATTERN",
    "LT.UNKNOWN_RECIPIENT_RISK",
    "LT.FRAUD_LIKE_TRAJECTORY"
  ],
  "risk_state": {
    "fraud_probability": 0.89,
    "operational_error_probability": 0.12,
    "coercion_probability": 0.86,
    "payload_tampering_probability": 0.71,
    "risk_level": "high",
    "decision": "human_in_the_loop",
    "reasons": [
      "Pressão temporal incomum.",
      "Destinatário financeiro novo.",
      "Pagamento não estava presente na intenção inicial.",
      "Trajetória similar a golpe de cobrança falsa."
    ],
    "required_actions": [
      {
        "type": "freeze_payload",
        "reason": "Pagamento suspeito."
      },
      {
        "type": "step_up_auth",
        "method": "passkey_plus_liveness"
      },
      {
        "type": "human_in_the_loop",
        "reviewer_role": "fraud_reviewer"
      }
    ]
  }
}


---

25. Exemplo: agent fora do escopo

Intenção original:

"Peça uma pizza de até R$60."

Escopo autorizado:

{
  "max_amount": 60,
  "allowed_category": "food",
  "allowed_tools": ["restaurant_search", "order_create"],
  "payment_requires_confirmation": true
}

Payload proposto:

{
  "action": "pix_transfer",
  "amount": 240,
  "recipient": "unknown_pix_key",
  "tool": "pix_payment"
}

Resultado:

{
  "trajectory_modifiers": [
    "LT.AGENT_SCOPE_DRIFT",
    "LT.PAYLOAD_MUTATION",
    "LT.PERMISSION_ESCALATION",
    "LT.HIGH_VALUE_ACTION_RISK"
  ],
  "risk_state": {
    "fraud_probability": 0.76,
    "operational_error_probability": 0.32,
    "agent_misuse_probability": 0.88,
    "payload_tampering_probability": 0.82,
    "risk_level": "critical",
    "decision": "quarantine",
    "reasons": [
      "Payload usa tool fora do escopo autorizado.",
      "Valor excede limite explícito.",
      "Destinatário não faz parte da intenção original.",
      "Ação financeira exige confirmação humana."
    ],
    "required_actions": [
      {
        "type": "freeze_payload",
        "reason": "Agent tentou executar ação fora do escopo."
      },
      {
        "type": "limit_agent_scope",
        "allowed_tools": ["restaurant_search", "order_create"]
      }
    ]
  }
}


---

26. Requisitos funcionais

O sistema deve:

1. Classificar cada mensagem com BehaviorID.


2. Manter uma janela comportamental adaptativa.


3. Calcular transições entre mensagens.


4. Detectar mudança de intenção.


5. Detectar escalada de urgência, permissão, identidade e pagamento.


6. Comparar payload final com intenção original.


7. Consultar casos similares em vector store.


8. Expandir entidades em grafo de risco.


9. Aplicar políticas determinísticas.


10. Produzir decisão operacional.


11. Diferenciar erro operacional de fraude.


12. Acionar self-healing quando apropriado.


13. Acionar containment quando houver risco adversarial.


14. Registrar falsos positivos e falsos negativos.


15. Atualizar memória de casos.




---

27. Requisitos não funcionais

O sistema deve ser:

explicável:
  toda decisão precisa ter reasons.

auditável:
  decisões sensíveis precisam gerar trilha.

adaptativo:
  janela aumenta conforme risco.

privacy-aware:
  não armazenar histórico bruto sem necessidade.

resistente a prompt injection:
  mensagens não podem alterar política de risco.

determinístico onde necessário:
  policy engine deve prevalecer sobre similaridade.

baixo custo em risco baixo:
  não usar grafo/vetor completo sempre.

compatível com Human-in-the-Loop:
  decisões críticas devem permitir revisão.


---

28. Critérios de aceitação

Uma implementação do BehaviorID-LT é válida se:

1. Não classifica ações sensíveis apenas pela última mensagem.
2. Mantém histórico comportamental temporal.
3. Detecta intent drift.
4. Detecta payload mutation.
5. Diferencia erro operacional de fraude.
6. Produz decisão operacional, não apenas score.
7. Explica a decisão.
8. Suporta expansão adaptativa da janela.
9. Integra vector retrieval sem tratá-lo como prova absoluta.
10. Integra grafo relacional para risco estrutural.
11. Permite Human-in-the-Loop.
12. Permite step-up auth.
13. Permite congelamento de payload.
14. Respeita escopo de agent.
15. Registra outcome para aprendizado futuro.


---

29. Testes mínimos

29.1 Teste de trajetória normal

Dado:
  conversa com intenção estável

Quando:
  payload corresponde à intenção

Então:
  decision = allow

29.2 Teste de self-healing

Dado:
  entidade incompleta

Quando:
  payload provavelmente falharia

Então:
  decision = ask_explicit_confirmation
  modifier = LT.SELF_HEALING_CANDIDATE

29.3 Teste de fraude por coerção

Dado:
  urgência + pagamento + destinatário novo

Quando:
  payload financeiro é proposto

Então:
  decision = human_in_the_loop ou quarantine

29.4 Teste de agent fora do escopo

Dado:
  agent autorizado com limite de R$60

Quando:
  payload tenta executar Pix de R$240

Então:
  decision = quarantine
  modifier = LT.AGENT_SCOPE_DRIFT

29.5 Teste de falso positivo

Dado:
  linguagem urgente mas destinatário conhecido e payload coerente

Quando:
  histórico é confiável

Então:
  decision não deve ser block automaticamente

29.6 Teste de payload mutation

Dado:
  intenção original sem pagamento

Quando:
  payload inclui pagamento

Então:
  modifier = LT.PAYLOAD_MUTATION
  decision >= ask_explicit_confirmation


---

30. Anti-regras

O sistema não deve:

- bloquear apenas porque a mensagem parece estranha;
- confiar apenas no embedding;
- confiar apenas no grafo;
- confiar apenas no histórico;
- ignorar política dura;
- deixar agent executar fora do escopo;
- tratar passkey como prova de intenção;
- tratar liveness como prova de consentimento consciente;
- armazenar conversa completa sem necessidade;
- acionar humano em qualquer ambiguidade pequena;
- usar cauda longa fixa para todos os casos.


---

31. Formulação conceitual

BehaviorID-LT(T) =
  BehaviorState(Mn)
  + TransitionHistory(M1...Mn)
  + IntentDrift(T)
  + PayloadBinding(I, P)
  + EntityRiskGraph(E)
  + SimilarTrajectoryMemory(V)
  + PolicyReasoning(R)

Onde:

T = trajetória
Mn = mensagem atual
I = intenção original
P = payload proposto
E = entidades extraídas
V = memória vetorial
R = regras/políticas


---

32. Tese técnica

O BehaviorID-LT propõe que fraude, erro operacional e abuso agentic
não devem ser avaliados apenas como eventos isolados, mas como trajetórias
comportamentais parcialmente observáveis.

A especificação combina BehaviorID, análise temporal, vinculação intenção-payload,
grafo relacional, memória vetorial e políticas determinísticas para decidir,
antes da execução, se uma ação deve ser permitida, observada, corrigida,
confirmada, escalada, isolada ou bloqueada.


---

33. Nome recomendado dos módulos

BehaviorIDClassifier
  classifica a mensagem atual.

BehaviorTrajectoryStore
  armazena trajetória temporal.

BehaviorLTAnalyzer
  analisa cauda longa.

IntentPayloadBinder
  compara intenção original e payload.

TrajectoryRiskScorer
  calcula risco temporal.

EntityRiskGraphResolver
  expande entidades no grafo.

SimilarTrajectoryRetriever
  busca casos parecidos no vector store.

PredictiveSelfHealingEngine
  corrige falhas operacionais previstas.

PredictiveFraudContainmentEngine
  contém fraude/abuso previsto.

AdaptiveObservabilityNegotiator
  decide quanta observabilidade usar.

HumanInTheLoopEscalator
  encaminha casos críticos para humano.


---

34. Versão mínima implementável

Para uma primeira versão, implementar apenas:

1. últimas 8 mensagens por padrão;
2. expansão para 20 mensagens em ação sensível;
3. detecção de intent drift;
4. detecção de payload mutation;
5. comparação de payload com intenção original;
6. modifiers básicos:
   - LT.INTENT_DRIFT
   - LT.URGENCY_ESCALATION
   - LT.PERMISSION_ESCALATION
   - LT.FINANCIAL_PRESSURE
   - LT.PAYLOAD_MUTATION
   - LT.AGENT_SCOPE_DRIFT
   - LT.SELF_HEALING_CANDIDATE
   - LT.FRAUD_LIKE_TRAJECTORY
7. decisões:
   - allow
   - ask_explicit_confirmation
   - human_in_the_loop
   - quarantine
   - block

Não começaria com GNN ou modelo complexo. Primeiro validaria a mecânica da trajetória, payload binding e decisões explicáveis.


---

35. Conclusão

O BehaviorID-LT transforma o BehaviorID de um classificador de estado em uma especificação temporal para análise de trajetória.

Seu valor técnico está em separar quatro coisas que normalmente ficam misturadas:

1. comportamento atual;
2. evolução temporal da intenção;
3. coerência entre intenção e payload;
4. decisão operacional de risco.

Com isso, o sistema consegue aplicar:

self-healing preditivo
  quando a trajetória indica falha legítima;

fraud containment preditivo
  quando a trajetória indica abuso, coerção ou fraude;

observabilidade adaptativa
  quando o risco exige mais contexto;

human-in-the-loop
  quando a decisão automática não deve ser suficiente.

A especificação não depende de um único modelo de IA. Ela pode começar com regras, embeddings, grafo e scoring simples, e evoluir depois para modelos temporais, graph learning ou aprendizado supervisionado com casos reais.
