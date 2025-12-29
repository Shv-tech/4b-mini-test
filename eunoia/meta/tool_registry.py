from typing import Dict
from eunoia.meta.tool_synthesizer import SynthesizedTool


class ToolRegistry:
    """
    Persistent registry of synthesized tools.
    """

    def __init__(self):
        self.tools: Dict[str, SynthesizedTool] = {}

    def add(self, tool: SynthesizedTool):
        self.tools[tool.name] = tool

    def has(self, name: str) -> bool:
        return name in self.tools

    def get(self, name: str) -> SynthesizedTool | None:
        return self.tools.get(name)