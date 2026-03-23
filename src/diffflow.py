"""DiffFlow - Intelligent diff and patch handling."""
from typing import List, Tuple, Optional
import difflib

class DiffFlow:
    def __init__(self):
        self.conflict_strategies = {
            'smart_merge': self._smart_merge,
            'take_source': lambda s, t: s,
            'take_target': lambda s, t: t
        }

    def generate_diff(self, source: str, target: str) -> List[str]:
        """Generate a diff between source and target strings."""
        diff = difflib.unified_diff(
            source.splitlines(keepends=True),
            target.splitlines(keepends=True)
        )
        return list(diff)

    def apply_patch(self, source: str, diff: List[str], 
                    strategy: str = 'smart_merge') -> Tuple[str, bool]:
        """Apply a diff to source text with intelligent conflict resolution.
        Returns (patched_text, had_conflicts)"""
        if strategy not in self.conflict_strategies:
            raise ValueError(f'Unknown strategy: {strategy}')

        lines = source.splitlines()
        current_line = 0
        patched_lines = []
        had_conflicts = False

        for diff_line in diff:
            if diff_line.startswith('---') or diff_line.startswith('+++'): 
                continue
            
            if diff_line.startswith('-'):
                if current_line >= len(lines) or \
                   lines[current_line] != diff_line[1:].strip():
                    had_conflicts = True
                    resolved = self.conflict_strategies[strategy](
                        diff_line[1:].strip(),
                        lines[current_line] if current_line < len(lines) else ''
                    )
                    patched_lines.append(resolved)
                current_line += 1
            elif diff_line.startswith('+'):
                patched_lines.append(diff_line[1:].strip())
            else:
                if current_line < len(lines):
                    patched_lines.append(lines[current_line])
                current_line += 1

        # Append any remaining lines
        while current_line < len(lines):
            patched_lines.append(lines[current_line])
            current_line += 1

        return '\n'.join(patched_lines), had_conflicts

    def _smart_merge(self, source_line: str, target_line: str) -> str:
        """Intelligently merge conflicting lines using similarity matching."""
        if not source_line or not target_line:
            return source_line or target_line

        # Use sequence matcher to find similarities
        matcher = difflib.SequenceMatcher(None, source_line, target_line)
        ratio = matcher.ratio()

        if ratio > 0.8:  # Lines are very similar
            # Use the longer line as it likely contains more information
            return source_line if len(source_line) > len(target_line) else target_line
        elif ratio > 0.5:  # Moderate similarity
            # Try to combine unique parts
            matching_blocks = matcher.get_matching_blocks()
            result = []
            last_a = last_b = 0
            
            for a, b, size in matching_blocks:
                # Add unique parts from both strings
                if a > last_a:
                    result.append(source_line[last_a:a])
                if b > last_b:
                    result.append(target_line[last_b:b])
                # Add matching part
                if size > 0:
                    result.append(source_line[a:a+size])
                last_a = a + size
                last_b = b + size

            return ''.join(result).strip()
        else:
            # Too different - preserve source
            return source_line

    def validate_patch(self, patch: List[str]) -> bool:
        """Validate patch format and structure."""
        if not patch:
            return False

        has_header = False
        has_content = False

        for line in patch:
            if line.startswith('---') or line.startswith('+++'):
                has_header = True
            elif line.startswith('-') or line.startswith('+') or line.startswith(' '):
                has_content = True

        return has_header and has_content