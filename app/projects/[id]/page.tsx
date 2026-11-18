"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

const API_BASE = "http://127.0.0.1:8000";

type UnitType = {
  id: number;
  direction: string;
  direction_display?: string;
  description: string;
  area?: string | null;
  image?: string | null;
  floor_plan?: string | null;
  model_3d?: string | null;
};

type Project = {
  id: number;
  title: string;
  description: string;
  address: string;
  is_for_sale: boolean;
  construction_status?: string;
  construction_progress?: number | null;
  construction_stages?: { id: number; title: string; progress: number; is_completed: boolean; notes?: string }[];
  construction_reports?: { id: number; title: string; description: string; report_date: string; image?: string | null; stage_title?: string }[];
  main_image?: string | null;
  model_3d?: string | null;
  parking_plan?: string | null;
  total_units?: number | null;
  floors_count?: number | null;
  units_per_floor?: number | null;
  building_width?: string | null;
  useful_area?: string | null;
  has_roof_garden?: boolean | null;
  has_pool?: boolean | null;
  is_sloped_design?: boolean | null;
  has_pilot?: boolean | null;
  pilot_area?: string | null;
  has_basement?: boolean | null;
  basement_area?: string | null;
  basement_plan?: string | null;
  has_game_room?: boolean | null;
  has_elevator?: boolean | null;
  unit_types?: UnitType[];
};

function mediaUrl(path?: string | null) {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${API_BASE}/${path.replace(/^\/+/, "")}`;
}

function num(value?: string | number | null) {
  if (value === null || value === undefined || value === "") return "";
  const n = Number(value);
  if (Number.isNaN(n)) return String(value);
  return n.toLocaleString("fa-IR", { maximumFractionDigits: 2 });
}

export default function ProjectDetail() {
  const params = useParams<{ id: string }>();
  const id = params?.id;

  const [project, setProject] = useState<Project | null>(null);
  const [status, setStatus] = useState<"loading" | "error" | "ready">("loading");

  useEffect(() => {
    if (!id) return;
    fetch(`${API_BASE}/api/projects/projects/${id}/`)
      .then((response) => {
        if (!response.ok) throw new Error("Project request failed");
        return response.json();
      })
      .then((data) => {
        setProject(data);
        setStatus("ready");
      })
      .catch((error) => {
        console.error("Project:", error);
        setStatus("error");
      });
  }, [id]);

  const header = (
    <header className="site-header is-solid">
      <Link href="/" className="brand">
        <img className="brand-logo" src="/logo.jpg" alt="لوگوی برتر" />
        <span>گروه ساختمانی برتر</span>
      </Link>
      <Link href="/#projects" className="back-link">
        بازگشت به پروژه‌ها
      </Link>
    </header>
  );

  if (status !== "ready" || !project) {
    return (
      <main dir="rtl">
        {header}
        <p className="detail-status">
          {status === "loading" ? "در حال دریافت اطلاعات پروژه..." : "پروژه پیدا نشد یا سرور در دسترس نیست."}
        </p>
      </main>
    );
  }

  const facts = [
    { label: "تعداد کل واحدها", value: num(project.total_units) },
    { label: "تعداد طبقات", value: num(project.floors_count) },
    { label: "واحد در هر طبقه", value: num(project.units_per_floor) },
    { label: "مساحت مفید طبقه", value: project.useful_area ? `${num(project.useful_area)} متر` : "" },
    { label: "عرض بنا", value: project.building_width ? `${num(project.building_width)} متر` : "" },
    { label: "متراژ پیلوت", value: project.has_pilot && project.pilot_area ? `${num(project.pilot_area)} متر` : "" },
    { label: "متراژ زیرزمین", value: project.has_basement && project.basement_area ? `${num(project.basement_area)} متر` : "" },
  ].filter((fact) => fact.value);

  const amenities = [
    { label: "آسانسور", on: project.has_elevator },
    { label: "روف گاردن", on: project.has_roof_garden },
    { label: "استخر", on: project.has_pool },
    { label: "اتاق بازی", on: project.has_game_room },
    { label: "پیلوت", on: project.has_pilot },
    { label: "زیرزمین", on: project.has_basement },
    { label: "طراحی در شیب", on: project.is_sloped_design },
  ].filter((item) => item.on);

  const plans = [
    { label: "پلان پارکینگ", src: project.parking_plan },
    { label: "پلان زیرزمین", src: project.basement_plan },
  ].filter((plan) => plan.src);

  const units = project.unit_types ?? [];

  return (
    <main dir="rtl">
      {header}

      {/* HERO */}
      <section className="detail-hero">
        {project.main_image ? (
          <img src={mediaUrl(project.main_image)} alt={project.title} />
        ) : (
          <div className="detail-hero-empty" />
        )}
        <div className="hero-shade" />
        <div className="detail-hero-copy">
          {project.is_for_sale && <span className="project-sale-label">قابل فروش</span>}
          {project.construction_status && (
            <span className={`project-construction-label status-${project.construction_status}`}>
              {project.construction_status === "in_progress" ? "در حال ساخت" :
                project.construction_status === "paused" ? "متوقف‌شده" :
                project.construction_status === "completed" ? "تکمیل‌شده" :
                project.construction_status === "delivered" ? "تحویل‌شده" :
                project.construction_status === "pending" ? "در انتظار شروع" :
                project.construction_status === "planning" ? "در حال برنامه‌ریزی" : "بایگانی‌شده"}
            </span>
          )}
          <h1>{project.title}</h1>
          {project.address && <p>{project.address}</p>}
        </div>
      </section>

      {/* FACTS BAR */}
      {facts.length > 0 && (
        <div className="facts-wrap">
          <dl className="facts-bar">
            {facts.map((fact) => (
              <div className="fact" key={fact.label}>
                <dd>{fact.value}</dd>
                <dt>{fact.label}</dt>
              </div>
            ))}
          </dl>
        </div>
      )}

      {/* DESCRIPTION */}
      <section className="section section-grid">
        <div className="detail-two">
          <div className="detail-side">
            <h2>درباره پروژه</h2>
            {project.model_3d && (
              <a className="solid-button" href={mediaUrl(project.model_3d)} target="_blank" rel="noreferrer">
                مشاهده مدل سه‌بعدی
              </a>
            )}
          </div>
          <p className="prose">{project.description}</p>
        </div>
      </section>


      {/* CONSTRUCTION PROGRESS — visible only while construction is active or paused */}
      {(project.construction_status === "in_progress" || project.construction_status === "paused") && (
        <section className="section section-construction-progress">
          <div className="container">
            <div className="block-head">
              <h2>روند پیشرفت ساخت</h2>
              <p>{project.construction_status === "paused" ? "پروژه در حال حاضر متوقف است" : "آخرین وضعیت اجرای پروژه"}</p>
            </div>
            {typeof project.construction_progress === "number" && (
              <div className="construction-overall-progress">
                <strong>{num(project.construction_progress)}٪</strong>
                <div className="construction-progress-track"><span style={{ width: `${project.construction_progress}%` }} /></div>
              </div>
            )}
            {project.construction_stages && project.construction_stages.length > 0 && (
              <div className="construction-stage-list">
                {project.construction_stages.map((stage) => (
                  <article className="construction-stage" key={stage.id}>
                    <div className="construction-stage-heading">
                      <h3>{stage.title}</h3><strong>{num(stage.progress)}٪</strong>
                    </div>
                    <div className="construction-progress-track"><span style={{ width: `${stage.progress}%` }} /></div>
                    {stage.notes && <p>{stage.notes}</p>}
                  </article>
                ))}
              </div>
            )}
            {project.construction_reports && project.construction_reports.length > 0 && (
              <div className="construction-report-list">
                <h3>گزارش‌های پیشرفت</h3>
                {project.construction_reports.map((report) => (
                  <article className="construction-report" key={report.id}>
                    {report.image && <img src={mediaUrl(report.image)} alt={report.title} />}
                    <div><h4>{report.title}</h4><small>{report.report_date}{report.stage_title ? ` · ${report.stage_title}` : ""}</small><p>{report.description}</p></div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* AMENITIES */}
      {amenities.length > 0 && (
        <section className="section section-concrete">
          <div className="container">
            <div className="block-head">
              <h2>امکانات پروژه</h2>
            </div>
            <ul className="amenities">
              {amenities.map((item) => (
                <li key={item.label}>
                  <span className="amenity-mark">✓</span>
                  {item.label}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* UNITS */}
      {units.length > 0 && (
        <section className="section section-navy">
          <div className="container">
            <div className="block-head">
              <h2>تیپ واحدها</h2>
              <p>نگاهی به جزئیات هر واحد، متراژ و پلان آن</p>
            </div>
            <div className="units">
              {units.map((unit) => (
                <article className="unit" key={unit.id}>
                  <div className="unit-top">
                    <h3>واحد {unit.direction_display ?? unit.direction}</h3>
                    {unit.area && <span className="unit-area">{num(unit.area)} متر مربع</span>}
                  </div>
                  <div className="unit-body">
                    <div className="unit-text">
                      <p className="prose">{unit.description}</p>
                      {unit.model_3d && (
                        <a className="solid-button" href={mediaUrl(unit.model_3d)} target="_blank" rel="noreferrer">
                          مدل سه‌بعدی واحد
                        </a>
                      )}
                    </div>
                    <div className="unit-media">
                      {unit.image && <img src={mediaUrl(unit.image)} alt={`واحد ${unit.direction_display ?? ""}`} />}
                      {unit.floor_plan && (
                        <a href={mediaUrl(unit.floor_plan)} target="_blank" rel="noreferrer" className="unit-plan">
                          <img src={mediaUrl(unit.floor_plan)} alt="پلان واحد" />
                          <span>مشاهده پلان در اندازه کامل</span>
                        </a>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* PLANS */}
      {plans.length > 0 && (
        <section className="section section-concrete">
          <div className="container">
            <div className="block-head">
              <h2>پلان‌ها</h2>
            </div>
            <div className="plans">
              {plans.map((plan) => (
                <figure key={plan.label}>
                  <a href={mediaUrl(plan.src)} target="_blank" rel="noreferrer">
                    <img src={mediaUrl(plan.src)} alt={plan.label} />
                  </a>
                  <figcaption>{plan.label}</figcaption>
                </figure>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="contact-section">
        <h2>به این پروژه علاقه دارید؟</h2>
        <p>برای دریافت اطلاعات بیشتر با گروه ساختمانی برتر در ارتباط باشید.</p>
        <Link href="/#contact" className="gold-button">ارتباط با ما</Link>
      </section>

      <footer className="site-footer">
        <div className="footer-brand">
          <img className="brand-logo" src="/logo.jpg" alt="لوگوی گروه ساختمانی برتر" />
          <span>گروه ساختمانی برتر</span>
        </div>
        <span className="copyright">© تمامی حقوق برای گروه ساختمانی برتر محفوظ است.</span>
      </footer>
    </main>
  );
}
