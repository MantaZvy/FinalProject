import { useState, useEffect } from "react";
import api from "../api";

const USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

const SectionHeader = ({ title }) => (
  <div className="section-header">
    <h2 className="section-title">{title}</h2>
    <div className="section-line" />
  </div>
);

export default function Documents() {
  const [applications, setApplications] = useState([]);
  const [savedDocs, setSavedDocs] = useState([]);
  const [selectedAppId, setSelectedAppId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(null); // "resume" | "cover_letter" | null
  const [preview, setPreview] = useState(null); // { type, content }
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    api
      .get("/applications/")
      .then((res) => setApplications(res.data))
      .catch(() => {});
    fetchDocs();
  }, []);

  const fetchDocs = () => {
    api
      .get("/documents/")
      .then((res) => setSavedDocs(res.data))
      .catch(() => {});
  };

  // Resume upload
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    setError(null);
    setUploadSuccess(null);
    const formData = new FormData();
    formData.append("user_id", USER_ID);
    formData.append("file", file);
    try {
      await api.post("/nlp/resume/parse", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadSuccess(
        `"${file.name}" uploaded and parsed successfully. Your profile keywords have been updated.`
      );
      fetchDocs();
    } catch (e) {
      setError("Resume upload failed. Make sure your backend is running.");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  // Ensure we have an application_id to generate against
  const resolveApplicationId = async () => {
    // Option A: user picked an existing application
    if (selectedAppId) return selectedAppId;

    // Option B: user pasted a JD — create a temp job + application
    if (!jobDescription.trim()) return null;

    // Create a job description entry
    const jobRes = await api.post("/jobs/", {
      title: "Custom Job",
      company: "Custom",
      description: jobDescription,
      skills_required: [],
      keywords: [],
      source: "manual",
    });
    const jobId = jobRes.data.job_id;

    // Create a linked application
    const appRes = await api.post("/applications/", {
      user_id: USER_ID,
      job_id: jobId,
      job_title: "Custom Job",
      company: "Custom",
      status: "applied",
    });
    return appRes.data.application_id;
  };

  const handleGenerate = async (type) => {
    setError(null);
    setPreview(null);

    if (!selectedAppId && !jobDescription.trim()) {
      setError(
        "Please select an existing application or paste a job description before generating."
      );
      return;
    }

    setGenerating(type);
    try {
      const appId = await resolveApplicationId();
      if (!appId) {
        setError("Could not resolve an application to generate for.");
        return;
      }

      const endpoint =
        type === "resume"
          ? `/ai_generation/resume/${appId}`
          : `/ai_generation/cover-letter/${appId}`;

      const res = await api.post(endpoint);
      setPreview({ type, content: res.data.content, appId });
    } catch (e) {
      const detail = e.response?.data?.detail;
      setError(
        detail ||
          "Generation failed. Make sure your profile has skills and a resume uploaded."
      );
    } finally {
      setGenerating(null);
    }
  };

  const handleSave = async () => {
    if (!preview) return;
    setSaving(true);
    try {
      await api.post("/documents/", {
        user_id: USER_ID,
        doc_type: preview.type,
        content: { text: preview.content },
        file_path: `${preview.type}_${Date.now()}.txt`,
      });
      setSaveSuccess(true);
      fetchDocs();
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (e) {
      setError("Failed to save document.");
    } finally {
      setSaving(false);
    }
  };

  const handleDownload = (content, type) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${type}_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleViewDoc = (doc) => {
    const content =
      typeof doc.content === "string"
        ? doc.content
        : doc.content?.text || JSON.stringify(doc.content, null, 2);
    setPreview({ type: doc.doc_type, content, appId: null });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Documents</h1>
          <p className="page-subtitle">
            Upload your resume and generate tailored documents
          </p>
        </div>
      </div>

      {error && (
        <div className="error-banner" style={{ marginBottom: "1.5rem" }}>
          {error}
          <button
            className="tag-remove"
            style={{ marginLeft: "8px", fontSize: "13px" }}
            onClick={() => setError(null)}
          >
            ✕
          </button>
        </div>
      )}

      {uploadSuccess && <div className="success-banner">{uploadSuccess}</div>}

      {/* Upload section */}
      <section className="profile-section">
        <SectionHeader title="Upload Resume" />
        <p className="profile-hint" style={{ marginBottom: "1rem" }}>
          Upload your resume to extract skills and keywords. This improves AI
          document generation quality.
        </p>
        <label className={`upload-btn ${uploading ? "disabled" : ""}`}>
          {uploading ? (
            <>
              <span className="spinner" /> Parsing resume...
            </>
          ) : (
            <>
              <span>↑</span> {uploading ? "Uploading..." : "Choose Resume File"}
            </>
          )}
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleUpload}
            disabled={uploading}
            style={{ display: "none" }}
          />
        </label>
        <span className="profile-hint" style={{ marginLeft: "1rem" }}>
          PDF, DOCX or TXT
        </span>
      </section>

      {/* Generate section */}
      <section className="profile-section">
        <SectionHeader title="Generate New Document" />

        <div className="generate-grid">
          {/* Option A: pick existing application */}
          <div className="generate-option">
            <div className="option-label">
              <span className="option-badge">Option A</span>
              Select an existing application
            </div>
            <select
              className="doc-select"
              value={selectedAppId}
              onChange={(e) => {
                setSelectedAppId(e.target.value);
                setJobDescription("");
              }}
            >
              <option value="">— Choose application —</option>
              {applications.map((app) => (
                <option key={app.application_id} value={app.application_id}>
                  {app.job_title || "Untitled"} @ {app.company || "Unknown"} (
                  {app.status})
                </option>
              ))}
            </select>
          </div>

          <div className="generate-divider">
            <div className="divider-line" />
            <span className="divider-or">or</span>
            <div className="divider-line" />
          </div>

          {/* Option B: paste JD */}
          <div className="generate-option">
            <div className="option-label">
              <span className="option-badge">Option B</span>
              Paste a job description
            </div>
            <textarea
              className="jd-textarea"
              rows={6}
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value);
                setSelectedAppId("");
              }}
              placeholder="Paste the full job description here — required skills, responsibilities, etc. The AI will tailor your document to match the keywords for better ATS screening."
            />
          </div>
        </div>

        <div className="generate-actions">
          <button
            className="btn btn-primary"
            onClick={() => handleGenerate("resume")}
            disabled={!!generating}
          >
            {generating === "resume" ? (
              <>
                <span className="spinner" /> Generating...
              </>
            ) : (
              "◫ Generate Resume"
            )}
          </button>
          <button
            className="btn btn-ghost"
            onClick={() => handleGenerate("cover_letter")}
            disabled={!!generating}
          >
            {generating === "cover_letter" ? (
              <>
                <span className="spinner" /> Generating...
              </>
            ) : (
              "✉ Generate Cover Letter"
            )}
          </button>
        </div>
      </section>

      {/* Preview section */}
      {preview && (
        <section className="profile-section">
          <SectionHeader title="Document Preview" />
          <div className="preview-header">
            <span className="preview-type-badge">
              {preview.type === "resume" ? "Resume" : "Cover Letter"}
            </span>
            {saveSuccess && (
              <span className="sync-time" style={{ color: "#22c55e" }}>
                Saved successfully
              </span>
            )}
          </div>
          <div className="doc-preview">
            <pre className="preview-content">{preview.content}</pre>
          </div>
          <div className="preview-actions">
            <button
              className="btn btn-ghost"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? "Saving..." : "Save Document"}
            </button>
            <button
              className="btn btn-primary"
              onClick={() => handleDownload(preview.content, preview.type)}
            >
              ↓ Download
            </button>
          </div>
        </section>
      )}

      {/* Saved documents */}
      <section className="profile-section">
        <SectionHeader title="Saved Documents" />
        {savedDocs.length === 0 ? (
          <span className="profile-empty">
            No saved documents yet. Generate and save one above.
          </span>
        ) : (
          <table className="app-table">
            <thead>
              <tr>
                <th>File</th>
                <th>Type</th>
                <th>Date Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {savedDocs.map((doc) => (
                <tr key={doc.document_id} className="table-row">
                  <td className="td-company">{doc.file_path || "document"}</td>
                  <td>
                    <span
                      className="preview-type-badge"
                      style={{ fontSize: "11px" }}
                    >
                      {doc.doc_type === "resume"
                        ? "Resume"
                        : doc.doc_type === "cover_letter"
                          ? "Cover Letter"
                          : doc.doc_type}
                    </span>
                  </td>
                  <td className="td-muted">
                    {doc.created_at
                      ? new Date(doc.created_at).toLocaleDateString("en-GB", {
                          day: "2-digit",
                          month: "short",
                          year: "2-digit",
                        })
                      : "—"}
                  </td>
                  <td>
                    <div style={{ display: "flex", gap: "8px" }}>
                      <button
                        className="btn btn-ghost"
                        style={{ padding: "4px 12px", fontSize: "12px" }}
                        onClick={() => handleViewDoc(doc)}
                      >
                        View
                      </button>
                      <button
                        className="btn btn-ghost"
                        style={{ padding: "4px 12px", fontSize: "12px" }}
                        onClick={() => {
                          const content =
                            typeof doc.content === "string"
                              ? doc.content
                              : doc.content?.text ||
                                JSON.stringify(doc.content, null, 2);
                          handleDownload(content, doc.doc_type);
                        }}
                      >
                        ↓ Download
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
