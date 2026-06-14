"""
Sixteen Threads -- Main Game Loop
===================================
Cinematic terminal interface using Rich.
Run: python main.py
"""

import json
import time
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.prompt import Prompt
from rich import box
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(__file__).parent))

from agents.agent_factory import load_agent_ids, create_all_agents
from game_engine.world_state import WorldState
from game_engine.gm_orchestrator import GMOrchestrator
from game_engine.disagreement import DisagreementResult

console = Console()

# Color palette matching the web UI
GOLD    = "yellow"
AMBER   = "dark_orange"
SPIRIT  = "medium_purple"
ORUN    = "cornflower_blue"
EMBER   = "red1"
CLOTH   = "cornsilk1"
MUTED   = "grey62"
GREEN   = "green3"
WAR     = "red1"
PEACE   = "green3"

AGENT_COLORS = {
    "akin":     "dark_orange",
    "kofi":     "yellow",
    "zawadi":   "green3",
    "thandiwe": "indian_red",
    "seku":     "medium_purple",
    "game_master": "cornsilk1",
}

AGENT_ICONS = {
    "akin":     "⚔",
    "kofi":     "🔮",
    "zawadi":   "📜",
    "thandiwe": "🌿",
    "seku":     "🎵",
    "game_master": "⬡",
}


def print_intro():
    console.clear()
    time.sleep(0.3)

    title = Text()
    title.append("\n\n  S I X T E E N   T H R E A D S\n", style=f"bold {CLOTH}")
    title.append("  A Multi-Agent Reasoning RPG\n", style=f"italic {GOLD}")
    title.append("  Built on Microsoft Azure AI Foundry\n\n", style=MUTED)
    console.print(title, justify="center")

    console.print(Rule(style=GOLD))

    lore = Text()
    lore.append("\n  The covenant cloth that held two worlds apart for three centuries\n", style=CLOTH)
    lore.append("  has been torn. The eternal flame at the Shrine of Ori-Oke is out.\n", style=CLOTH)
    lore.append("  Mama Moremi has vanished. Seven kingdoms are sharpening their spears.\n\n", style=CLOTH)
    lore.append("  You are Adaeze. You carry no weapon. You carry words.\n\n", style=f"italic {GOLD}")
    console.print(lore, justify="center")

    console.print(Rule(style=GOLD))

    info = Table.grid(padding=(0, 4))
    info.add_column(style=MUTED, justify="right")
    info.add_column(style=CLOTH)
    info.add_row("TRACK", "Reasoning Agents -- Microsoft Agents League 2026")
    info.add_row("SETTING", "West African Mythology -- Yoruba, Akan, Kikuyu, Zulu, Mandinka")
    info.add_row("AGENTS", "6 Reasoning Agents (GM Oya + 5 party members)")
    info.add_row("IQ LAYER", "Foundry IQ -- 9 indexed lore documents")
    console.print(info, justify="center")
    console.print()


def print_world_state(world_state: WorldState):
    state = world_state.get()
    meta  = state["game_meta"]
    flags = state["world_flags"]
    party = state["party"]

    # War probability bar
    war_pct   = int(meta["war_probability"] * 100)
    bar_filled = int(war_pct / 5)
    bar = "[" + "█" * bar_filled + "░" * (20 - bar_filled) + "]"
    war_color  = WAR if war_pct > 60 else (AMBER if war_pct > 40 else GREEN)

    war_text = Text()
    war_text.append(f"  WAR PROBABILITY  ", style=MUTED)
    war_text.append(f"{bar}", style=war_color)
    war_text.append(f"  {war_pct}%", style=f"bold {war_color}")
    console.print(war_text)

    # Agent trust table
    trust_table = Table(box=box.SIMPLE, show_header=True, header_style=MUTED)
    trust_table.add_column("Agent", style=CLOTH, width=14)
    trust_table.add_column("Trust", justify="right", width=6)
    trust_table.add_column("State", width=22)
    trust_table.add_column("War Stance", width=24)

    for key in ["akin", "kofi", "zawadi", "thandiwe", "seku"]:
        agent = party.get(key, {})
        trust = agent.get("trust", 0)
        color = AGENT_COLORS.get(key, CLOTH)
        icon  = AGENT_ICONS.get(key, "")
        stance = agent.get("war_stance", "unknown").replace("_", " ")
        emotional = agent.get("emotional_state", "").replace("_", " ")

        trust_bar = "█" * int(trust / 10) + "░" * (10 - int(trust / 10))
        trust_text = Text()
        trust_text.append(f"{trust}", style=color)

        trust_table.add_row(
            f"{icon} {key.capitalize()}",
            str(trust),
            f"[{color}]{emotional}[/]",
            f"[{color}]{stance}[/]",
        )

    console.print(
        Panel(trust_table, title=f"[{GOLD}]PARTY STATUS[/]",
              border_style=GOLD, padding=(0, 1))
    )

    # Active flags
    active_flags = [k for k, v in flags.items() if v is True]
    if active_flags:
        flag_text = Text()
        for f in active_flags:
            flag_text.append(f"  {f.replace('_', '-')}  ", style=GREEN)
        console.print(Panel(flag_text, title=f"[{GOLD}]ACTIVE FLAGS[/]",
                            border_style=MUTED, padding=(0, 1)))


def print_reasoning_trace(disagreement: DisagreementResult):
    console.print()
    console.print(Rule(title=f"[{GOLD}] REASONING TRACE [/]", style=GOLD))

    # Positions table
    pos_table = Table(box=box.SIMPLE, show_header=True, header_style=MUTED, title="Agent Positions")
    pos_table.add_column("Agent", width=12)
    pos_table.add_column("Stance", width=28)
    pos_table.add_column("Conf", width=6, justify="right")
    pos_table.add_column("Cred", width=6, justify="right")

    for p in disagreement.positions:
        color  = AGENT_COLORS.get(p.agent, CLOTH)
        stance = p.stance.replace("_", " ").upper()

        if p.confidence == 0.0:
            conf_style = MUTED
        elif p.confidence >= 0.85:
            conf_style = GREEN
        elif p.confidence >= 0.70:
            conf_style = AMBER
        else:
            conf_style = EMBER

        pos_table.add_row(
            f"[{color}]{p.agent.upper()}[/]",
            f"[{color}]{stance}[/]",
            f"[{conf_style}]{p.confidence:.2f}[/]",
            f"[{MUTED}]{int(p.credibility)}[/]",
        )

    console.print(pos_table)

    # Foundry IQ evidence
    iq_lines = disagreement.iq_evidence.split("\n")
    iq_display = "\n".join(l for l in iq_lines[:6] if l.strip())
    console.print(
        Panel(
            Text(iq_display, style=MUTED),
            title=f"[{SPIRIT}] FOUNDRY IQ EVIDENCE [/]",
            border_style=SPIRIT,
            padding=(0, 1),
        )
    )

    # Resolution
    resolution_color = AGENT_COLORS.get(disagreement.resolution_agent, GOLD)
    resolution_text  = Text()
    resolution_text.append("RESOLUTION:   ", style=MUTED)
    resolution_text.append(
        f"{disagreement.resolution_agent.upper()} -- {disagreement.resolution.replace('_', ' ').upper()}",
        style=f"bold {resolution_color}"
    )
    resolution_text.append(f"   confidence: {disagreement.final_confidence:.2f}\n", style=MUTED)
    resolution_text.append("REASONING:    ", style=MUTED)
    resolution_text.append(disagreement.reasoning, style=CLOTH)

    if disagreement.flags_set:
        resolution_text.append("\nFLAGS SET:    ", style=MUTED)
        resolution_text.append(
            ", ".join(f"{k}: {v}" for k, v in disagreement.flags_set.items()),
            style=GREEN
        )

    if disagreement.trust_changes:
        resolution_text.append("\nTRUST DELTA:  ", style=MUTED)
        for agent, delta in disagreement.trust_changes.items():
            color = GREEN if delta > 0 else (EMBER if delta < 0 else MUTED)
            sign  = "+" if delta >= 0 else ""
            resolution_text.append(f"{agent}: {sign}{delta}  ", style=color)

    console.print(
        Panel(resolution_text, title=f"[{GOLD}] GM RESOLUTION [/]",
              border_style=GOLD, padding=(0, 1))
    )
    console.print(Rule(style=GOLD))


def print_agent_responses(agent_responses: dict):
    if not agent_responses:
        return
    console.print()
    console.print(Rule(title=f"[{MUTED}] AGENT RESPONSES [/]", style=MUTED))

    for agent_key, response in agent_responses.items():
        if not response or "[error]" in response.lower():
            continue
        color = AGENT_COLORS.get(agent_key, CLOTH)
        icon  = AGENT_ICONS.get(agent_key, "")
        console.print(
            Panel(
                Text(response[:400], style=CLOTH),
                title=f"[{color}]{icon} {agent_key.upper()}[/]",
                border_style=color,
                padding=(0, 1),
            )
        )


def print_narration(narration: str):
    console.print()
    console.print(Rule(title=f"[{CLOTH}] SCENE [/]", style=CLOTH))
    console.print(
        Panel(
            Text(narration, style=CLOTH),
            title=f"[{GOLD}] OYA -- GAME MASTER [/]",
            border_style=GOLD,
            padding=(1, 2),
        )
    )


def run_game_loop(orchestrator: GMOrchestrator, world_state: WorldState):
    console.print()
    console.print(Rule(title=f"[{GOLD}] BEGINNING JOURNEY [/]", style=GOLD))
    console.print()

    # Print initial world state
    print_world_state(world_state)

    # Opening narration
    opening = (
        "Night Three on the road to Ori-Oke. The fire burns low.\n\n"
        "The world has been quietly wrong since you left Ile-Olu: a baobab "
        "flowering upward, a village of children who all dreamed the same dream "
        "and will not say what it was, a river that disagreed with itself at the "
        "crossing.\n\n"
        "At the edge of the camp's light, approximately a hundred meters into "
        "the dark, Seku stands with someone. The someone casts no shadow.\n\n"
        "The party watches. Nobody speaks first.\n\n"
        "What does Adaeze do?"
    )
    print_narration(opening)

    while True:
        console.print()
        player_input = Prompt.ask(
            f"[{GOLD}]>[/] [{CLOTH}]Adaeze[/]",
            console=console,
        ).strip()

        if not player_input:
            continue

        if player_input.lower() in ("quit", "exit", "q"):
            console.print(f"\n[{GOLD}]The threads remember what you chose.[/]\n")
            break

        if player_input.lower() == "state":
            print_world_state(world_state)
            continue

        if player_input.lower() == "help":
            help_text = (
                "Commands:\n"
                "  [any text]  -- take an action as Adaeze\n"
                "  state       -- show current world state\n"
                "  quit        -- exit the game\n\n"
                "Try: 'I use Zawadi's listening technique on Seku'\n"
                "Or:  'I ask Kofi what the Akrafokonmu disc is showing'\n"
                "Or:  'I confront Seku directly about the figure'"
            )
            console.print(Panel(help_text, border_style=MUTED))
            continue

        # Process the turn
        with Progress(
            SpinnerColumn(spinner_name="dots", style=GOLD),
            TextColumn(f"[{MUTED}]Agents reasoning...[/]"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("thinking", total=None)
            turn_result = orchestrator.process_turn(player_input)

        # Display agent responses
        print_agent_responses(turn_result["agent_responses"])

        # Display reasoning trace if disagreement occurred
        if turn_result["disagreement"]:
            print_reasoning_trace(turn_result["disagreement"])

        # Display GM narration
        if turn_result["narration"]:
            print_narration(turn_result["narration"])

        # Show updated world state
        print_world_state(world_state)


def main():
    print_intro()

    console.print(f"\n[{GOLD}]Initializing Sixteen Threads...[/]\n")

    # Load or create agent IDs
    agent_ids = load_agent_ids()

    if not agent_ids or not any(agent_ids.values()):
        console.print(f"[{AMBER}]No agents found. Creating agents in Azure AI Foundry...[/]\n")
        agent_ids = create_all_agents()

    if not any(agent_ids.values()):
        console.print(f"[{EMBER}]Agent creation failed. Check your .env and Azure credentials.[/]")
        sys.exit(1)

    console.print(f"[{GREEN}]Agents loaded:[/]")
    for key, aid in agent_ids.items():
        status = f"[{GREEN}]OK[/]" if aid else f"[{EMBER}]MISSING[/]"
        console.print(f"  {status}  {key:<20} {aid or 'not created'}")

    console.print()

    # Initialize world state and orchestrator
    world_state  = WorldState()
    orchestrator = GMOrchestrator(world_state, agent_ids)

    console.print(f"[{GREEN}]World state initialized.[/]")
    console.print(f"[{GREEN}]Foundry IQ connected: sixteen-threads-lore[/]")
    console.print()

    # Start the game
    run_game_loop(orchestrator, world_state)


if __name__ == "__main__":
    main()
