# Layers of facts

Start at layer 1 and go down one layer only when every signal so far is weak. Each layer costs more to reach and shows a narrower slice. Stop at the first strong signal.

MCP tools are deferred: load them with ToolSearch (`select:<name>,<name>`) in one call before use.

## 1. Application and platform: already collected, cheapest

The table shows the author's stack as an example. Replace each tool with the one that reaches the same fact in your stack.

| Fact | Where |
| --- | --- |
| Logs | Grafana Loki: `mcp__grafana__query_loki_logs`, `mcp__grafana__query_loki_patterns`. Railway services: `mcp__railway__get-logs`. Crashed pod: `kubectl logs --previous`. |
| Metrics | Prometheus: `mcp__grafana__query_prometheus`, `mcp__grafana__query_prometheus_histogram`. Railway: `mcp__railway__get-service-metrics`, `mcp__railway__http-error-rate`, `mcp__railway__http-response-time`. |
| Traces | Railway: `mcp__railway__list-traces`, `mcp__railway__get-trace`. Grafana may proxy Tempo. |
| Errors, product events, flags | PostHog: `mcp__plugin_posthog_posthog__exec` (error-tracking, logs, feature-flag, query). |
| Data and query behaviour | ClickHouse: `mcp__clickhouse__run_select_query`, including `system.query_log` for what queries actually ran. |
| Deploys and config | `git log -p -- helm/<env>/`, `kubectl rollout history`, `kubectl get events`, `kubectl describe pod`, `mcp__railway__list-deployments`. |
| Code history | `git log -S '<symbol>'`, `git log <last-good>..<first-bad>`, PR descriptions, Linear postmortems. |

## 2. Network

Inside the pod or host (`kubectl exec`): `getent hosts` or `dig` (count the answers), `ss -tanp` (connection states and counts), `tcpdump` when present. Compare counts between control and variable: DNS answers, open connections, retries, resets.

## 3. Storage

`lsof -p <pid>`, `df -i`, `strace -f -e trace=file -p <pid>` (files opened per request). For ClickHouse: `system.parts`, `system.merges`, read and written bytes in `system.query_log`.

## 4. Process and runtime

Python: `py-spy dump --pid <pid>` (where every thread is now), `py-spy record` (where time goes). Go: `pprof` heap and goroutine profiles. Node: `--inspect` heap snapshot. Thread states, GC pauses, file descriptor counts, lock waits.

## 5. Kernel and OS

`dmesg` (OOM kills), cgroup `cpu.stat` (throttling), `strace -c` (syscall counts), IPC state.

## 6. Host

Node metrics through Prometheus (node_exporter): CPU steal, NIC drops, disk errors.

## App logic: down the request path

For a logic bug, the layers are the steps a request passes through. Compare control and variable at each step, from the outside in. The first step where they differ holds the cause.

1. What the user sees: rendered page or UI (headless browser).
2. What the server sent: page data or API response (`__data.json`, the JSON body).
3. The route loader or controller that built it.
4. The repository or query layer: the query it builds and the rows it gets back.
5. Raw rows in the database.

## Learned in this codebase

Signals and sources that past debug sessions found live in `.claude/debug-layers.md` at the project root, not in this file. `/debug-retro` adds lines there: the source, the exact query or command, and the signal it showed. Read that file before you go down a layer.
