from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bootstrap-agents-md.py"
spec = importlib.util.spec_from_file_location("bootstrap_layered", SCRIPT)
bootstrap = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bootstrap)


def make_layer(root: Path, layer_id: str | None, heading: str, body: str,
               reference_name: str | None = None) -> Path:
    components = root / "agents-md-components"
    components.mkdir(parents=True)
    component = components / "rules.md"
    component.write_text(f"# {heading}\n\n{body}\n", encoding="utf-8")
    manifest = root / "agents-md-manifest.yaml"
    layer_line = f"layer_id: {layer_id}\n" if layer_id else ""
    manifest.write_text(
        f"version: 2\n{layer_line}components:\n  - path: agents-md-components/rules.md\n",
        encoding="utf-8",
    )
    if reference_name:
        references = root / "agents-md-references"
        references.mkdir()
        (references / reference_name).write_text(f"# {heading} reference\n\n{body}\n", encoding="utf-8")
    return manifest


def render(manifest: Path, destination: Path, overlays: list[Path] | None = None,
           replace: bool = False, link_base: Path | None = None) -> None:
    bootstrap.install_layered(
        manifest,
        destination,
        destination / ".claude-unused",
        replace=replace,
        opencode_home=None,
        overlay_manifests=overlays or [],
        link_base=link_base,
        agents_path_label="<test>/AGENTS.md" if link_base else None,
    )


def test_shared_only_is_stable_and_excludes_overlay_content() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared = make_layer(root / "shared", None, "Shared rules", "SHARED_ONLY_SENTINEL", "shared.md")
        private = make_layer(root / "overlay", "private-device", "Private rules", "PRIVATE_ONLY_SENTINEL", "private.md")
        first = root / "first"
        second = root / "second"

        logical_target = root / "logical-codex-home"
        render(shared, first, link_base=logical_target)
        render(shared, second, link_base=logical_target)

        assert (first / "AGENTS.md").read_bytes() == (second / "AGENTS.md").read_bytes()
        rendered = (first / "AGENTS.md").read_text(encoding="utf-8")
        assert "SHARED_ONLY_SENTINEL" in rendered
        assert "PRIVATE_ONLY_SENTINEL" not in rendered
        assert (first / "agents-md-references" / "shared.md").is_file()
        assert not (first / "agents-md-references" / "private.md").exists()
        assert private.is_file()


def test_ordered_composition_merges_components_and_references_without_copying_sources() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared_root = root / "public-source"
        private_root = root / "separate-overlay"
        shared = make_layer(shared_root, None, "Shared rules", "SHARED_SENTINEL", "shared.md")
        private = make_layer(private_root, "private-device", "Private rules", "PRIVATE_SENTINEL", "private.md")
        public_before = {path.relative_to(shared_root): path.read_bytes() for path in shared_root.rglob("*") if path.is_file()}
        destination = root / "home" / ".codex"

        render(shared, destination, [private])

        rendered = (destination / "AGENTS.md").read_text(encoding="utf-8")
        assert rendered.index("SHARED_SENTINEL") < rendered.index("PRIVATE_SENTINEL")
        assert (destination / "agents-md-references" / "shared.md").is_file()
        assert (destination / "agents-md-references" / "private.md").is_file()
        public_after = {path.relative_to(shared_root): path.read_bytes() for path in shared_root.rglob("*") if path.is_file()}
        assert public_after == public_before
        assert not any(path.name == "PRIVATE_SENTINEL" for path in shared_root.rglob("*"))


def test_reference_and_heading_conflicts_fail_before_output() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared = make_layer(root / "shared", None, "Same heading", "shared", "collision.md")
        private = make_layer(root / "overlay", "private-device", "Same heading", "private", "collision.md")
        destination = root / "output"

        with pytest.raises(ValueError, match="Duplicate guidance heading anchor|Conflicting runtime guidance destination"):
            render(shared, destination, [private])
        assert not (destination / "AGENTS.md").exists()


def test_missing_overlay_and_layer_ownership_ambiguity_fail_closed() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared = make_layer(root / "shared", None, "Shared", "shared", "shared.md")
        private = make_layer(root / "overlay", "private-device", "Private", "private", "private.md")
        destination = root / "output"

        with pytest.raises(FileNotFoundError):
            render(shared, destination, [root / "missing.yaml"])

        render(shared, destination)
        with pytest.raises(ValueError, match="layer ownership differs|Reconcile existing preferences"):
            render(shared, destination, [private])
        render(shared, destination, [private], replace=True)
        with pytest.raises(ValueError, match="layer ownership differs|Reconcile existing preferences"):
            render(shared, destination)


def test_overlay_cannot_read_components_outside_its_manifest_directory() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared = make_layer(root / "shared", None, "Shared", "shared")
        overlay_root = root / "overlay"
        overlay_root.mkdir()
        outside = root / "outside.md"
        outside.write_text("# Outside\n\nnot owned by overlay\n", encoding="utf-8")
        overlay = overlay_root / "agents-md-manifest.yaml"
        overlay.write_text(
            "version: 2\nlayer_id: overlay\ncomponents:\n  - path: ../outside.md\n",
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="inside its manifest directory"):
            render(shared, root / "output", [overlay])
        assert not (root / "output" / "AGENTS.md").exists()


def test_non_directory_output_fails_before_writing() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shared = make_layer(root / "shared", None, "Shared", "shared")
        destination = root / "not-a-directory"
        destination.write_text("preserve me\n", encoding="utf-8")

        with pytest.raises(ValueError, match="harness home directory"):
            render(shared, destination)
        assert destination.read_text(encoding="utf-8") == "preserve me\n"
