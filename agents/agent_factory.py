import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.ai.agents import AgentsClient
from azure.identity import InteractiveBrowserCredential

load_dotenv()

sys.path.append(str(Path(__file__).parent))
from system_prompts import AGENT_PROMPTS

ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL    = os.getenv("AZURE_MODEL_DEPLOYMENT", "gpt-4.1-mini")

AGENT_CONFIGS = [
    {"key": "game_master", "name": "Oya-GameMaster",     "tools": ["code_interpreter"]},
    {"key": "akin",        "name": "Akin-OyoWarrior",    "tools": []},
    {"key": "kofi",        "name": "Kofi-OkomfoPanyin",  "tools": []},
    {"key": "zawadi",      "name": "Zawadi-DangerKeeper","tools": []},
    {"key": "thandiwe",    "name": "Thandiwe-Inyanga",   "tools": ["code_interpreter"]},
    {"key": "seku",        "name": "Seku-Kouyate",       "tools": []},
]

def get_client():
    credential = InteractiveBrowserCredential(
        tenant_id="common"
    )
    return AgentsClient(
        endpoint=ENDPOINT,
        credential=credential,
    )

def create_all_agents():
    client    = get_client()
    agent_ids = {}
    print("\n[SIXTEEN THREADS] Creating agents...\n")
    for cfg in AGENT_CONFIGS:
        key    = cfg["key"]
        prompt = AGENT_PROMPTS[key]
        tools  = []
        if "code_interpreter" in cfg["tools"]:
            tools.append({"type": "code_interpreter"})
        try:
            agent = client.create_agent(
                model=MODEL,
                name=cfg["name"],
                instructions=prompt,
                tools=tools if tools else None,
            )
            agent_ids[key] = agent.id
            print(f"  OK   {cfg['name']:<35} {agent.id}")
        except Exception as e:
            print(f"  ERR  {cfg['name']:<35} {e}")
            agent_ids[key] = None
    ids_path = Path(__file__).parent / "agent_ids.json"
    with open(ids_path, "w") as f:
        json.dump(agent_ids, f, indent=2)
    print(f"\nSaved to {ids_path}\n")
    return agent_ids

def load_agent_ids():
    ids_path = Path(__file__).parent / "agent_ids.json"
    if ids_path.exists():
        with open(ids_path) as f:
            return json.load(f)
    return {}

def delete_all_agents():
    client    = get_client()
    agent_ids = load_agent_ids()
    for key, aid in agent_ids.items():
        if aid:
            try:
                client.delete_agent(aid)
                print(f"  DELETED  {key}: {aid}")
            except Exception as e:
                print(f"  ERR      {key}: {e}")
    ids_path = Path(__file__).parent / "agent_ids.json"
    if ids_path.exists():
        ids_path.unlink()

def verify_agents():
    client = get_client()
    result = client.list_agents()
    for a in result.data:
        print(f"  {a.name:<40} {a.id}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--delete", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if args.delete:
        delete_all_agents()
    elif args.verify:
        verify_agents()
    else:
        create_all_agents()
