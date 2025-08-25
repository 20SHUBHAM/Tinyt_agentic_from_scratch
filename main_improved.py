import json
import random
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

import streamlit as st


# -----------------------------
# Data models
# -----------------------------
@dataclass
class Persona:
    id: str
    name: str
    age: int
    occupation: str
    background: str
    motivations: List[str]
    constraints: List[str]
    personality: str


def seed_random(seed_text: str) -> None:
    seed_value = abs(hash(seed_text)) % (2 ** 32)
    random.seed(seed_value)


def generate_persona_name() -> str:
    first_names = [
        "Alex", "Jordan", "Taylor", "Casey", "Robin", "Sam", "Avery", "Morgan",
        "Riley", "Drew", "Jamie", "Quinn",
    ]
    last_names = [
        "Chen", "Garcia", "Patel", "O'Neal", "Khan", "Johnson", "Singh", "Kim",
        "Martinez", "Williams", "Nguyen", "Brown",
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def sample_from(description: str, options: List[str], weights: List[float] | None = None) -> str:
    if not weights:
        return random.choice(options)
    return random.choices(options, weights=weights, k=1)[0]


def synthesize_personas(description: str, num_personas: int) -> List[Persona]:
    seed_random(description)

    occupations = [
        "Undergraduate Student", "Graduate Student", "Software Engineer", "Barista",
        "Freelance Designer", "Marketing Intern", "Teaching Assistant", "Sales Associate",
        "Content Creator", "Research Assistant",
    ]
    personalities = [
        "Analytical and cautious", "Enthusiastic and outgoing", "Pragmatic and skeptical",
        "Empathetic listener", "Detail-oriented planner", "Creative risk-taker",
    ]

    motivation_pool = [
        "Improve health/fitness", "Save money", "Build social connections",
        "Optimize time", "Advance career skills", "Reduce stress",
        "Track progress with data", "Stay motivated with gamification",
    ]
    constraint_pool = [
        "Limited budget", "Time constraints", "Privacy concerns", "Beginner-level experience",
        "Accessibility needs", "Unreliable internet", "Device storage limits",
    ]

    personas: List[Persona] = []
    used_names: set[str] = set()

    for _ in range(num_personas):
        # Ensure distinct names within a run
        for _retry in range(20):
            name = generate_persona_name()
            if name not in used_names:
                used_names.add(name)
                break

        age = random.randint(18, 55)
        occupation = sample_from(description, occupations)
        personality = sample_from(description, personalities)
        motivations = random.sample(motivation_pool, k=random.randint(2, 3))
        constraints = random.sample(constraint_pool, k=random.randint(1, 2))
        background = (
            f"{name} is a {age}-year-old {occupation}. In the context of '{description}', "
            f"they bring {personality.lower()} energy."
        )

        personas.append(
            Persona(
                id=str(uuid.uuid4()),
                name=name,
                age=age,
                occupation=occupation,
                background=background,
                motivations=motivations,
                constraints=constraints,
                personality=personality,
            )
        )

    return personas


def init_state() -> None:
    if "personas" not in st.session_state:
        st.session_state.personas = []
    if "persona_description" not in st.session_state:
        st.session_state.persona_description = "College students interested in fitness apps"
    if "num_personas" not in st.session_state:
        st.session_state.num_personas = 5


def render_personas_section() -> None:
    st.subheader("Step 1: Dynamic Persona Creation")
    st.write("Create authentic, diverse personas from a natural language description.")

    st.text_area(
        "Describe your target participants",
        key="persona_description",
        placeholder="e.g., College students interested in fitness apps",
        height=100,
    )
    st.slider("How many participants?", min_value=3, max_value=12, key="num_personas")

    generate_clicked = st.button("Generate Participants")
    if generate_clicked:
        if not st.session_state.persona_description.strip():
            st.warning("Please provide a short description to guide persona generation.")
        else:
            st.session_state.personas = synthesize_personas(
                st.session_state.persona_description.strip(),
                int(st.session_state.num_personas),
            )

    if st.session_state.personas:
        st.success(f"Generated {len(st.session_state.personas)} participants")
        for p in st.session_state.personas:
            with st.expander(f"{p.name} — {p.occupation} ({p.age})"):
                st.markdown("**Personality:** " + p.personality)
                st.markdown("**Background:** " + p.background)
                st.markdown("**Motivations:** " + ", ".join(p.motivations))
                st.markdown("**Constraints:** " + ", ".join(p.constraints))

        # Export option for reuse in later steps
        st.download_button(
            label="Download personas (JSON)",
            data=json.dumps([asdict(p) for p in st.session_state.personas], indent=2),
            file_name="personas.json",
            mime="application/json",
        )


def main() -> None:
    st.set_page_config(page_title="Agentic FGD (TinyTroupe-inspired)", page_icon="🧪", layout="wide")
    init_state()

    st.title("Agentic Focus Group Simulator")
    st.caption("Step 1 of 5 · Persona generation. Subsequent steps will build on this.")

    with st.container():
        render_personas_section()

    st.divider()
    st.info(
        "Next steps (coming soon): Framework generation, Focus group simulation, Summary, and Q&A.",
        icon="🛠️",
    )


if __name__ == "__main__":
    main()

