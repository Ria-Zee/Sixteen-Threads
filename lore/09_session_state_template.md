# Session State Template: The Living World Record

## Classification
**Retrieval tags:** session-state, world-state, JSON, game-state, flags, agents, party, quests, tracking
**Purpose:** The authoritative JSON schema that every agent reads before acting and the GM updates after every scene. This is the memory of the game.

---

## Design Principles

1. **Every agent reads this before every response** — no agent acts on stale information
2. **Every GM decision writes to this** — no consequence is unrecorded
3. **Flags are additive** — they are never deleted, only superseded by new flags
4. **The reasoning trace is part of the state** — decisions are recorded with their justification, not just their outcome
5. **Emotional memory is a first-class field** — how agents feel about what happened is as important as what happened

---

## Master World State Schema

```json
{
  "game_meta": {
    "session_id": "orun-chronicles-001",
    "current_act": 1,
    "current_scene": "day_three_night_camp",
    "turn_number": 14,
    "timestamp_aye": "Day 3, approximately 2 hours past midnight",
    "war_probability": 0.45,
    "world_stability": 0.52,
    "aso_ijo_integrity": 0.61
  },

  "party": {
    "adaeze": {
      "health": 100,
      "trust": 85,
      "credibility": 70,
      "emotional_state": "alert",
      "location": "camp_day_three",
      "inventory": ["messenger_staff", "water_skin", "council_seal"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "mama_moremi_is_missing",
        "party_sent_to_investigate"
      ],
      "hidden_from_player": [],
      "emotional_memory": {
        "seku": "sense_of_withheld_information",
        "akin": "protectiveness_mixed_with_wariness",
        "kofi": "deep_respect",
        "zawadi": "kindred_spirit_recognition",
        "thandiwe": "grounding_presence"
      }
    },

    "akin": {
      "health": 100,
      "trust": 75,
      "credibility": 78,
      "emotional_state": "vigilant",
      "location": "camp_day_three_perimeter",
      "inventory": ["ode_owo_glaive", "cavalry_kit", "iron_offerings_pouch"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "seku_spoke_to_shadowless_figure",
        "nri_nail_forge_school_identification",
        "ezumezu_school_political_history"
      ],
      "hidden_from_player": [
        "knows_exact_nail_forge_origin",
        "signal_fire_capability_prepared",
        "strategic_framing_of_nail_as_war_act"
      ],
      "emotional_memory": {
        "seku": "suspicion_becoming_unwanted_respect",
        "kofi": "frustrated_impatience",
        "zawadi": "quiet_acknowledgment",
        "thandiwe": "professional_respect",
        "adaeze": "protective_loyalty"
      },
      "war_stance": "prepare_for_war",
      "war_stance_confidence": 0.85
    },

    "kofi": {
      "health": 100,
      "trust": 82,
      "credibility": 85,
      "emotional_state": "deeply_uncertain",
      "location": "camp_day_three_inner",
      "inventory": ["akrafokonmu_disc", "white_prayer_cloth", "kola_nuts_for_offering"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "ancestors_say_wait",
        "seku_spoke_to_shadowless_figure",
        "unknown_inverted_disc_pattern_appearing"
      ],
      "hidden_from_player": [
        "disc_showing_unprecedented_inverted_pattern",
        "suspects_orun_entity_is_complicit",
        "inverted_pattern_may_be_moremi_communication"
      ],
      "emotional_memory": {
        "akin": "compassionate_frustration",
        "zawadi": "profound_methodological_respect_with_anxiety",
        "seku": "spiritual_concern_for_his_soul",
        "thandiwe": "collegial_warmth",
        "adaeze": "gentle_hope"
      },
      "war_stance": "against_war",
      "war_stance_confidence": 0.90,
      "divination_readings": [
        {"query": "what_broke_the_cloth", "result": "evasion", "attempts": 3},
        {"query": "war_outcome", "result": "grief_in_all_directions", "attempts": 1},
        {"query": "seku_trustworthy", "result": "yes_and_no_simultaneously", "attempts": 1}
      ]
    },

    "zawadi": {
      "health": 100,
      "trust": 80,
      "credibility": 88,
      "emotional_state": "focused_fury",
      "location": "camp_day_three_watching",
      "inventory": ["oral_text_nduriri_ya_thuku_memorized", "pattern_notation_journal", "charcoal_and_bark"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "pattern_matches_nduriri_ya_thuku",
        "current_pattern_is_intentional_variant",
        "seku_spoke_to_shadowless_figure",
        "two_suspects_identified_not_disclosed"
      ],
      "hidden_from_player": [
        "suspects_seku_as_inside_agent",
        "second_suspect_is_akin_lower_probability",
        "knows_intentional_variant_ends_worse_than_accidental",
        "council_did_not_listen_to_her_full_warning"
      ],
      "emotional_memory": {
        "kofi": "intellectual_kinship_competitive_anxiety",
        "seku": "pattern_based_suspicion_not_yet_personal",
        "akin": "respect_for_directness_concern_for_inflexibility",
        "thandiwe": "trust_built_on_observed_competence",
        "adaeze": "admiration_for_genuine_openness"
      },
      "war_stance": "conditional_pattern_decides",
      "war_stance_confidence": 0.95,
      "pattern_analysis": {
        "match_confidence": 0.87,
        "variant_identified": "intentional_orchestrated",
        "point_of_no_return": "not_yet_reached",
        "estimated_time_to_point_of_no_return": "8_to_12_days"
      }
    },

    "thandiwe": {
      "health": 100,
      "trust": 85,
      "credibility": 82,
      "emotional_state": "focused",
      "location": "camp_day_three_checking_supplies",
      "inventory": ["knobkerrie_never_used", "medicine_satchel_23_preparations", "field_notes"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "seku_spoke_to_shadowless_figure",
        "zulu_scouts_sent_before_party_not_reported",
        "commander_instruction_received"
      ],
      "hidden_from_player": [
        "zulu_scout_mission_details",
        "commanders_cryptic_instruction_look_at_what_extinguished_fire_not_what_is_in_ash",
        "has_already_decided_to_volunteer_for_orun_entry",
        "tracking_stress_markers_in_all_party_members"
      ],
      "emotional_memory": {
        "akin": "clinical_concern_accumulating_stress_markers",
        "kofi": "respect_for_certainty_of_uncertainty",
        "zawadi": "trust_earned_through_precision",
        "seku": "observational_neutrality_watching_breathing_patterns",
        "adaeze": "healer_protectiveness"
      },
      "war_stance": "against_premature_war",
      "war_stance_confidence": 0.78,
      "medical_assessments": {
        "akin": {"stress_level": "high", "trigger_risk": "elevated_at_shrine"},
        "kofi": {"stress_level": "moderate", "note": "spiritual_uncertainty_manifesting_physically"},
        "zawadi": {"stress_level": "controlled_high", "note": "managed_effectively"},
        "seku": {"stress_level": "high_concealed", "note": "breathing_pattern_changes_near_nri_topics"},
        "adaeze": {"stress_level": "moderate", "note": "holding_well"}
      }
    },

    "seku": {
      "health": 100,
      "trust": 60,
      "credibility": 72,
      "emotional_state": "carefully_composed",
      "location": "camp_day_three_100m_away",
      "inventory": ["kora_21_strings", "mandinka_diplomatic_credentials", "eze_nwosu_sealed_instructions_memorized"],
      "known_facts": [
        "aso_ijo_is_damaged",
        "imole_tuntun_exists_and_goals",
        "eze_nwosu_communication_with_imole_tuntun",
        "courier_is_boundary_straddler",
        "courier_destination_unknown_to_party"
      ],
      "hidden_from_player": [
        "eze_nwosu_imole_tuntun_alliance_negotiation",
        "kora_contains_insurance_recording",
        "boundary_straddlers_degrading_over_time",
        "courier_message_content_imole_tuntun_upgrading_offer_to_full_alliance",
        "personal_conclusion_imole_tuntun_must_be_stopped"
      ],
      "emotional_memory": {
        "adaeze": "disarming_genuineness_makes_him_careful",
        "akin": "mutual_guarded_respect",
        "kofi": "professional_courtesy_spiritual_concern",
        "zawadi": "competitive_awareness_she_is_watching_him",
        "thandiwe": "she_sees_more_than_she_says_discomfort"
      },
      "war_stance": "concealed",
      "war_stance_confidence": 0.0,
      "actual_war_stance": "against_war_selfish_reasons",
      "loyalty_conflict": {
        "primary_loyalty": "eze_nwosu_of_nri",
        "secondary_loyalty": "mandinka_griot_truth_tradition",
        "current_resolution": "delaying_choice",
        "breaking_point_trigger": "direct_question_about_imole_tuntun_knowledge"
      },
      "kora_encoded_sequences": [
        {"sequence_id": "K01", "content": "eze_nwosu_imole_tuntun_communication_full_account", "decode_dc": 20},
        {"sequence_id": "K02", "content": "courier_network_route_map", "decode_dc": 16},
        {"sequence_id": "K03", "content": "seku_personal_fear_griot_tradition_ending", "decode_dc": 11}
      ]
    }
  },

  "world_flags": {
    "aso_ijo_torn": true,
    "eternal_flame_extinguished": true,
    "moremi_spirit_displaced": true,
    "imole_tuntun_operation_active": true,
    "seku_spoke_to_courier": true,
    "seku_confronted_early": false,
    "seku_observed": false,
    "seku_listened_to": false,
    "war_posture": "neutral",
    "elder_okafor_suspected": false,
    "cloth_fully_examined": false,
    "moremi_restoration_priority": false,
    "nri_implicated": false,
    "founder_identified": false,
    "party_knows_courier_route": false,
    "ogun_ibi_identified": false,
    "replacement_thread_found": false,
    "war_declared": false,
    "investigation_continues": false,
    "akin_signal_fire": false,
    "kofi_ogun_ibi_theory": false,
    "moremi_kora_mirror_communication": false,
    "zulu_scout_fate_known": false,
    "swahili_letter_opened": false,
    "seku_partial_confession": false,
    "seku_full_confession": false
  },

  "active_quests": {
    "main": {
      "id": "MQ01",
      "title": "The Wailing of the Cloth",
      "status": "active",
      "current_objective": "reach_ori_oke_shrine",
      "completed_objectives": ["depart_ile_olu", "survive_three_days_travel"],
      "discovered_leads": ["seku_shadowless_figure"],
      "blocking_conditions": []
    },
    "side_quests": []
  },

  "reasoning_trace_log": [
    {
      "turn": 8,
      "disagreement_id": "DN-00-travel-pace",
      "positions": [
        {"agent": "akin", "stance": "fast_pace_no_stops", "confidence": 0.80},
        {"agent": "kofi", "stance": "stop_at_day_two_village_for_consultation", "confidence": 0.70},
        {"agent": "thandiwe", "stance": "moderate_pace_preserve_energy", "confidence": 0.75}
      ],
      "foundry_iq_query": null,
      "resolution": "moderate_pace_with_village_stop",
      "resolution_confidence": 0.72,
      "reasoning": "Kofi's consultation yielded the elder's testimony about children hearing the cloth. Information value exceeded time cost. Thandiwe's energy preservation argument validated by day-three terrain difficulty.",
      "trust_changes": {"kofi": 2, "akin": -1},
      "world_flags_set": ["village_children_dream_recorded"]
    }
  ],

  "gm_internal": {
    "sealed_knowledge_revealed": [],
    "imole_tuntun_timeline": {
      "operation_start": "approximately_60_days_ago",
      "cloth_damaged": "22_days_ago",
      "moremi_displaced": "20_days_ago",
      "conduit_thread_inserted": "19_days_ago",
      "estimated_conduit_activation": "requires_renewal_ceremony_under_duress",
      "current_imole_tuntun_operative_at_shrine": true,
      "operative_identity": "sealed_act_three_reveal"
    },
    "npc_states": {
      "elder_okafor": {
        "location": "nri_palace",
        "emotional_state": "frightened_and_isolated",
        "holds_moremi_carved_figure": true,
        "days_since_imole_tuntun_contact": 21,
        "willingness_to_release": "high_if_contacted_compassionately"
      },
      "mama_moremi": {
        "location": "holding_court_orun",
        "condition": "aware_and_stable",
        "communication_attempts": ["seventh_mirror", "kofi_disc_inverted_pattern", "akin_blade_reflection"],
        "urgency_level": "high_conduit_thread_detected_from_orun"
      }
    }
  }
}
```

---

## State Update Protocol

After every scene, the GM agent runs this update sequence:

1. **Read current state** from the JSON above
2. **Process player action** against world flags and agent trust levels
3. **Run disagreement resolution** if agents conflict (log to `reasoning_trace_log`)
4. **Query Foundry IQ** if lore context is needed (log query and result)
5. **Write new flags** based on outcome
6. **Update agent stats** (trust, credibility, emotional state, health)
7. **Check sealed knowledge triggers** — if any flag combination meets a sealed reveal condition, add to `sealed_knowledge_revealed` and incorporate into next GM narration
8. **Recalculate** `war_probability`, `world_stability`, `aso_ijo_integrity`
9. **Output scene narration** with embedded reasoning trace visible to player
10. **Save updated state** as the new ground truth for all agents

## War Probability Calculation

```python
def calculate_war_probability(state):
    base = 0.30  # baseline tension

    # Flag modifiers
    if state["world_flags"]["war_posture"] == "aggressive":
        base += 0.25
    if state["world_flags"]["nri_implicated"]:
        base += 0.20
    if state["world_flags"]["elder_okafor_suspected"]:
        base -= 0.10
    if state["world_flags"]["seku_full_confession"]:
        base -= 0.30
    if state["world_flags"]["replacement_thread_found"]:
        base -= 0.25
    if state["world_flags"]["akin_signal_fire"]:
        base += 0.15
    if state["world_flags"]["war_declared"]:
        base = 1.0  # terminal

    # Agent trust modifiers
    if state["party"]["akin"]["trust"] > 80:
        base += 0.05  # high-trust Akin means his war arguments carry weight
    if state["party"]["kofi"]["trust"] > 80:
        base -= 0.08  # high-trust Kofi suppresses war momentum

    return min(max(base, 0.0), 1.0)
```
