"""
Sixteen Threads -- GM Orchestrator (Oya)
Uses AzureOpenAI client with full thread/message support.
"""
import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from game_engine.world_state import WorldState
from game_engine.disagreement import (
    resolve_disagreement,
    build_dn01_shadowless_figure,
    build_dn02_nri_nail,
    build_dn04_war_debate,
)

load_dotenv()

SCENE_AGENTS = {
    "day_three_night_camp": ["akin", "kofi", "zawadi", "thandiwe", "seku"],
    "shrine_outer_court":   ["akin", "kofi", "zawadi", "thandiwe"],
    "house_of_voices":      ["kofi", "zawadi", "thandiwe", "seku"],
    "inner_sanctum":        ["kofi", "zawadi", "thandiwe"],
    "fire_keep":            ["akin", "kofi", "zawadi", "thandiwe", "seku"],
    "war_debate":           ["akin", "kofi", "zawadi", "thandiwe", "seku"],
}

DISAGREEMENT_TRIGGERS = {
    "shadowless": "DN-01",
    "seku":       "DN-01",
    "figure":     "DN-01",
    "nail":       "DN-02",
    "fire keep":  "DN-02",
    "nri":        "DN-02",
    "war":        "DN-04",
    "debate":     "DN-04",
    "vote":       "DN-04",
}

_client = None


def get_client():
    global _client
    if _client is None:
        _client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_AI_API_KEY"),
            api_version="2024-05-01-preview",
        )
    return _client


class GMOrchestrator:
    def __init__(self, world_state: WorldState, agent_ids: dict):
        self.state = world_state
        self.agent_ids = agent_ids
        self.client = get_client()

    def detect_disagreement_trigger(self, player_input: str):
        lower = player_input.lower()
        for keyword, dn_id in DISAGREEMENT_TRIGGERS.items():
            if keyword in lower:
                return dn_id
        return None

    def build_agent_context(self, agent_key: str) -> str:
        d = self.state.get_agent(agent_key)
        flags = self.state.get_flags()
        meta = self.state.get()["game_meta"]
        af = [k for k, v in flags.items() if v is True]
        act = meta["current_act"]
        scene = meta["current_scene"]
        turn = meta["turn_number"]
        war_pct = int(meta["war_probability"] * 100)
        health = d.get("health", 100)
        trust = d.get("trust", 75)
        emotional = d.get("emotional_state", "neutral")
        stance = d.get("war_stance", "unknown")
        confidence = d.get("war_stance_confidence", 0.0)
        return (
            "WORLD STATE:\n"
            f"Act: {act} | Scene: {scene} | Turn: {turn}\n"
            f"War Probability: {war_pct}%\n\n"
            "YOUR STATE:\n"
            f"Health: {health} | Trust: {trust}\n"
            f"Emotional State: {emotional}\n"
            f"War Stance: {stance} (confidence: {confidence})\n\n"
            f"ACTIVE FLAGS: {af}\n\n"
            "Respond in character. Reference your cultural tradition.\n"
            "Format: [STANCE: your_stance] [CONFIDENCE: 0.XX] [ARGUMENT: 2-3 sentences]"
        )

    def run_agent(self, agent_key: str, prompt: str) -> str:
        agent_id = self.agent_ids.get(agent_key)
        if not agent_id:
            return f"[{agent_key.upper()} not available]"
        try:
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt,
            )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=agent_id,
                timeout=120,
                poll_interval_ms=3000,
            )
            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                for msg in messages.data:
                    if msg.role == "assistant":
                        for block in msg.content:
                            if hasattr(block, "text"):
                                return block.text.value
            return f"[{agent_key.upper()} run status: {run.status}]"
        except Exception as e:
            return f"[{agent_key.upper()} error: {e}]"

    def run_gm(self, scene_context: str, player_action: str) -> str:
        state_summary = self.state.summary()
        flags = self.state.get_flags()
        af = {k: v for k, v in flags.items() if v is True}
        gm_prompt = (
            "WORLD STATE: " + state_summary + "\n"
            "ACTIVE FLAGS: " + json.dumps(af) + "\n\n"
            "SCENE CONTEXT:\n" + scene_context + "\n\n"
            "PLAYER ACTION: " + player_action + "\n\n"
            "You are Oya, Game Master of Sixteen Threads.\n"
            "Narrate the scene in vivid present tense.\n"
            "Reference specific West African cultural details from the lore.\n"
            "Show the consequences of the player choice.\n"
            "End with what the party observes next and what Adaeze must decide.\n"
            "Keep narration under 200 words."
        )
        return self.run_agent("game_master", gm_prompt)

    def process_turn(self, player_input: str) -> dict:
        result = {
            "player_input": player_input,
            "agent_responses": {},
            "disagreement": None,
            "narration": "",
        }

        dn_trigger = self.detect_disagreement_trigger(player_input)
        current_scene = self.state.get()["game_meta"]["current_scene"]
        relevant_agents = SCENE_AGENTS.get(
            current_scene, list(self.agent_ids.keys())
        )

        agent_prompt = (
            "Player action: " + player_input + "\n"
            "World state: " + self.state.summary() + "\n"
            "Respond in character with your stance, argument, and confidence."
        )

        for agent_key in relevant_agents:
            if agent_key == "game_master":
                continue
            context = self.build_agent_context(agent_key)
            response = self.run_agent(agent_key, context + "\n\n" + agent_prompt)
            result["agent_responses"][agent_key] = response

        if dn_trigger:
            dn_builders = {
                "DN-01": build_dn01_shadowless_figure,
                "DN-02": build_dn02_nri_nail,
                "DN-04": build_dn04_war_debate,
            }
            if dn_trigger in dn_builders:
                dn_id, conflict, positions, iq_query = dn_builders[dn_trigger]()
                flags = self.state.get_flags()
                disagreement = resolve_disagreement(
                    dn_id, conflict, positions, iq_query, flags
                )
                result["disagreement"] = disagreement
                self.state.log_reasoning_trace(disagreement.to_dict())
                self.state.apply_delta({
                    "flags_set": disagreement.flags_set,
                    "trust_changes": disagreement.trust_changes,
                })

        art = "\n\n".join(
            f"[{k.upper()}]: {v}"
            for k, v in result["agent_responses"].items()
        )
        dt = ""
        if result["disagreement"]:
            d = result["disagreement"]
            dt = (
                "\nCONFLICT RESOLVED: " + d.resolution_agent.upper() +
                " wins stance " + d.resolution +
                "\nConfidence: " + str(d.final_confidence) + "\n"
            )

        scene_context = "Agent responses:\n" + art + "\n" + dt
        result["narration"] = self.run_gm(scene_context, player_input)
        self.state.update_war_probability()
        return result
