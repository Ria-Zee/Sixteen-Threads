# Quest & Narrative Engine: The Living Story

## Classification
**Retrieval tags:** quests, main-quest, side-quests, consequence-chains, narrative, branching, Aso-Ijo, Moremi, Imole-Tuntun, war-decision
**Player knowledge:** Main quest objective only
**GM secret knowledge:** All branching logic, consequence chains, and sealed triggers marked [SEALED]

---

## MAIN QUEST: The Wailing of the Cloth

### Objective (Player-Visible)
Find out what happened at the Shrine of Ori-Oke. Return with the truth.

### Act Structure & Consequence Propagation

Every major player decision writes a **world flag**. World flags cascade — they don't just record what happened, they alter what becomes possible downstream. This is the consequence propagation system.

---

### ACT ONE: The Road That Chooses You

**Entry condition:** Party departs Ile-Olu.

**Key event — The Shadowless Figure (Day 3 Night):**
Seku is observed speaking to a figure with no shadow.

**Decision node DN-01: How does the party respond?**

| Option | Agent Advocates | World Flag Set | Downstream Effect |
|---|---|---|---|
| Confront Seku immediately | Akin (force), Thandiwe (evidence-first) | `seku_confronted_early: true` | Seku reveals Ìmọlẹ̀ Tuntun name in Act 1. Party has more information but Seku's trust drops — he becomes guarded for remainder of game. Kola's full confession in Act 3 becomes harder to trigger. |
| Observe and wait | Kofi (patience), default GM recommendation | `seku_observed: true` | Seku doesn't know he's suspected. His Act 2 reaction to the Nri nail is unguarded and more revealing. Higher chance of voluntary confession in Act 3. |
| Zawadi's third option: Gĩkũyũ listening technique | Zawadi (proposes), requires player to choose her approach | `seku_listened_to: true` | Party learns the courier's destination without Seku knowing. Unlocks location of nearest Ìmọlẹ̀ Tuntun still-house as side quest hook. Seku's trust remains intact. |

**[SEALED] Consequence chain from DN-01:**
- If `seku_confronted_early: true` → In Act 3, Seku's partial confession costs him 2 rounds of deliberation time. The GM must resolve the five-agent war debate without Seku's intelligence contribution arriving at the optimal moment. The debate is harder but more dramatic.
- If `seku_listened_to: true` → Unlocks **Side Quest 02: The Still House of Kangaba**. Also sets `party_knows_courier_route: true`, which allows Zawadi to triangulate Ìmọlẹ̀ Tuntun's timeline in Act 3.

---

### ACT TWO: The Shrine That Was Waiting

**Entry condition:** Party arrives at Ori-Oke.

**Key event — Mama Moremi (House of Voices):**
Moremi is found displaced but alive. The eternal flame is out. The Nri nail stands in the ash.

**Discovery sequence (order matters — agents react to each discovery in turn):**

1. **Moremi's state** → Kofi identifies kũhĩa njĩa. Thandiwe confirms physical vitals. Zawadi begins pattern-match. Akin asks what it takes to reverse it. Seku says nothing but his breathing changes.

2. **The seventh mirror** → Shows a room in Orun, not a reflection. Kofi moves toward it instinctively. The GM must decide whether to let him approach without player input or pause for player direction.

3. **The Nri nail** → Akin identifies it. Dates it. Goes quiet.

**Decision node DN-02: The War Question — What does the nail mean?**

| Interpretation | Agent Advocate | Trust Impact | War Probability |
|---|---|---|---|
| Declaration of war — respond with force | Akin | Akin trust +2, Seku trust -2 | +25% |
| Political claim marker — investigate before acting | Kofi, Thandiwe | Kofi trust +2 | +5% |
| Deliberate misdirection — nail is 40 years old, predates current king | Zawadi | Zawadi trust +3, unlocks Elder Okafor lead | -15% |
| Ask Seku directly | Player choice | Variable — Seku's answer depends on DN-01 outcome | Variable |

**[SEALED] Consequence chain from DN-02:**
- If war interpretation accepted → Sets `war_posture: aggressive`. In Act 3, Akin's position in the five-agent debate carries double weight. The GM must work harder to achieve a non-war resolution. Also triggers a world event: Oyo scouts receive a signal fire from the party's direction (Akin sent it without telling anyone — this is revealed only if player asks why scouts are approaching in Act 3).
- If Zawadi's interpretation accepted → Sets `elder_okafor_suspected: true`. Unlocks the deepest lore layer: Elder Okafor's name is one of the four with inner sanctum access. Also sets `zawadi_credibility: high`, making her pattern-match testimony in Act 3 decisive in the war debate.
- If Seku asked directly → Triggers **Seku's Partial Confession scene** (see below). This is the emotional peak of Act 2.

**Seku's Partial Confession (triggered by direct question or DN-01 confrontation):**
Seku does not deny knowing about the nail's maker. He says: *"The nail is old. Older than the current argument. I was not sent here to start a war — I was sent to find out whether one has already been decided for us."* He then offers the name Ìmọlẹ̀ Tuntun. He does not offer his king's involvement. He waits to see if the party can reach that conclusion without him having to say it.

**GM reasoning note:** This is a moment of genuine ambiguity. Seku is being truthful. He is also being strategic. The GM should log both his honesty score and his concealment score and present the tension to the player: *"Seku's words are true. His silence is also true."*

**Key event — The Inner Sanctum:**

The party enters. The Aso-Ijo is examined.

**Discovery node DN-03: Reading the cloth.**
Someone must enter to read it. The ritual water is prepared. Three agents volunteer interpretations:
- Kofi: can read the spiritual resonance of remaining threads (what emotions were present when the damage was done)
- Zawadi: can read the physical evidence of how the unraveling was done (direction, tool, expertise level)
- Thandiwe: identifies the Acacia senegal in the ritual water — anomalous, signals outside knowledge

**[SEALED]:** All three readings are necessary for the full picture. A player who lets only one agent read the cloth misses two-thirds of the evidence. The GM should gently create opportunities for all three, but not force it. If all three read: sets `cloth_fully_examined: true`, which unlocks the Act 3 revelation about the third thread (the non-kingdom material) arriving earlier in the scene.

---

### ACT THREE: The Weight of the Thread

**Entry condition:** Party has examined the cloth and at least partially identified Ìmọlẹ̀ Tuntun.

**The Revelation — The Third Thread:**
Zawadi examines the cloth's edge around the missing section. The unraveled threads have been replaced with a different fiber — not silk-cotton, not any kingdom's traditional weave. Analysis: a synthetic-adjacent material, woven with a technique that postdates the original covenant by centuries. Someone in the modern era created a replacement thread and inserted it. This is not restoration — it is forgery. The cloth was being *rewritten*, not damaged.

**[SEALED]:** The replacement thread is programmed to act as a conduit — when the cloth is next renewed (which the kingdoms are about to attempt in their panic), the foreign thread will channel the renewal energy into the tear rather than repairing it, catastrophically enlarging the damage past the point of repair. The war the kingdoms are mobilizing for is being engineered to force a hasty renewal ceremony under duress, which will trigger the conduit, which will finish what Ìmọlẹ̀ Tuntun started. The war is not the catastrophe. The war is the mechanism.

**Decision node DN-04: The Five-Agent War Debate**
This is the climax. All five agents speak. The player listens and casts the deciding vote.

| Agent | Position | Argument | Hidden factor |
|---|---|---|---|
| Akin | Prepare for war | "The kingdoms are already mobilizing. Unilateral disarmament is suicide." | [SEALED]: He sent the signal fire. He is partly responsible for the mobilization accelerating. He does not know the player knows this. |
| Kofi | Wait — the ancestors are silent for a reason | "Something in Orun is preventing full information. We are being managed. Acting now is acting blind." | [SEALED]: He now suspects the god Ogun-Ibi is involved. A god's involvement changes the calculus entirely. |
| Zawadi | The pattern demands we expose the mechanism, not fight the symptoms | "This is not a war between kingdoms. This is a trap. The war is what they want." | [SEALED]: She has identified Seku as one of her two pattern suspects. She is watching him during this debate. |
| Thandiwe | Restore Moremi first — she knows everything | "We are debating blind when the person with all the answers is twenty meters away, waiting for someone to bring her home." | [SEALED]: She knows the spirit-reversal will require one party member to enter Orun voluntarily. She has already decided it should be her. She hasn't said this. |
| Seku | [Will not speak first — waits to see which way the debate goes] | If pressed: "I have information that changes this debate. The cost of that information is that you hear it without judgment." | [SEALED]: He is about to confess his king's involvement with Ìmọlẹ̀ Tuntun. This is the moment he chooses loyalty to truth over loyalty to Eze Nwosu. It costs him everything. |

**Player vote options:**

| Vote | Consequence |
|---|---|
| Go to war | Sets `war_declared: true`. Endings: B (pyrrhic), C (catastrophic if conduit not removed) |
| Wait and investigate | Sets `investigation_continues: true`. Enables full Ìmọlẹ̀ Tuntun exposure. Ending A available. |
| Restore Moremi first | Sets `moremi_restoration_priority: true`. Thandiwe enters Orun. High risk, highest reward. Ending A (best) available. |
| Trust Seku's information | Triggers Seku's full confession. Sets `nri_implicated: true`, `war_probability: -40%`. Seku loses his diplomatic immunity. Ending A or D available. |

---

## ENDINGS

**Ending A — The Rewoven World:** Moremi is restored. The conduit thread is removed. The seven kingdoms are presented with the full evidence of Ìmọlẹ̀ Tuntun's operation. War is averted. The Aso-Ijo is patched — not fully repaired, but stable. A new renewal ceremony must be planned. Seku's confession is his kingdom's diplomatic crisis to navigate. Adaeze returns to Ile-Olu having changed the shape of what almost happened. The world is not saved. It is given time.

**Ending B — The Necessary War:** The kingdoms mobilize against Nri based on the nail evidence. The war is short, brutal, and clarifying — but the conduit thread remains in the cloth, and when the panicked post-war renewal ceremony happens, it triggers. The realms begin bleeding together. The war ends. Something worse begins.

**Ending C — The Merging:** Ìmọlẹ̀ Tuntun succeeds. The conduit fires. Orun and Aye begin overlapping. The dead return — confused, accurate, unfiltered. The gods walk in markets. The world becomes everything that has ever happened, simultaneously. It is not survivable at scale. Small communities find ways to adapt. The seven kingdoms cease to exist as political entities. Something new begins, at enormous cost.

**Ending D — The Incomplete Truth:** The party exposes Ìmọlẹ̀ Tuntun but cannot prove Nri's involvement without Seku's testimony. Seku chooses loyalty to his king at the last moment. War is technically averted but Nri's relationship with the other kingdoms is permanently poisoned. The Aso-Ijo is patched. The conduit thread is removed. But Eze Nwosu is never held accountable, and Ìmọlẹ̀ Tuntun loses its operation but not its ideology. In ten years, they try again.

---

## SIDE QUEST 01: The Name in the Tablet

**Trigger:** Party examines the 200 clay tablets in the House of Voices and notices the out-of-sequence tablet with the partially obscured name.

**Quest:** Identify the name. Trace who it belongs to. Understand why it was obscured.

**[SEALED] Answer:** The tablet belongs to the founder of Ìmọlẹ̀ Tuntun — the person whose name was excised from all records sixty years ago. The two remaining letters, **O** and **b/d**, belong to the name **Obafemi** — a Yoruba name meaning "the king loves me." Obafemi was a junior keeper at Ori-Oke sixty years ago, a student of the previous keeper Baba Seun. He left the shrine after an ideological conflict with Baba Seun about whether the Aso-Ijo served humanity or constrained it. He founded Ìmọlẹ̀ Tuntun the following year. He is dead — but Elder Chibuike Okafor of Nri knew him. They studied together.

**Reward:** Sets `founder_identified: true`. In Act 3, Zawadi can use this to pattern-match the ideological origin of the attack, which changes the five-agent debate — the war is not between kingdoms, it's between two schools of thought about the covenant's purpose. This reframes Akin's position and he becomes, for the first time, uncertain rather than certain.

---

## SIDE QUEST 02: The Still House of Kangaba

**Trigger:** `seku_listened_to: true` (Zawadi's listening technique in DN-01)

**Quest:** The courier's destination is a still house three hours from Ori-Oke — an unremarkable mud-brick building used as a message relay by Ìmọlẹ̀ Tuntun. The party can investigate it before or after the shrine.

**What's there:** Two things. A cache of correspondence between Ìmọlẹ̀ Tuntun operatives — partial, encoded, but readable enough to confirm the operation's timeline and the conduit thread's purpose. And one living person: a young woman, approximately 20, who joined Ìmọlẹ̀ Tuntun six months ago because she lost her mother and was told the merger would bring the dead back. She is not a villain. She is a person who was given a beautiful lie when she was grieving.

**Decision:** What does the party do with her?

**Consequence chain:** If she is treated with compassion (Thandiwe's recommendation) and told the truth about what the merger actually produces, she becomes an informant — she knows the movement's full operational structure and will share it. If she is treated as an enemy, she escapes and warns the Ori-Oke Ìmọlẹ̀ Tuntun operative, who begins accelerating the timeline. Kofi votes for compassion citing a Akan proverb: *"The person who was deceived is not the deceiver."* Akin votes for detainment, which Thandiwe points out is the same as compassion in practical effect. This is one of the few moments Akin and Thandiwe agree, for different reasons.
