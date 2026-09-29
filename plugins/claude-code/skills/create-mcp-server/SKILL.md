---
name: create-mcp-server
description: Set up, install, or configure an MCP server. Use when the user asks to "setup mcp", "install mcp server", "add mcp server", "configure mcp", "connect mcp server", or wants to add a new MCP server to their system.
argument-hint: [server-name or description]
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
---

# Setup MCP Server

Install and configure MCP servers using `mcpm` (MCP Package Manager) and connect them to MCP clients.

## Current State

Installed servers: !`mcpm ls 2>&1 | tail -n +3`

Available clients: !`mcpm client ls 2>&1 | grep -E '^\|' | tail -n +2`

Global config: file:~/.config/mcpm/servers.json

## Workflow

### 1. Determine the Server

If `$ARGUMENTS` names a server, proceed. Otherwise, use `AskUserQuestion` to clarify what the user needs.

Search the registry first:

```bash
mcpm search <query> --table
```

If a match exists, get details:

```bash
mcpm info <server-name>
```

If no registry match exists, search the web for the server's installation instructions and determine whether it runs via `npx`, a binary, `uvx`, `docker`, or another method.

### 2. Install the Server

**Registry server** (found via `mcpm search`):

```bash
mcpm install <server-name>
```

This is interactive and will prompt for env vars. Tell the user to run this themselves with `!` prefix if it requires interactive input.

**Custom server** (not in registry):

```bash
MCPM_NON_INTERACTIVE=true mcpm new <server-name> \
  --type stdio \
  --command <cmd> \
  --args "<space-separated args>" \
  --env "KEY1=value1,KEY2=value2" \
  --force
```

Common patterns:
- **npx**: `--command npx --args "-y <package-name> <flags>"`
- **uvx**: `--command uvx --args "<package-name> <flags>"`
- **binary**: `--command <binary-path> --args "<flags>"`
- **docker**: `--command docker --args "run -i --rm <image> <flags>"`
- **remote/SSE**: `--type remote --url <url>`

### 3. Configure Environment Variables

If the server needs API keys or tokens:

1. Check `mcpm info <server-name>` for required env vars
2. Ask the user for values using `AskUserQuestion`
3. Edit the server config: tell the user to run `! mcpm edit <server-name>`

Never hardcode secrets. Use `${ENV_VAR}` references where possible.

### 4. Connect to Client(s)

Add the server to one or more clients:

```bash
mcpm client edit <client-name> --add-server <server-name> --force
```

Common client names: `claude-code`, `goose-cli`, `claude-desktop`, `cursor`, `vscode`

To see available clients: `mcpm client ls`

### 5. Test the Server

Verify the server works:

```bash
mcpm inspect <server-name>
```

This launches the MCP Inspector for interactive testing. Tell the user to run this themselves with `!` prefix.

### 6. Add Permissions (Claude Code)

If the server was added to Claude Code, the user may want to allow specific MCP tools in their settings. MCP tool permissions follow the pattern `mcp__<server-name>__<tool-name>`.

Check `file:~/.config/claude/settings.json` for existing MCP permissions as reference.

### 7. Summary

Report what was done:
- Server name and how it was installed
- Which client(s) it was connected to
- Any env vars that need to be set
- How to test it (`mcpm inspect <name>`)

## Reference

| Command | Purpose |
|---------|---------|
| `mcpm search <query> --table` | Find servers in registry |
| `mcpm info <name>` | Server details and env vars |
| `mcpm install <name>` | Install from registry |
| `mcpm new <name> --type stdio --command <cmd> --args "<args>"` | Create custom server |
| `mcpm edit <name>` | Edit existing server config |
| `mcpm uninstall <name>` | Remove a server |
| `mcpm client edit <client> --add-server <name> --force` | Connect to client |
| `mcpm client edit <client> --remove-server <name> --force` | Disconnect from client |
| `mcpm inspect <name>` | Test with MCP Inspector |
| `mcpm ls` | List installed servers |
| `mcpm client ls` | List available clients |
