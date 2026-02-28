# Full Session Prompt Ledger (Actual Global Log Source)

Session id: `019c9b4d-c06c-7910-bfa2-f24daba39295`  
Source file: `artifacts_prompts/session_prompt_raw_from_history.md`  
Extracted prompt file: `artifacts_prompts/session_prompt_raw_from_history.md`

## Full ordered prompt list

| Prompt ID | UTC Time | User Prompt (short label) |
|---|---|---|
| P01 | 2026-02-26T18:56:53Z | 25-slide AI agents presentation scope |
| P02 | 2026-02-26T19:03:32Z | Codex/Jules/Copilot/Gemini workflow slide content |
| P03 | 2026-02-26T19:07:39Z | Robotics tooling and real-world sensor/control framing |
| P04 | 2026-02-26T19:08:35Z | Add slide: how to create a skill |
| P05 | 2026-02-26T19:09:41Z | Add slides for most relevant skills |
| P06 | 2026-02-26T19:14:06Z | YOLO/high-risk mode preference |
| P07 | 2026-02-26T19:14:50Z | Explain agents/subagents/depth/types |
| P08 | 2026-02-26T19:17:42Z | GPT 5.2 Pro/planning mode/subscriptions/local models |
| P09 | 2026-02-26T19:20:54Z | Codex vs Gemini vs Claude slide + Ralph Wiggum slide |
| P10 | 2026-02-26T19:23:23Z | Correct Ralph Wiggum technique (research needed) |
| P11 | 2026-02-26T19:25:25Z | Factual correctness + styling + images for all slides |
| P12 | 2026-02-26T19:25:41Z | Spawn many subagents |
| P13 | 2026-02-26T19:27:08Z | Spawn many subagents (repeat) |
| P14 | 2026-02-26T19:29:49Z | More agents for refs/styling; 3 refs per slide |
| P15 | 2026-02-26T19:37:58Z | 6 build + 10 research agents for robotics maze simulation |
| P16 | 2026-02-26T19:42:34Z | Spawn logger agent and maintain CSV timeline |
| P17 | 2026-02-26T19:44:56Z | Deck assets/images missing |
| P18 | 2026-02-26T19:47:40Z | Add simulation screenshots |
| P19 | 2026-02-26T19:50:06Z | Create GitHub issue with >=10 post-2021 refs |
| P20 | 2026-02-26T19:51:57Z | Create second issue with pre-2021 refs |
| P21 | 2026-02-26T19:52:57Z | If pybullet fails use mujoco; everything under pixi |
| P22 | 2026-02-26T21:17:59Z | Continue pybullet->mujoco + pixi direction |
| P23 | 2026-02-26T21:21:12Z | Test + screenshots + analysis + debug; add 2 expanded issues |
| P24 | 2026-02-26T21:25:40Z | Spawn Larry monitor with rotating icecream messages |
| P25 | 2026-02-26T21:33:17Z | How to check code works |
| P26 | 2026-02-26T21:34:10Z | Root pixi command for simulation only |
| P27 | 2026-02-26T21:35:08Z | Improve/test GUI; run from root; setup options in GUI |
| P28 | 2026-02-26T21:36:04Z | Fix presentation images/refs/aesthetics |
| P29 | 2026-02-26T21:39:00Z | Spawn 3 agents to copy skills to `/skills` + gitignore |
| P30 | 2026-02-26T21:43:42Z | GUI closes/no robot visible; fix dynamics + real URDF |
| P31 | 2026-02-26T21:53:14Z | Remove Adoption/Closing slides; ensure slide images |
| P32 | 2026-02-26T21:54:51Z | What agents are currently working |
| P33 | 2026-02-26T21:56:11Z | Continue all tasks; no interruptions |
| P34 | 2026-02-26T21:58:28Z | 36 agents on 36 distinct tasks |
| P35 | 2026-02-26T22:54:37Z | Verify all agents fully closed |
| P36 | 2026-02-26T22:54:44Z | Verify all agents fully closed (repeat) |
| P37 | 2026-02-26T23:09:21Z | Start IEEE paper orchestration (>=40 refs, >=2021) |
| P38 | 2026-02-26T23:09:41Z | Repeat IEEE paper orchestration prompt |
| P39 | 2026-02-26T23:15:24Z | Implement the plan |
| P40 | 2026-02-27T07:58:51Z | Raise ~10 GitHub issues for pending verification/work |
| P41 | 2026-02-27T10:25:40Z | Confirm local readmes/logs up to date |
| P42 | 2026-02-27T10:28:17Z | Spawn ~16 agents to refresh logs/readmes |
| P43 | 2026-02-27T12:01:43Z | Ask what repo is about |
| P44 | 2026-02-27T18:44:42Z | Ask for paper plan .md + slideshow of prompts/steps/results |
| P45 | 2026-02-27T18:48:24Z | Say plan/prompts incomplete; request full chatlog investigation |
| P46 | 2026-02-27T18:51:08Z | Repeat and ask to resume specific session id |
| P47 | 2026-02-27T18:56:53Z | Ask if actual session log was used |
| P48 | 2026-02-27T18:59:04Z | Instruct use global Codex logs and place 3 files in `artifacts_prompts/` |

## Mapping to major outputs

- Presentation artifacts:
  - `agents.pptx`
  - `presentation_assets/slide_references.json`
  - `presentation_assets/slide_image_map.json`
- Robotics implementation artifacts:
  - `robotics_maze/src/main.py`
  - `robotics_maze/src/sim.py`
  - `robotics_maze/src/robot.py`
  - `robotics_maze/src/benchmark.py`
- Testing/screenshot artifacts:
  - `robotics_maze/testing/TEST_RUN_LOG.md`
  - `robotics_maze/testing/screenshots/`
  - `robotics_maze/testing/reports/screenshot_analysis.md`
- Coordination/log artifacts:
  - `robotics_maze/coordination/session_event_log.csv`
  - `robotics_maze/coordination/AGENT_DASHBOARD.md`
- Paper artifacts:
  - `paper/ieee_tro_robotics_maze/coordination/review_rounds/`
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_source.zip`
- GitHub issue tracks:
  - `#1`, `#2`, `#5`, `#6`, `#9`-`#18`

## Verification note

This ledger is driven by actual global session log entries from `artifacts_prompts/session_prompt_raw_from_history.md` for this exact session id.
