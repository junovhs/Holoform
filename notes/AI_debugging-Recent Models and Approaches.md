AI-Assisted Debugging in Large Codebases: Recent Models and Approaches
Context-Aware Code Representations for Large Codebases
Modern research emphasizes token-efficient, context-aware code representations to handle codebases with hundreds of thousands of lines. Pretrained neural models for code increasingly incorporate structural context so that meaning is captured with fewer tokens:
Structural Code Embeddings: GraphCodeBERT (ICLR 2021) is a representative model that augments Transformer-based code embeddings with semantic structure (data-flow relations) instead of treating code as a flat sequence. By encoding “where-the-value-comes-from” data dependencies between variables, it captures code semantics in a compact form and improves downstream tasks like code search and code refinement
paperswithcode.com
paperswithcode.com
. Such structure-aware models leverage inherent code hierarchies (ASTs, control/data flow) to provide richer context than plain token sequences.
Code-Aware Transformers: More recent code models (e.g. CodeT5 or CodeX variants) also aim to handle long code by using pointer mechanisms, caching, or multi-span attention to focus on relevant parts of the code. These approaches maintain awareness of code boundaries (functions, classes) to avoid exceeding token limits. The general trend is to pretrain on large code corpora with tasks that preserve code semantics (e.g. identifier prediction, code-to-docstring alignment) so the embeddings are context-rich but token-efficient. Such embeddings can later be used for code search or fed into larger LLMs as expert knowledge without retraining
uwspace.uwaterloo.ca
uwspace.uwaterloo.ca
. In essence, they serve as building blocks that bridge the lexical gap between natural language queries and code by encoding code in a more semantic vector space.
Graph-Based and Dependency-Driven Analysis
Hybrid approaches that combine static or dynamic program analysis with neural reasoning have shown promise for pinpointing relevant code in complex systems. These methods build graph representations of codebases or execution data, enabling an AI to reason over dependencies and relationships:
Graph-Guided Code Localization: LocAgent (2025) introduces a graph-based framework to localize bug-relevant code given a natural language issue description
arxiv.org
. It parses the entire codebase into a heterogeneous graph of nodes (files, classes, functions) and edges (structural relations like imports, calls, inheritance). This lightweight representation captures the project’s architecture and dependency graph. An LLM-based agent can then perform multi-hop traversal over the graph to find code related to the query, rather than reading 400k lines sequentially. This yields efficient, focused search across components. LocAgent’s graph-guided reasoning significantly improved localization accuracy – reaching ~92% file-level precision on benchmarks – by enabling the model to hop between relevant modules and ignore unrelated code
arxiv.org
. The approach demonstrates how explicit code graphs help an AI navigate large codebases and find the likely culprit area for a bug.
Neuro-Symbolic Static Analysis: IRIS (ICLR 2025) is a neuro-symbolic vulnerability detection system that illustrates broader applications of graph analysis
openreview.net
. It uses a static analyzer to produce code property graphs (e.g. for taint flows) and then employs an LLM (GPT-4) to fill in specifications and interpret those graphs. By having the LLM infer missing rules (like what constitutes a sensitive sink) and examine cross-file paths, IRIS can perform whole-repository security reasoning that pure static tools miss
openreview.net
. Notably, IRIS found twice as many real vulnerabilities as CodeQL in a test suite by leveraging the combined power of formal analysis and LLM semantic understanding. This kind of static-analysis-plus-LLM approach could similarly be used for debugging – e.g. generating an explanatory trace of why a UI element is never rendered, based on code paths.
Dynamic Dependency Graphs: On the dynamic side, DepGraph (2024) uses graph neural networks for fault localization with causal signals from test execution
arxiv.org
. It builds a graph of program elements (e.g. AST nodes) annotated with runtime coverage data and historical change metrics. This GNN-based model, an evolution of the earlier Grace system, learns to rank suspicious code by propagating information from failing tests through the dependency graph. By integrating the inter-procedural call graph and even code revision history into the representation, DepGraph achieved more accurate fault localization (20% more bugs found in top-1 rank) while greatly reducing complexity and runtime
arxiv.org
. The use of execution traces and control/data flow links is essentially a form of causal inference – it helps identify the code whose execution correlates with the bug (e.g. lines executed only in failing scenarios). This shows the benefit of combining statistical debugging techniques (like coverage-based suspicion) with learned graph representations for scaling to large programs.
Hierarchical and Multi-Granularity Bug Localization
Instead of treating bug localization as a single-step mapping from a report to code, some recent work breaks the problem into multiple granularity levels – file, class, function, down to line – using specialized models or steps at each level. This hierarchical strategy reflects how human debuggers narrow down issues stepwise and provides a way to manage large code context in slices:
Multi-Level Localization via LLMs: BugCerberus (2023) exemplifies a hierarchical pipeline. It uses three coordinated LLM-based models to localize bugs at the file level, then function within that file, then specific statements
arxiv.org
. First, given a bug report and high-level context, a file-level model predicts the most relevant file(s). Next, a finer model takes the file’s content and the bug description to pinpoint the suspicious function or component. Finally, a statement-level model examines that function’s code to highlight the exact line or block causing the issue. Crucially, BugCerberus feeds each model with intermediate context gleaned from static analysis. For example, it analyzes program slices for the candidate functions and lines
arxiv.org
arxiv.org
. A program slicing tool (using a dependency graph via Joern) extracts the backward slice (what the code depends on) and forward slice (what the code affects) for a given statement, essentially the causal context of that line
arxiv.org
. By supplying these slices to the statement-level LLM, the model can “understand” the wider state and data conditions around a line, improving its judgment of bug relevance. This tiered approach, while involving custom model tuning at each stage, achieved state-of-the-art localization down to the line level, significantly boosting automated fix success rates when paired with a code repair tool
arxiv.org
. The hierarchical paradigm suggests that scoping the code progressively (from broad to narrow) can handle scale: each model only attends to a manageable chunk (e.g. one file or one function) at a time, yet the chain as a whole finds a needle in a 400k-line haystack.
Explainable Localization: An added benefit of multi-step frameworks is that they can provide natural explanations at each step. For instance, BugCerberus could potentially explain “File X is likely because the bug report’s component name appears there; Function Y in that file is suspicious because it controls the UI rendering; and specifically the check on line Z might hide the button.” In practice, recent research explicitly addresses explainability: BugLLM (2023), discussed below, not only retrieves code locations but also uses chain-of-thought prompting to generate explanations for why those files are relevant
uwspace.uwaterloo.ca
. Such explanations improve developer trust and help validate that the model’s reasoning is grounded in actual code logic (e.g. pointing out a missing UI update call). Hierarchical models lend themselves to this because each stage’s output can be accompanied by a rationale (even as simple as “narrowed down by keyword match, refined by data flow analysis”), aligning with the goal of transparent AI-assisted debugging.
Retrieval-Augmented Debugging and Semantic Search
Another major direction is using information retrieval and embedding-based search to cope with large codebases. These approaches treat the codebase as an external knowledge source to query, rather than something to feed entirely into an LLM context. By retrieving only the most relevant pieces of code for a given query or bug description, they achieve both scalability and context-awareness:
Semantic Code Search for Bug Localization: BugLLM (2023) proposes a zero-shot bug localization method that does not require model fine-tuning, instead leveraging pre-trained LLMs and a code vector database
uwspace.uwaterloo.ca
uwspace.uwaterloo.ca
. In an ingestion phase, the entire codebase is parsed into logical chunks (using an AST to split files into coherent units like classes or functions). Each chunk is embedded into a vector space (e.g. using OpenAI’s Ada-2 embedding model) and indexed in a similarity search engine
uwspace.uwaterloo.ca
. Then at inference time, the bug report is reformulated into a semantic query: an LLM is prompted to strip the user’s complaint down to technical keywords and concepts (filtering out unrelated narrative)
uwspace.uwaterloo.ca
. This refined query vector is used to retrieve the top-N most similar code chunks (potentially those mentioning the “button” component or related UI logic). Finally, another LLM step assesses each retrieved snippet in the context of the bug (“could this code cause the button to not show?”) to filter down to the most causally relevant ones
uwspace.uwaterloo.ca
. BugLLM demonstrated competitive accuracy (around 45–61% top-5 hit rate in locating the buggy file) compared to prior trained models, all while requiring no specialized training and scaling to large projects
uwspace.uwaterloo.ca
. This showcases the power of embedding-based RAG (Retrieval-Augmented Generation) for debugging: one can plug in a general-purpose LLM and augment it with a smart code search index, allowing it to handle big codebases by focusing only on pertinent slices.
Retrieval-Augmented Testing Assistants: Beyond direct bug report localization, retrieval is being used to assist debugging in interactive settings. For example, Copilot for Testing (2024) describes an AI assistant that continuously monitors a live codebase and retrieves context for an LLM during automated testing
arxiv.org
arxiv.org
. It maintains a graph-based index of code contexts (with nodes as code embeddings and edges linking related files or components). The embeddings are dynamically updated based on factors like file content semantics, the developer’s current cursor location, recent bug history, and code dependency metrics
arxiv.org
arxiv.org
. When a potential bug is detected (e.g. a test fails or a user query is issued), the system pulls the most relevant code fragments into the LLM’s prompt (such as the function under test, plus closely connected modules or recent edit areas). This context-aware prompt construction guides the LLM to generate focused analyses or fix suggestions, rather than guessing in the dark. Early results showed significant improvement in bug detection and critical test coverage by combining code retrieval with the generative abilities of LLMs
arxiv.org
arxiv.org
. The takeaway is that RAG architectures can keep an LLM “aware” of a large evolving codebase by feeding it just-in-time information – effectively giving it memory beyond its token limit. This is especially useful for pinpointing UI issues: if a test or query refers to a UI element, the retriever can surface the UI component’s definition and usage locations, helping the LLM zero in on the relevant part of the code.
UI-to-Code Mapping and Multimodal Debugging Strategies
When debugging issues that manifest in the user interface (e.g. “this button isn’t showing up”), the challenge is to connect high-level UI symptoms to the low-level code causing them. Recent research has started exploring multi-modal and domain-specific techniques that link natural language, visual UI elements, and code:
Mapping Bug Descriptions to GUI Actions: AstroBR (2025) tackles the problem of understanding and validating bug reproduction steps for mobile apps by combining language and UI analysis
arxiv.org
. It uses an LLM to parse a bug report and identify the described steps-to-reproduce (S2R) in the text. These steps (e.g. “Go to the Settings screen, click the search icon, type 'A'…”) are then mapped onto a GUI model of the app obtained via dynamic analysis (essentially a state graph of the app’s screens and possible user interactions). By aligning the natural language steps with actual UI components and actions in the app’s execution trace, the system can assess whether the report’s instructions are complete and correct. AstroBR improved S2R understanding by over 25% F1-score versus prior work
arxiv.org
, which means it more reliably links phrases like “search icon” or “Category screen” to the actual UI elements and states. Although focused on reproducing bugs, this approach highlights how bridging the UI-to-code gap (through a GUI state model) can aid debugging: once the AI knows which UI element and which action are involved, it can more directly find the underlying code (e.g. the event handler or UI layout file) responsible for that element’s behavior.
Domain-Specific Retrieval for UI Issues: Another example is BugRepro (2025), which integrates LLMs with domain knowledge for Android bug fixing. It employs a retrieval-augmented generation approach to fetch similar past bug reports and their solutions as guidance
arxiv.org
. In the context of a missing UI element, BugRepro’s retriever might pull up previous cases where a button failed to render, along with the known causes (perhaps a misconfigured XML layout or a conditional visibility flag). By providing these analogous examples to the LLM, the system can follow a proven sequence of actions to reproduce and diagnose the new bug. This method notably improved bug reproduction success rates (it managed to reproduce ~96 crashes versus 38 and 55 by previous methods)
arxiv.org
arxiv.org
. The key insight is that UI-related bugs often follow patterns (a button not showing might be due to similar reasons across apps), so a model that can recognize and retrieve those patterns can localize the fault more effectively. It’s a blend of case-based reasoning with modern AI: the LLM is not trained on a specific app, but it leverages a library of past UI bug cases to reason about the new one.
Component Graphs and Causal Tracing: Emerging research also points toward using component dependency graphs that include UI elements. For instance, in a web app, one could build a graph linking front-end components (buttons, dialogs) to the backend code that populates or toggles them. An AI agent could then traverse this graph when a UI issue is reported – e.g. starting from the “SubmitButton” UI component node, following edges to the React component or template that renders it, and further to the business logic that decides its visibility. By doing so, the agent identifies the causal chain from user interface to underlying code. While we are just seeing early forays in this direction, it aligns with techniques like program slicing and causal analysis applied to UI events. We already see components of this in the above systems: LocAgent’s heterogeneous graph could naturally include GUI elements as first-class nodes, and BugCerberus’s slicing can trace data flow that might explain why a UI field remains empty. We anticipate more hybrid models that integrate GUI structure (view hierarchies, user event flows) with code analysis, allowing AI debuggers to not only find the offending code module but also explain it in terms of UI behavior (“the button is never set to visible because the code in module X never gets the event from screen Y”). This area sits at the intersection of software engineering and explainable AI, aiming to make the AI’s reasoning understandable in the same way a human developer connects an interface symptom to a code fix.
References (Selected)
Niu et al. “When Deep Learning Meets IR-Based Bug Localization: A Survey.” ACM CSUR (2025) – Comprehensive survey of 61 studies on deep learning for bug localization, highlighting use of code semantics and LLMs
arxiv.org
arxiv.org
.
Chen et al. “LocAgent: Graph-Guided LLM Agents for Code Localization.” ArXiv preprint (2025) – Proposes graph-of-code representation (files, classes, functions with dependencies) to enable multi-hop reasoning in LLMs for pinpointing relevant code from issue descriptions
arxiv.org
arxiv.org
.
Chang et al. “BugCerberus: Hierarchical Localization Framework Leveraging LLMs.” ArXiv preprint (2023) – Introduces multi-level bug localization (file/function/statement) with specialized LLMs at each level and uses program dependency slicing to provide context to fine-grained models
arxiv.org
arxiv.org
.
Sutskever et al. “BugLLM: Explainable Bug Localization through LLMs.” Master’s Thesis (2023) – Presents a zero-shot method using AST-guided code chunk indexing and semantic search. Demonstrates competitive accuracy without training, and generates chain-of-thought explanations for retrieved code locations
uwspace.uwaterloo.ca
uwspace.uwaterloo.ca
.
Rafi et al. “Towards Better GNN-based Fault Localization through Enhanced Code Representation.” ArXiv preprint (2024) – Proposes DepGraph, a graph representation integrating call graphs and code change history, used with GNNs. Achieves state-of-the-art accuracy in fault localization with improved scalability over prior AST-based graphs
arxiv.org
.
Wang et al. “AI Copilot with Context-Based RAG for Testing.” ArXiv preprint (2024) – Describes a retrieval-augmented LLM system that constructs graph-based code embeddings (incorporating file paths, code content, bug frequency, etc.) to supply relevant context to an LLM during automated testing
arxiv.org
arxiv.org
.
Li et al. “IRIS: LLM-Assisted Static Analysis for Security Vulnerabilities.” ICLR (2025) – Demonstrates a neuro-symbolic approach combining GPT-4 with static analysis graphs for whole-repo reasoning. LLM infers missing specs and checks flows, doubling the detected vulnerabilities vs. a standard tool
openreview.net
.
Mahmud et al. “AstroBR: Assessing Bug Reproduction Steps via Language and UI Analysis.” ArXiv preprint (2025) – Leverages LLMs to parse bug reports and map steps-to-reproduce onto GUI interactions obtained from dynamic analysis. Improves identification of missing or unclear reproduction steps by linking natural language to program state models
arxiv.org
.
Yin et al. “BugRepro: Enhancing Android Bug Reproduction with Domain-Specific Knowledge.” ArXiv preprint (2025) – Uses retrieval of similar past bug reports (with known Steps-to-Reproduce) to guide an LLM agent in reproducing new bugs. Integrates domain knowledge of mobile UI patterns to achieve higher success in replaying crashes
arxiv.org
arxiv.org
.
Guo et al. “GraphCodeBERT: Pre-training Code Representations with Data Flow.” ICLR (2021) – Early work on incorporating code structure into neural models. Uses a data-flow graph to inform attention during pre-training, yielding better code understanding and search performance than sequence-only models
paperswithcode.com
paperswithcode.com