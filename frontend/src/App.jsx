import { useState } from "react";
import { BrowserRouter, Route, NavLink, Routes } from "react-router-dom";
import Applications from "./pages/Applications";
import Profile from "./pages/Profile";
import Documents from "./pages/Documents";
import React from "react";
import "./App.css";

const USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

const Navbar = () => (
  <nav className="navbar">
    <div className="navbar-inner">
      <div className="navbar-brand">
        <span className="brand-icon">◈</span>
        <span className="brand-name">ApplyAI</span>
      </div>
      <div className="navbar-links">
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
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <span className="nav-icon">◎</span> Profile
        </NavLink>
        <NavLink
          to="/documents"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <span className="nav-icon">◫</span> Documents
        </NavLink>
      </div>
      <div className="navbar-user">
        <div className="user-avatar">U</div>
        <span className="user-label">User</span>
      </div>
    </div>
  </nav>
);

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar />
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
