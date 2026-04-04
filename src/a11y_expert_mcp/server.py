"""A11y Expert MCP Server — accessibility guidance for AI coding assistants."""

import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("a11y-expert")

# ---------------------------------------------------------------------------
# Knowledge base loader
# ---------------------------------------------------------------------------

KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


def _load_knowledge() -> dict[str, str]:
    """Load all .instructions.md files into a dict keyed by component name."""
    knowledge: dict[str, str] = {}
    if not KNOWLEDGE_DIR.exists():
        return knowledge
    for f in sorted(KNOWLEDGE_DIR.glob("*.instructions.md")):
        name = f.stem.replace(".instructions", "").replace("_", " ").replace("-", " ")
        knowledge[name] = f.read_text(encoding="utf-8")
    return knowledge


# Load once at startup
KNOWLEDGE = _load_knowledge()

# Build a quick index for searching
COMPONENT_NAMES = sorted(KNOWLEDGE.keys())


def _find_relevant_patterns(query: str, max_results: int = 3) -> list[tuple[str, str]]:
    """Simple keyword matching to find relevant patterns. No vector DB needed."""
    query_lower = query.lower()
    scored: list[tuple[int, str]] = []

    for name, content in KNOWLEDGE.items():
        score = 0
        # Exact name match = highest
        if name in query_lower:
            score += 100
        # Check for word overlap
        query_words = set(re.findall(r"\w+", query_lower))
        name_words = set(re.findall(r"\w+", name.lower()))
        score += len(query_words & name_words) * 20
        # Check content for query words (sample first 2000 chars for speed)
        content_sample = content[:2000].lower()
        for word in query_words:
            if len(word) > 3 and word in content_sample:
                score += 5
        if score > 0:
            scored.append((score, name))

    scored.sort(reverse=True)
    return [(name, KNOWLEDGE[name]) for _, name in scored[:max_results]]


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_pattern(component: str) -> str:
    """Get the accessible implementation pattern for a UI component.

    Args:
        component: The component name (e.g., "modal", "tabs", "combobox",
                   "carousel", "menu", "dialog", "tooltip", "alert",
                   "switch", "listbox", "treeview", "slider", "feed",
                   "grid", "disclosure", "landmarks", "headings", "buttons",
                   "link", "spinbutton", "meter", "menu button").

    Returns:
        Detailed WAI-ARIA Authoring Practices pattern with code examples,
        keyboard interaction requirements, and ARIA roles/states/properties.
    """
    results = _find_relevant_patterns(component, max_results=1)
    if results:
        name, content = results[0]
        return f"# Accessible {name.title()} Pattern\n\n{content}"

    # Fuzzy fallback — list available patterns
    return (
        f"No exact pattern found for '{component}'.\n\n"
        f"Available patterns:\n"
        + "\n".join(f"- {name}" for name in COMPONENT_NAMES)
        + "\n\nTry one of these, or describe what you're building."
    )


@mcp.tool()
def review_code(code: str, component_type: str = "") -> str:
    """Review code for accessibility issues and suggest fixes.

    Args:
        code: The HTML, JSX, TSX, Vue, or Svelte component code to review.
        component_type: Optional hint about what the component is
                        (e.g., "modal", "dropdown", "form").

    Returns:
        Accessibility issues found with specific fix suggestions and
        references to WAI-ARIA patterns.
    """
    issues: list[str] = []
    suggestions: list[str] = []
    code_lower = code.lower()

    # ---- Check for common accessibility anti-patterns ----

    # 1. Click handlers on non-interactive elements
    if re.search(r"<div[^>]*onclick|<span[^>]*onclick|<div[^>]*onClick|<span[^>]*onClick", code):
        issues.append("Click handler on non-interactive element (<div> or <span>)")
        suggestions.append(
            "Use <button> instead of <div onClick>. If you must use a div, "
            "add role=\"button\", tabindex=\"0\", and onKeyDown handler for Enter/Space."
        )

    # 2. Missing alt text on images
    if re.search(r"<img(?![^>]*alt\s*=)", code):
        issues.append("Image missing alt attribute")
        suggestions.append(
            "Add alt=\"descriptive text\" for meaningful images, "
            "or alt=\"\" for decorative images."
        )

    # 3. Missing form labels
    if re.search(r"<input|<select|<textarea", code) and not re.search(
        r"<label|aria-label|aria-labelledby", code
    ):
        issues.append("Form inputs may be missing labels")
        suggestions.append(
            "Every form input needs a <label> with matching for/id, "
            "or aria-label/aria-labelledby."
        )

    # 4. Missing button text
    if re.search(r"<button[^>]*>\s*<(?:svg|img|i|icon)", code) and not re.search(
        r"aria-label", code
    ):
        issues.append("Button appears to have only an icon with no accessible name")
        suggestions.append("Add aria-label to icon-only buttons: <button aria-label=\"Close\">")

    # 5. Improper heading hierarchy
    headings = re.findall(r"<h(\d)", code)
    if headings:
        levels = [int(h) for h in headings]
        for i in range(1, len(levels)):
            if levels[i] > levels[i - 1] + 1:
                issues.append(f"Heading level skips from h{levels[i-1]} to h{levels[i]}")
                suggestions.append("Don't skip heading levels. Go h1 → h2 → h3, not h1 → h3.")
                break

    # 6. Missing dialog/modal roles
    if any(word in code_lower for word in ["modal", "dialog", "popup", "overlay"]):
        if "role=\"dialog\"" not in code and "role='dialog'" not in code:
            issues.append("Modal/dialog may be missing role=\"dialog\" and aria-modal=\"true\"")
            suggestions.append(
                "Add role=\"dialog\" aria-modal=\"true\" aria-labelledby=\"title-id\" "
                "to the dialog container. Trap focus inside the dialog."
            )

    # 7. tabindex > 0
    if re.search(r'tabindex\s*=\s*["\']?[1-9]', code):
        issues.append("tabindex with positive value found")
        suggestions.append(
            "Never use tabindex > 0. It breaks natural tab order. "
            "Use tabindex=\"0\" to add to tab order, tabindex=\"-1\" for programmatic focus."
        )

    # 8. Missing lang attribute
    if "<html" in code_lower and "lang=" not in code_lower:
        issues.append("Missing lang attribute on <html>")
        suggestions.append('Add lang attribute: <html lang="en"> (use appropriate language code)')

    # 9. autoplay media
    if "autoplay" in code_lower:
        issues.append("Autoplay media detected")
        suggestions.append(
            "Autoplay can be disorienting. Provide pause/stop controls. "
            "WCAG 1.4.2 requires a mechanism to pause or stop auto-playing audio."
        )

    # 10. Missing aria-live for dynamic content
    if any(word in code_lower for word in ["toast", "notification", "snackbar", "alert"]):
        if "aria-live" not in code and 'role="alert"' not in code and "role='alert'" not in code:
            issues.append("Dynamic notification may be missing aria-live or role=\"alert\"")
            suggestions.append(
                "Use aria-live=\"polite\" for non-urgent updates, "
                "aria-live=\"assertive\" or role=\"alert\" for important notifications."
            )

    # ---- Get relevant patterns for context ----
    search_query = component_type or code[:200]
    relevant = _find_relevant_patterns(search_query, max_results=2)

    # ---- Build response ----
    response_parts: list[str] = []

    if issues:
        response_parts.append(f"## Found {len(issues)} accessibility issue(s)\n")
        for i, (issue, suggestion) in enumerate(zip(issues, suggestions), 1):
            response_parts.append(f"### Issue {i}: {issue}\n**Fix:** {suggestion}\n")
    else:
        response_parts.append(
            "## No obvious accessibility issues detected\n\n"
            "Note: This is a static check. Always test with a screen reader "
            "(NVDA, VoiceOver) and keyboard navigation for full coverage.\n"
        )

    if relevant:
        response_parts.append("\n## Relevant accessibility patterns\n")
        for name, content in relevant:
            # Extract just the critical rules section
            critical_match = re.search(
                r"(## CRITICAL RULES.*?)(?=\n## [A-Z]|\Z)", content, re.DOTALL
            )
            if critical_match:
                response_parts.append(f"### {name.title()}\n{critical_match.group(1)[:1500]}\n")
            else:
                response_parts.append(
                    f"### {name.title()}\n{content[:800]}\n...(use get_pattern for full details)\n"
                )

    return "\n".join(response_parts)


@mcp.tool()
def list_patterns() -> str:
    """List all available accessible component patterns.

    Returns:
        A list of all component patterns available in the knowledge base.
    """
    if not COMPONENT_NAMES:
        return "No patterns loaded. Check that the knowledge directory exists."

    lines = [f"## Available Accessibility Patterns ({len(COMPONENT_NAMES)} components)\n"]
    for name in COMPONENT_NAMES:
        lines.append(f"- **{name.title()}** — use `get_pattern(\"{name}\")` for full details")
    return "\n".join(lines)


@mcp.tool()
def check_contrast(foreground: str, background: str) -> str:
    """Check if two colors meet WCAG contrast ratio requirements.

    Args:
        foreground: Foreground color as hex (e.g., "#333333" or "333").
        background: Background color as hex (e.g., "#ffffff" or "fff").

    Returns:
        Contrast ratio and pass/fail for WCAG AA and AAA levels.
    """

    def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    def relative_luminance(r: int, g: int, b: int) -> float:
        def channel(c: int) -> float:
            s = c / 255.0
            return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    try:
        fg_rgb = hex_to_rgb(foreground)
        bg_rgb = hex_to_rgb(background)
    except (ValueError, IndexError):
        return "Invalid color format. Use hex like '#333333' or '#fff'."

    lum_fg = relative_luminance(*fg_rgb)
    lum_bg = relative_luminance(*bg_rgb)

    lighter = max(lum_fg, lum_bg)
    darker = min(lum_fg, lum_bg)
    ratio = (lighter + 0.05) / (darker + 0.05)

    # WCAG thresholds
    aa_normal = ratio >= 4.5
    aa_large = ratio >= 3.0
    aaa_normal = ratio >= 7.0
    aaa_large = ratio >= 4.5

    return (
        f"## Contrast Check: {foreground} on {background}\n\n"
        f"**Contrast ratio: {ratio:.2f}:1**\n\n"
        f"| Level | Normal Text (< 18pt) | Large Text (≥ 18pt / 14pt bold) |\n"
        f"|-------|---------------------|----------------------------------|\n"
        f"| AA    | {'PASS' if aa_normal else 'FAIL'} (need 4.5:1) | "
        f"{'PASS' if aa_large else 'FAIL'} (need 3:1) |\n"
        f"| AAA   | {'PASS' if aaa_normal else 'FAIL'} (need 7:1) | "
        f"{'PASS' if aaa_large else 'FAIL'} (need 4.5:1) |\n"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
