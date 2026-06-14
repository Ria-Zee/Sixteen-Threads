import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LORE_DIR = Path(__file__).parent.parent / "lore"

LORE_KEYWORDS = {
    "aso-ijo":    "01_world_overview.md",
    "covenant":   "01_world_overview.md",
    "orun":       "01_world_overview.md",
    "aye":        "01_world_overview.md",
    "seku":       "02_characters.md",
    "akin":       "02_characters.md",
    "kofi":       "02_characters.md",
    "zawadi":     "02_characters.md",
    "thandiwe":   "02_characters.md",
    "moremi":     "02_characters.md",
    "imole":      "03_factions.md",
    "tuntun":     "03_factions.md",
    "nri":        "03_factions.md",
    "kingdom":    "03_factions.md",
    "shrine":     "04_locations.md",
    "ori-oke":    "04_locations.md",
    "camp":       "04_locations.md",
    "quest":      "05_quests.md",
    "nail":       "06_artifacts.md",
    "kora":       "06_artifacts.md",
    "cloth":      "06_artifacts.md",
    "straddler":  "07_bestiary.md",
    "ogun":       "07_bestiary.md",
    "trust":      "08_homebrew_rules.md",
    "roll":       "08_homebrew_rules.md",
    "confidence": "08_homebrew_rules.md",
    "state":      "09_session_state_template.md",
}


def query_lore(query: str, top: int = 3) -> list[dict]:
    query_lower = query.lower()
    matched_files = set()

    for keyword, filename in LORE_KEYWORDS.items():
        if keyword in query_lower:
            matched_files.add(filename)

    if not matched_files:
        matched_files = {"01_world_overview.md", "02_characters.md"}

    results = []
    for filename in list(matched_files)[:top]:
        filepath = LORE_DIR / filename
        if filepath.exists():
            content = filepath.read_text()
            query_words = query_lower.split()
            relevant_lines = [
                line for line in content.split("\n")
                if any(w in line.lower() for w in query_words)
            ]
            excerpt = "\n".join(relevant_lines[:20]) if relevant_lines else content[:500]
            results.append({
                "content": excerpt,
                "source":  filename,
                "score":   0.85,
            })

    return results


def format_for_gm(query: str, top: int = 3) -> str:
    results = query_lore(query, top=top)

    if not results:
        return f"[FOUNDRY IQ QUERY]: {query}\n[No results found]"

    lines = [f"[FOUNDRY IQ QUERY]: {query}"]
    for i, r in enumerate(results, 1):
        lines.append(f"\n[RESULT {i}] Source: {r['source']} | Score: {r['score']:.2f}")
        lines.append(r["content"][:600])

    return "\n".join(lines)


def query_character(name: str) -> str:
    return format_for_gm(f"{name} background personality hidden knowledge")

def query_location(name: str) -> str:
    return format_for_gm(f"{name} description layout secrets")

def query_faction(name: str) -> str:
    return format_for_gm(f"{name} goals agenda hidden plans")

def query_artifact(name: str) -> str:
    return format_for_gm(f"{name} properties significance sealed knowledge")

def query_rules(mechanic: str) -> str:
    return format_for_gm(f"{mechanic} rules mechanics how it works")


if __name__ == "__main__":
    print("Testing Foundry IQ file-based retrieval...\n")
    result = format_for_gm("What is the Aso-Ijo covenant cloth")
    print(result)
    print("\n---\n")
    result = format_for_gm("Seku Kouyate hidden agenda Nri connection")
    print(result)
