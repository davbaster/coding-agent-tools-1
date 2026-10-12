from skillLoader import SkillLoader


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