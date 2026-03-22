#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Tuple
import difflib
import sys

@dataclass
class DiffBlock:
    old_start: int
    old_lines: List[str]
    new_start: int 
    new_lines: List[str]
    change_type: str  # 'modify', 'add', 'delete'

class DiffFlow:
    def __init__(self, old_text: str, new_text: str):
        self.old_lines = old_text.splitlines()
        self.new_lines = new_text.splitlines()
        self.differ = difflib.SequenceMatcher(None, self.old_lines, self.new_lines)
        self.diff_blocks = []

    def compute_diff(self) -> List[DiffBlock]:
        for tag, i1, i2, j1, j2 in self.differ.get_opcodes():
            if tag == 'equal':
                continue
            
            block = DiffBlock(
                old_start=i1,
                old_lines=self.old_lines[i1:i2],
                new_start=j1,
                new_lines=self.new_lines[j1:j2],
                change_type=tag
            )
            self.diff_blocks.append(block)
        return self.diff_blocks

    def visualize_side_by_side(self, width: int = 80) -> str:
        """Generate side-by-side diff visualization"""
        output = []
        half_width = (width - 3) // 2

        for block in self.diff_blocks:
            # Format line numbers
            old_num = f"{block.old_start + 1:<4}"
            new_num = f"{block.new_start + 1:<4}"

            # Handle different change types
            if block.change_type == 'replace':
                for old, new in zip(block.old_lines, block.new_lines):
                    old_part = f"{old_num} {old:{half_width}}"
                    new_part = f"{new_num} {new:{half_width}}"
                    output.append(f"{old_part} | {new_part}")

            elif block.change_type == 'delete':
                for old in block.old_lines:
                    output.append(f"{old_num} {old:{half_width}} | {' ' * (half_width + 4)}")

            elif block.change_type == 'insert':
                for new in block.new_lines:
                    output.append(f"{' ' * (half_width + 4)} | {new_num} {new:{half_width}}")

        return '\n'.join(output)

def main():
    # Example usage
    old_text = """def hello():
    print('Hello')
    return True"""

    new_text = """def hello_world():
    print('Hello World!')
    return True
    # Added comment"""

    differ = DiffFlow(old_text, new_text)
    blocks = differ.compute_diff()
    print(differ.visualize_side_by_side())

if __name__ == '__main__':
    main()
