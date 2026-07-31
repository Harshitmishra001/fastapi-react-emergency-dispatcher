# Disaster & Emergency Resource Coordinator: Project Documentation

This document explains the architecture, workflow, and components of the Disaster & Emergency Resource Coordinator project using a **Lightweight Agile / STAR (Situation, Task, Action, Result)** hybrid approach. This format is designed to make it easy for developers, product managers, and stakeholders to understand *why* we built this, *what* we built, and *how* it works under the hood.

---

## 1. Situation: The Problem We Are Solving

During a natural disaster or emergency, communication channels (SMS, social media, radio) are flooded with chaotic, unstructured, and often duplicate reports of people needing help. 
Emergency dispatchers are overwhelmed, struggling to parse these messages, verify their legitimacy, match them to available resources, and create fair dispatch plans without missing critical needs.

## 2. Task: Our Agile Objectives

We needed to build an intelligent, multi-agent AI system to automate the triage and dispatch planning process, while keeping a "Human-in-the-Loop" for critical safety oversight.

**Key Epics (Agile Stories):**
- **Epic 1 (Ingestion):** As a system, I want to parse messy text messages into structured needs (Water, Medical, Shelter).
- **Epic 2 (Verification):** As a dispatcher, I want the system to flag low-confidence or duplicate reports so I don't waste time on false alarms.
- **Epic 3 (Resource Matching):** As a system, I want to mathematically match verified needs against our current inventory of resources based on location and urgency.
- **Epic 4 (Planning & Evaluation):** As a dispatcher, I want the system to draft a dispatch plan and automatically evaluate it for fairness and coverage before I approve it.
- **Epic 5 (Human Oversight):** As a dispatcher, I want a dashboard to manually review flagged items and override the AI when necessary.

---

## 3. Action: How the System Works (The Implementation)

We implemented a **Multi-Agent Architecture** orchestrated by **LangGraph**, communicating with a **FastAPI backend** and a **React (Vite) frontend**. 

Here is an easy-to-understand breakdown of each section.

### A. The Core AI Agents (`backend/agents/`)
Instead of one giant AI trying to do everything, we split the work into five specialized "Agents", each with a specific job:

1. **Ingestion Agent:** 
   - *Job:* Reads the raw, messy text (e.g., "Send blankets to 5th st ASAP!") and turns it into structured data (Type: Shelter, Urgency: High).
   - *Fallback:* If the AI fails to parse it, it falls back to a fast, regex keyword scanner.
2. **Verification Agent:** 
   - *Job:* Looks at the extracted need and checks if it's a duplicate of something we already know using local `sentence-transformers`. It assigns a "confidence score". If the score is too low, it flags the report for **Human Review**.
3. **Resource Matcher:** 
   - *Job:* Takes all verified needs and looks at our available resources in the database. It greedily matches the highest urgency needs to the closest available resources.
4. **Plan Synthesizer:** 
   - *Job:* Takes the matches and drafts a human-readable "Dispatch Narrative" (e.g., "Deploying 50 blankets from Warehouse A to 5th St.").
5. **Evaluator Agent:** 
   - *Job:* Acts as the internal critic. It reviews the Synthesizer's plan and scores it on **Fairness** and **Coverage**. If the plan fails, it rejects the plan and forces the system to try again (up to 2 times).

### B. The Orchestrator (`backend/graph/`)
We use **LangGraph** to connect these 5 agents into a flowchart (a State Graph). 
- **State (`state.py`):** Holds the memory of the current report as it moves from agent to agent.
- **Graph (`build_graph.py`):** Defines the arrows connecting the agents. 
- **Human-in-the-Loop:** LangGraph has a built-in memory checkpoint. If the Verification Agent flags a report, the graph *pauses execution*. It waits for a human dispatcher to click "Approve" or "Reject" on the frontend before the graph resumes.

### C. The API Backend (`backend/api/`, `backend/db/`, `backend/security/`)
- **FastAPI Routes (`routes.py`):** Exposes endpoints for the frontend to submit reports (`/reports`), fetch the review queue (`/review/queue`), and view plans (`/plans`).
- **Database (`models.py`):** Uses SQLAlchemy with a local SQLite database to store Reports, Needs, Resources, and Allocations.
- **Security:** 
  - *Input Sanitization:* Prevents malicious users from injecting XML tags (`<raw_text>`) to confuse the AI.
  - *Rate Limiting:* Prevents spam attacks using an in-memory sliding window.
  - *Auth:* Role-based access control (RBAC) ensuring only `reviewers` and `admins` can approve plans or manage resources.

### D. The Frontend (`frontend/`)
Built with **React, Vite, and Tailwind CSS v4**.
- **Live Map (`LiveMap.jsx`):** A sleek, dark-mode dashboard showing abstract visual pings of incoming needs, available resources, and dispatched units.
- **Review Queue (`ReviewQueue.jsx`):** The interface where human dispatchers see low-confidence AI decisions. They can read the AI's reasoning and click "Approve" or "Reject & Edit".

---

## 4. Result: The Value Delivered

By combining the **STAR** problem-solving approach with **Lightweight Agile** development, we achieved:
1. **Speed:** The multi-agent pipeline processes chaotic data in seconds.
2. **Safety:** The Evaluator Agent and the Human-in-the-Loop ensure the AI never autonomously deploys resources to hallucinated or low-confidence locations.
3. **Modularity:** Because the agents are decoupled via LangGraph, we can swap out the local LLM (like `smollm3-3b` via LM Studio) for a larger cloud model without breaking the pipeline.
4. **Scalability:** The FastAPI and React stack is ready to be dockerized and deployed to the cloud when moving out of local development.
