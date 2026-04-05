# A11y Expert MCP

An accessibility expert for your AI coding assistant. This [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server gives AI tools like Claude, Cursor, and Windsurf real-time access to WAI-ARIA patterns, code review, contrast checking, and WCAG guidance — so the code they write is accessible from the start.

## What's Inside

### 🔧 Tools

| Tool | What it does |
|------|-------------|
| **`get_pattern`** | Get the full WAI-ARIA implementation pattern for any UI component — roles, states, keyboard interaction, and code examples. |
| **`review_code`** | Paste HTML/JSX/TSX/Vue/Svelte code and get a list of accessibility issues with specific fixes and WCAG references. Detects 10+ anti-patterns including missing labels, click-on-divs, broken heading hierarchy, missing dialog roles, and more. |
| **`list_patterns`** | See all 33 component patterns available in the knowledge base. |
| **`check_contrast`** | Check any two hex colors against WCAG AA and AAA contrast requirements for both normal and large text. |

### 📚 Knowledge Base (33 Components)

Every pattern comes from the [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) and includes roles, states, properties, keyboard interaction, and code examples.

| | | | |
|---|---|---|---|
| Accordion | Alert | Alert Dialog | Breadcrumbs |
| Buttons | Carousel | Checkbox | Combobox |
| Dialog (Modal) | Disclosure | Feed | Grid |
| Headings | Image Labeling | Landmarks | Link |
| Listbox | Menu | Menu Button | Meter |
| Radio | Slider | Slider (Multi-thumb) | Spinbutton |
| Switch | Tables | Tabs | Toolbar |
| Tooltip | Treeview | Treegrid | Window Splitter |
| Accessibility (General) | | | |

### 💬 Prompts

Pre-built workflows your AI assistant can use:

| Prompt | What it does |
|--------|-------------|
| **`audit-component`** | Step-by-step accessibility audit — checks ARIA, keyboard, focus, contrast, headings, touch targets. Provide code + optional component type. |
| **`make-accessible`** | Rewrites inaccessible code into a fully accessible implementation with WAI-ARIA patterns and comments explaining every change. |
| **`check-form-accessibility`** | Form-specific audit — labels, required fields, error handling, fieldsets, autocomplete, tab order, and submit feedback. |
| **`wcag-checklist`** | Generates a WCAG 2.2 compliance checklist (AA or AAA) organized by principle, tailored to your page or component. |
| **`aria-guide`** | Complete ARIA implementation guide for a component — roles, attributes, keyboard table, focus management, screen reader script, and code example. |

### 📖 Resources

Browsable knowledge base for MCP clients:

- **`a11y://patterns`** — Index of all 33 component patterns
- **`a11y://patterns/{component}`** — Full pattern detail for any component

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Option 1: Run directly with uvx (no install needed)

```bash
uvx a11y-expert-mcp
```

### Option 2: Install with pip

```bash
pip install a11y-expert-mcp
```

Then run:

```bash
a11y-expert-mcp
```

### Option 3: Run from source

```bash
git clone https://github.com/Elizabeth1979/a11y-expert-mcp.git
cd a11y-expert-mcp
uv run a11y-expert-mcp
```

## Configuration

### Claude Desktop / Claude Code

Add to your MCP config (`~/.claude/config.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "a11y": {
      "command": "uvx",
      "args": ["a11y-expert-mcp"]
    }
  }
}
```

Or if running from source:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/a11y-expert-mcp", "a11y-expert-mcp"]
    }
  }
}
```

### Cursor / Windsurf / Other MCP Clients

Use the same `command` and `args` — check your editor's MCP configuration docs for the exact config file location.

## Usage Examples

Once connected, your AI assistant can:

**Get an accessible pattern:**
> "How do I build an accessible tabs component?"
> → The assistant calls `get_pattern("tabs")` and gets the full WAI-ARIA pattern with keyboard interaction and code.

**Review code for issues:**
> "Check this modal for accessibility problems"
> → The assistant calls `review_code(code, component_type="modal")` and gets specific issues with fixes.

**Check color contrast:**
> "Does #666 on #fff pass WCAG?"
> → The assistant calls `check_contrast("#666", "#fff")` and gets AA/AAA results for normal and large text.

**Generate a WCAG checklist:**
> "Give me a WCAG AA checklist for my checkout page"
> → The assistant uses the `wcag-checklist` prompt to generate a tailored compliance checklist.

## How It Works

The server bundles 33 WAI-ARIA pattern documents as a knowledge base. When your AI assistant asks about a component, it gets the real specification — not hallucinated ARIA attributes. The `review_code` tool runs 10+ static checks for common anti-patterns (click handlers on divs, missing labels, broken heading hierarchy, positive tabindex, etc.) and cross-references relevant patterns.

No external API calls. No database. Everything runs locally.

## Tech Stack

- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- Python 3.11+
- WAI-ARIA Authoring Practices knowledge base (bundled markdown files)

## License

MIT

## Author

Elli ([@Elizabeth1979](https://github.com/Elizabeth1979))
