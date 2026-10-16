from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "agents-md-preview" / "macos"
spec = importlib.util.spec_from_file_location("bootstrap", SCRIPTS / "bootstrap-agents-md.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


def generate_preview(destination: Path) -> None:
    bootstrap.install_layered(
        ROOT / "global-guidance" / "agents-md-manifest.yaml",
        destination,
        destination / ".claude-unused",
        replace=True,
        opencode_home=None,
        agents_path_label="<preview>/AGENTS.md",
    )


def file_map(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".claude-unused" not in path.parts
    }


def test_agents_md_preview_matches_generated_output() -> None:
    with tempfile.TemporaryDirectory(dir=ROOT / "tests" / "fixtures") as tmp:
        generated = Path(tmp) / "macos"
        generate_preview(generated)
        assert file_map(generated) == file_map(FIXTURE)


def test_agents_md_preview_relative_links_resolve() -> None:
    markdown_files = [FIXTURE / "AGENTS.md", *sorted((FIXTURE / "agents-md-references").glob("*.md"))]
    pattern = re.compile(r"\[[^\]]+\]\((?:<)?([^)>]+)(?:>)?\)")
    missing: list[str] = []
    for markdown in markdown_files:
        for target in pattern.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (markdown.parent / path_part).resolve()
            if not resolved.exists():
                missing.append(f"{markdown.relative_to(FIXTURE)} -> {target}")
    assert missing == []


def test_agents_md_preview_exposes_grouped_navigation() -> None:
    rendered = (FIXTURE / "AGENTS.md").read_text(encoding="utf-8")
    assert "- [🛠️ Workspace and agent system](#workspace-and-agent-system)" in rendered
    assert "  - [🛠️ Updating this AGENTS.md](#agents-md-maintenance)" in rendered
    assert "- [🎛️ Runtime and interaction](#runtime-and-interaction)" in rendered
    assert "- [🧭 Reasoning and agent behavior](#reasoning-and-agent-behavior)" in rendered
    assert "- [🧠 Information presentation](#information-presentation)" in rendered
    assert "  - [🧱 Structural and semantic coherence](#structural-semantic-coherence)" in rendered
    assert "  - [⏱️ Effort and scope checkpoints](#effort-scope-checkpoints)" in rendered
    assert "**Before substantial human effort:**" in rendered
    assert "Agent-only research or runtime does not count." in rendered
    assert "**During focused technical problem-solving:**" in rendered
    assert "troubleshooting why unexpected behavior occurs or expected behavior fails" in rendered
    assert "failures between interacting systems" in rendered
    assert "repeatedly seeks explanations" in rendered
    assert "before further debugging or explanation" in rendered
    assert rendered.count("[effort checkpoint procedure](agents-md-references/effort-scope-checkpoints.md)") == 2
    assert "**Find the baseline.**" not in rendered
    assert "3–5 story points per engineer" not in rendered
    assert "Global guidance component:" not in rendered
    assert sum(line == "---" for line in rendered.splitlines()) == 4
    assert sum(line == "<br><br>" for line in rendered.splitlines()) == 4


def test_requirements_scope_validation_trigger_and_reference() -> None:
    entrypoint = (FIXTURE / "AGENTS.md").read_text(encoding="utf-8")
    procedure = (FIXTURE / "agents-md-references" / "requirements-scope-validation.md").read_text(encoding="utf-8")
    assert "- [🎯 Requirements and scope validation](#requirements-scope-validation)" in entrypoint
    assert "**Before implementing company or other shared work:**" in entrypoint
    assert "whether requested by the user or initiated by the agent" in entrypoint
    assert "This does not apply to the user\u0027s personal projects when the user alone controls the scope." in entrypoint
    assert "[requirements and scope validation procedure](agents-md-references/requirements-scope-validation.md)" in entrypoint
    assert "**Establish the baseline.**" in procedure
    assert "**Identify intended changes.**" in procedure
    assert "**Test proportionality and scope fit.**" in procedure
    assert "**Clarify and record scope decisions.**" in procedure
    assert "**Implement and verify agreed work.**" in procedure
    assert procedure.index("**Establish the baseline.**") < procedure.index("**Identify intended changes.**") < procedure.index("**Determine what belongs in the work.**") < procedure.index("**Test proportionality and scope fit.**") < procedure.index("**Clarify and record scope decisions.**") < procedure.index("**Implement and verify agreed work.**")
    for category in ("**Explicitly required**", "**Implicitly expected engineering work**", "**Technically necessary**", "**Inferred / disputed requirement**", "**Proposed scope expansion**", "**Unresolved facts or contracts**"):
        assert category in procedure
        assert category not in entrypoint
    assert "focused unit tests" in procedure
    assert "new end-to-end framework" in procedure
    assert "separately triggered [effort checkpoint procedure](effort-scope-checkpoints.md)" in procedure
    assert "Before implementing company or other shared work" not in procedure
    assert "personal tool" not in procedure
    assert "current ticket and its accepted acceptance criteria as the controlling scope" in procedure
    assert "accumulating or documenting a requirement does not approve it as part of this ticket" in procedure
    assert "| **Refine the current ticket** |" in procedure
    assert "| **Create a separate ticket** |" in procedure
    assert "| **Defer or decline** |" in procedure
    assert "revisit the estimate and priority" in procedure
    assert "Do not unilaterally rewrite acceptance criteria, create a new ticket, or implement an unapproved expansion" in procedure
    assert "accumulated requirements, including a working `requirements.md`" in procedure
    assert "Slack discussions, PR feedback" in procedure
    assert "do not prematurely label it either required or scope creep" in procedure
    assert "A plausible interpretation alone is not proof." in procedure
    assert "Obtain evidence instead of inventing a mapping, heuristic, or contract." in procedure
    assert "If a claimed implicit requirement is disputed" in procedure
    assert "Seek domain or technical expertise for missing facts" in procedure
    assert "contested scope with the appropriate decision-maker" in procedure
    assert "Implement expanded requirements only after the agreed ticket update or separate work item authorizes them" in procedure


def test_effort_checkpoint_reference_contains_procedure() -> None:
    entrypoint = (FIXTURE / "AGENTS.md").read_text(encoding="utf-8")
    procedure_path = FIXTURE / "agents-md-references" / "effort-scope-checkpoints.md"
    procedure = procedure_path.read_text(encoding="utf-8")

    assert "[effort checkpoint procedure](agents-md-references/effort-scope-checkpoints.md)" in entrypoint
    assert "[effort capacity model](effort-capacity-model.md)" in procedure
    assert "[requirements and scope validation procedure](requirements-scope-validation.md)" in procedure
    assert "approval of an added requirement alone does not replace" in procedure
    assert "**Team-ticket fallback:**" in procedure
    assert "Estimate remaining **human effort**" in procedure
    assert "Exclude unattended agent research, generation, and runtime" in procedure
    assert "**28.25 planned hours per engineer per week**" in procedure
    assert procedure.index("**Find the baseline.**") < procedure.index("**Team-ticket fallback:**") < procedure.index("**Estimate the remainder.**")
    assert "| Refinement |" not in procedure
    assert "| Sprint planning |" not in procedure
    for section in (
        "**Find the baseline.**",
        "**Estimate the remainder.**",
        "**Compare.**",
        "**Clarify with stakeholders.**",
        "**Evaluate stakeholder input.**",
        "| Source | What it can validate | What it does not validate by itself |",
        "| User as owner of a personal tool |",
    ):
        assert section in procedure
        assert section not in entrypoint


def test_effort_capacity_model_is_separate_and_linked() -> None:
    fixture_reference_dir = FIXTURE / "agents-md-references"
    procedure = (fixture_reference_dir / "effort-scope-checkpoints.md").read_text(encoding="utf-8")
    capacity_model = (fixture_reference_dir / "effort-capacity-model.md").read_text(encoding="utf-8")
    assert "[effort capacity model](effort-capacity-model.md)" in procedure
    for assumption in (
        "3–5 story points per engineer",
        "| Workweek | 40 hours |",
        "| Daily Scrum | 5 × 15 minutes = 1.25 hours |",
        "| Refinement | Approximately 1.5 hours |",
        "| Sprint planning | 1 hour |",
        "| Unplanned work (requests, assistance, incidents, bugs) | 20% = 8 hours |",
        "Approximately 28.25 hours per week",
    ):
        assert assumption in capacity_model
        assert assumption not in procedure


def test_agents_md_components_are_physically_grouped() -> None:
    component_root = ROOT / "global-guidance" / "agents-md-components"
    assert {path.name for path in component_root.iterdir()} == {
        "information-presentation",
        "reasoning-and-agent-behavior",
        "runtime-and-interaction",
        "workspace-and-agent-system",
    }
    assert all(path.is_dir() for path in component_root.iterdir())
