/**
 * api.js — capa de comunicación con el backend Flask
 * Todas las llamadas HTTP pasan por aquí.
 */

const API_BASE = 'http://localhost:5000/api';

// ─── Token ────────────────────────────────────────────────────────────────────
const Auth = {
  getToken: () => localStorage.getItem('token'),
  getUser:  () => JSON.parse(localStorage.getItem('user') || 'null'),
  getRoles: () => {
    const u = Auth.getUser();
    return u ? (u.roles || []).map(r => r.toUpperCase()) : [];
  },
  hasRole: (...roles) => roles.some(r => Auth.getRoles().includes(r.toUpperCase())),
  isAdmin: () => Auth.hasRole('ADMINISTRADOR'),
  save: (token, usuario) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(usuario));
  },
  clear: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  isAuthenticated: () => !!Auth.getToken(),
  guardPage: (...allowedRoles) => {
    if (!Auth.isAuthenticated()) {
      window.location.href = '../index.html';
      return false;
    }
    if (allowedRoles.length && !Auth.hasRole(...allowedRoles)) {
      window.location.href = 'dashboard.html';
      return false;
    }
    return true;
  }
};

// ─── Request base ─────────────────────────────────────────────────────────────
async function request(method, path, body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = Auth.getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${path}`, opts);
  const json = await res.json();

  if (res.status === 401) {
    Auth.clear();
    window.location.href = '../index.html';
    return null;
  }
  return { ok: res.ok, status: res.status, ...json };
}

const get  = (path)        => request('GET',    path);
const post = (path, body)  => request('POST',   path, body);
const put  = (path, body)  => request('PUT',    path, body);
const del  = (path)        => request('DELETE', path);
const patch = (path, body) => request('PATCH',  path, body);

// ─── Endpoints ────────────────────────────────────────────────────────────────
const API = {
  auth: {
    login: (usuario, password) => post('/auth/login', { usuario, password }),
    me:    () => get('/auth/me'),
  },
  usuarios: {
    list:   ()         => get('/usuarios/'),
    get:    (id)       => get(`/usuarios/${id}`),
    create: (data)     => post('/usuarios/', data),
    update: (id, data) => put(`/usuarios/${id}`, data),
    delete: (id)       => del(`/usuarios/${id}`),
  },
  alumnos: {
    list:   ()         => get('/alumnos/'),
    get:    (id)       => get(`/alumnos/${id}`),
    me:     ()         => get('/alumnos/me'),
    create: (data)     => post('/alumnos/', data),
    update: (id, data) => put(`/alumnos/${id}`, data),
    delete: (id)       => del(`/alumnos/${id}`),
  },
  docentes: {
    list:   ()         => get('/docentes/'),
    get:    (id)       => get(`/docentes/${id}`),
    create: (data)     => post('/docentes/', data),
    update: (id, data) => put(`/docentes/${id}`, data),
    delete: (id)       => del(`/docentes/${id}`),
  },
  carreras: {
    list:   (soloActivas = false) => get(`/carreras/?activas=${soloActivas}`),
    get:    (id)       => get(`/carreras/${id}`),
    create: (data)     => post('/carreras/', data),
    update: (id, data) => put(`/carreras/${id}`, data),
    delete: (id)       => del(`/carreras/${id}`),
  },
  materias: {
    list:   (params = {}) => {
      const q = new URLSearchParams(params).toString();
      return get(`/materias/${q ? '?' + q : ''}`);
    },
    get:    (id)       => get(`/materias/${id}`),
    create: (data)     => post('/materias/', data),
    update: (id, data) => put(`/materias/${id}`, data),
    delete: (id)       => del(`/materias/${id}`),
  },
  inscripciones: {
    list:     (params = {}) => {
      const q = new URLSearchParams(params).toString();
      return get(`/inscripciones/${q ? '?' + q : ''}`);
    },
    byAlumno: (id)         => get(`/inscripciones/alumno/${id}`),
    create:   (data)       => post('/inscripciones/', data),
    estado:   (id, estado, motivo_baja = null) => {
      const body = { estado };
      if (motivo_baja) body.motivo_baja = motivo_baja;
      return patch(`/inscripciones/${id}/estado`, body);
    },
    delete:   (id)         => del(`/inscripciones/${id}`),
  },
  tickets: {
    list:   ()          => get('/tickets/'),
    create: (data)      => post('/tickets/', data),
    status: (id, estatus) => patch(`/tickets/${id}/estatus`, { estatus }),
  },
  pagos: {
    list:   ()         => get('/pagos/'),
    mine:   ()         => get('/pagos/mis-pagos'),
    payEnrollment: (data) => post('/pagos/pagar-inscripcion', data),
    create: (data)     => post('/pagos/', data),
    update: (id, data) => put(`/pagos/${id}`, data),
  },
  auditoria: {
    list: (limit = 200) => get(`/auditoria/?limit=${limit}`),
  },
};
