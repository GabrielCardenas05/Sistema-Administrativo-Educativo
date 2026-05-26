/**
 * ui.js — utilidades de interfaz compartidas entre todas las páginas
 */

// ─── Toast ────────────────────────────────────────────────────────────────────
const Toast = {
  _container: null,
  _getContainer() {
    if (!this._container) {
      this._container = document.createElement('div');
      this._container.style.cssText = 'position:fixed;top:1rem;right:1rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;';
      document.body.appendChild(this._container);
    }
    return this._container;
  },
  show(message, type = 'success') {
    const colors = { success: '#198754', error: '#dc3545', warning: '#ffc107', info: '#0dcaf0' };
    const icons  = { success: 'bi-check-circle-fill', error: 'bi-x-circle-fill', warning: 'bi-exclamation-triangle-fill', info: 'bi-info-circle-fill' };

    const toast = document.createElement('div');
    toast.style.cssText = `
      background:${colors[type] || colors.info};color:#fff;padding:.75rem 1.1rem;
      border-radius:.5rem;font-size:.9rem;display:flex;align-items:center;gap:.6rem;
      box-shadow:0 4px 16px rgba(0,0,0,.25);max-width:340px;
      animation:toastIn .25s ease;
    `;
    toast.innerHTML = `<i class="bi ${icons[type] || icons.info}"></i><span>${message}</span>`;
    this._getContainer().appendChild(toast);

    if (!document.getElementById('_toast_style')) {
      const s = document.createElement('style');
      s.id = '_toast_style';
      s.textContent = `@keyframes toastIn{from{opacity:0;transform:translateX(2rem)}to{opacity:1;transform:translateX(0)}}`;
      document.head.appendChild(s);
    }

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity .3s';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },
  success: (m) => Toast.show(m, 'success'),
  error:   (m) => Toast.show(m, 'error'),
  warning: (m) => Toast.show(m, 'warning'),
  info:    (m) => Toast.show(m, 'info'),
};

// ─── Loading overlay ──────────────────────────────────────────────────────────
const Loader = {
  show(container) {
    const el = document.createElement('div');
    el.className = '_loader_overlay';
    el.style.cssText = 'position:absolute;inset:0;background:rgba(255,255,255,.6);display:flex;align-items:center;justify-content:center;z-index:10;border-radius:inherit;';
    el.innerHTML = '<div class="spinner-border text-primary" style="width:2rem;height:2rem;"></div>';
    if (container) {
      container.style.position = 'relative';
      container.appendChild(el);
    }
    return el;
  },
  hide(el) { el && el.remove(); },
};

// ─── Confirm dialog ───────────────────────────────────────────────────────────
function confirmDialog(message) {
  return new Promise(resolve => {
    // Usar modal de Bootstrap si está disponible
    const modal = document.getElementById('confirmModal');
    if (modal) {
      document.getElementById('confirmModalMsg').textContent = message;
      const bsModal = new bootstrap.Modal(modal);
      bsModal.show();
      const btn = document.getElementById('confirmModalOk');
      const handler = () => { btn.removeEventListener('click', handler); bsModal.hide(); resolve(true); };
      btn.addEventListener('click', handler);
      modal.addEventListener('hidden.bs.modal', () => resolve(false), { once: true });
    } else {
      resolve(window.confirm(message));
    }
  });
}

// ─── Tabla dinámica ───────────────────────────────────────────────────────────
/**
 * Renderiza una tabla simple con datos.
 * @param {HTMLElement} tbody - elemento tbody
 * @param {Array} rows - filas de datos
 * @param {Function} rowRenderer - fn(item) => string HTML de <td>s
 */
function renderTable(tbody, rows, rowRenderer) {
  if (!rows || rows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="99" class="text-center text-muted py-4">Sin registros</td></tr>`;
    return;
  }
  tbody.innerHTML = rows.map(item => `<tr>${rowRenderer(item)}</tr>`).join('');
}

// ─── Poblar <select> ──────────────────────────────────────────────────────────
function fillSelect(selectEl, items, valueKey, labelKey, placeholder = '— Seleccionar —') {
  selectEl.innerHTML = `<option value="">${placeholder}</option>` +
    items.map(i => `<option value="${i[valueKey]}">${i[labelKey]}</option>`).join('');
}

// ─── Leer formulario como objeto ──────────────────────────────────────────────
function formToObj(form) {
  const data = {};
  new FormData(form).forEach((v, k) => { data[k] = v.trim() === '' ? null : v.trim(); });
  return data;
}

// ─── Llenar formulario desde objeto ──────────────────────────────────────────
function objToForm(form, data) {
  Object.entries(data).forEach(([k, v]) => {
    const el = form.elements[k];
    if (el && v !== null && v !== undefined) el.value = v;
  });
}

// ─── Sidebar activo ───────────────────────────────────────────────────────────
function setActiveNav(page) {
  document.querySelectorAll('.nav-link[data-page]').forEach(link => {
    link.classList.toggle('active', link.dataset.page === page);
  });
}

// ─── Nombre de usuario en header ─────────────────────────────────────────────
function renderUserInfo() {
  const user = Auth.getUser();
  if (!user) return;
  document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.usuario);
  document.querySelectorAll('[data-user-role]').forEach(el => el.textContent = (user.roles || []).join(', '));
}
