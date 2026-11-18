"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import "./dashboard.css";

import { API_BASE } from "../../lib/api";

type Project = {
  id: number;
  title: string;
  address?: string;
  description?: string;
  main_image?: string | null;
  is_for_sale?: boolean;
  created_at?: string;
};

type SiteSection = {
  id: number;
  key: string;
  title: string;
  subtitle?: string;
  content?: string;
  image?: string | null;
  updated_at?: string;
};

type Tab = "overview" | "projects" | "content";

function unwrap<T,>(value: unknown): T[] {
  if (Array.isArray(value)) return value as T[];
  if (value && typeof value === "object" && "results" in value) {
    const results = (value as { results?: unknown }).results;
    return Array.isArray(results) ? (results as T[]) : [];
  }
  return [];
}

function imageUrl(path?: string | null) {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${API_BASE}/${path.replace(/^\/+/, "")}`;
}

const sectionNames: Record<string, string> = {
  about: "درباره ما",
  community: "جامعه و مسئولیت",
  services: "خدمات",
  approach: "رویکرد ما",
};

export default function DashboardPage() {
  const [tab, setTab] = useState<Tab>("overview");
  const [projects, setProjects] = useState<Project[]>([]);
  const [sections, setSections] = useState<SiteSection[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function loadDashboard() {
      setLoading(true);
      setError("");
      try {
        const [projectResponse, sectionResponse] = await Promise.all([
          fetch(`${API_BASE}/api/projects/projects/`, { cache: "no-store" }),
          fetch(`${API_BASE}/api/pages/sections/`, { cache: "no-store" }),
        ]);
        if (!projectResponse.ok || !sectionResponse.ok) {
          throw new Error("دریافت اطلاعات از سرور با مشکل روبه‌رو شد.");
        }
        const [projectData, sectionData] = await Promise.all([
          projectResponse.json(),
          sectionResponse.json(),
        ]);
        if (!active) return;
        setProjects(unwrap<Project>(projectData));
        setSections(unwrap<SiteSection>(sectionData));
      } catch {
        if (active) setError("ارتباط با سرور برقرار نشد. مطمئن شو بک‌اند جنگو در حال اجراست.");
      } finally {
        if (active) setLoading(false);
      }
    }
    loadDashboard();
    return () => { active = false; };
  }, []);

  const filteredProjects = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("fa");
    if (!query) return projects;
    return projects.filter((project) =>
      [project.title, project.address].some((value) =>
        (value || "").toLocaleLowerCase("fa").includes(query)
      )
    );
  }, [projects, search]);

  const forSaleCount = projects.filter((project) => project.is_for_sale).length;

  return (
    <main className="bartar-dashboard" dir="rtl">
      <aside className="dashboard-sidebar">
        <Link href="/" className="dashboard-brand" aria-label="بازگشت به سایت برتر">
          <span className="brand-symbol">ب</span>
          <span><strong>بَرتر</strong><small>گروه ساختمانی</small></span>
        </Link>

        <div className="sidebar-caption">مدیریت مجموعه</div>
        <nav className="dashboard-nav" aria-label="منوی مدیریت">
          <button className={tab === "overview" ? "active" : ""} onClick={() => setTab("overview")}>
            <span className="nav-icon">▦</span><span>نمای کلی</span>
          </button>
          <button className={tab === "projects" ? "active" : ""} onClick={() => setTab("projects")}>
            <span className="nav-icon">▤</span><span>پروژه‌ها</span><em>{projects.length}</em>
          </button>
          <button className={tab === "content" ? "active" : ""} onClick={() => setTab("content")}>
            <span className="nav-icon">▧</span><span>محتوای سایت</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-status"><span /> اتصال به پنل اطلاعات</div>
          <a href={`${API_BASE}/admin/`} target="_blank" rel="noreferrer" className="django-link">
            مدیریت اصلی جنگو <span>↗</span>
          </a>
          <Link href="/" className="back-to-site">مشاهده وب‌سایت <span>←</span></Link>
        </div>
      </aside>

      <section className="dashboard-main">
        <header className="dashboard-topbar">
          <div className="breadcrumb"><span>برتر</span><b>/</b><strong>پنل مدیریت</strong></div>
          <div className="topbar-right">
            <span className="topbar-date">داشبورد مدیریتی</span>
            <div className="profile-chip"><span className="profile-avatar">ب</span><span><b>مدیریت برتر</b><small>پنل مجموعه</small></span></div>
          </div>
        </header>

        <div className="dashboard-content">
          <div className="welcome-row">
            <div>
              <div className="eyebrow"><span /> پنل اختصاصی گروه ساختمانی برتر</div>
              <h1>{tab === "projects" ? "مدیریت پروژه‌ها" : tab === "content" ? "مدیریت محتوای سایت" : "نمای کلی مجموعه"}</h1>
              <p>نمایی یکپارچه از پروژه‌ها و محتوای وب‌سایت برتر</p>
            </div>
            <a className="outline-action" href="/" target="_blank" rel="noreferrer">مشاهده وب‌سایت <span>↗</span></a>
          </div>

          {error && <div className="dashboard-alert">{error}</div>}

          {tab === "overview" && (
            <>
              <div className="stats-grid">
                <article className="stat-card stat-primary"><div className="stat-top"><span>پروژه‌های ثبت‌شده</span><i>▤</i></div><strong>{loading ? "—" : projects.length.toLocaleString("fa-IR")}</strong><small>مجموع پروژه‌های موجود در سامانه</small><div className="stat-decoration">01</div></article>
                <article className="stat-card"><div className="stat-top"><span>پروژه‌های قابل فروش</span><i>⌂</i></div><strong>{loading ? "—" : forSaleCount.toLocaleString("fa-IR")}</strong><small>پروژه‌هایی که برای فروش علامت‌گذاری شده‌اند</small></article>
                <article className="stat-card"><div className="stat-top"><span>بخش‌های محتوایی</span><i>▧</i></div><strong>{loading ? "—" : sections.length.toLocaleString("fa-IR")}</strong><small>بخش‌های دریافت‌شده از وب‌سایت</small></article>
                <article className="stat-card stat-muted"><div className="stat-top"><span>وضعیت ارتباط</span><i>⌁</i></div><strong className="connection-value">{loading ? "در حال بررسی" : error ? "قطع" : "متصل"}</strong><small>وضعیت ارتباط با سرور محلی</small><span className="connection-dot" /></article>
              </div>

              <div className="dashboard-columns">
                <section className="panel-card recent-panel">
                  <div className="panel-heading"><div><span className="panel-kicker">آخرین اطلاعات</span><h2>پروژه‌های مجموعه</h2></div><button onClick={() => setTab("projects")} className="text-action">همه پروژه‌ها <span>←</span></button></div>
                  {loading ? <div className="empty-state">در حال دریافت اطلاعات...</div> : projects.length === 0 ? <div className="empty-state">هنوز پروژه‌ای ثبت نشده است.</div> : (
                    <div className="recent-list">{projects.slice(0, 5).map((project) => (
                      <div className="recent-item" key={project.id}>
                        <div className="recent-thumb">{project.main_image ? <img src={imageUrl(project.main_image)} alt="" /> : <span>ب</span>}</div>
                        <div className="recent-info"><strong>{project.title}</strong><small>{project.address || "نشانی ثبت نشده"}</small></div>
                        <span className={project.is_for_sale ? "status-pill available" : "status-pill"}>{project.is_for_sale ? "قابل فروش" : "معرفی پروژه"}</span>
                      </div>
                    ))}</div>
                  )}
                </section>

                <section className="panel-card content-panel">
                  <div className="panel-heading"><div><span className="panel-kicker">ساختار وب‌سایت</span><h2>بخش‌های محتوا</h2></div><span className="mini-count">{sections.length.toLocaleString("fa-IR")} بخش</span></div>
                  <div className="section-shortcuts">{sections.map((section) => <div className="section-shortcut" key={section.id}><span className="shortcut-mark">✳</span><div><strong>{sectionNames[section.key] || section.title}</strong><small>{section.title}</small></div><span className="shortcut-arrow">←</span></div>)}</div>
                  {sections.length === 0 && !loading && <div className="empty-state">محتوایی برای نمایش دریافت نشد.</div>}
                </section>
              </div>
            </>
          )}

          {tab === "projects" && (
            <section className="panel-card full-panel">
              <div className="panel-heading project-heading"><div><span className="panel-kicker">آرشیو اجرایی</span><h2>فهرست پروژه‌ها</h2></div><label className="search-box"><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="جست‌وجوی نام یا نشانی پروژه..." /></label></div>
              {loading ? <div className="empty-state">در حال دریافت اطلاعات...</div> : (
                <div className="projects-table-wrap"><table className="projects-table"><thead><tr><th>پروژه</th><th>نشانی</th><th>وضعیت</th><th>شناسه</th></tr></thead><tbody>
                  {filteredProjects.map((project) => <tr key={project.id}><td><div className="table-project">{project.main_image ? <img src={imageUrl(project.main_image)} alt="" /> : <span className="table-placeholder">ب</span>}<strong>{project.title}</strong></div></td><td>{project.address || "—"}</td><td><span className={project.is_for_sale ? "status-pill available" : "status-pill"}>{project.is_for_sale ? "قابل فروش" : "معرفی پروژه"}</span></td><td className="id-cell">#{project.id.toLocaleString("fa-IR")}</td></tr>)}
                </tbody></table>{filteredProjects.length === 0 && <div className="empty-state">پروژه‌ای با این عبارت پیدا نشد.</div>}</div>
              )}
            </section>
          )}

          {tab === "content" && (
            <section className="panel-card full-panel">
              <div className="panel-heading"><div><span className="panel-kicker">مدیریت صفحات</span><h2>بخش‌های محتوایی وب‌سایت</h2></div><span className="mini-count">{sections.length.toLocaleString("fa-IR")} بخش</span></div>
              <div className="content-grid">{sections.map((section) => <article className="content-card" key={section.id}>
                <div className="content-card-image">{section.image ? <img src={imageUrl(section.image)} alt="" /> : <span>بَرتر</span>}<b>{sectionNames[section.key] || "بخش سایت"}</b></div>
                <div className="content-card-body"><h3>{section.title}</h3><p>{section.subtitle || "زیرعنوانی ثبت نشده است"}</p><small>{section.content ? `${section.content.slice(0, 105)}${section.content.length > 105 ? "..." : ""}` : "متنی برای این بخش ثبت نشده است."}</small></div>
              </article>)}</div>
              {sections.length === 0 && !loading && <div className="empty-state">بخشی برای نمایش دریافت نشد.</div>}
            </section>
          )}

          <div className="dashboard-footnote"><span>i</span><p>این نسخه فعلاً اطلاعات را از API موجود می‌خواند. عملیات افزودن، ویرایش و حذف پس از پیاده‌سازی ورود امن و دسترسی‌های مدیریتی فعال می‌شود.</p></div>
        </div>
      </section>
    </main>
  );
}
