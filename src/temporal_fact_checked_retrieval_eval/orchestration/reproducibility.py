"""Environment reproducibility snapshots for MLflow runs."""

import importlib.metadata
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ReproducibilityReport:
    """Minimal environment snapshot stored alongside each MLflow run."""

    processor: str
    """Processor architecture string."""
    system: str
    """Operating system name."""
    release: str
    """Operating system release string."""
    machine: str
    """Machine architecture string."""
    python_version: str
    """Python interpreter version."""
    python_implementation: str
    """Python implementation name."""
    platform: str
    """Full platform string."""
    total_ram_bytes: int
    """Total physical RAM in bytes when detectable."""
    total_disk_bytes: int
    """Total filesystem capacity in bytes for the repository volume."""
    installed_packages: dict[str, str]
    """Installed package version mapping."""
    git_commit_hash: str
    """Current git commit hash."""
    git_branch: str
    """Current git branch or ref name."""
    git_dirty: bool
    """Whether the working tree has uncommitted changes."""
    git_status_porcelain: str
    """Raw porcelain status for the working tree."""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    """ISO-8601 timestamp when report was created."""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the report."""
        return {
            "processor": self.processor,
            "system": self.system,
            "release": self.release,
            "machine": self.machine,
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
            "platform": self.platform,
            "total_ram_bytes": self.total_ram_bytes,
            "total_disk_bytes": self.total_disk_bytes,
            "installed_packages": self.installed_packages,
            "git_commit_hash": self.git_commit_hash,
            "git_branch": self.git_branch,
            "git_dirty": self.git_dirty,
            "git_status_porcelain": self.git_status_porcelain,
            "created_at": self.created_at,
        }


def collect_reproducibility_report() -> ReproducibilityReport:
    """Capture processor, memory, packages, and git state for the current run."""
    repo_root = Path(__file__).resolve().parents[3]
    git_commit_hash = _read_git_commit_hash(repo_root)
    git_branch = _read_git_branch(repo_root)
    git_status_porcelain = _read_git_status_porcelain(repo_root)
    total_ram_bytes = _read_total_ram_bytes()
    total_disk_bytes = _read_total_disk_bytes(repo_root)

    return ReproducibilityReport(
        processor=platform.processor() or "unknown",
        system=platform.system(),
        release=platform.release(),
        machine=platform.machine(),
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        platform=platform.platform(),
        total_ram_bytes=total_ram_bytes,
        total_disk_bytes=total_disk_bytes,
        installed_packages=_cached_installed_packages(),
        git_commit_hash=git_commit_hash,
        git_branch=git_branch,
        git_dirty=bool(git_status_porcelain.strip()),
        git_status_porcelain=git_status_porcelain,
    )


def _read_git_commit_hash(repo_root: Path) -> str:
    """Read the current commit hash from the local git metadata."""
    git_dir = repo_root / ".git"
    head_path = git_dir / "HEAD"
    if git_dir.is_file():
        git_dir_text = git_dir.read_text(encoding="utf-8").strip()
        if git_dir_text.startswith("gitdir:"):
            git_dir = (
                repo_root / git_dir_text.split("gitdir:", maxsplit=1)[1].strip()
            ).resolve()
            head_path = git_dir / "HEAD"

    try:
        head_contents = head_path.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"

    if head_contents.startswith("ref: "):
        ref_name = head_contents.removeprefix("ref: ").strip()
        ref_path = git_dir / ref_name
        try:
            return ref_path.read_text(encoding="utf-8").strip() or "unknown"
        except OSError:
            return "unknown"

    return head_contents or "unknown"


def _read_git_branch(repo_root: Path) -> str:
    """Read the current git branch or detached HEAD description."""
    git_dir = repo_root / ".git"
    head_path = git_dir / "HEAD"
    if git_dir.is_file():
        git_dir_text = git_dir.read_text(encoding="utf-8").strip()
        if git_dir_text.startswith("gitdir:"):
            git_dir = (
                repo_root / git_dir_text.split("gitdir:", maxsplit=1)[1].strip()
            ).resolve()
            head_path = git_dir / "HEAD"

    try:
        head_contents = head_path.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"

    if head_contents.startswith("ref: "):
        return head_contents.removeprefix("ref: ").strip() or "unknown"
    return "detached-head"


def _read_git_status_porcelain(repo_root: Path) -> str:
    """Read the working tree status in porcelain format."""
    try:
        git_executable = shutil.which("git")
        if git_executable is None:
            return ""
        completed = subprocess.run(
            [git_executable, "status", "--porcelain=v1", "-uall"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    return completed.stdout.strip()


def _read_total_ram_bytes() -> int:
    """Read total physical RAM in bytes with platform-aware fallbacks."""
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        if (
            isinstance(pages, int)
            and isinstance(page_size, int)
            and pages > 0
            and page_size > 0
        ):
            return int(pages * page_size)
    except (AttributeError, OSError, ValueError):
        pass

    if platform.system() == "Darwin":
        try:
            sysctl_executable = shutil.which("sysctl")
            if sysctl_executable is None:
                return 0
            completed = subprocess.run(
                [sysctl_executable, "-n", "hw.memsize"],
                check=True,
                capture_output=True,
                text=True,
            )
            value = int(completed.stdout.strip())
            if value > 0:
                return value
        except (OSError, ValueError, subprocess.CalledProcessError):
            pass

    return 0


def _read_total_disk_bytes(repo_root: Path) -> int:
    """Read total filesystem capacity for the repository volume in bytes."""
    try:
        return int(shutil.disk_usage(repo_root).total)
    except OSError:
        return 0


def _collect_installed_packages() -> dict[str, str]:
    """Collect installed package versions for the active Python environment."""
    packages: dict[str, str] = {}
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        version = distribution.version
        if not name or not version:
            continue
        packages[name] = version
    return dict(sorted(packages.items(), key=lambda item: item[0].lower()))


@lru_cache(maxsize=1)
def _cached_installed_packages() -> dict[str, str]:
    """Return a cached package-version snapshot for the active environment."""
    return _collect_installed_packages()
