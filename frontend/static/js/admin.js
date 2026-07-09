const API = 'http://127.0.0.1:5000/api';

// ── Tabs ──────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(`tab-${name}`).classList.remove('hidden');
  event.target.classList.add('active');
  if (name === 'sintomas')       cargarSintomas();
  if (name === 'fallas')         cargarFallas();
  if (name === 'recomendaciones') cargarRecomendaciones();
  if (name === 'reglas')         cargarReglas();
  if (name === 'bot')            cargarBotConfig();
}

// ── Síntomas ──────────────────────────────────────────────────
async function cargarSintomas() {
  const res  = await fetch(`${API}/sintomas`);
  const data = await res.json();
  const dyn  = await fetch(`${API}/crud/sintomas`).then(r => r.json());
  const dynIds = new Set(dyn.sintomas.map(s => s.id));

  const list = document.getElementById('lista-sintomas');
  list.innerHTML = '';
  data.sintomas.forEach(s => {
    const isDynamic = dynIds.has(s.id);
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-info">
        <div class="item-id">${s.id} <span class="${isDynamic ? 'tag-origen-dynamic' : 'tag-origen-base'}">${isDynamic ? 'dinámico' : 'base'}</span></div>
        <div class="item-name">${s.nombre}</div>
      </div>
      <div class="item-actions">
        ${isDynamic ? `<button class="btn btn-danger" onclick="eliminarSintoma('${s.id}')">Eliminar</button>` : '<span style="color:var(--muted);font-size:0.8rem">solo lectura</span>'}
      </div>`;
    list.appendChild(card);
  });
}

async function crearSintoma() {
  const sid    = document.getElementById('sin-id').value.trim().replace(/ /g, '_');
  const nombre = document.getElementById('sin-nombre').value.trim();
  if (!sid || !nombre) return alert('Completa todos los campos');
  const res  = await fetch(`${API}/crud/sintomas`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: sid, nombre})
  });
  const data = await res.json();
  alert(data.mensaje);
  if (data.ok) {
    document.getElementById('sin-id').value = '';
    document.getElementById('sin-nombre').value = '';
    cargarSintomas();
  }
}

async function eliminarSintoma(sid) {
  if (!confirm(`¿Eliminar síntoma "${sid}"?`)) return;
  const res  = await fetch(`${API}/crud/sintomas/${sid}`, { method: 'DELETE' });
  const data = await res.json();
  alert(data.mensaje);
  cargarSintomas();
}

// ── Fallas ────────────────────────────────────────────────────
async function cargarFallas() {
  const res  = await fetch(`${API}/crud/fallas`);
  const data = await res.json();
  const list = document.getElementById('lista-fallas');
  list.innerHTML = '';

  // También mostrar fallas base
  const base = await fetch(`${API}/crud/reglas`).then(r => r.json());
  const todasFallas = base.reglas || [];

  todasFallas.forEach(f => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-info">
        <div class="item-id">${f.falla_id} <span class="${f.origen === 'dynamic' ? 'tag-origen-dynamic' : 'tag-origen-base'}">${f.origen}</span></div>
        <div class="item-detail">Síntomas: ${f.sintomas.join(', ')}</div>
      </div>
      <div class="item-actions">
        ${f.origen === 'dynamic' ? `<button class="btn btn-danger" onclick="eliminarFalla('${f.falla_id}')">Eliminar</button>` : '<span style="color:var(--muted);font-size:0.8rem">solo lectura</span>'}
      </div>`;
    list.appendChild(card);
  });
}

async function crearFalla() {
  const fid   = document.getElementById('falla-id').value.trim().replace(/ /g, '_');
  const nombre = document.getElementById('falla-nombre').value.trim();
  const sinStr = document.getElementById('falla-sintomas').value.trim();
  const rec    = document.getElementById('falla-rec').value.trim();
  if (!fid || !nombre || !sinStr || !rec) return alert('Completa todos los campos');
  const sintomas = sinStr.split(',').map(s => s.trim()).filter(Boolean);
  const res  = await fetch(`${API}/crud/fallas`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: fid, nombre, sintomas, recomendacion: rec})
  });
  const data = await res.json();
  alert(data.mensaje);
  if (data.ok) {
    ['falla-id','falla-nombre','falla-sintomas','falla-rec'].forEach(id => document.getElementById(id).value = '');
    cargarFallas();
  }
}

async function eliminarFalla(fid) {
  if (!confirm(`¿Eliminar falla "${fid}"?`)) return;
  const res  = await fetch(`${API}/crud/fallas/${fid}`, { method: 'DELETE' });
  const data = await res.json();
  alert(data.mensaje);
  cargarFallas();
}

// ── Recomendaciones ───────────────────────────────────────────
async function cargarRecomendaciones() {
  const res  = await fetch(`${API}/crud/recomendaciones`);
  const data = await res.json();
  const list = document.getElementById('lista-recomendaciones');
  list.innerHTML = '';
  data.recomendaciones.forEach(r => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-info">
        <div class="item-id">${r.falla_id}</div>
        <div class="item-detail">${r.texto}</div>
      </div>
      <div class="item-actions">
        <button class="btn btn-secondary" onclick="editarRecomendacion('${r.falla_id}', \`${r.texto}\`)">Editar</button>
        <button class="btn btn-danger" onclick="eliminarRecomendacion('${r.falla_id}')">Eliminar</button>
      </div>`;
    list.appendChild(card);
  });
}

function editarRecomendacion(fid, texto) {
  document.getElementById('rec-falla-id').value = fid;
  document.getElementById('rec-texto').value    = texto;
}

async function crearRecomendacion() {
  const fid   = document.getElementById('rec-falla-id').value.trim();
  const texto = document.getElementById('rec-texto').value.trim();
  if (!fid || !texto) return alert('Completa todos los campos');
  const res  = await fetch(`${API}/crud/recomendaciones`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({falla_id: fid, texto})
  });
  const data = await res.json();
  alert(data.mensaje);
  cargarRecomendaciones();
}

async function eliminarRecomendacion(fid) {
  const id = fid || document.getElementById('rec-falla-id').value.trim();
  if (!id) return alert('Ingresa el ID de la falla');
  if (!confirm(`¿Eliminar recomendación de "${id}"?`)) return;
  const res  = await fetch(`${API}/crud/recomendaciones/${id}`, { method: 'DELETE' });
  const data = await res.json();
  alert(data.mensaje);
  cargarRecomendaciones();
}

// ── Reglas ────────────────────────────────────────────────────
async function cargarReglas() {
  const res  = await fetch(`${API}/crud/reglas`);
  const data = await res.json();
  const list = document.getElementById('lista-reglas');
  list.innerHTML = '';
  data.reglas.forEach(r => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-info">
        <div class="item-id">${r.falla_id} <span class="${r.origen === 'dynamic' ? 'tag-origen-dynamic' : 'tag-origen-base'}">${r.origen}</span></div>
        <div class="item-detail">Síntomas: ${r.sintomas.join(', ')}</div>
      </div>
      <div class="item-actions">
        ${r.origen === 'dynamic' ? `<button class="btn btn-danger" onclick="eliminarRegla('${r.falla_id}')">Eliminar</button>` : '<span style="color:var(--muted);font-size:0.8rem">solo lectura</span>'}
      </div>`;
    list.appendChild(card);
  });
}

async function crearRegla() {
  const fid    = document.getElementById('regla-falla-id').value.trim().replace(/ /g, '_');
  const sinStr = document.getElementById('regla-sintomas').value.trim();
  if (!fid || !sinStr) return alert('Completa todos los campos');
  const sintomas = sinStr.split(',').map(s => s.trim()).filter(Boolean);
  const res  = await fetch(`${API}/crud/reglas`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({falla_id: fid, sintomas})
  });
  const data = await res.json();
  alert(data.mensaje);
  if (data.ok) {
    document.getElementById('regla-falla-id').value = '';
    document.getElementById('regla-sintomas').value = '';
    cargarReglas();
  }
}

async function eliminarRegla(fid) {
  if (!confirm(`¿Eliminar regla de "${fid}"?`)) return;
  const res  = await fetch(`${API}/crud/reglas/${fid}`, { method: 'DELETE' });
  const data = await res.json();
  alert(data.mensaje);
  cargarReglas();
}

// ── Bot Config ────────────────────────────────────────────────
async function cargarBotConfig() {
  const res    = await fetch(`${API}/crud/bot/config`);
  const data   = await res.json();
  const config = data.config;
  document.getElementById('bot-token').value          = config.token || '';
  document.getElementById('bot-chat-id').value        = config.chat_id || '';
  document.getElementById('bot-msg-bienvenida').value = config.msg_bienvenida || '';
  document.getElementById('bot-msg-no-resultado').value = config.msg_no_resultado || '';
  document.getElementById('bot-msg-error').value      = config.msg_error || '';
  actualizarEstadoBot(config.activo);
}

function actualizarEstadoBot(activo) {
  const label  = document.getElementById('bot-status-label');
  const btn    = document.getElementById('btn-toggle-bot');
  label.textContent  = `Estado: ${activo ? '🟢 Activo' : '🔴 Inactivo'}`;
  btn.textContent    = activo ? 'Desactivar bot' : 'Activar bot';
  btn.className      = `btn ${activo ? 'btn-danger' : 'btn-primary'}`;
}

async function toggleBot() {
  const res  = await fetch(`${API}/crud/bot/toggle`, { method: 'POST' });
  const data = await res.json();
  actualizarEstadoBot(data.activo);
}

async function guardarBotConfig() {
  const config = {
    token:            document.getElementById('bot-token').value.trim(),
    chat_id:          document.getElementById('bot-chat-id').value.trim(),
    msg_bienvenida:   document.getElementById('bot-msg-bienvenida').value.trim(),
    msg_no_resultado: document.getElementById('bot-msg-no-resultado').value.trim(),
    msg_error:        document.getElementById('bot-msg-error').value.trim()
  };
  const res  = await fetch(`${API}/crud/bot/config`, {
    method: 'PUT', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(config)
  });
  const data = await res.json();
  alert(data.mensaje);
}

// ── Init ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  cargarSintomas();
});