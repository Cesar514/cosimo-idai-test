# Raw Prompt Log from artifacts_prompts/session_prompt_raw_from_history.md

Session: `019c9b4d-c06c-7910-bfa2-f24daba39295`
Total prompts: 48

## P01 - 2026-02-26T18:56:53Z

There's a pptx, I'm giving a presentation of the latest on AI agents:

Multi-agentic Workflows: Orchestrating Coding Agents with CLI Tools, skills.md, and MCPs

Event Details
Date: Friday 27 February 2026
Time: 11:00, Lunch at 12
Location: Elm House 214/Teams
Lead: Cesar Contreras
Scope
What “multi-agent workflow” means in practice for research code
Live walkthrough: triggering multiple agents (Jules, Copilot, Codex CLI, Gemini CLI) for a small research task
How skills.md and MCPs structure repeatable workflows
Short introduction to Prism (OpenAI)
Key Topics
From blank repo to a working proof-of-concept using multiple agents
Role split: planner agent vs implementer agent vs reviewer agent
skills.md patterns for repeatable tasks (setup, coding, tests, docs)
MCP basics: why it helps, what it connects, how it fits into a workflow
Debug loop: using agents to find root cause, patch, test, and document
Requirements
Very basic coding familiarity
No prior language-specific expertise required
Comfort with VS Code or a similar IDE
Comfort utilizing GIT
Comfort with CLI tools or basic knowledge of them (preferred)


basically, I need to make 25 slides. with the different topics on here, and up to date explanations on the most hardcore way to use LLMs. and agentic systems, and all the available tools/techniques. And their usage in testing, research and writing. Also mention some of my experimental work in using agentic systems in robots. and the high risk high reward.

## P02 - 2026-02-26T19:03:32Z

My workflow is I use codex cli, for managing agents, and subagents at distinct depths. Then I use the codex git skills to publish some issues or lateral Ideas I might have into the research (or if I want certain research to be done), this then allows to use either Jules (via a tag in github) or Copilot (via an assignment in github), to do the research or solve the given issue or  let them try other parallel approaches. (maybe a slide on this could work) also I use gemini cli to examine and criticize my codex work. or to find issues, and bugs, and to classify them by difficulty, and push the issues to github so then i can assign an agent. I also use codex review to review whatever work other agents have done

## P03 - 2026-02-26T19:07:39Z

In robotics (and other systems, as long as they are ocnnected to a computer, they can be controlled as everything can be used as a tool. 5.3 Codex is great at this, so as long as we can find a way to connect, even the real world, or acquiring data from camera/sensors, is not impossible, and that can also be used by our agents. Even for data collection in the real world. or allowing them to use our own scripts as tools.

## P04 - 2026-02-26T19:08:35Z

Add a slide. of how to create a skill (you can see our skill-creator skill), to explain how it works.

## P05 - 2026-02-26T19:09:41Z

now, also talk about our skills most related to our topic (add 1 slide for each of them that you think are the most related to include)

## P06 - 2026-02-26T19:14:06Z

i only operate in -yolo mode. since high reward, requires the highest risks.

## P07 - 2026-02-26T19:14:50Z

also explain the agent, spawning subagents, spawning sub agents, and max depth. and why it's a marvelous function in codex, and the types of agents that exist.

## P08 - 2026-02-26T19:17:42Z

the usage of GPT 5.2 Pro. (Why it helps)
Codex planning mode (also available in gemini)
and the price of all these ubscriptions
(Also about local models)

## P09 - 2026-02-26T19:20:54Z

- also add the difference with the 3 main agents. Codex follows the rules you give. gemini cli, takes some initiative, and deviates. Claude tries to improve everything it's way, and does much more than asked. your choice matters. (Slide on this)

- Then slide on ralph wiggum

## P10 - 2026-02-26T19:23:23Z

research the ralph wiggum technique  as this is wrong!!

## P11 - 2026-02-26T19:25:25Z

Check every slide to know if the content of each is factually correct. also add some styling and images

## P12 - 2026-02-26T19:25:41Z

spawn as many subagents as possible to aid you with the different parts

## P13 - 2026-02-26T19:27:08Z

spawn as many subagents as possible to aid you with the different parts

## P14 - 2026-02-26T19:29:49Z

spawn even more agents with the purpose of doing research. and adding 3 references to each slide (in very small at the bottom), some agents should find references others focus on the styling

## P15 - 2026-02-26T19:37:58Z

Put some 6 agents to work on a robotic simulation that can be ran on python, and researching how to get it going by cloning some urdfs (this should be able to run on this mac), preferably let's do some mobile robotics, tell the agents to create a robot, and it's sim environment, in which the robot in our sim should be using a* to solve a maze as fast as possible. but also implement some maths for the generation of this labyrinths in the 3D environment, and everything the robot reaches the center, he starts at a new map. put another 10 agents to look alternative methods to A* to improve this (SOTA methods) for the labyrinth. allow communication between the agents via .md where they write up their progress another agent should be doing some supervision on all these agents. and test which methods are the fastest.

## P16 - 2026-02-26T19:42:34Z

can you spawn another agent that writes a CSV, with all the instructions. I've given (with timestamps preferably), and with the different agents and tasks that have been spawned, and have ocurred over the session. and keep him working on this whenever new stuff is given as an instruction or happens

## P17 - 2026-02-26T19:44:56Z

i see that the assets haven't been added to the presentation pptx (nor the images etc)

## P18 - 2026-02-26T19:47:40Z

can you also add some screenshots of the simulation that the agents did? [$screenshot](skills/screenshot/SKILL.md)

## P19 - 2026-02-26T19:50:06Z

can you push a test issue in github that says "verify the recommendations of robotics methods that exist in the repository exist, with at least 10 references from literature post 2021 ... or something similar using the github mcp

## P20 - 2026-02-26T19:51:57Z

can you add a second issue with the same purpose, but instead to do justifications with pre 2021 refs?

## P21 - 2026-02-26T19:52:57Z

if pybullet doesn't work, then use mujoco. Also remember. everything under a pixi environment for easier testing and everything

## P22 - 2026-02-26T21:17:59Z

if pybullet doesn't work, then use mujoco. Also remember. everything under a pixi environment for easier testing and everything please continue

## P23 - 2026-02-26T21:21:12Z

once it's working, let the agents test it and take screenshots in a testing folder and then analyze those screenshots to see if everything is alright, and to debug.

also, post 2 more isses (repeating exactly the same issues as before, but wanting at least 20 references with 4 sentences for each explaining why)

## P24 - 2026-02-26T21:25:40Z

Can you span "Larry" He monitors, and should say "Icecream" [flavor] with flavor being a different flavor everytime. everytime he polls for the agents

## P25 - 2026-02-26T21:33:17Z

gow do I check that the code works?

## P26 - 2026-02-26T21:34:10Z

i want the command to running the pixi of the sim directly. nothing else of the testing. just simulations

## P27 - 2026-02-26T21:35:08Z

Tell some agents to incorporate, and test gui better (I want to run the pixi directly from the main folder, and not have to enter robotics_maze subfolder. And also for the options for setup to appear directly on the GUI.

## P28 - 2026-02-26T21:36:04Z

Also, put agents to fix the presentation. As images need to be integrated to every single slide. references should be in every slide. and also, everything should be very aesthetic [$frontend-design](skills/frontend-design/SKILL.md)

## P29 - 2026-02-26T21:39:00Z

Can you spawn 3 agents to work on copying the skills from the main skills directory, to our main directory under /skills (The skills mentioned in our presentation, so we can share them?, keep them in the gitignore for now)

## P30 - 2026-02-26T21:43:42Z

the agents that are running the gui. I am never able to see our robot in the maze, it just immediately closes, instead of using real velocities (dynamics and physics on the robot movement, also are you using a real robot urdf? else fix to use one)

## P31 - 2026-02-26T21:53:14Z

get Jenny to remove Adoption Plan and Closing (and anything related to that slide. as not in the plans.), still the other agents havent added images to all slides! what's haappening, check them out

## P32 - 2026-02-26T21:54:51Z

What agents are working currently on what? don't leave any task interrupted

## P33 - 2026-02-26T21:56:11Z

What agents are working currently on what? don't leave any task interrupted I gave you several tasks to perform. so everything must be completed. go on please with everything

## P34 - 2026-02-26T21:58:28Z

Jenny didn't finished, and I see a lot of agents open. put an agent for the work on the GUI, another agent for the dynamics, another for the pptx, and the removal of stuff related to that. others to the images. others to the references. others to use the [$frontend-design](skills/frontend-design/SKILL.md) others to write a readme.md of everything happening in this repository. other for [$smart-docs](skills/smart-docs/SKILL.md) , and so on... I want to have 36 agents on 36 distinct tasks

## P35 - 2026-02-26T22:54:37Z

check that all agents have been fully closed

## P36 - 2026-02-26T22:54:44Z

check that all agents have been fully closed

## P37 - 2026-02-26T23:09:21Z

For the next part you are coordinating agents to write a latex paper in IEEE about everything that is implemented and researched for the implementation of this robotics setup (implemented and still to implement. The quality of the paper should be best robotics journal standards. so you need to coordinate researcher agents, reviewer agents, math agents, verifier agents, literature review agents, figure looking agents. and agents for critizing, commenting, and improving the paper. (Like reviewers from journals that give comments and get back). all the references for the paper must be from 2021 and newer, and should be at least 40.

## P38 - 2026-02-26T23:09:41Z

For the next part you are coordinating agents to write a latex paper in IEEE about everything that is implemented and researched for the implementation of this robotics setup (implemented and still to implement. The quality of the paper should be best robotics journal standards. so you need to coordinate researcher agents, reviewer agents, math agents, verifier agents, literature review agents, figure looking agents. and agents for critizing, commenting, and improving the paper. (Like reviewers from journals that give comments and get back). all the references for the paper must be from 2021 and newer, and should be at least 40.

## P39 - 2026-02-26T23:15:24Z

Implement the plan.

## P40 - 2026-02-27T07:58:51Z

Raise around 10 issues to github specifying some parts of the paper/literature/realsim/maths/etc that require work or verification

## P41 - 2026-02-27T10:25:40Z

have all the local readmes and logs been updated with all the latest?

## P42 - 2026-02-27T10:28:17Z

spawn aroun 16 agents to review the logs and readmes and append/modify/add whatever is missing from the logs. so everything is up to date.

## P43 - 2026-02-27T12:01:43Z

what is this repo about

## P44 - 2026-02-27T18:44:42Z

What would be great is if you can add the plan we used for the paper writing to an .md so people reading the repo can read it. Also Putting all the prompts, and steps we took into a SLIDESHOW, (and the outputs or results of each step), so people can follow through in everything we did in this repo to get things working

## P45 - 2026-02-27T18:48:24Z

I think this is not the real plan we used, and this are not all the prompts. You need to investigate this session chatlog fully

## P46 - 2026-02-27T18:51:08Z

I think this is not the real plan we used, and this are not all the prompts. You need to investigate this session chatlog fully. codex resume 019c9b4d-c06c-7910-bfa2-f24daba39295

## P47 - 2026-02-27T18:56:53Z

did you used the session log to read the actual prompts and actual plan?

## P48 - 2026-02-27T18:59:04Z

this is missing a lot of data. you need to actually check codex global folder, and find the actual logs. instead. and put this 3 requested files in a folder called artifacts_prompts/ 019c9b4d-c06c-7910-bfa2-f24daba39295 should be this session

