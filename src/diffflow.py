"""DiffFlow core implementation for tracking and managing diffs with version control."""

from typing import Dict, List, Optional
import hashlib
import json
from datetime import datetime

class DiffFlow:
    def __init__(self):
        self.diffs: Dict[str, List[Dict]] = {}
        self.versions: Dict[str, str] = {}
        self._current_version = '0'

    def _generate_hash(self, content: str) -> str:
        """Generate a unique hash for content."""
        return hashlib.sha256(content.encode()).hexdigest()[:8]

    def add_diff(self, source: str, target: str, diff_content: str) -> str:
        """Add a new diff with versioning support."""
        diff_id = self._generate_hash(diff_content)
        timestamp = datetime.utcnow().isoformat()

        diff_entry = {
            'id': diff_id,
            'source': source,
            'target': target,
            'content': diff_content,
            'timestamp': timestamp,
            'version': str(int(self._current_version) + 1)
        }

        if source not in self.diffs:
            self.diffs[source] = []

        self.diffs[source].append(diff_entry)
        self._current_version = diff_entry['version']
        self.versions[self._current_version] = diff_id

        return diff_id

    def get_diff(self, diff_id: str) -> Optional[Dict]:
        """Retrieve a specific diff by ID."""
        for source_diffs in self.diffs.values():
            for diff in source_diffs:
                if diff['id'] == diff_id:
                    return diff
        return None

    def rollback_to_version(self, version: str) -> bool:
        """Rollback to a specific version."""
        if version not in self.versions:
            return False

        # Remove all diffs after the specified version
        for source in self.diffs:
            self.diffs[source] = [d for d in self.diffs[source] if int(d['version']) <= int(version)]

        # Update current version
        self._current_version = version
        return True

    def export_state(self) -> str:
        """Export current state as JSON."""
        state = {
            'diffs': self.diffs,
            'versions': self.versions,
            'current_version': self._current_version
        }
        return json.dumps(state, indent=2)

    def import_state(self, state_json: str) -> bool:
        """Import state from JSON."""
        try:
            state = json.loads(state_json)
            self.diffs = state['diffs']
            self.versions = state['versions']
            self._current_version = state['current_version']
            return True
        except (json.JSONDecodeError, KeyError):
            return False

    def get_version_history(self) -> List[Dict]:
        """Get complete version history."""
        history = []
        for version, diff_id in sorted(self.versions.items()):
            diff = self.get_diff(diff_id)
            if diff:
                history.append({
                    'version': version,
                    'diff_id': diff_id,
                    'timestamp': diff['timestamp']
                })
        return history
