from dataclasses import dataclass
from pathlib import Path
import frontmatter

@dataclass
class Skill:
    name: str
    description: str
    content: str


class SkillLoader:

    def __init__(self, skills_dir: Path | str = None):
        self.skills_dir = Path(skills_dir)

    def load_skill(self, name: str) -> Skill | None:
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return None

        parsed = frontmatter.load(skill_file)

        return Skill(
            name=parsed.metadata.get("name", name),
            description=parsed.metadata.get("description", ""),
            content=parsed.content,
        )

    def list_skills(self) -> list[Skill]:
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_dir in sorted(self.skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill = self.load_skill(skill_dir.name)
            if skill:
                skills.append(skill)

        return skills

    
    def get_description(self) -> str:
        skills = self.list_skills()

        skills_listing = "\n".join(
            f"  - {s.name}: {s.description}"
            for s in skills
        )

        return skills_listing


class SkillsTool:
    """Wrapper for the skill loader that exposes skill() as a tool."""

    def __init__(self, skill_loader: SkillLoader):
        self.skill_loader = skill_loader

    def skill(self, name: str) -> dict:
        """Load a skill to get specialized instructions."""
        result = self.skill_loader.load_skill(name)
        return {
            "name": result.name,
            "description": result.description,
            "content": result.content,
        }