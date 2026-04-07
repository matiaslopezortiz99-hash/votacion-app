import { useState, useEffect, useCallback } from "react";

const IDEAS = [
  "Global Comercial Meeting 2026", "Communication Milestones & Events", "New campaing: From fiber to form", "Communication focus: Building our fututre tohether", "Idea 5",
  "Presentations: Global/By market/Mill", "Autmatization through IA: DataBase; Balnace scorecard,dashboard,reports", "Fiberplace: Onboarding material", "Idea 9", "Idea 10"
];

const COLORS = [
  "#FF6B35", "#F7C948", "#2EC4B6", "#E71D36", "#011627",
  "#9B5DE5", "#00F5D4", "#FEE440", "#F15BB5", "#00BBF9"
];

export default function VotacionApp() {
  const [votes, setVotes] = useState({});
  const [selected, setSelected] = useState(null);
  const [voted, setVoted] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(true);
  const [animatedWidths, setAnimatedWidths] = useState({});
  const [adminMode, setAdminMode] = useState(false);

  // Load votes from persistent storage
  const loadVotes = useCallback(async () => {
    try {
      const result = await window.storage.get("voting-data", true);
      if (result && result.value) {
        setVotes(JSON.parse(result.value));
      }
    } catch {
      setVotes({});
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadVotes();
    // Check if user already voted
    const checkVoted = async () => {
      try {
        const result = await window.storage.get("has-voted");
        if (result && result.value === "true") {
          setVoted(true);
          setShowResults(true);
        }
      } catch {}
    };
    checkVoted();
  }, [loadVotes]);

  // Animate bars when showing results
  useEffect(() => {
    if (showResults) {
      const totalVotes = Object.values(votes).reduce((a, b) => a + b, 0);
      if (totalVotes === 0) return;
      const timer = setTimeout(() => {
        const widths = {};
        IDEAS.forEach((idea) => {
          widths[idea] = ((votes[idea] || 0) / totalVotes) * 100;
        });
        setAnimatedWidths(widths);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [showResults, votes]);

  const handleVote = async () => {
    if (!selected || voted) return;
    const newVotes = { ...votes, [selected]: (votes[selected] || 0) + 1 };
    setVotes(newVotes);
    setVoted(true);
    setShowResults(true);
    try {
      await window.storage.set("voting-data", JSON.stringify(newVotes), true);
      await window.storage.set("has-voted", "true");
    } catch (e) {
      console.error("Error saving vote:", e);
    }
  };

  const handleReset = async () => {
    setVotes({});
    setVoted(false);
    setSelected(null);
    setShowResults(false);
    setAnimatedWidths({});
    try {
      await window.storage.set("voting-data", JSON.stringify({}), true);
      await window.storage.delete("has-voted");
    } catch {}
  };

  const totalVotes = Object.values(votes).reduce((a, b) => a + b, 0);

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loader}>
          <div style={styles.loaderDot} />
          <p style={styles.loaderText}>Cargando votación...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.headerIcon}>💡</div>
          <h1 style={styles.title}>Votación en Vivo</h1>
          <p style={styles.subtitle}>
            {voted
              ? `${totalVotes} voto${totalVotes !== 1 ? "s" : ""} registrado${totalVotes !== 1 ? "s" : ""}`
              : "Selecciona la idea que más te guste"}
          </p>
        </div>

        {/* Voting Section */}
        {!voted && (
          <div style={styles.optionsGrid}>
            {IDEAS.map((idea, i) => (
              <button
                key={idea}
                onClick={() => setSelected(idea)}
                style={{
                  ...styles.optionBtn,
                  borderColor: selected === idea ? COLORS[i] : "rgba(255,255,255,0.08)",
                  background: selected === idea
                    ? `linear-gradient(135deg, ${COLORS[i]}22, ${COLORS[i]}11)`
                    : "rgba(255,255,255,0.03)",
                  transform: selected === idea ? "scale(1.02)" : "scale(1)",
                  boxShadow: selected === idea
                    ? `0 0 20px ${COLORS[i]}33, inset 0 0 20px ${COLORS[i]}11`
                    : "none",
                }}
              >
                <span style={{
                  ...styles.optionNumber,
                  color: selected === idea ? COLORS[i] : "rgba(255,255,255,0.3)",
                }}>{i + 1}</span>
                <span style={{
                  ...styles.optionText,
                  color: selected === idea ? "#fff" : "rgba(255,255,255,0.6)",
                }}>{idea}</span>
                {selected === idea && (
                  <span style={{ ...styles.checkmark, color: COLORS[i] }}>✓</span>
                )}
              </button>
            ))}
          </div>
        )}

        {/* Vote Button */}
        {!voted && (
          <button
            onClick={handleVote}
            disabled={!selected}
            style={{
              ...styles.voteBtn,
              opacity: selected ? 1 : 0.4,
              cursor: selected ? "pointer" : "not-allowed",
              transform: selected ? "translateY(0)" : "translateY(2px)",
            }}
          >
            Enviar Voto
          </button>
        )}

        {/* Results Section */}
        {showResults && (
          <div style={styles.resultsSection}>
            <h2 style={styles.resultsTitle}>📊 Resultados</h2>
            {IDEAS.map((idea, i) => {
              const count = votes[idea] || 0;
              const pct = totalVotes > 0 ? ((count / totalVotes) * 100).toFixed(1) : 0;
              const barWidth = animatedWidths[idea] || 0;
              return (
                <div key={idea} style={styles.barRow}>
                  <div style={styles.barLabel}>
                    <span style={styles.barName}>{idea}</span>
                    <span style={styles.barCount}>{count} — {pct}%</span>
                  </div>
                  <div style={styles.barTrack}>
                    <div
                      style={{
                        ...styles.barFill,
                        width: `${barWidth}%`,
                        background: `linear-gradient(90deg, ${COLORS[i]}, ${COLORS[i]}cc)`,
                        boxShadow: `0 0 12px ${COLORS[i]}44`,
                      }}
                    />
                  </div>
                </div>
              );
            })}

            <div style={styles.actionsRow}>
              <button onClick={loadVotes} style={styles.refreshBtn}>
                🔄 Refrescar
              </button>
              <button
                onClick={() => setAdminMode(!adminMode)}
                style={styles.adminToggle}
              >
                ⚙️
              </button>
            </div>

            {adminMode && (
              <div style={styles.adminPanel}>
                <p style={styles.adminWarning}>⚠️ Zona de admin</p>
                <button onClick={handleReset} style={styles.resetBtn}>
                  Reiniciar toda la votación
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "linear-gradient(160deg, #0a0a0f 0%, #111128 40%, #0d1117 100%)",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    padding: "20px 16px",
    fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif",
  },
  card: {
    width: "100%",
    maxWidth: 520,
    background: "rgba(255,255,255,0.04)",
    borderRadius: 20,
    border: "1px solid rgba(255,255,255,0.08)",
    padding: "32px 24px",
    backdropFilter: "blur(20px)",
  },
  header: {
    textAlign: "center",
    marginBottom: 28,
  },
  headerIcon: {
    fontSize: 48,
    marginBottom: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: 700,
    color: "#fff",
    margin: "0 0 6px",
    letterSpacing: "-0.5px",
  },
  subtitle: {
    fontSize: 14,
    color: "rgba(255,255,255,0.45)",
    margin: 0,
  },
  optionsGrid: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
    marginBottom: 20,
  },
  optionBtn: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    padding: "14px 16px",
    borderRadius: 12,
    border: "1.5px solid",
    cursor: "pointer",
    transition: "all 0.2s ease",
    textAlign: "left",
    position: "relative",
  },
  optionNumber: {
    fontSize: 13,
    fontWeight: 700,
    minWidth: 22,
    transition: "color 0.2s",
  },
  optionText: {
    fontSize: 15,
    fontWeight: 500,
    flex: 1,
    transition: "color 0.2s",
  },
  checkmark: {
    fontSize: 18,
    fontWeight: 700,
  },
  voteBtn: {
    width: "100%",
    padding: "16px",
    borderRadius: 14,
    border: "none",
    background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
    color: "#fff",
    fontSize: 16,
    fontWeight: 700,
    cursor: "pointer",
    transition: "all 0.25s ease",
    letterSpacing: "0.3px",
  },
  resultsSection: {
    marginTop: 8,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 700,
    color: "#fff",
    marginBottom: 20,
    textAlign: "center",
  },
  barRow: {
    marginBottom: 14,
  },
  barLabel: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: 5,
  },
  barName: {
    fontSize: 13,
    fontWeight: 600,
    color: "rgba(255,255,255,0.75)",
  },
  barCount: {
    fontSize: 12,
    color: "rgba(255,255,255,0.4)",
    fontVariantNumeric: "tabular-nums",
  },
  barTrack: {
    height: 10,
    borderRadius: 6,
    background: "rgba(255,255,255,0.06)",
    overflow: "hidden",
  },
  barFill: {
    height: "100%",
    borderRadius: 6,
    transition: "width 0.8s cubic-bezier(0.22, 1, 0.36, 1)",
    minWidth: 0,
  },
  actionsRow: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
    marginTop: 24,
  },
  refreshBtn: {
    padding: "10px 24px",
    borderRadius: 10,
    border: "1px solid rgba(255,255,255,0.12)",
    background: "rgba(255,255,255,0.05)",
    color: "rgba(255,255,255,0.7)",
    fontSize: 14,
    cursor: "pointer",
    transition: "all 0.2s",
  },
  adminToggle: {
    padding: "10px 12px",
    borderRadius: 10,
    border: "1px solid rgba(255,255,255,0.08)",
    background: "transparent",
    fontSize: 16,
    cursor: "pointer",
    opacity: 0.4,
  },
  adminPanel: {
    marginTop: 16,
    padding: 16,
    borderRadius: 12,
    border: "1px solid rgba(255,80,80,0.2)",
    background: "rgba(255,50,50,0.05)",
    textAlign: "center",
  },
  adminWarning: {
    fontSize: 12,
    color: "rgba(255,100,100,0.7)",
    marginBottom: 12,
    marginTop: 0,
  },
  resetBtn: {
    padding: "10px 20px",
    borderRadius: 8,
    border: "1px solid rgba(255,80,80,0.3)",
    background: "rgba(255,50,50,0.15)",
    color: "#ff6b6b",
    fontSize: 13,
    fontWeight: 600,
    cursor: "pointer",
  },
  loader: {
    textAlign: "center",
    marginTop: 100,
  },
  loaderDot: {
    width: 40,
    height: 40,
    borderRadius: "50%",
    border: "3px solid rgba(255,255,255,0.1)",
    borderTopColor: "#6366f1",
    margin: "0 auto 16px",
    animation: "spin 1s linear infinite",
  },
  loaderText: {
    color: "rgba(255,255,255,0.4)",
    fontSize: 14,
  },
};
