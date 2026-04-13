import { useState, useEffect } from "react";
import api from "../api";

const USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

const STATUS_CONFIG = {
  applied: { color: "#9ca3af", label: "Applied" },
  awaiting: { color: "#3b82f6", label: "Awaiting Reply" },
  interview: { color: "#f59e0b", label: "Interview" },
  offer: { color: "#22c55e", label: "Offer" },
  rejected: { color: "#ef4444", label: "Rejected" },
  unknown: { color: "#6b7280", label: "Unknown" },
};

const StatusDot = ({ status }) => {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG.unknown;
  return (
    <span className="status-badge" style={{ "--dot-color": cfg.color }}>
      <span className="dot" />
      {cfg.label}
    </span>
  );
};

const StatCard = ({ label, value, accent }) => (
  <div className="stat-card" style={{ "--accent": accent }}>
    <span className="stat-value">{value}</span>
    <span className="stat-label">{label}</span>
  </div>
);

//analytics modal
function AnalyticsModal({ app, onClose }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [computing, setComputing] = useState(false);
  const [error, setError] = useState(null);
  const [showJdInput, setShowJdInput] = useState(false);
  const [jdText, setJdText] = useState("");
  const [updatingJd, setUpdatingJd] = useState(false);

  const fetchScore = async () => {
    setLoading(true);
    try {
      const res = await api.get("/match_scores/");
      const scores = res.data.filter(
        (s) => s.application_id === app.application_id
      );
      if (scores.length > 0) {
        // get most recent
        const latest = scores.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        )[0];
        setScore(latest);
      } else {
        setScore(null);
      }
    } catch (e) {
      setError("Failed to load analytics.");
    } finally {
      setLoading(false);
    }
  };

  const handleCompute = async () => {
    setComputing(true);
    setError(null);
    try {
      const res = await api.post(`/match_scores/compute/${app.application_id}`);
      setScore(res.data);
    } catch (e) {
      const detail = e.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : "Failed to compute. Make sure you have a resume uploaded and the application has a linked job."
      );
    } finally {
      setComputing(false);
    }
  };
  const handleUpdateJd = async () => {
    if (!jdText.trim()) return;
    setUpdatingJd(true);
    try {
      // fetch the application to get job_id
      const appRes = await api.get(`/applications/${app.application_id}`);
      const jobId = appRes.data.job_id;
      if (!jobId) {
        setError("No linked job found for this application.");
        return;
      }
      // update the job description
      await api.put(`/jobs/${jobId}`, {
        description: jdText,
        skills_required: [],
        keywords: [],
      });
      // recompute match score
      const res = await api.post(`/match_scores/compute/${app.application_id}`);
      setScore(res.data);
      setShowJdInput(false);
      setJdText("");
    } catch (e) {
      setError("Failed to update job description.");
    } finally {
      setUpdatingJd(false);
    }
  };

  useEffect(() => {
    fetchScore();
  }, []);

  const pct = score ? Math.round((score.similarity_score || 0) * 100) : 0;
  const barColor = pct >= 60 ? "#22c55e" : pct >= 30 ? "#f59e0b" : "#ef4444";

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal analytics-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <div>
            <h2>Predictive Analytics</h2>
            <p
              style={{
                fontSize: "13px",
                color: "var(--text-muted)",
                marginTop: "2px",
              }}
            >
              {app.job_title || "Untitled"} @ {app.company || "Unknown"}
            </p>
          </div>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {loading ? (
          <div className="empty-state" style={{ padding: "2rem" }}>
            Loading analytics...
          </div>
        ) : score ? (
          <div className="analytics-content">
            {/*match score bar*/}
            <div className="analytics-section">
              <div className="analytics-section-title">Resume Match Score</div>
              <div className="score-display">
                <span className="score-number" style={{ color: barColor }}>
                  {pct}%
                </span>
                <span className="score-model">
                  via {score.model_used || "hybrid_match"}
                </span>
              </div>
              <div className="score-bar-bg">
                <div
                  className="score-bar-fill"
                  style={{ width: `${pct}%`, background: barColor }}
                />
              </div>
              <div className="score-labels">
                <span>Low match</span>
                <span>Strong match</span>
              </div>
            </div>

            {/*matched skills*/}
            <div className="analytics-section">
              <div className="analytics-section-title">
                Matched Skills
                <span className="analytics-count matched-count">
                  {(score.matched_skills || []).length}
                </span>
              </div>
              <div className="tag-list-display">
                {(score.matched_skills || []).length > 0 ? (
                  (score.matched_skills || []).map((s, i) => (
                    <span key={i} className="skill-tag matched">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="profile-empty">
                    No matched skills found.
                  </span>
                )}
              </div>
            </div>

            {/*missing skills*/}
            <div className="analytics-section">
              <div className="analytics-section-title">
                Missing Skills
                <span className="analytics-count missing-count">
                  {(score.missing_skills || []).length}
                </span>
              </div>
              <div className="tag-list-display">
                {(score.missing_skills || []).length > 0 ? (
                  (score.missing_skills || []).map((s, i) => (
                    <span key={i} className="skill-tag missing">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="profile-empty">
                    No missing skills — great match!
                  </span>
                )}
              </div>
            </div>

            {/*explanations*/}
            {score.explanation && (
              <div className="analytics-section">
                <div className="analytics-section-title">Analysis</div>
                <p className="analytics-explanation">{score.explanation}</p>
              </div>
            )}

            {/*recs*/}
            {(score.recommendations || []).length > 0 && (
              <div className="analytics-section">
                <div className="analytics-section-title">Recommendations</div>
                <div className="recommendations-list">
                  {(score.recommendations || []).map((rec, i) => (
                    <div key={i} className="rec-card">
                      <div className="rec-header">
                        <span className="rec-skill">{rec.skill}</span>
                        <span className="rec-category">{rec.category}</span>
                      </div>
                      <p className="rec-text">{rec.recommendation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="analytics-section">
              <div className="analytics-section-title">Job Description</div>
              {!showJdInput ? (
                <button
                  className="btn btn-ghost"
                  style={{ fontSize: "12px" }}
                  onClick={() => setShowJdInput(true)}
                >
                  + Paste job description to improve score
                </button>
              ) : (
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "8px",
                  }}
                >
                  <textarea
                    className="jd-textarea"
                    rows={5}
                    value={jdText}
                    onChange={(e) => setJdText(e.target.value)}
                    placeholder="Paste the full job description here..."
                  />
                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      className="btn btn-ghost"
                      onClick={() => setShowJdInput(false)}
                    >
                      Cancel
                    </button>
                    <button
                      className="btn btn-primary"
                      onClick={handleUpdateJd}
                      disabled={updatingJd}
                    >
                      {updatingJd ? (
                        <>
                          <span className="spinner" /> Updating...
                        </>
                      ) : (
                        "Update & Recompute"
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
            <button
              className="btn btn-ghost"
              style={{ marginTop: "0.5rem", fontSize: "12px" }}
              onClick={handleCompute}
              disabled={computing}
            >
              {computing ? (
                <>
                  <span className="spinner" /> Recomputing...
                </>
              ) : (
                "↻ Recompute Score"
              )}
            </button>
          </div>
        ) : (
          <div className="analytics-empty">
            <p>No match score computed yet for this application.</p>
            <p className="profile-hint" style={{ marginTop: "6px" }}>
              Make sure you have a resume uploaded on the Documents page first.
            </p>
            <button
              className="btn btn-primary"
              style={{ marginTop: "1rem" }}
              onClick={handleCompute}
              disabled={computing}
            >
              {computing ? (
                <>
                  <span className="spinner" /> Computing...
                </>
              ) : (
                "◎ Compute Match Score"
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Applications() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [lastSync, setLastSync] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [analyticsApp, setAnalyticsApp] = useState(null);
  const [error, setError] = useState(null);

  const fetchApps = async () => {
    try {
      const res = await api.get("/applications/");
      setApps(
        res.data.filter(
          (a) => !(a.company === "Custom" && a.job_title === "Custom Job")
        )
      );
      setError(null);
    } catch (e) {
      setError("Failed to load applications. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleGmailSync = async () => {
    setSyncing(true);
    try {
      const res = await api.get(`/applications/sync-and-list/${USER_ID}`);
      setApps(
        res.data.filter(
          (a) => !(a.company === "Custom" && a.job_title === "Custom Job")
        )
      );
      setLastSync(new Date().toLocaleTimeString());
      setError(null);
    } catch (e) {
      setError("Gmail sync failed. Make sure the backend is running.");
    } finally {
      setSyncing(false);
    }
  };

  useEffect(() => {
    fetchApps();
  }, []);

  const counts = {
    total: apps.length,
    interview: apps.filter((a) => a.status === "interview").length,
    offer: apps.filter((a) => a.status === "offer").length,
    rejected: apps.filter((a) => a.status === "rejected").length,
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Applications</h1>
          <p className="page-subtitle">
            Track and manage your job applications
          </p>
        </div>
        <div className="header-actions">
          {lastSync && (
            <span className="sync-time">Last synced {lastSync}</span>
          )}
          <button
            className="btn btn-ghost"
            onClick={handleGmailSync}
            disabled={syncing}
          >
            {syncing ? (
              <>
                <span className="spinner" /> Syncing...
              </>
            ) : (
              <>✉ Import from Gmail</>
            )}
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setShowAddModal(true)}
          >
            + Add Application
          </button>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="stats-row">
        <StatCard label="Total" value={counts.total} accent="#a78bfa" />
        <StatCard
          label="Interviews"
          value={counts.interview}
          accent="#f59e0b"
        />
        <StatCard label="Offers" value={counts.offer} accent="#22c55e" />
        <StatCard label="Rejected" value={counts.rejected} accent="#ef4444" />
      </div>

      <div className="table-card">
        {loading ? (
          <div className="empty-state">Loading applications...</div>
        ) : apps.length === 0 ? (
          <div className="empty-state">
            <p>No applications yet.</p>
            <p className="empty-hint">
              Click "+ Add Application" or "Import from Gmail" to get started.
            </p>
          </div>
        ) : (
          <table className="app-table">
            <thead>
              <tr>
                <th>Company</th>
                <th>Role</th>
                <th>Date Applied</th>
                <th>Interview Date</th>
                <th>Status</th>
                <th>Meeting</th>
                <th>Analytics</th>
              </tr>
            </thead>
            <tbody>
              {apps.map((app) => (
                <tr key={app.application_id} className="table-row">
                  <td className="td-company">{app.company || "—"}</td>
                  <td>{app.job_title || "—"}</td>
                  <td className="td-muted">
                    {app.applied_date
                      ? new Date(app.applied_date).toLocaleDateString("en-GB", {
                          day: "2-digit",
                          month: "short",
                          year: "2-digit",
                        })
                      : "—"}
                  </td>
                  <td className="td-muted">
                    {app.interview_date
                      ? new Date(app.interview_date).toLocaleDateString(
                          "en-GB",
                          { day: "2-digit", month: "short", year: "2-digit" }
                        )
                      : "—"}
                  </td>
                  <td>
                    <StatusDot status={app.status} />
                  </td>
                  <td>
                    {app.meeting_link ? (
                      <a
                        href={app.meeting_link}
                        target="_blank"
                        rel="noreferrer"
                        className="meet-link"
                      >
                        Join ↗
                      </a>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td>
                    <button
                      className="analytics-btn"
                      onClick={() => setAnalyticsApp(app)}
                    >
                      ◎ View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="legend">
        <span className="legend-label">Status legend:</span>
        {Object.entries(STATUS_CONFIG)
          .filter(([k]) => k !== "unknown")
          .map(([key, cfg]) => (
            <span key={key} className="legend-item">
              <span className="legend-dot" style={{ background: cfg.color }} />
              {cfg.label}
            </span>
          ))}
      </div>

      {showAddModal && (
        <AddModal onClose={() => setShowAddModal(false)} onSaved={fetchApps} />
      )}

      {analyticsApp && (
        <AnalyticsModal
          app={analyticsApp}
          onClose={() => setAnalyticsApp(null)}
        />
      )}
    </div>
  );
}

function AddModal({ onClose, onSaved }) {
  const [form, setForm] = useState({
    company: "",
    job_title: "",
    status: "applied",
    applied_date: "",
    platform: "",
    salary_range: "",
    notes: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!form.company || !form.job_title) {
      setError("Company and role are required.");
      return;
    }
    setSaving(true);
    try {
      await api.post("/applications/", {
        ...form,
        user_id: USER_ID,
        job_id: null,
        platform: form.platform || null,
        salary_range: form.salary_range || null,
        notes: form.notes || null,
        applied_date: form.applied_date || null,
      });
      onSaved();
      onClose();
    } catch (e) {
      setError("Failed to save. Check all fields and try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add Application</h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        {error && <div className="error-banner">{error}</div>}
        <div className="form-group">
          <label>Company</label>
          <input
            value={form.company}
            onChange={(e) => setForm({ ...form, company: e.target.value })}
            placeholder="e.g. Google"
          />
        </div>
        <div className="form-group">
          <label>Role</label>
          <input
            value={form.job_title}
            onChange={(e) => setForm({ ...form, job_title: e.target.value })}
            placeholder="e.g. Backend Engineer"
          />
        </div>
        <div className="form-group">
          <label>Status</label>
          <select
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          >
            <option value="applied">Applied</option>
            <option value="interview">Interview</option>
            <option value="offer">Offer</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
        <div className="form-group">
          <label>Date Applied</label>
          <input
            type="date"
            value={form.applied_date}
            onChange={(e) => setForm({ ...form, applied_date: e.target.value })}
          />
        </div>
        <div className="modal-actions">
          <button className="btn btn-ghost" onClick={onClose}>
            Cancel
          </button>
          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={saving}
          >
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}
