"""
Sixteen Threads -- World State Manager
=======================================
Loads, saves, and updates the canonical game state JSON.
Every agent reads this before acting. GM writes to it after every scene.
"""

import json
import copy
from pathlib import Path
from datetime import datetime
from typing import Any

STATE_PATH = Path(__file__).parent.parent / "game_engine" / "current_state.json"
HISTORY_DIR = Path(__file__).parent.parent / "game_engine" / "history"


DEFAULT_STATE = {
    "game_meta": {
        "session_id": "sixteen-threads-001",
        "current_act": 1,
        "current_scene": "day_three_night_camp",
        "turn_number": 0,
        "timestamp_aye": "Day 3, approximately 2 hours past midnight",
        "war_probability": 0.45,
        "world_stability": 0.52,
        "aso_ijo_integrity": 0.61,
    },
    "party": {
        "adaeze": {
            "health": 100, "trust": 85, "credibility": 70,
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
            "health": 100, "trust": 75, "credibility": 78,
            "emotional_state": "vigilant",
            "location": "camp_day_three_perimeter",
            "inventory": ["ode_owo_glaive", "cavalry_kit", "iron_offerings_pouch"],
            "known_facts": [
                "aso_ijo_is_damaged",
                "seku_spoke_to_shadowless_figure",
                "nri_nail_forge_school_identification"
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
            "health": 100, "trust": 82, "credibility": 85,
            "emotional_state": "deeply_uncertain",
            "location": "camp_day_three_inner",
            "inventory": ["akrafokonmu_disc", "white_prayer_cloth", "kola_nuts"],
            "known_facts": [
                "aso_ijo_is_damaged",
                "ancestors_say_wait",
                "seku_spoke_to_shadowless_figure",
                "unknown_inverted_disc_pattern_appearing"
            ],
            "hidden_from_player": [
                "disc_showing_unprecedented_inverted_pattern",
                "suspects_orun_entity_complicit",
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
                {"query": "war_outcome", "result": "grief_in_all_directions", "attempts": 1}
            ]
        },
        "zawadi": {
            "health": 100, "trust": 80, "credibility": 88,
            "emotional_state": "focused_fury",
            "location": "camp_day_three_watching",
            "inventory": ["nduriri_ya_thuku_memorized", "pattern_notation_journal", "charcoal_and_bark"],
            "known_facts": [
                "aso_ijo_is_damaged",
                "pattern_matches_nduriri_ya_thuku",
                "current_pattern_is_intentional_variant",
                "seku_spoke_to_shadowless_figure"
            ],
            "hidden_from_player": [
                "suspects_seku_as_inside_agent",
                "knows_intentional_variant_ends_worse",
                "council_did_not_hear_full_warning"
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
                "estimated_days_remaining": "8_to_12"
            }
        },
        "thandiwe": {
            "health": 100, "trust": 85, "credibility": 82,
            "emotional_state": "focused",
            "location": "camp_day_three_checking_supplies",
            "inventory": ["knobkerrie_never_used", "medicine_satchel_23_preparations", "field_notes"],
            "known_facts": [
                "aso_ijo_is_damaged",
                "seku_spoke_to_shadowless_figure",
                "zulu_scouts_sent_before_party_not_reported"
            ],
            "hidden_from_player": [
                "zulu_scout_mission_details",
                "commanders_cryptic_instruction",
                "has_decided_to_volunteer_for_orun_entry",
                "tracking_stress_markers_all_party_members"
            ],
            "emotional_memory": {
                "akin": "clinical_concern_accumulating_stress_markers",
                "kofi": "respect_for_certainty_of_uncertainty",
                "zawadi": "trust_earned_through_precision",
                "seku": "observational_neutrality_watching_breathing",
                "adaeze": "healer_protectiveness"
            },
            "war_stance": "against_premature_war",
            "war_stance_confidence": 0.78,
            "medical_assessments": {
                "akin": {"stress_level": "high", "trigger_risk": "elevated_at_shrine"},
                "kofi": {"stress_level": "moderate", "note": "spiritual_uncertainty_manifesting"},
                "zawadi": {"stress_level": "controlled_high", "note": "managed_effectively"},
                "seku": {"stress_level": "high_concealed", "note": "breathing_changes_near_nri_topics"},
                "adaeze": {"stress_level": "moderate", "note": "holding_well"}
            }
        },
        "seku": {
            "health": 100, "trust": 60, "credibility": 72,
            "emotional_state": "carefully_composed",
            "location": "camp_day_three_100m_away",
            "inventory": ["kora_21_strings", "mandinka_diplomatic_credentials"],
            "known_facts": [
                "aso_ijo_is_damaged",
                "imole_tuntun_exists_and_goals",
                "eze_nwosu_communication_with_imole_tuntun",
                "courier_is_boundary_straddler"
            ],
            "hidden_from_player": [
                "eze_nwosu_imole_tuntun_alliance_negotiation",
                "kora_contains_insurance_recording",
                "boundary_straddlers_degrading_over_time",
                "personal_conclusion_imole_tuntun_must_be_stopped"
            ],
            "emotional_memory": {
                "adaeze": "disarming_genuineness_makes_him_careful",
                "akin": "mutual_guarded_respect",
                "kofi": "professional_courtesy_spiritual_concern",
                "zawadi": "competitive_awareness_she_is_watching_him",
                "thandiwe": "she_sees_more_than_she_says"
            },
            "war_stance": "concealed",
            "war_stance_confidence": 0.0,
            "actual_war_stance": "against_war_selfish_reasons",
            "loyalty_conflict": {
                "primary": "eze_nwosu_of_nri",
                "secondary": "mandinka_griot_truth_tradition",
                "current_resolution": "delaying_choice",
                "breaking_point_trigger": "direct_question_about_imole_tuntun_nri_connection"
            },
            "kora_encoded_sequences": [
                {"id": "K01", "content": "eze_nwosu_imole_tuntun_full_account", "decode_dc": 20},
                {"id": "K02", "content": "courier_network_route_map", "decode_dc": 16},
                {"id": "K03", "content": "seku_personal_fear_griot_tradition_ending", "decode_dc": 11}
            ]
        }
    },
    "world_flags": {
        "aso_ijo_torn": True,
        "eternal_flame_extinguished": True,
        "moremi_spirit_displaced": True,
        "imole_tuntun_operation_active": True,
        "seku_spoke_to_courier": True,
        "seku_confronted_early": False,
        "seku_observed": False,
        "seku_listened_to": False,
        "war_posture": "neutral",
        "elder_okafor_suspected": False,
        "cloth_fully_examined": False,
        "moremi_restoration_priority": False,
        "nri_implicated": False,
        "founder_identified": False,
        "party_knows_courier_route": False,
        "ogun_ibi_identified": False,
        "replacement_thread_found": False,
        "war_declared": False,
        "investigation_continues": False,
        "akin_signal_fire": False,
        "seku_partial_confession": False,
        "seku_full_confession": False,
    },
    "active_quests": {
        "main": {
            "id": "MQ01",
            "title": "The Wailing of the Cloth",
            "status": "active",
            "current_objective": "reach_ori_oke_shrine",
            "completed_objectives": ["depart_ile_olu", "survive_three_days_travel"],
            "discovered_leads": ["seku_shadowless_figure"],
        },
        "side_quests": []
    },
    "reasoning_trace_log": [],
    "gm_internal": {
        "sealed_knowledge_revealed": [],
        "imole_tuntun_timeline": {
            "operation_start": "approximately_60_days_ago",
            "cloth_damaged": "22_days_ago",
            "moremi_displaced": "20_days_ago",
            "conduit_thread_inserted": "19_days_ago",
        },
    }
}


class WorldState:
    def __init__(self):
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        if STATE_PATH.exists():
            self._state = self._load()
        else:
            self._state = copy.deepcopy(DEFAULT_STATE)
            self._save()

    def _load(self) -> dict:
        with open(STATE_PATH) as f:
            return json.load(f)

    def _save(self):
        with open(STATE_PATH, "w") as f:
            json.dump(self._state, f, indent=2)

    def get(self) -> dict:
        return copy.deepcopy(self._state)

    def get_agent(self, agent_key: str) -> dict:
        return copy.deepcopy(self._state["party"].get(agent_key, {}))

    def get_flags(self) -> dict:
        return copy.deepcopy(self._state["world_flags"])

    def set_flag(self, flag: str, value: Any):
        self._state["world_flags"][flag] = value
        self._save()

    def update_agent_trust(self, agent_key: str, delta: int):
        if agent_key in self._state["party"]:
            current = self._state["party"][agent_key]["trust"]
            self._state["party"][agent_key]["trust"] = max(0, min(100, current + delta))
            self._save()

    def update_agent_stat(self, agent_key: str, stat: str, value: Any):
        if agent_key in self._state["party"]:
            self._state["party"][agent_key][stat] = value
            self._save()

    def update_war_probability(self):
        state  = self._state
        flags  = state["world_flags"]
        party  = state["party"]
        base   = 0.30

        if flags.get("war_posture") == "aggressive":    base += 0.25
        if flags.get("nri_implicated"):                 base += 0.20
        if flags.get("elder_okafor_suspected"):         base -= 0.10
        if flags.get("seku_full_confession"):           base -= 0.30
        if flags.get("replacement_thread_found"):       base -= 0.25
        if flags.get("akin_signal_fire"):               base += 0.15
        if flags.get("war_declared"):                   base = 1.0

        akin_trust  = party.get("akin",  {}).get("trust", 75)
        kofi_trust  = party.get("kofi",  {}).get("trust", 82)

        if akin_trust > 80:  base += 0.05
        if kofi_trust > 80:  base -= 0.08

        self._state["game_meta"]["war_probability"] = round(max(0.0, min(1.0, base)), 2)
        self._save()
        return self._state["game_meta"]["war_probability"]

    def log_reasoning_trace(self, trace: dict):
        trace["timestamp"] = datetime.now().isoformat()
        self._state["reasoning_trace_log"].append(trace)
        self._state["game_meta"]["turn_number"] += 1
        self._save()

    def apply_delta(self, delta: dict):
        """Apply a GM state delta. Delta format:
        {
          "flags_set":    {"flag_name": value},
          "trust_changes": {"agent_key": delta_int},
          "stat_changes":  {"agent_key": {"stat": value}},
          "world_updates": {"meta_key": value}
        }
        """
        for flag, val in delta.get("flags_set", {}).items():
            self.set_flag(flag, val)

        for agent, delta_val in delta.get("trust_changes", {}).items():
            self.update_agent_trust(agent, delta_val)

        for agent, stats in delta.get("stat_changes", {}).items():
            for stat, val in stats.items():
                self.update_agent_stat(agent, stat, val)

        for key, val in delta.get("world_updates", {}).items():
            self._state["game_meta"][key] = val

        self.update_war_probability()
        self._save()

    def reset(self):
        self._state = copy.deepcopy(DEFAULT_STATE)
        self._save()
        print("[WorldState] Reset to default.")

    def summary(self) -> str:
        meta  = self._state["game_meta"]
        flags = self._state["world_flags"]
        party = self._state["party"]

        active_flags = [k for k, v in flags.items() if v is True]
        trust_summary = {k: v["trust"] for k, v in party.items() if isinstance(v, dict) and "trust" in v}

        return (
            f"Act {meta['current_act']} | Scene: {meta['current_scene']} | "
            f"Turn {meta['turn_number']} | War: {int(meta['war_probability']*100)}% | "
            f"Flags: {active_flags} | Trust: {trust_summary}"
        )
