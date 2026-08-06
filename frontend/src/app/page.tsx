import { SystemStatus } from "@/components/system-status";

const setupCards = [
  {
    number: "01",
    status: "Ready",
    title: "Next.js Frontend",
    description:
      "A typed App Router foundation with responsive styling, environment validation, and component tests.",
  },
  {
    number: "02",
    status: "Ready",
    title: "FastAPI Backend",
    description:
      "A typed Python API foundation with health and readiness endpoints for local development.",
  },
  {
    number: "03",
    status: "Planned",
    title: "Future RAG Pipeline",
    description:
      "Grounded retrieval, citations, orchestration, and model integration remain reserved for a later phase.",
  },
] as const;

const futureStack = ["LangChain", "LangGraph", "Groq", "Supabase", "pgvector"] as const;

export default function Home() {
  return (
    <main className="site-shell">
      <header className="site-header">
        <div className="page-container header-inner">
          <div className="brand-lockup" aria-label="TaskFlow AI Assistant">
            <span className="brand-mark" aria-hidden="true">
              TF
            </span>
            <span className="brand-name">TaskFlow AI Assistant</span>
          </div>
          <span className="fictional-label">Fictional demonstration SaaS product</span>
        </div>
      </header>

      <div className="page-container page-content">
        <section className="hero" aria-labelledby="page-heading">
          <div className="hero-copy">
            <div className="phase-badge" aria-label="Current project phase: Phase 2">
              <span className="phase-dot" aria-hidden="true" />
              Phase 2 · Project foundation
            </div>
            <h1 id="page-heading">Customer Support Knowledge Assistant</h1>
            <p className="hero-description">
              The project foundation is ready for local development. The typed Next.js frontend can
              now verify its connection to the FastAPI backend while future assistant capabilities
              remain intentionally out of scope.
            </p>
          </div>

          <SystemStatus />
        </section>

        <section className="setup-section" aria-labelledby="setup-heading">
          <div className="section-heading-row">
            <div>
              <p className="section-kicker">Foundation overview</p>
              <h2 id="setup-heading">Core setup</h2>
            </div>
            <p className="section-summary">A stable base before retrieval and generation begin.</p>
          </div>

          <div className="setup-grid">
            {setupCards.map((card) => (
              <article className="setup-card" key={card.title}>
                <div className="card-topline">
                  <span className="card-number">{card.number}</span>
                  <span className={card.status === "Ready" ? "card-status ready" : "card-status"}>
                    {card.status}
                  </span>
                </div>
                <h3>{card.title}</h3>
                <p>{card.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="future-section" aria-labelledby="future-heading">
          <div className="future-copy">
            <p className="section-kicker">Future stack</p>
            <h2 id="future-heading">Prepared for the next layers</h2>
            <p>
              The foundation keeps clean boundaries for the tools planned in the product brief,
              without initializing or calling them during Phase 2.
            </p>
          </div>
          <ul className="stack-list" aria-label="Planned future technology stack">
            {futureStack.map((technology) => (
              <li key={technology}>{technology}</li>
            ))}
          </ul>
        </section>

        <aside className="scope-note" aria-label="Current implementation scope">
          <span className="scope-icon" aria-hidden="true">
            i
          </span>
          <p>
            <strong>The RAG workflow is not implemented yet.</strong> This screen verifies only the
            Phase 2 application foundation and local API connection.
          </p>
        </aside>
      </div>
    </main>
  );
}
