import { useState, useEffect } from "react";
import api from "../api";

const USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

const SectionHeader = ({ title }) => (
  <div className="section-header">
    <h2 className="section-title">{title}</h2>
    <div className="section-line" />
  </div>
);

const Tag = ({ label, onRemove }) => (
  <span className="tag">
    {label}
    {onRemove && (
      <button className="tag-remove" onClick={onRemove}>
        ✕
      </button>
    )}
  </span>
);

const TagInput = ({ tags, onChange, placeholder }) => {
  const [input, setInput] = useState("");

  const handleKeyDown = (e) => {
    if ((e.key === "Enter" || e.key === ",") && input.trim()) {
      e.preventDefault();
      if (!tags.includes(input.trim())) {
        onChange([...tags, input.trim()]);
      }
      setInput("");
    }
  };

  const removeTag = (index) => {
    onChange(tags.filter((_, i) => i !== index));
  };

  return (
    <div className="tag-input-box">
      <div className="tag-list">
        {tags.map((tag, i) => (
          <Tag key={i} label={tag} onRemove={() => removeTag(i)} />
        ))}
        <input
          className="tag-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={tags.length === 0 ? placeholder : "Add more..."}
        />
      </div>
    </div>
  );
};

const EntryCard = ({ entry, fields, onRemove }) => (
  <div className="entry-card">
    <div className="entry-card-header">
      <div>
        <span className="entry-title">
          {entry.role || entry.degree || "Untitled"}
        </span>
        {(entry.company || entry.institution) && (
          <span className="entry-subtitle">
            {" "}
            — {entry.company || entry.institution}
          </span>
        )}
      </div>
      <button className="tag-remove entry-remove" onClick={onRemove}>
        ✕
      </button>
    </div>
    {entry.years && <span className="entry-years">{entry.years}</span>}
    {entry.description && <p className="entry-desc">{entry.description}</p>}
  </div>
);

const EntryForm = ({ fields, onAdd, onCancel }) => {
  const [form, setForm] = useState(
    Object.fromEntries(fields.map((f) => [f.key, ""]))
  );

  const handleAdd = () => {
    const primary = fields[0].key;
    if (!form[primary].trim()) return;
    onAdd(form);
  };

  return (
    <div className="entry-form">
      {fields.map((f) => (
        <div className="form-group" key={f.key}>
          <label>{f.label}</label>
          {f.type === "textarea" ? (
            <textarea
              rows={3}
              value={form[f.key]}
              onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
              placeholder={f.placeholder}
            />
          ) : (
            <input
              value={form[f.key]}
              onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
              placeholder={f.placeholder}
            />
          )}
        </div>
      ))}
      <div className="entry-form-actions">
        <button className="btn btn-ghost" onClick={onCancel}>
          Cancel
        </button>
        <button className="btn btn-primary" onClick={handleAdd}>
          Add
        </button>
      </div>
    </div>
  );
};

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const [summary, setSummary] = useState("");
  const [skills, setSkills] = useState([]);
  const [certifications, setCertifications] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [education, setEducation] = useState([]);
  const [experience, setExperience] = useState([]);

  const [showEduForm, setShowEduForm] = useState(false);
  const [showExpForm, setShowExpForm] = useState(false);

  useEffect(() => {
    api
      .get(`/job_seekers/${USER_ID}`)
      .then((res) => {
        const d = res.data;
        setProfile(d);
        setSummary(d.profile_summary || "");
        setSkills(d.skills || []);
        setCertifications(d.certifications || []);
        setKeywords(d.keywords || []);
        setEducation(d.education?.education || []);
        setExperience(d.experience?.experience || []);
      })
      .catch(() => setError("Could not load profile. Is the backend running?"))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      await api.put(`/job_seekers/${USER_ID}`, {
        profile_summary: summary,
        skills,
        certifications,
        keywords,
        education: { education },
        experience: { experience },
      });
      setSuccess(true);
      setEditing(false);
      setTimeout(() => setSuccess(false), 3000);
    } catch (e) {
      setError("Failed to save profile.");
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (profile) {
      setSummary(profile.profile_summary || "");
      setSkills(profile.skills || []);
      setCertifications(profile.certifications || []);
      setKeywords(profile.keywords || []);
      setEducation(profile.education?.education || []);
      setExperience(profile.experience?.experience || []);
    }
    setEditing(false);
  };

  if (loading)
    return (
      <div className="page">
        <div className="empty-state">Loading profile...</div>
      </div>
    );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Profile</h1>
          <p className="page-subtitle">Your professional career data</p>
        </div>
        <div className="header-actions">
          {success && (
            <span className="sync-time" style={{ color: "#22c55e" }}>
              Saved successfully
            </span>
          )}
          {editing ? (
            <>
              <button className="btn btn-ghost" onClick={handleCancel}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? "Saving..." : "Save Profile"}
              </button>
            </>
          ) : (
            <button className="btn btn-ghost" onClick={() => setEditing(true)}>
              Edit Profile
            </button>
          )}
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="profile-sections">
        {/* Career Summary */}
        <section className="profile-section">
          <SectionHeader title="Career Summary" />
          {editing ? (
            <div className="form-group">
              <label>Short description of your career goals or summary</label>
              <textarea
                rows={4}
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="e.g. Final year Computer Science student with experience in backend development..."
              />
            </div>
          ) : (
            <p className="profile-text">
              {summary || (
                <span className="profile-empty">No summary added yet.</span>
              )}
            </p>
          )}
        </section>

        {/* Skills */}
        <section className="profile-section">
          <SectionHeader title="Skills" />
          {editing ? (
            <div className="form-group">
              <label>Press Enter or comma to add a skill</label>
              <TagInput
                tags={skills}
                onChange={setSkills}
                placeholder="e.g. Python, FastAPI, React..."
              />
            </div>
          ) : (
            <div className="tag-list-display">
              {skills.length > 0 ? (
                skills.map((s, i) => <Tag key={i} label={s} />)
              ) : (
                <span className="profile-empty">No skills added yet.</span>
              )}
            </div>
          )}
        </section>

        {/* Certifications */}
        <section className="profile-section">
          <SectionHeader title="Certifications" />
          {editing ? (
            <div className="form-group">
              <label>Press Enter or comma to add a certification</label>
              <TagInput
                tags={certifications}
                onChange={setCertifications}
                placeholder="e.g. AWS Certified, Google Cloud..."
              />
            </div>
          ) : (
            <div className="tag-list-display">
              {certifications.length > 0 ? (
                certifications.map((c, i) => <Tag key={i} label={c} />)
              ) : (
                <span className="profile-empty">
                  No certifications added yet.
                </span>
              )}
            </div>
          )}
        </section>

        {/* Keywords */}
        <section className="profile-section">
          <SectionHeader title="Keywords" />
          <p className="profile-hint">
            These are extracted automatically when you upload a resume via the
            Documents page.
          </p>
          <div className="tag-list-display" style={{ marginTop: "0.75rem" }}>
            {keywords.length > 0 ? (
              keywords.map((k, i) => <Tag key={i} label={k} />)
            ) : (
              <span className="profile-empty">
                No keywords yet. Upload a resume to auto-extract them.
              </span>
            )}
          </div>
        </section>

        {/* Education */}
        <section className="profile-section">
          <SectionHeader title="Education" />
          <div className="entries-list">
            {education.map((entry, i) => (
              <EntryCard
                key={i}
                entry={entry}
                onRemove={
                  editing
                    ? () => setEducation(education.filter((_, j) => j !== i))
                    : null
                }
              />
            ))}
            {education.length === 0 && !showEduForm && (
              <span className="profile-empty">No education entries yet.</span>
            )}
          </div>
          {editing && !showEduForm && (
            <button
              className="btn btn-ghost add-entry-btn"
              onClick={() => setShowEduForm(true)}
            >
              + Add Education
            </button>
          )}
          {showEduForm && (
            <EntryForm
              fields={[
                {
                  key: "degree",
                  label: "Degree",
                  placeholder: "e.g. BSc Computer Science",
                },
                {
                  key: "institution",
                  label: "Institution",
                  placeholder: "e.g. University of London",
                },
                {
                  key: "years",
                  label: "Years",
                  placeholder: "e.g. 2022 – 2026",
                },
                {
                  key: "description",
                  label: "Description",
                  placeholder: "Relevant modules, achievements...",
                  type: "textarea",
                },
              ]}
              onAdd={(entry) => {
                setEducation([...education, entry]);
                setShowEduForm(false);
              }}
              onCancel={() => setShowEduForm(false)}
            />
          )}
        </section>

        {/* Experience */}
        <section className="profile-section">
          <SectionHeader title="Experience" />
          <div className="entries-list">
            {experience.map((entry, i) => (
              <EntryCard
                key={i}
                entry={entry}
                onRemove={
                  editing
                    ? () => setExperience(experience.filter((_, j) => j !== i))
                    : null
                }
              />
            ))}
            {experience.length === 0 && !showExpForm && (
              <span className="profile-empty">No experience entries yet.</span>
            )}
          </div>
          {editing && !showExpForm && (
            <button
              className="btn btn-ghost add-entry-btn"
              onClick={() => setShowExpForm(true)}
            >
              + Add Experience
            </button>
          )}
          {showExpForm && (
            <EntryForm
              fields={[
                {
                  key: "role",
                  label: "Role",
                  placeholder: "e.g. Backend Developer",
                },
                {
                  key: "company",
                  label: "Company",
                  placeholder: "e.g. Tech Corp",
                },
                {
                  key: "years",
                  label: "Years",
                  placeholder: "e.g. 2024 – Present",
                },
                {
                  key: "description",
                  label: "Description",
                  placeholder: "Key responsibilities and achievements...",
                  type: "textarea",
                },
              ]}
              onAdd={(entry) => {
                setExperience([...experience, entry]);
                setShowExpForm(false);
              }}
              onCancel={() => setShowExpForm(false)}
            />
          )}
        </section>
      </div>
    </div>
  );
}
