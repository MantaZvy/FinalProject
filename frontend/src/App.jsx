import { useState } from "react";
import {
  BrowserRouter as Route,
  NavLink,
  BrowserRouter,
  Routes,
} from "react-router-dom";
import Applications from "./pages/Applications";
import Profile from "./pages/Profile";
import Documents from "./pages/Documents";
import React from "react";
import "./App.css";

const USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

const Sidebar = () => (
  <aside className="sidebar">
    <div className="sidebar-brand">
      <span className="brand-icon">◈</span>
      <span className="brand-name">ApplyAI</span>
    </div>
    <nav className="sidebar-nav">
      <NavLink
        to="/"
        end
        className={({ isActive }) =>
          isActive ? "nav-item active" : "nav-item"
        }
      >
        <span className="nav-icon">⊞</span> Applications
      </NavLink>
      <NavLink
        to="/profile"
        end
        className={({ isActive }) =>
          isActive ? "nav-item active" : "nav-item"
        }
      >
        <span className="nav-icon">◎</span> Profile
      </NavLink>
      <NavLink
        to="/documents"
        end
        className={({ isActive }) =>
          isActive ? "nav-item active" : "nav-item"
        }
      >
        <span className="nav-icon">▣</span> Documents
      </NavLink>
    </nav>
    <div className="sidebar-footer">
      <div className="user-pill">
        <div className="user-avatar">S</div>
        <span className="user-label">Manta Z.</span>
      </div>
    </div>
  </aside>
);

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Applications userId={USER_ID} />} />
            <Route path="/profile" element={<Profile userId={USER_ID} />} />
            <Route path="/documents" element={<Documents userId={USER_ID} />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
