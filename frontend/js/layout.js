/**
 * layout.js — inyecta sidebar + header en las páginas internas
 * Uso: <script src="../js/layout.js"></script>
 *      <script>Layout.init('dashboard');</script>
 */

const Layout = {
  init(activePage) {
    this._injectHTML(activePage);
    renderUserInfo();
    this._bindLogout();
    this._bindSidebarVisibility();
    setActiveNav(activePage);
    this._movePageContentWhenReady();
  },

  _injectHTML(activePage) {
    // Calcular si el rol puede ver ciertas secciones
    const isAdmin      = Auth.hasRole('ADMINISTRADOR');
    const isAdminOrAdm = Auth.hasRole('ADMINISTRADOR', 'ADMINISTRATIVO');

    document.body.insertAdjacentHTML('afterbegin', `
      <!-- Modal de confirmación global -->
      <div class="modal fade" id="confirmModal" tabindex="-1">
        <div class="modal-dialog modal-sm modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body p-4 text-center">
              <i class="bi bi-exclamation-triangle-fill text-warning fs-2 mb-3 d-block"></i>
              <p class="mb-0" id="confirmModalMsg">¿Estás seguro?</p>
            </div>
            <div class="modal-footer justify-content-center border-0 pt-0 pb-3">
              <button class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
              <button class="btn btn-danger btn-sm" id="confirmModalOk">Confirmar</button>
            </div>
          </div>
        </div>
      </div>

      <div class="app-wrapper">
        <!-- ── Sidebar ── -->
        <aside class="app-sidebar shadow" id="appSidebar">
          <div class="sidebar-brand p-3 d-flex align-items-center gap-2">
            <div style="width:36px;height:36px;background:#1a6fc4;border-radius:.6rem;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.2rem;flex-shrink:0;">
              <i class="bi bi-mortarboard-fill"></i>
            </div>
            <div class="brand-text" style="line-height:1.2;">
              <div style="font-weight:800;color:#fff;font-size:.95rem;">SAE</div>
              <div style="font-size:.7rem;color:rgba(255,255,255,.5);font-weight:400;">Sistema Educativo</div>
            </div>
          </div>

          <nav class="sidebar-nav mt-2">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link" data-page="dashboard" href="dashboard.html">
                  <i class="bi bi-speedometer2 me-2"></i> Dashboard
                </a>
              </li>

              ${isAdminOrAdm || Auth.hasRole('DOCENTE') ? `
              <li class="sidebar-header">Académico</li>
              ` : ''}

              ${isAdminOrAdm ? `
              <li class="nav-item">
                <a class="nav-link" data-page="alumnos" href="alumnos.html">
                  <i class="bi bi-people me-2"></i> Alumnos
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="docentes" href="docentes.html">
                  <i class="bi bi-person-badge me-2"></i> Docentes
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="carreras" href="carreras.html">
                  <i class="bi bi-diagram-3 me-2"></i> Carreras
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="materias" href="materias.html">
                  <i class="bi bi-journal-bookmark me-2"></i> Materias
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="inscripciones" href="inscripciones.html">
                  <i class="bi bi-clipboard2-check me-2"></i> Inscripciones
                </a>
              </li>
              ` : ''}

              ${isAdminOrAdm ? `
              <li class="sidebar-header">Administración</li>
              ${isAdmin ? `
              <li class="nav-item">
                <a class="nav-link" data-page="usuarios" href="usuarios.html">
                  <i class="bi bi-person-gear me-2"></i> Usuarios
                </a>
              </li>
              ` : ''}
              <li class="nav-item">
                <a class="nav-link" data-page="pagos" href="pagos.html">
                  <i class="bi bi-cash-coin me-2"></i> Pagos
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="bitacora" href="bitacora.html">
                  <i class="bi bi-journal-text me-2"></i> Bitácora
                </a>
              </li>
              ` : ''}

              ${Auth.hasRole('DOCENTE') && !isAdminOrAdm ? `
              <li class="nav-item">
                <a class="nav-link" data-page="alumnos" href="alumnos.html">
                  <i class="bi bi-people me-2"></i> Alumnos
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="inscripciones" href="inscripciones.html">
                  <i class="bi bi-clipboard2-check me-2"></i> Inscripciones
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="materias" href="materias.html">
                  <i class="bi bi-journal-bookmark me-2"></i> Materias
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="pagos" href="pagos.html">
                  <i class="bi bi-cash-coin me-2"></i> Pagos
                </a>
              </li>
              ` : ''}

              ${Auth.hasRole('ALUMNO') ? `
              <li class="sidebar-header">Mi Perfil</li>
              <li class="nav-item">
                <a class="nav-link" data-page="mi-perfil" href="mi-perfil.html">
                  <i class="bi bi-person-circle me-2"></i> Mi Perfil
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="inscripciones" href="inscripciones.html">
                  <i class="bi bi-clipboard2-check me-2"></i> Inscripciones
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-page="materias" href="materias.html">
                  <i class="bi bi-journal-bookmark me-2"></i> Materias
                </a>
              </li>
              ` : ''}

              <li class="sidebar-header">Soporte</li>
              <li class="nav-item">
                <a class="nav-link" data-page="tickets" href="tickets.html">
                  <i class="bi bi-ticket-detailed me-2"></i> Tickets
                </a>
              </li>
            </ul>
          </nav>

          <div class="sidebar-footer p-3 mt-auto" style="border-top:1px solid rgba(255,255,255,.08);">
            <div class="d-flex align-items-center gap-2">
              <div style="width:34px;height:34px;background:rgba(255,255,255,.12);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;flex-shrink:0;">
                <i class="bi bi-person-fill"></i>
              </div>
              <div style="min-width:0;">
                <div style="color:#fff;font-size:.85rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" data-user-name>—</div>
                <div style="color:rgba(255,255,255,.45);font-size:.7rem;" data-user-role>—</div>
              </div>
              <button onclick="Layout._logout()" class="btn btn-sm ms-auto"
                style="background:rgba(255,255,255,.1);color:rgba(255,255,255,.7);border:0;border-radius:.4rem;padding:.3rem .5rem;"
                title="Cerrar sesión">
                <i class="bi bi-box-arrow-right"></i>
              </button>
            </div>
          </div>
        </aside>

        <!-- ── Main content wrapper ── -->
        <main class="app-main">
          <!-- Header -->
          <div class="app-content-header d-flex align-items-center px-4 py-2" style="border-bottom:1px solid #e5e7eb;background:#fff;">
            <button class="btn btn-sm btn-light me-3 d-lg-none" id="sidebarToggle">
              <i class="bi bi-list fs-5"></i>
            </button>
            <nav aria-label="breadcrumb" class="flex-grow-1">
              <ol class="breadcrumb mb-0" id="breadcrumb">
                <li class="breadcrumb-item"><a href="dashboard.html" style="color:var(--brand-primary);text-decoration:none;">Inicio</a></li>
              </ol>
            </nav>
            <div class="d-flex align-items-center gap-2">
              <span class="badge" style="background:#e0f2fe;color:#0369a1;font-size:.75rem;" data-user-role>—</span>
              <span style="font-size:.88rem;font-weight:600;color:#374151;" data-user-name>—</span>
            </div>
          </div>
          <!-- Page content injected here -->
          <div class="app-content p-4" id="pageContent"></div>
        </main><!-- /app-main -->
      </div><!-- /app-wrapper -->
    `);
  },

  _movePageContentWhenReady() {
    const moveContent = () => {
      const target = document.getElementById('pageContent');
      if (!target) return;

      const nodes = Array.from(document.body.childNodes).filter(node => {
        if (node.nodeType === Node.TEXT_NODE && !node.textContent.trim()) return false;
        if (node.nodeType !== Node.ELEMENT_NODE) return true;
        if (node.classList.contains('app-wrapper')) return false;
        if (node.matches('script[src*="../js/api.js"], script[src*="../js/ui.js"], script[src*="../js/layout.js"]')) return false;
        return true;
      });

      nodes.forEach(node => target.appendChild(node));
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', moveContent, { once: true });
    } else {
      moveContent();
    }
  },

  _bindLogout() {
    window.Layout = window.Layout || this;
  },

  _logout() {
    if (confirm('¿Cerrar sesión?')) {
      Auth.clear();
      window.location.href = '../index.html';
    }
  },

  _bindSidebarVisibility() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('appSidebar');
    if (toggle && sidebar) {
      toggle.addEventListener('click', () => {
        sidebar.classList.toggle('d-none');
      });
    }
  },

  setBreadcrumb(items) {
    const bc = document.getElementById('breadcrumb');
    if (!bc) return;
    const extra = items.map((item, i) =>
      i === items.length - 1
        ? `<li class="breadcrumb-item active">${item.label}</li>`
        : `<li class="breadcrumb-item"><a href="${item.href || '#'}" style="color:var(--brand-primary);text-decoration:none;">${item.label}</a></li>`
    ).join('');
    bc.innerHTML = `<li class="breadcrumb-item"><a href="dashboard.html" style="color:var(--brand-primary);text-decoration:none;">Inicio</a></li>${extra}`;
  }
};
