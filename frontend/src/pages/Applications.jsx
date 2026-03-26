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

export default function Applications() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [lastSync, setLastSync] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
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
    </div>
  );
}

function AddModal({ onClose, onSaved }) {
  const [form, setForm] = useState({
    company: "",
    job_title: "",
    status: "applied",
    applied_date: "",
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
