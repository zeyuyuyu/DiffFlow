# DiffFlow - Intelligent Diff Highlighting
from typing import List, Tuple, Optional
import re

class DiffHighlighter:
    def __init__(self):
        self.language_patterns = {
            'python': {
                'function': r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                'class': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                'import': r'^import\s+.*|^from\s+.*\s+import\s+.*'
            }
        }

    def highlight_diff(self, old_code: str, new_code: str, language: str = 'python') -> List[Tuple[str, str]]:
        """Analyzes and highlights meaningful differences between code versions.

        Args:
            old_code: Previous version of the code
            new_code: Current version of the code
            language: Programming language for syntax awareness

        Returns:
            List of tuples containing (change_type, highlighted_diff)
        """
        old_lines = old_code.split('\n')
        new_lines = new_code.split('\n')
        changes = []

        # Track structural elements
        old_elements = self._extract_elements(old_code, language)
        new_elements = self._extract_elements(new_code, language)

        for change in self._compute_diff(old_lines, new_lines):
            change_type = change[0]
            content = change[1]

            if change_type == 'added':
                highlighted = self._highlight_syntax(content, language)
                if self._is_significant_change(content, new_elements):
                    changes.append(('significant_add', highlighted))
                else:
                    changes.append(('minor_add', highlighted))

            elif change_type == 'removed':
                highlighted = self._highlight_syntax(content, language)
                if self._is_significant_change(content, old_elements):
                    changes.append(('significant_remove', highlighted))
                else:
                    changes.append(('minor_remove', highlighted))

        return changes

    def _extract_elements(self, code: str, language: str) -> dict:
        """Extracts important code elements based on language patterns."""
        elements = {'functions': [], 'classes': [], 'imports': []}
        patterns = self.language_patterns.get(language, {})

        for element_type, pattern in patterns.items():
            matches = re.finditer(pattern, code)
            elements[element_type] = [m.group(1) if m.groups() else m.group(0) for m in matches]

        return elements

    def _compute_diff(self, old_lines: List[str], new_lines: List[str]) -> List[Tuple[str, str]]:
        """Computes basic diff between line sequences."""
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, old_lines, new_lines)
        changes = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                changes.extend([('removed', line) for line in old_lines[i1:i2]])
                changes.extend([('added', line) for line in new_lines[j1:j2]])
            elif tag == 'delete':
                changes.extend([('removed', line) for line in old_lines[i1:i2]])
            elif tag == 'insert':
                changes.extend([('added', line) for line in new_lines[j1:j2]])

        return changes

    def _highlight_syntax(self, line: str, language: str) -> str:
        """Applies syntax highlighting to a line of code."""
        # Basic syntax highlighting - can be extended for more complex highlighting
        patterns = self.language_patterns.get(language, {})
        highlighted = line

        for element_type, pattern in patterns.items():
            highlighted = re.sub(pattern, f'**\\1**' if '\\1' in pattern else f'**{pattern}**', highlighted)

        return highlighted

    def _is_significant_change(self, content: str, elements: dict) -> bool:
        """Determines if a change is structurally significant."""
        # Check if change affects function/class definitions or imports
        return any(
            content.strip().startswith(elem) for elem_list in elements.values()
            for elem in elem_list
        )
