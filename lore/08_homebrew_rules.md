# Homebrew Rules: The Mechanics of Aye-Orun

## Classification
**Retrieval tags:** rules, mechanics, dice, checks, combat, trust, health, confidence, disagreement, agent-mechanics, game-system
**Player knowledge:** Full — these are the visible rules of the game
**GM note:** These rules exist to be enforced by the GM agent in code. Every rule has a corresponding world state field.

---

## Core Philosophy

This is not a combat game wearing a story costume. It is a **reasoning game with consequences**. The primary resource is not health points — it is **Trust** and **Information**. Characters can be physically fine and catastrophically compromised. The rules reflect this.

---

## The Five Core Stats (Per Character Agent)

Each agent tracks five stats. These are stored in world state and updated after every major scene.

```json
{
  "agent_id": "akin",
  "health": 100,
  "trust": 75,
  "credibility": 80,
  "emotional_state": "vigilant",
  "hidden_knowledge": ["nail_forge_school", "signal_fire_sent"]
}
```

**Health (0–100):** Physical condition. Reaches 0 only in extreme circumstances — this game rarely kills agents through combat. More commonly depleted through: spirit-realm exposure without preparation (-15), forcing entry through iron barriers (-10), extended kũhĩa njĩa adjacent states (-20 per day).

**Trust (0–100):** How much the party (and player) trusts this agent. Starts at values reflecting their initial disposition. Drops when an agent is caught concealing information, rises when they demonstrate loyalty under pressure. At Trust 0, an agent becomes unreliable — they begin optimizing for their own goals over the party's. At Trust 100, an agent will sacrifice something personal for the party without being asked.

**Credibility (0–100):** How much weight the GM gives this agent's arguments in disagreement resolution. Earned through being correct. Lost through being wrong confidently. A high-credibility agent can shift the GM's confidence score by ±20 in a disagreement. A low-credibility agent's arguments require corroboration.

**Emotional State:** A tag that modifies behavior. States: `vigilant`, `uncertain`, `grieving`, `focused`, `compromised`, `resolved`. The GM uses emotional state to determine how an agent phrases their arguments and what information they volunteer versus withhold.

**Hidden Knowledge:** A list of facts the agent knows but has not shared. The GM tracks this. When relevant hidden knowledge would change a scene outcome, the GM must make a judgment call: does the agent share it voluntarily, share it under pressure, or withhold it (and if so, why)?

---

## Ability Checks

When an agent attempts something uncertain, the GM rolls a d20 and adds the relevant modifier. Result determines outcome tier.

**Modifiers by agent and domain:**

| Domain | Akin | Kofi | Zawadi | Thandiwe | Seku | Adaeze |
|---|---|---|---|---|---|---|
| Combat / Force | +7 | -2 | +1 | +3 | +1 | -1 |
| Spirit / Divination | -1 | +8 | +4 | +2 | +1 | +0 |
| Pattern / History | +2 | +4 | +8 | +3 | +5 | +3 |
| Healing / Medicine | +1 | +2 | +3 | +8 | +1 | +2 |
| Diplomacy / Persuasion | +3 | +5 | +4 | +4 | +8 | +7 |
| Deception / Concealment | +2 | +1 | +6 | +2 | +7 | +3 |
| Endurance / Will | +6 | +5 | +5 | +6 | +4 | +5 |

**Outcome tiers:**
- **1–5: Failure with complication** — the attempt fails AND creates a new problem
- **6–10: Failure** — the attempt fails, no new problem
- **11–15: Partial success** — the attempt partially succeeds; GM determines what is gained and what is not
- **16–19: Success** — full success
- **20: Critical success** — success plus an unexpected bonus (additional information, trust gain, or a world flag set favorably)

**Natural 20 special rule:** When any agent rolls a natural 20, they gain one piece of information from their Hidden Knowledge list automatically — the success makes them generous. When Seku rolls a natural 20 on a diplomacy check, he reveals one level deeper of his concealed information. The GM tracks what has been revealed.

---

## The Trust Economy

Trust is the game's primary currency. It flows between: player ↔ agents, and agents ↔ agents.

**Trust gain events:**
- Agent shares information that costs them something (+5 to +15 depending on personal cost)
- Agent's prediction proves accurate (+5)
- Agent voluntarily changes position after hearing new evidence (+8 — this is rare and valuable)
- Agent protects another party member without being asked (+10)
- Agent's hidden knowledge revealed to have been relevant and withheld: they proactively confess it (+12)

**Trust loss events:**
- Agent caught withholding relevant information (-10 to -20 depending on stakes)
- Agent's prediction proves wrong (-5)
- Agent refuses to update position despite contradicting evidence (-8)
- Agent acts on personal agenda without disclosure (-15)
- Agent lies directly (-25 — trust rarely recovers from direct lies)

**Trust thresholds and effects:**

| Trust Level | Agent Behavior |
|---|---|
| 90–100 | Agent shares hidden knowledge proactively. Will argue against their own position if evidence warrants. |
| 70–89 | Normal operation. Agent shares when asked directly. Advocates for position confidently. |
| 50–69 | Agent becomes selective — shares information that supports their position, withholds information that doesn't. |
| 30–49 | Agent begins optimizing for their own agenda. Arguments become subtly self-serving. GM flags this for player. |
| 10–29 | Agent is operating independently. They remain in the party but are no longer fully cooperative. |
| 0–9 | Agent leaves the party or becomes actively obstructive. Seku at 0 trust would report to his king and potentially warn Ìmọlẹ̀ Tuntun. |

---

## The Disagreement Resolution System

This is the system's signature mechanic — what makes it a **reasoning game** rather than a choice game.

When two or more agents advocate for conflicting courses of action, the GM does not simply average their positions or defer to the highest-trust agent. The GM runs a structured resolution:

### Step 1: Position Declaration
Each disagreeing agent states their position and primary argument. The GM logs:
```json
{
  "disagreement_id": "DN-02-nail-interpretation",
  "positions": [
    {"agent": "akin", "stance": "declaration_of_war", "argument": "Iron claim on sacred fire = act of war in any tradition", "confidence": 0.85},
    {"agent": "kofi", "stance": "investigate_first", "argument": "Claim markers are political not military; acting on military assumption is premature", "confidence": 0.75},
    {"agent": "zawadi", "stance": "misdirection", "argument": "40-year-old nail predates current king's reign; implicates Nri institution not current government", "confidence": 0.90}
  ]
}
```

### Step 2: Foundry IQ Query
The GM queries the knowledge base for relevant lore. The query result modifies confidence scores:
- If retrieved lore supports an agent's position: their confidence +0.10
- If retrieved lore contradicts an agent's position: their confidence -0.15
- If retrieved lore provides new information not in any position: GM creates a new position option

### Step 3: Cross-examination
Each agent may challenge one other agent's argument. Challenge success depends on:
- Challenger's Credibility score (determines how seriously the GM weights the challenge)
- Ability check if the challenge requires specific expertise
- Logical validity (the GM evaluates this — a valid challenge lands regardless of credibility)

### Step 4: GM Resolution
The GM calculates a weighted confidence score across all positions, incorporating:
- Each agent's Credibility score
- Foundry IQ evidence
- Cross-examination outcomes
- Player's known preferences (player can bias but not determine outcome)

The GM then produces:
```json
{
  "resolution": "zawadi_misdirection",
  "confidence": 0.82,
  "reasoning_trace": "Zawadi's dating argument is supported by forge-school records in Foundry IQ. Kofi's political distinction is valid but incomplete — the nail's age makes current-Nri culpability unlikely. Akin's military reading is emotionally coherent but factually unsupported by the evidence. Credibility weighting: Zawadi +3, Kofi +2, Akin -1 (overconfident on incomplete evidence). Resolution: investigate Elder Okafor connection.",
  "world_flags_set": ["elder_okafor_suspected", "zawadi_credibility_high"],
  "trust_changes": {"zawadi": +3, "akin": -1}
}
```

The player sees the reasoning trace in full. This is the transparency that makes the system trustworthy.

---

## Spirit Realm Rules (Orun Mechanics)

Entering Orun voluntarily requires:
1. Ritual preparation (Thandiwe handles this — Acacia senegal bath, specific prayer sequence)
2. A strong reason — Orun's geography resists purposeless entry. A person who enters without genuine intent finds the realm extends indefinitely around them.
3. An anchor — a physical object held by someone in Aye, connected to the traveler. Without an anchor, the traveler cannot find the return path.

**Inside Orun:**
- Time does not pass in Aye while someone is in Orun — for Aye, the traveler simply stops. For the traveler, Orun time is experienced normally.
- The traveler retains all memories and personality but emotional states are muted — fear, anger, grief are present but at lower amplitude. Clarity is heightened.
- Navigation is by memory and intent: think of the place you need to reach, and the road arranges itself. Uncertainty about your destination produces a road that loops.
- Spirits in Orun cannot be physically harmed. Guardians can expel a traveler — this returns them to Aye instantly, with 30 health damage from the transition shock.

**Returning from Orun:**
- The anchor is pulled by the person holding it in Aye — they must physically pull the connected object toward them.
- If the anchor is dropped, destroyed, or taken while the traveler is in Orun: the traveler cannot return without a god's intervention or the resolution of whatever displaced them.
- Moremi's situation: her anchor is held by Elder Okafor (the carved figure). He must release it. He can do this at any distance — the release is an act of will, not a physical one. He must decide to release her.

---

## Health and Harm

Combat is rare and resolved quickly. The GM does not narrate extended fight sequences — combat is a check, a consequence, and a state update.

**Combat check:** Attacker rolls d20 + combat modifier vs. Defender's d20 + endurance modifier. Winner deals 10–30 health damage (d20 roll determines amount within range).

**Non-combat harm sources:**
- Spirit-realm exposure without preparation: -15 health per scene
- Prolonged contact with boundary-straddler (the dual-state is contagious in small doses over time): -5 health per hour of proximity
- Emotional state `compromised` (sustained distress): -5 health per day, resists healing until cause addressed
- Thandiwe's treatment: +15–25 health per rest period (she is extremely good at her job)

**Death:** An agent reaching 0 health does not die automatically. They are incapacitated — Thandiwe has ten minutes to stabilize them, after which they recover with permanent consequences (a stat reduction, an emotional state change, or a piece of hidden knowledge revealed by the trauma). Player characters who reach 0 in Orun cannot be stabilized — they have twenty minutes of game time to find a resolution.

---

## The Kora Code (Seku's Special Mechanic)

If any player or agent has the Mandinka griot listening skill (or learns it during the game), they can request that Seku "speak through the kora." Seku will play a sequence. The listener rolls d20 + pattern modifier to decode.

- **Roll 1–10:** They hear music. Beautiful, uninformative.
- **Roll 11–15:** They decode the emotional content — they understand what Seku *feels* about a topic, not what he knows.
- **Roll 16–19:** They decode one specific piece of information Seku has encoded.
- **Roll 20:** They decode the insurance sequence — the full account of Eze Nwosu's communication with Ìmọlẹ̀ Tuntun, encoded as a precaution. Seku does not know they have heard this. The GM must decide how Seku reacts when the player demonstrates knowledge they could only have from the kora.
