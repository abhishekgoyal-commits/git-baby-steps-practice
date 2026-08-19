# Agent Instructions Directory

This directory contains specialized agent instructions for common project tasks.

## Available Instructions

### [create-status-report.agent.md](create-status-report.agent.md)
**Purpose:** Generate concise weekly status reports for stakeholder communication

**Key Specs:**
- Format: Markdown
- Max 20 lines, bullet points only
- Sections: Accomplishments, Blockers, Next Week
- Tone: Professional, metric-focused
- Avoids: Fluff language, vague statements

**Usage:** When creating weekly status updates, sync team progress, or reporting to leadership

### [creating-instructions.agent.md](creating-instructions.agent.md)
**Purpose:** Create and maintain platform-agnostic project instructions and IDE wrappers

**Keywords:** create instruction, update instruction, configure instructions, agent instructions, instruction catalog

**Usage:** When adding, revising, validating, or wiring project instruction files

---

## Adding New Instructions

When creating new instruction files:
1. Use `.agent.md` extension
2. Start with a clear Purpose section
3. Include specific constraints and format requirements
4. Add validation checklist for quality assurance
5. Update this index file with a description and usage note

---

## Quick Reference

| Instruction | Purpose | Format | Owner |
|---|---|---|---|
| create-status-report | Weekly status reporting | Markdown, ≤20 lines | Project Team |
