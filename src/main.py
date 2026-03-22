import os
import git
import openai
from pathlib import Path
from typing import Dict, List

class DiffFlow:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(repo_path)
        self.openai_client = openai.Client()

    def analyze_changes(self) -> Dict[str, List[str]]:
        diff = self.repo.index.diff(None)
        impact_map = {}
        
        for change in diff:
            file_path = change.a_path
            changed_content = self._get_file_diff(change)
            impact = self._analyze_impact(file_path, changed_content)
            impact_map[file_path] = impact
            
        return impact_map
    
    def _get_file_diff(self, change) -> str:
        return change.diff.decode('utf-8')
    
    def _analyze_impact(self, file_path: str, content: str) -> List[str]:
        # AI-powered impact analysis
        response = self.openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Analyze code change impact"},
                {"role": "user", "content": f"Analyze impact:\n{content}"}
            ]
        )
        return self._parse_impact_response(response)

def main():
    flow = DiffFlow(os.getcwd())
    impact = flow.analyze_changes()
    print("Change Impact Analysis:")
    print(json.dumps(impact, indent=2))

if __name__ == "__main__":
    main()