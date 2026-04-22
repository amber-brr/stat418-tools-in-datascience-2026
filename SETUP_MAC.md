# Student Setup Guide - macOS

This guide will help you set up your development environment for STAT 418 on macOS.

## What You'll Install

1. **Git** - Version control system
2. **Python 3.11+** - Programming language
3. **uv** - Fast Python package manager
4. **VSCode** - Code editor
5. **AI Coding Assistant** - Either Cline or Claude Code (official) with OpenRouter

**Time Required**: 30-45 minutes

---

## Prerequisites

- macOS 10.15 (Catalina) or later
- Admin/sudo access on your machine
- Stable internet connection
- At least 5GB of free disk space

---

## 1. Git Installation

Install Xcode Command Line Tools (includes Git):

```bash
xcode-select --install
```

A dialog will appear - click "Install" and follow the prompts.

### Verify Installation

Open Terminal and run:

```bash
git --version
# Should show: git version 2.x.x or higher
```

### Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@ucla.edu"
```

---

## 2. Python 3.11+ Installation

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.11** or later for macOS
3. Open the downloaded `.pkg` file
4. Follow the installation wizard (use default settings)

### Verify Installation

```bash
python3 --version
# Should show: Python 3.11.x or higher
```

---

## 3. uv Installation

uv is a fast Python package manager that replaces pip.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, **close and reopen your terminal**.

### Verify Installation

```bash
uv --version
# Should show: uv x.x.x
```

### Quick uv Tutorial

```bash
# Create a new project directory
mkdir my-project
cd my-project

# Initialize a uv project (creates pyproject.toml)
uv init

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Your prompt should now show (.venv) at the beginning

# Install packages
uv pip install pandas numpy

# Or add dependencies to your project
uv add pandas numpy

# Deactivate when done
deactivate
```

---

## 4. VSCode Installation

1. Visit [code.visualstudio.com](https://code.visualstudio.com/)
2. Click "Download for Mac"
3. Open the downloaded `.zip` file
4. Drag "Visual Studio Code" to your Applications folder
5. Open VSCode from Applications

### Install Shell Command

1. Open VSCode
2. Press `Cmd+Shift+P`
3. Type "Shell Command: Install 'code' command in PATH"
4. Press Enter

### Install Required Extensions

Open VSCode and install these extensions:

**1. Python Extension**
- Press `Cmd+Shift+X`
- Search for "Python"
- Click Install on "Python" by Microsoft

**2. AI Coding Assistant (Choose ONE)**

**Option A: Cline** (Recommended for now - tested and working)
- Search for "Cline"
- Click Install on "Cline" (formerly Claude Dev)
- Works with OpenRouter for free/paid models

**Option B: Claude Code** (Official Anthropic extension - newer)
- Search for "Claude Code"
- Click Install on "Claude Code" by Anthropic
- Official extension, may have better integration
- **Note**: Configuration with OpenRouter is still being tested

**3. GitLens Extension**
- Search for "GitLens"
- Click Install on "GitLens" by GitKraken

### Configure Python in VSCode

1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python 3.11+ installation from the list

---

## 5. AI Coding Assistant Setup with OpenRouter

We'll set up an AI coding assistant in VSCode using OpenRouter's API to access Claude and other models. You have two options:

### Step 1: Get a Free OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai/)
2. Click "Sign In" in the top right
3. Sign in with your Google account (use your UCLA account or personal)
4. Once signed in, click on your profile icon → "Keys"
5. Click "Create Key"
6. Give it a name like "STAT418-Course"
7. Copy the API key and save it somewhere safe (you won't be able to see it again)

**Important**: OpenRouter provides free credits for new users and has free models available. The free tier is sufficient for this course.

### Step 2: Configure Your AI Assistant

Choose **ONE** of the following options:

---

#### **Option A: Cline (Recommended - Tested and Working)**

1. In VSCode, click the Cline icon in the left sidebar (robot/chat icon)
2. Click the settings gear icon (⚙️) in the Cline panel
3. In the settings that appear:
   - **API Provider**: Select "OpenRouter"
   - **API Key**: Paste your OpenRouter API key
   - **Model**: Select one of the recommended free models below, or "anthropic/claude-3.5-sonnet" (paid, but highest quality)

**Test Cline:**
1. Create a new file: `test.py`
2. Click the Cline icon in the left sidebar
3. Type: "Write a function that adds two numbers and returns the result"
4. Press Enter

If you get a response with Python code, you're all set! ✓

---

#### **Option B: Claude Code (Official - Newer, Being Tested)**

**Note**: This is the official Anthropic extension. Configuration with OpenRouter is still being verified for the course.

1. In VSCode, click the Claude Code icon in the left sidebar
2. Open the extension settings (gear icon or Command Palette → "Claude Code: Settings")
3. Configure the following:
   - **API Provider/Base URL**: Look for custom API endpoint settings
   - If available, set to: `https://openrouter.ai/api/v1`
   - **API Key**: Paste your OpenRouter API key
   - **Model**: Specify the model (e.g., `anthropic/claude-3.5-sonnet`)

**Alternative Configuration** (if custom endpoints aren't supported):
- You may need to use Anthropic's API directly
- Visit [console.anthropic.com](https://console.anthropic.com/) to get an Anthropic API key
- Note: Anthropic API has different pricing than OpenRouter

**Test Claude Code:**
1. Create a new file: `test.py`
2. Open Claude Code panel
3. Ask: "Write a function that adds two numbers and returns the result"
4. If you get a response with Python code, you're all set! ✓

**Important**: If Claude Code doesn't work with OpenRouter by the second lecture, we'll provide updated instructions or recommend using Cline instead.

---

### Top 3 Free Models for Coding

These models are completely free on OpenRouter and work well for coding tasks:

1. **`meta-llama/llama-3.3-70b-instruct:free`** - Best overall choice (recommended)
   - Large, capable model with strong reasoning
   - Good rate limits for interactive use
   
2. **`nvidia/nemotron-3-super-120b-a12b:free`** - Excellent for coding
   - Large model with excellent reasoning and code generation
   - Reliable rate limits
   
3. **`nousresearch/hermes-3-llama-3.1-405b:free`** - Most capable
   - Huge 405B model, excellent for complex tasks
   - May be slower due to size

**Recommendation:** Start with `meta-llama/llama-3.3-70b-instruct:free` or `nvidia/nemotron-3-super-120b-a12b:free` for the best balance of capability and usability.

You can switch models anytime in the Cline settings.

---

## 6. Fork and Clone the Course Repository

**From this point forward, use VSCode's integrated terminal** (View → Terminal or `` Cmd+` ``)

### Step 1: Fork the Repository

1. Visit the course repository: [github.com/natelangholz/stat418-tools-in-datascience-2026](https://github.com/natelangholz/stat418-tools-in-datascience-2026)
2. Click the "Fork" button in the top right
3. This creates a copy of the repository under your GitHub account
4. You'll submit all assignments and your final project to different branches of your forked repo

### Step 2: Clone Your Fork

Open VSCode's integrated terminal (View → Terminal or `` Cmd+` ``) and run:

```bash
# Navigate to where you want to store course materials
cd ~/Documents  # or wherever you prefer

# Clone YOUR fork (replace YOUR-USERNAME with your GitHub username)
git clone https://github.com/YOUR-USERNAME/stat418-tools-in-datascience-2026.git

# Navigate into the repository
cd stat418-tools-in-datascience-2026

# Add the original repo as 'upstream' to get updates
git remote add upstream https://github.com/natelangholz/stat418-tools-in-datascience-2026.git
```

### Step 3: Set Up the Project Environment

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate

# Install course dependencies
uv pip install -e .

# Install optional dependencies for LLM work
uv pip install -e ".[llm]"

# Install web development dependencies
uv pip install -e ".[web]"
```

---

## 7. Verification Test

Let's verify everything works together.

### Test the Course Environment

```bash
# Make sure you're in the course directory
cd stat418-tools-in-datascience-2026

# Activate virtual environment if not already active
source .venv/bin/activate

# Create a test file
cat > test_setup.py << 'EOF'
import sys
import pandas as pd
import numpy as np
import requests

print("✓ Python version:", sys.version)
print("✓ Pandas version:", pd.__version__)
print("✓ NumPy version:", np.__version__)
print("✓ Requests version:", requests.__version__)
print("\n✓✓✓ Setup successful! ✓✓✓")
EOF

# Run the test
python test_setup.py
```

**Expected output**: Version information and "Setup successful!"

### Test in VSCode with Claude Code

```bash
# Open the course directory in VSCode
code .
```

In VSCode:
1. Open `test_setup.py`
2. Click the Cline icon
3. Ask: "Add docstrings to this code and explain what it does"
4. If Cline responds with documentation, everything is working! ✓

---

## 8. Setting Up Your .env File

For projects that use API keys, you'll need a `.env` file:

```bash
# In your project directory, copy the example
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**IMPORTANT**: Never commit `.env` to git! It's already in `.gitignore`.