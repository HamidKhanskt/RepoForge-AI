
<img width="1449" height="465" alt="Screenshot 2026-08-26 at 9 08 15 PM" src="https://github.com/user-attachments/assets/aaeb690a-67be-46f5-a6a2-1ca5145ac124" />

<img width="1424" height="455" alt="Screenshot 2026-08-26 at 9 08 25 PM" src="https://github.com/user-attachments/assets/f39b43d7-3239-42e7-ac18-cbfde8622c2d" />

<img width="1412" height="575" alt="Screenshot 2026-08-26 at 9 08 32 PM" src="https://github.com/user-attachments/assets/38b4e1e4-e56d-40d7-8f5f-d530049aabf6" />

<img width="1126" height="303" alt="Screenshot 2026-08-26 at 9 08 42 PM" src="https://github.com/user-attachments/assets/3b5cfa81-4e2c-42e4-b0a4-e18903179b48" />

# ⚡ RepoForge-AI

### Evidence-Driven Agentic AI for Repository Analysis, Optimization & Verification

> **RepoForge-AI** is an agentic AI engineering platform that autonomously analyzes software repositories, identifies engineering and performance issues, gathers evidence, proposes improvements, evaluates its own reasoning, and verifies the resulting analysis.

Instead of simply asking an LLM *"how can I improve this code?"*, RepoForge-AI follows a structured engineering workflow designed around **repository evidence, multi-agent reasoning, evaluation, and verification**.

---

## 🚀 What Does RepoForge-AI Do?

RepoForge-AI takes a GitHub repository and turns it into an **evidence-backed engineering analysis**.

### The system can:

🔍 **Inspect repositories**
Analyze repository structure, source files, functions, tests, and implementation patterns.

🧠 **Plan investigations**
Break an engineering problem into a sequence of research and analysis steps.

📊 **Detect engineering issues**
Identify patterns such as repeated operations, repeated function calls, and potential performance risks.

🔎 **Collect evidence**
Ground recommendations in concrete observations discovered inside the repository.

💡 **Generate solutions**
Produce engineering recommendations based on the observed evidence rather than generic advice.

🛡️ **Verify claims**
Evaluate whether the generated analysis is sufficiently supported by repository evidence.

🧪 **Run verification**
Execute available tests to determine whether the repository remains verifiable.

📄 **Generate engineering reports**
Combine the investigation, evidence, evaluation, proposed solution, and verification status into a structured final report.

---

# 🧠 Agentic Architecture

RepoForge-AI is designed as a **multi-agent workflow orchestrated with LangGraph**.

```text
                         ┌──────────────────────┐
                         │     GitHub Repo      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Planning Agent     │
                         │  Understand Problem  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Repository Agent     │
                         │ Inspect & Analyze    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Evidence Collection  │
                         │ Grounded Findings    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Solution Agent      │
                         │ Engineering Fixes    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Evaluator Agent    │
                         │ Claim Verification   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Verification Agent   │
                         │ Tests & Validation   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Final Report       │
                         │ Evidence + Solution  │
                         └──────────────────────┘
```

---

# 🤖 Multi-Agent System

RepoForge-AI separates responsibilities across specialized agents.

| Agent                        | Responsibility                            |
| ---------------------------- | ----------------------------------------- |
| 🧭 **Planner**               | Creates the investigation strategy        |
| 🔬 **Repository Agent**      | Inspects and analyzes repository contents |
| 🔎 **Evidence Agent**        | Collects concrete repository evidence     |
| ⚙️ **Optimizer**             | Identifies optimization opportunities     |
| 💡 **Solution Agent**        | Generates engineering recommendations     |
| 🧪 **Evaluator**             | Evaluates evidence and generated claims   |
| 🛡️ **Claim Verifier**       | Checks whether claims are supported       |
| ✅ **Optimization Validator** | Validates proposed optimization results   |

This separation allows RepoForge-AI to behave more like an **engineering investigation pipeline** than a single LLM prompt.

---

# 🔄 LangGraph Workflow

The workflow is orchestrated using **LangGraph**, allowing the system to maintain shared state while moving through multiple specialized stages.

```text
                    START
                      │
                      ▼
                 ┌─────────┐
                 │ Planner │
                 └────┬────┘
                      │
                      ▼
              ┌───────────────┐
              │ Repository    │
              │ Analysis      │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Evidence      │
              │ Collection    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Optimization  │
              │ Analysis      │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Solution      │
              │ Generation    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Claim         │
              │ Verification  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Test /        │
              │ Verification  │
              └───────┬───────┘
                      │
                      ▼
                    REPORT
```

---

# 🔬 Example Analysis

RepoForge-AI was tested against a real software repository and produced an evidence-backed engineering investigation.

### Repository analyzed

**Estate-Mind-AI**

### Repository scan

* 📁 **16 files discovered**
* 🔎 **33 engineering/performance findings**
* 🧪 **Verification tests passed**
* ✅ **Evaluation status: accepted**
* 📊 **Evaluation score: 1.00**

### Example findings

The system identified:

```text
HIGH
app.py
clean_text() is called inside a loop.

HIGH
app.py
safe_float() is called inside a loop.

HIGH
app.py
get_value() is called inside a loop.

HIGH
src/agents/market_research.py
tavily_search() is called inside a loop.
```

It also identified repeated operations throughout the investment-analysis pipeline, including calls to:

* `float()`
* `round()`
* `print()`
* `_safe_float()`
* `_normalize_score()`
* `calculate_scenario()`

The important part is that these findings were **derived from repository inspection**, rather than being invented as generic optimization suggestions.

---

# 🛡️ Evidence-First Engineering

One of the core ideas behind RepoForge-AI is:

> **An engineering recommendation should be grounded in observable evidence.**

The system therefore separates:

```text
Observation
     ↓
Evidence
     ↓
Root-Cause Candidate
     ↓
Proposed Solution
     ↓
Claim Evaluation
     ↓
Verification
```

This helps reduce the risk of an AI system producing confident recommendations that are not actually supported by the codebase.

---

# 📊 Self-Evaluation

RepoForge-AI includes an evaluation layer that examines the quality of the investigation.

Example evaluation:

```json
{
  "status": "accepted",
  "score": 1.0,
  "claim_score": 1.0,
  "reason": "Investigation contains sufficient verified repository evidence."
}
```

This creates an additional layer between:

**"The AI generated an answer"**

and

**"The AI generated an answer that passed an evaluation process."**

---

# 🧪 Verification

The project includes automated tests covering major components of the system.

Example verification result:

```text
1 passed in 0.81s
```

The system also explicitly distinguishes between:

### Static analysis

Repository inspection and code-pattern analysis.

### Runtime performance analysis

Actual runtime benchmarking when a supported benchmark target is available.

If a repository does not provide a supported runtime benchmark target, RepoForge-AI reports that limitation instead of pretending that runtime performance was measured.

---

# 🏗️ Project Structure

```text
RepoForge-AI/
│
├── app.py
├── run.py
│
├── app/
│   ├── checkout.py
│   ├── database.py
│   └── shipping.py
│
├── demo_target/
│   ├── app/
│   │   ├── checkout.py
│   │   ├── database.py
│   │   └── shipping.py
│   │
│   └── tests/
│       └── test_checkout.py
│
├── src/
│   │
│   ├── agents/
│   │   ├── planner.py
│   │   ├── repository_agent.py
│   │   ├── optimizer.py
│   │   ├── solution_agent.py
│   │   └── evaluator.py
│   │
│   ├── config/
│   │
│   ├── evaluation/
│   │   ├── claim_verifier.py
│   │   └── optimization_validator.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── workflow.py
│   │   └── optimization_loop.py
│   │
│   └── tools/
│       ├── repository.py
│       ├── scanner.py
│       ├── evidence.py
│       ├── performance.py
│       ├── comparator.py
│       └── verification.py
│
└── tests/
    ├── test_graph.py
    ├── test_optimizer.py
    ├── test_repository_agent.py
    ├── test_performance.py
    ├── test_verification.py
    └── ...
```

---

# ⚙️ Technology Stack

### 🤖 AI / Agentic AI

* **LangChain**
* **LangGraph**
* LLM-based agent reasoning
* Multi-agent orchestration
* Structured agent state
* Evidence-grounded generation

### 🧠 Engineering

* Python
* Static repository analysis
* Automated verification
* Claim evaluation
* Optimization analysis
* Test-driven validation

### 🖥️ Application

* Streamlit
* GitHub repository analysis
* Structured engineering reports

---

# 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/HamidKhanskt/RepoForge-AI.git
cd RepoForge-AI
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate it

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch the application

```bash
streamlit run app.py
```

The application should then be available at:

```text
http://localhost:8501
```

---

# 🧪 Running Tests

Run the complete test suite with:

```bash
pytest
```

Or run an individual test:

```bash
pytest test_graph.py
```

---

# 🎯 Why This Project?

Traditional code-analysis tools can identify patterns.

Traditional LLM applications can explain code.

RepoForge-AI combines these ideas into an **agentic engineering workflow**:

```text
Repository
    ↓
Understand
    ↓
Investigate
    ↓
Collect Evidence
    ↓
Reason
    ↓
Recommend
    ↓
Evaluate
    ↓
Verify
```

The goal is to move from:

> **AI-generated suggestions**

toward:

> **AI-assisted engineering investigations backed by repository evidence.**

---

# 🔮 Future Improvements

Planned directions include:

* ⚡ Runtime benchmarking
* 📈 Before/after performance comparison
* 🔧 Automated code patch generation
* 🔄 Patch → Test → Evaluate optimization loops
* 🧠 More specialized engineering agents
* 📊 Historical repository performance tracking
* 🔐 Security and dependency analysis
* 🧪 Regression testing after generated patches
* 🔍 Deeper AST-based code analysis
* 🐳 Dockerized deployment
* ☁️ Cloud deployment
* 📑 Richer engineering reports

---

# 📌 Current Limitations

RepoForge-AI currently focuses primarily on **repository inspection and evidence-driven recommendations**.

Runtime performance benchmarking depends on the target repository providing a supported benchmark target.

Therefore, the system distinguishes between:

```text
Static Repository Evidence
        ≠
Runtime Performance Measurements
```

This distinction is intentional and prevents unsupported performance claims.

---

# 💼 Engineering Skills Demonstrated

This project demonstrates practical experience with:

* 🧠 Agentic AI architecture
* 🔗 LangChain
* 🕸️ LangGraph
* 🤖 Multi-agent systems
* 🔍 Repository analysis
* 📊 Evidence-driven reasoning
* 🧪 Automated testing
* 🛡️ Claim verification
* ⚙️ Software optimization
* 🔄 Stateful workflows
* 📈 Performance analysis
* 🏗️ Modular Python architecture
* 📋 Structured engineering reports

---

# ⭐ Project Highlights

```text
                REPOFORGE-AI
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ANALYZE       REASON       VERIFY
        │            │            │
        ▼            ▼            ▼
   Repository     Agents       Tests
    Evidence     LangGraph   Evaluation
        │            │            │
        └────────────┼────────────┘
                     ▼
             ENGINEERING REPORT
```

---

## 👨‍💻 Author

**Hamid Khan**

Built as a portfolio project exploring **Agentic AI, LangChain, LangGraph, software engineering automation, and evidence-driven reasoning**.

---

## ⭐ If you find this project interesting

Feel free to explore the architecture, experiment with the agents, and use the project as a starting point for building more advanced agentic software-engineering systems.

**If you like the project, consider giving the repository a ⭐.**
