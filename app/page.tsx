
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_BASE = "http://127.0.0.1:8000";

type Theme = "light" | "dark";

type Project = {
  id: number;
  title: string;
  address?: string;
  main_image?: string | null;
  is_for_sale?: boolean;
};

type Section = {
  id: number;
  key: string;
  title: string;
  subtitle: string;
  content: string;
  image: string | null;
};

const serviceStages = [
  { number: "01", title: "طراحی و معماری", description: "طراحی و شکل‌گیری ایده اولیه پروژه." },
  { number: "02", title: "مطالعات و برنامه‌ریزی", description: "بررسی شرایط پروژه و برنامه‌ریزی مراحل اجرا." },
  { number: "03", title: "مهندسی و آماده‌سازی", description: "آماده‌سازی فنی و مهندسی پیش از شروع عملیات." },
  { number: "04", title: "ساخت و اجرا", description: "اجرای پروژه بر اساس نقشه‌ها و استانداردهای فنی." },
  { number: "05", title: "بازسازی و نوسازی", description: "بهسازی و بازآفرینی فضاها و ساختمان‌ها." },
  { number: "06", title: "نظارت و کنترل کیفیت", description: "کنترل روند اجرا و کیفیت مراحل ساخت." },
];

function mediaUrl(path?: string | null) {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${API_BASE}/${path.replace(/^\/+/, "")}`;
}

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [sections, setSections] = useState<Record<string, Section>>({});
  const [filter, setFilter] = useState<"all" | "sale">("all");
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const [activeStage, setActiveStage] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [projectError, setProjectError] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [headerHidden, setHeaderHidden] = useState(false);

  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const savedTheme = localStorage.getItem("bartar-theme");

    const initialTheme: Theme =
      savedTheme === "dark" ? "dark" : "light";

    setTheme(initialTheme);
    document.documentElement.dataset.theme = initialTheme;
  }, []);

  function toggleTheme() {
    const nextTheme: Theme = theme === "light" ? "dark" : "light";

    setTheme(nextTheme);
    document.documentElement.dataset.theme = nextTheme;
    localStorage.setItem("bartar-theme", nextTheme);
  }

  useEffect(() => {
    let previousY = window.scrollY;

    const onScroll = () => {
      const currentY = window.scrollY;
      const hero = document.getElementById("home");
      const heroEnd = hero ? hero.offsetHeight : window.innerHeight;
      const pastHero = currentY >= heroEnd - 90;
      const hasMoved = currentY > 2;
      const movingDown = currentY > previousY;
      const movingUp = currentY < previousY;

      // Any tiny scroll turns the header black. After the hero, hide it
      // while scrolling down and reveal it as soon as scrolling up begins.
      setScrolled(hasMoved);
      if (!pastHero || movingUp || currentY <= 2) {
        setHeaderHidden(false);
      } else if (pastHero && movingDown) {
        setHeaderHidden(true);
      }

      if (pastHero && movingDown) {
        setOpenMenu(null);
      }

      previousY = currentY;
    };

    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    fetch(`${API_BASE}/api/projects/projects/`)
      .then((response) => {
        if (!response.ok) throw new Error("Projects request failed");
        return response.json();
      })
      .then((data) => {
        setProjects(Array.isArray(data) ? data : data.results ?? []);
      })
      .catch((error) => {
        console.error("Projects:", error);
        setProjectError(true);
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetch(`${API_BASE}/api/pages/sections/`)
      .then((response) => {
        if (!response.ok) throw new Error("Sections request failed");
        return response.json();
      })
      .then((data) => {
        const list: Section[] = Array.isArray(data) ? data : data.results ?? [];
        const map: Record<string, Section> = {};

        list.forEach((item) => {
          map[item.key] = item;
        });

        setSections(map);
      })
      .catch((error) => console.error("Sections:", error));
  }, []);

  const about = sections.about;
  const community = sections.community;
  const services = sections.services;
  const approach = sections.approach;

  const visibleProjects =
    filter === "sale"
      ? projects.filter((p) => p.is_for_sale)
      : projects;

  function toggleMenu(name: string) {
    setOpenMenu((current) => (current === name ? null : name));
  }

  function closeMenu() {
    setOpenMenu(null);
  }

  function goToSection(id: string) {
    setOpenMenu(null);

    window.setTimeout(() => {
      document.getElementById(id)?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 150);
  }

  return (
    <main dir="rtl">
        {/* HEADER */}
        <header className={`site-header ${scrolled ? "is-solid" : ""} ${headerHidden ? "is-hidden" : ""}`} onMouseLeave={closeMenu}>
          <Link href="/" className="brand-capsule" onClick={closeMenu}>
            <img className="brand-logo" src="/logoo.png" alt="لوگوی برتر" />
          </Link>

          <nav className="nav-capsule">
            <Link className="nav-link" href="/" onClick={closeMenu}>
              صفحه اصلی
            </Link>

            <button
              className={`nav-link ${openMenu === "about" ? "active" : ""}`}
              onMouseEnter={() => setOpenMenu("about")}
              onClick={() => toggleMenu("about")}
              aria-expanded={openMenu === "about"}
            >
              درباره ما
              <span className="nav-menu-mark" aria-hidden="true"><i /><i /><i /></span>
            </button>

            <button
              className={`nav-link ${openMenu === "projects" ? "active" : ""}`}
              onMouseEnter={() => setOpenMenu("projects")}
              onClick={() => toggleMenu("projects")}
              aria-expanded={openMenu === "projects"}
            >
              پروژه‌های ما
              <span className="nav-chevron">⌄</span>
            </button>

            <button
              className={`nav-link ${openMenu === "services" ? "active" : ""}`}
              onMouseEnter={() => setOpenMenu("services")}
              onClick={() => toggleMenu("services")}
              aria-expanded={openMenu === "services"}
            >
              خدمات ما
              <span className="nav-chevron">⌄</span>
            </button>
          </nav>

          {/* THEME TOGGLE */}
          <button
            type="button"
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={
              theme === "light"
                ? "فعال کردن حالت شب"
                : "فعال کردن حالت روز"
            }
            title={
              theme === "light"
                ? "حالت شب"
                : "حالت روز"
            }
          >
            {theme === "light" ? "☾" : "☀"}
          </button>

          {/* MEGA MENU */}
          {openMenu && (
            <div className="mega-menu" key={openMenu}>
              <div className="mega-menu-top">
                <div>
                  <span className="mega-eyebrow">
                    BARTAR CONSTRUCTION GROUP
                  </span>

                  <h2>
                    {openMenu === "about" && "درباره گروه ساختمانی برتر"}
                    {openMenu === "projects" && "پروژه‌های گروه برتر"}
                    {openMenu === "services" && "خدمات و تخصص‌های ما"}
                  </h2>

                  <p>
                    {openMenu === "about" &&
                      "با مجموعه، ارزش‌ها و رویکرد ما در مسیر ساخت‌وساز آشنا شوید."}
                    {openMenu === "projects" &&
                      "نگاهی به پروژه‌ها و فعالیت‌های اجرایی گروه ساختمانی برتر."}
                    {openMenu === "services" &&
                      "از شکل‌گیری ایده تا اجرا و نظارت، همراه شما هستیم."}
                  </p>
                </div>

                <button
                  className="mega-close"
                  onClick={closeMenu}
                  aria-label="بستن منو"
                >
                  ×
                </button>
              </div>

              {/* ABOUT MENU */}
              {openMenu === "about" && (
                <div className="mega-grid about-mega-grid">
                  <a
                    href="#about"
                    className="mega-card"
                    onClick={(e) => {
                      e.preventDefault();
                      goToSection("about");
                    }}
                  >
                    <div className="mega-card-image">
                      {about?.image ? (
                        <img src={mediaUrl(about.image)} alt={about.title} />
                      ) : (
                        <div className="mega-image-placeholder">01</div>
                      )}
                    </div>

                    <div className="mega-card-content">
                      <span className="mega-card-number">
                        01 / معرفی مجموعه
                      </span>
                      <h3>گروه ساختمانی برتر</h3>
                      <p>آشنایی با مجموعه و مسیر فعالیت ما</p>
                      <span className="mega-card-arrow">←</span>
                    </div>
                  </a>

                  <a
                    href="#approach"
                    className="mega-card"
                    onClick={(e) => {
                      e.preventDefault();
                      goToSection("approach");
                    }}
                  >
                    <div className="mega-card-image">
                      {approach?.image ? (
                        <img src={mediaUrl(approach.image)} alt={approach.title} />
                      ) : (
                        <div className="mega-image-placeholder">02</div>
                      )}
                    </div>

                    <div className="mega-card-content">
                      <span className="mega-card-number">
                        02 / نگرش ما
                      </span>
                      <h3>رویکرد ما</h3>
                      <p>نگاه ما به طراحی، ساخت و کیفیت</p>
                      <span className="mega-card-arrow">←</span>
                    </div>
                  </a>

                  <a
                    href="#community"
                    className="mega-card"
                    onClick={(e) => {
                      e.preventDefault();
                      goToSection("community");
                    }}
                  >
                    <div className="mega-card-image">
                      {community?.image ? (
                        <img src={mediaUrl(community.image)} alt={community.title} />
                      ) : (
                        <div className="mega-image-placeholder">03</div>
                      )}
                    </div>

                    <div className="mega-card-content">
                      <span className="mega-card-number">
                        03 / مسئولیت اجتماعی
                      </span>
                      <h3>جامعه و مسئولیت</h3>
                      <p>نگاهی فراتر از ساخت‌وساز</p>
                      <span className="mega-card-arrow">←</span>
                    </div>
                  </a>
                </div>
              )}

              {/* PROJECTS MENU */}
              {openMenu === "projects" && (
                <div className="mega-projects">
                  <div className="mega-project-filters">
                    <button
                      className={
                        filter === "all" ? "mega-filter active" : "mega-filter"
                      }
                      onClick={() => setFilter("all")}
                    >
                      تمام پروژه‌ها
                    </button>

                    <button
                      className={
                        filter === "sale" ? "mega-filter active" : "mega-filter"
                      }
                      onClick={() => setFilter("sale")}
                    >
                      پروژه‌های قابل فروش
                    </button>

                    <a
                      href="#projects"
                      className="mega-all-link"
                      onClick={(e) => {
                        e.preventDefault();
                        goToSection("projects");
                      }}
                    >
                      مشاهده همه پروژه‌ها ←
                    </a>
                  </div>

                  {loading ? (
                    <p className="mega-status">
                      در حال دریافت پروژه‌ها...
                    </p>
                  ) : projectError ? (
                    <p className="mega-status">
                      دریافت پروژه‌ها با خطا مواجه شد.
                    </p>
                  ) : visibleProjects.length > 0 ? (
                    <div className="mega-project-grid">
                      {visibleProjects.slice(0, 3).map((project) => (
                        <Link
                          href={`/projects/${project.id}`}
                          className="mega-project-card"
                          key={project.id}
                          onClick={closeMenu}
                        >
                          <div className="mega-project-image">
                            {project.main_image ? (
                              <img
                                src={mediaUrl(project.main_image)}
                                alt={project.title}
                              />
                            ) : (
                              <div className="mega-image-placeholder">B</div>
                            )}

                            {project.is_for_sale && (
                              <span className="mega-sale-label">
                                قابل فروش
                              </span>
                            )}
                          </div>

                          <div className="mega-project-info">
                            <h3>{project.title}</h3>
                            <p>{project.address || "گروه ساختمانی برتر"}</p>
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <p className="mega-status">
                      پروژه‌ای برای نمایش وجود ندارد.
                    </p>
                  )}
                </div>
              )}

              {/* SERVICES MENU */}
              {openMenu === "services" && (
                <div className="mega-services-grid">
                  {serviceStages.map((stage, index) => (
                    <a
                      href="#services"
                      className="mega-service-card"
                      key={stage.number}
                      onClick={(e) => {
                        e.preventDefault();
                        setActiveStage(index);
                        goToSection("services");
                      }}
                    >
                      <span className="mega-service-number">
                        {stage.number}
                      </span>

                      <div>
                        <h3>{stage.title}</h3>
                        <p>{stage.description}</p>
                      </div>

                      <span className="mega-service-arrow">↙</span>
                    </a>
                  ))}
                </div>
              )}

              <div className="mega-menu-footer">
                <span>گروه ساختمانی برتر</span>
                <span>ساختن، فراتر از ساخت‌وساز</span>
              </div>
            </div>
          )}
        </header>

      {/* HERO */}
      <section className="hero" id="home">
        <video
          className="hero-video"
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
        >
          <source src="/hero.mp4" type="video/mp4" />
        </video>

        <div className="hero-shade" />



        <div className="hero-title-line">
          <span className="hero-small-title">گروه ساختمانی</span>
          <h1>برتر</h1>
          <small className="hero-tag">(مظاهر)</small>
        </div>

        <a href="#about" className="hero-down" aria-label="رفتن به بخش بعد">
          <span>↓</span>
        </a>
      </section>

      {/* ABOUT SECTION */}
      <section className="section about-section" id="about">
        <div className="container about-container">

          <div className="about-editorial-main">
            <div className="about-editorial-image">
              {about?.image ? (
                <img
                  src={mediaUrl(about.image)}
                  alt={about.title || "گروه ساختمانی برتر"}
                />
              ) : (
                <div className="about-editorial-image-placeholder">
                  BARTAR CONSTRUCTION GROUP
                </div>
              )}
            </div>

            <div className="about-editorial-description">
              {about?.subtitle && (
                <h3>{about.subtitle}</h3>
              )}

              <div className="about-editorial-accent" />

              <p>
                {about?.content ||
                  "محتوای معرفی مجموعه از پنل مدیریت نمایش داده خواهد شد."}
              </p>
            </div>
          </div>

          <div className="about-editorial-bottom">
            <div><strong>کیفیت در ساخت</strong></div>
            <div><strong>تعهد در اجرا</strong></div>
            <div><strong>ماندگاری در زمان</strong></div>
          </div>

        </div>
      </section>

      {/* PROJECTS + SERVICES */}
      <section className="section section-concrete" id="projects-services">
        <div className="work-grid">
          <div className="work-projects" id="projects">
            <div className="block-head">
              <h2>پروژه‌های ما</h2>
              <p>
                نگاهی به بخشی از پروژه‌ها و فعالیت‌های گروه ساختمانی برتر
              </p>
            </div>

            <div className="project-filters">
              <button
                className={
                  filter === "all" ? "filter-chip selected" : "filter-chip"
                }
                onClick={() => setFilter("all")}
              >
                تمام پروژه‌ها
              </button>

              <button
                className={
                  filter === "sale" ? "filter-chip selected" : "filter-chip"
                }
                onClick={() => setFilter("sale")}
              >
                قابل فروش
              </button>
            </div>

            {loading ? (
              <p className="project-status">
                در حال دریافت پروژه‌ها...
              </p>
            ) : projectError ? (
              <p className="project-status">
                دریافت پروژه‌ها با خطا مواجه شد. مطمئن شوید سرور روشن است.
              </p>
            ) : visibleProjects.length > 0 ? (
              <div className="projects-list">
                {visibleProjects.map((project) => (
                  <Link
                    href={`/projects/${project.id}`}
                    className="p-card"
                    key={project.id}
                  >
                    <div className="p-card-image">
                      {project.main_image ? (
                        <img
                          src={mediaUrl(project.main_image)}
                          alt={project.title}
                        />
                      ) : (
                        <div className="project-no-image">
                          تصویر پروژه ثبت نشده
                        </div>
                      )}

                      {project.is_for_sale && (
                        <span className="project-sale-label">
                          قابل فروش
                        </span>
                      )}
                    </div>

                    <div className="p-card-bar">
                      <div>
                        <h3>{project.title}</h3>
                        {project.address && <p>{project.address}</p>}
                      </div>

                      <span className="p-card-go">
                        مشاهده جزئیات
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="project-status">
                پروژه‌ای برای نمایش وجود ندارد.
              </p>
            )}
          </div>

          <aside className="work-services" id="services">
            <div className="services-panel">
              <div className="services-head">
                <h2>{services?.title || "خدمات ما"}</h2>
                <p>
                  {services?.subtitle ||
                    "همراهی در تمام مراحل شکل‌گیری تا اجرای پروژه"}
                </p>
              </div>

              {services?.image && (
                <div className="services-image">
                  <img
                    src={mediaUrl(services.image)}
                    alt="خدمات گروه ساختمانی برتر"
                  />
                </div>
              )}

              <div className="service-table">
                {serviceStages.map((stage, index) => (
                  <div
                    className={
                      activeStage === index
                        ? "service-row open"
                        : "service-row"
                    }
                    key={stage.number}
                  >
                    <button
                      className="service-row-button"
                      onClick={() =>
                        setActiveStage(
                          activeStage === index ? null : index
                        )
                      }
                      aria-expanded={activeStage === index}
                    >
                      <span className="service-row-number">
                        {stage.number}
                      </span>

                      <span className="service-row-title">
                        {stage.title}
                      </span>

                      <span className="service-row-icon">
                        {activeStage === index ? "−" : "+"}
                      </span>
                    </button>

                    {activeStage === index && (
                      <p className="service-row-description">
                        {stage.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {services?.content && (
                <p className="services-note">{services.content}</p>
              )}
            </div>
          </aside>
        </div>
      </section>

      {/* COMMUNITY */}
      <section className="section section-tint" id="community">
        <div className="container">
          <div className={community?.image ? "split" : "split single"}>
            {community?.image && (
              <div className="split-media">
                <img
                  src={mediaUrl(community.image)}
                  alt={community.title}
                />
              </div>
            )}

            <div className="split-text">
              <h2>{community?.title || "جامعه و مسئولیت"}</h2>
              {community?.subtitle && (
                <p className="lead">{community.subtitle}</p>
              )}

              <p className="prose">
                {community?.content ||
                  "محتوای این بخش از پنل مدیریت نمایش داده خواهد شد."}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* APPROACH */}
      <section className="section section-navy" id="approach">
        <div className={approach?.image ? "split" : "split single"}>
          {approach?.image && (
            <div className="split-media">
              <img
                src={mediaUrl(approach.image)}
                alt={approach.title}
              />
            </div>
          )}

          <div className="split-text">
            <h2>{approach?.title || "رویکرد ما"}</h2>
            {approach?.subtitle && (
              <p className="lead">{approach.subtitle}</p>
            )}

            {approach?.content && (
              <p className="prose">{approach.content}</p>
            )}
          </div>
        </div>
      </section>

      {/* CONTACT */}
      <section className="contact-section" id="contact">
        <h2>ارتباط با گروه ساختمانی برتر</h2>
        <p>برای شروع یک همکاری تازه با ما در ارتباط باشید.</p>
      </section>

      {/* FOOTER */}
      <footer className="site-footer">
        <div className="footer-brand">
          <img
            className="brand-logo"
            src="/logoo.png"
            alt="لوگوی گروه ساختمانی برتر"
          />
          <span>گروه ساختمانی برتر</span>
        </div>

        <span className="copyright">
          © تمامی حقوق برای گروه ساختمانی برتر محفوظ است.
        </span>
      </footer>
    </main>
  );
}
