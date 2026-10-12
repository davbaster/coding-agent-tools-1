
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