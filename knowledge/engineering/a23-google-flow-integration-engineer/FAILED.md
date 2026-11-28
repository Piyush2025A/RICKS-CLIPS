# A23 FAILED approaches (never delete)
## X-a23-001: Cloud session drives Flow in a browser  (2026-11-27)
- **Tried:** ask the cloud session to read the user's Flow tab via Claude in Chrome (D014).
- **Result:** no `claude-in-chrome` tools exposed in the cloud session; nothing operated.
- **Why it failed:** cloud sessions do not expose local Chrome (MEDIUM; cause not isolated).
- **Lesson / do instead:** Flow runs in the local session only.
- **Revisit if:** official cloud-browser support is announced and verified.
## X-a23-002: Remote Control / attached computer folder as cloud-local bridge  (2026-11-27)
- **Tried:** D019-D021 native folder sharing on Linux Mint, Claude Desktop 6.28899.6.
- **Result:** blocked; the Linux computer does not offer folders to cloud sessions.
- **Lesson / do instead:** Google Drive connector (D023).
- **Revisit if:** Linux support for folder attach ships.
