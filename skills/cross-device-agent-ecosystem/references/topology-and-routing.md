# Topology and routing

Use this reference to select where a task should run or to isolate a failed
cross-device workflow. The inventory below is owner-verified baseline context,
not proof that a host is currently reachable.

## Private device map

| Device or environment | Durable role |
| --- | --- |
| MacBook Air M4 running macOS | Private desktop agent host, coordinating interface, and SSH client for the Dell environments. |
| Dell Tower ECT1250 running Windows 11 | Native Windows ChatGPT host for Windows files, PowerShell, GUI work, Chrome-extension workflows, and foreground Computer Use. |
| Ubuntu 24.04 in WSL2 on the Dell tower | Parallel Linux development host with Codex CLI and the Codex app server installed; target for raw SSH and Mac app SSH projects. |
| Samsung Galaxy S25 FE running Android | Mobile controller for paired desktop hosts and their local or SSH-backed projects. |

The Mac, Windows host, and Android controller use Arthur's private
ChatGPT/Codex account and workspace where Remote requires it. Live availability,
permissions, and trust still belong to the selected host and connection.

## Choose the interface

| Need | Interface | Execution location |
| --- | --- | --- |
| Windows GUI, Chrome extension, or Computer Use | ChatGPT Remote / Control other devices to the Windows-native desktop host | Native Windows session on the Dell tower |
| Windows files or PowerShell from the Mac | Raw SSH to the configured native-Windows alias | Native Windows shell and filesystem |
| Linux files, shell, development, or a Codex remote project on the Dell tower | Raw SSH or an app SSH project through the configured WSL alias | Ubuntu in WSL2 |
| Continue or steer work from the phone | Android Remote through a paired desktop host | The selected desktop host, or its selected SSH-backed project |
| Human keyboard/mouse switching or transfer of approved text, images, or files | Logitech Flow / Logi Options+ | Between the private Mac and Windows computers |
| Cross-machine skill and global-guidance refresh | GitHub plus SkillPort automation | Each configured private environment |

Logitech Flow is a convenience transport, not a security approval mechanism.
Transfer only material the human has approved for the destination.

## Do not collapse the layers

1. **ChatGPT Remote / Control other devices** pairs a phone or supported desktop
   with a ChatGPT desktop host. It exposes that host's projects, chats, files,
   host-local authentication context, permissions, plugins, browser setup,
   Computer Use, and tools. It is not a general-purpose SSH session.
2. **Raw SSH** is independent of Codex. It can execute the remote login shell and
   read, write, or transfer files within that SSH account's permissions. The
   Mac has verified raw SSH paths to native Windows and to WSL; use configured
   aliases without exposing their connection details.
3. **An app SSH project** makes the desktop app start the remote Codex app server
   through SSH and run project chats against that host's filesystem and login
   shell. The Mac app's verified target is WSL, where the required Linux shell
   and Codex runtime are available.
4. In this setup, native-Windows SSH correctly provides a Windows shell for raw
   PowerShell work but did not satisfy the desktop app's Unix-shell expectations.
   Use WSL for app SSH projects; keep native-Windows SSH for raw Windows work.
5. Configuring Mac app SSH to WSL does not change the Windows app. Windows native
   agent plus Windows Chrome/Computer Use and WSL-backed remote projects are
   designed to coexist.
6. Android is primarily a controller of paired desktop hosts. Route phone work
   as phone -> paired desktop host -> local or SSH-backed project. Do not invent
   a phone-to-SSH credential setup or assume host trust metadata exists on the
   phone.

Official behavior is documented in OpenAI's
[Remote connections](https://learn.chatgpt.com/docs/remote-connections) and
[ChatGPT desktop app for Windows](https://learn.chatgpt.com/docs/windows/windows-app)
pages. Recheck those pages before changing product-specific invariants when the
current app behavior differs from this reference.

## Preconditions

- Remote: the selected desktop host is awake, online, running ChatGPT, permitted
  to accept connections, and signed into the same authorized account/workspace
  as the controller.
- Foreground Windows Computer Use: the Windows session is unlocked and available
  to the task.
- Raw or app SSH: the endpoint is reachable from the controlling desktop, its
  configured alias resolves, and the intended remote shell/runtime is available.
- App SSH: `codex` is available to the remote login shell and the project exists
  on that remote filesystem.
- Any route: host permissions, approvals, sandbox boundaries, browser state,
  plugins, and tools remain those of the host where execution occurs.

## Dispatch a Codex task to another connected desktop host

Controlling one computer from another does not move the current Codex task. To
run new work on a connected desktop host, create a task whose execution host is
that destination instead of trying to operate destination-local apps from the
source task.

1. List accessible Codex tasks and projects. Identify the destination by its
   human-readable host name and retain the host identifier returned by the app;
   never invent or hardcode a machine identifier.
2. Prefer creating a fresh task in a suitable project on the destination host.
   Check the project's repository status and use its normal local or worktree
   environment as appropriate.
3. If the app does not expose a suitable destination project, choose a recent,
   accessible task already backed by that host and fork it into a same-directory
   child. Rename the child for the new work, then send the complete task prompt
   to the child with the destination host identifier.
4. Do not place unrelated work directly into the existing task merely because it
   proves the host is reachable. The clean child preserves the original task's
   context and ownership.
5. Verify the new task once with a bounded status snapshot. Report that the
   request was dispatched and name the destination host. Let the destination
   task carry out host-local work under its own permissions.

A fork can fail when the selected source task is stale or its rollout is no
longer loaded. In that case, select a more recent loaded or idle task on the same
host and try once more. Do not repeatedly poll unchanged state, and do not treat
an unavailable stale task as evidence that the host itself is disconnected.

Keep the prompt self-contained: state the desired outcome, identify resources by
human-readable names or approved links, and preserve the source task's permission
boundaries. Do not include credentials, private connection details, or local
machine identifiers.

## Troubleshoot the exact layer first

Before trying fixes, state the failed path end to end and identify the first
boundary without evidence:

1. Is the desktop host awake, online, and signed in?
2. Is this a Remote pairing problem, a raw SSH reachability/login-shell problem,
   an app SSH/Codex-runtime problem, a WSL problem, or a browser-extension /
   Computer Use problem?
3. Which host and filesystem does the current project actually use?
4. Which shell is executing the failing command: Windows agent shell,
   integrated terminal, raw SSH login shell, or WSL app-server shell?
5. Which permission, sandbox, browser, or trust boundary applies there?

Gather a safe status result from the failing layer, then make a layer-local
change. Do not change the Windows Agent Environment, default shell, SSH target,
or global synchronization setup merely because a neighboring layer failed.
