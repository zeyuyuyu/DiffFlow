# DiffFlow

## AI-Powered Git Change Impact Analysis

DiffFlow is a next-generation tool that analyzes Git diffs to predict and visualize the full impact of code changes across your codebase. Using advanced AI models and static analysis, it helps developers understand the ripple effects of their changes before they commit.

### Key Features

- 🔄 Real-time change impact visualization
- 🤖 AI-powered dependency chain analysis
- 🎯 Predictive test coverage mapping
- 📊 Risk scoring for each modified component
- 🔗 Integration with GitHub Actions

### How It Works

1. DiffFlow monitors your local changes in real-time
2. Analyzes modified code using LLM-based understanding
3. Maps dependencies and potential impact paths
4. Generates interactive visualization of affected components
5. Suggests tests that should be run based on changes

### Installation

```bash
pip install diffflow
```

### Usage

```bash
diffflow analyze
```

### Configuration

Create a `diffflow.yaml` in your project root:

```yaml
model: gpt-5
ignore_patterns:
  - "*.md"
  - "tests/*"
risk_threshold: 0.7
```

### Requirements

- Python 3.11+
- Git 2.40+
- OpenAI API key for AI features

### License

MIT