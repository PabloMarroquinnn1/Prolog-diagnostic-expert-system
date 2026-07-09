const API = 'http://127.0.0.1:5000/api';

let sintomasSeleccionados = new Set();

document.addEventListener('DOMContentLoaded', () => {
  cargarSintomas();
  document.getElementById('btn-diagnosticar').addEventListener('click', hacerDiagnostico);
  document.getElementById('btn-limpiar').addEventListener('click', limpiarSeleccion);
  document.getElementById('btn-nuevo').addEventListener('click', mostrarSintomas);
  document.getElementById('btn-historial').addEventListener('click', mostrarHistorial);
  document.getElementById('btn-volver').addEventListener('click', mostrarSintomas);
  document.getElementById('btn-limpiar-historial').addEventListener('click', limpiarHistorial);
});

async function cargarSintomas() {
  const grid = document.getElementById('sintomas-grid');
  try {
    const res  = await fetch(`${API}/sintomas`);
    const data = await res.json();
    grid.innerHTML = '';
    data.sintomas.forEach(s => {
      const sid = s.id;
      console.log('ID recibido:', sid);
      const chip = document.createElement('label');
      chip.className = 'sintoma-chip';
      chip.innerHTML = `<input type="checkbox" value="${sid}"> ${s.nombre}`;
      chip.querySelector('input').addEventListener('change', e => {
        console.log('Seleccionando:', sid, 'checked:', e.target.checked);
        if (e.target.checked) {
          sintomasSeleccionados.add(sid);
        } else {
          sintomasSeleccionados.delete(sid);
        }
        chip.classList.toggle('selected', e.target.checked);
      });
      grid.appendChild(chip);
    });
  } catch (err) {
    console.error('Error cargando sintomas:', err);
    grid.innerHTML = '<p class="loading">Error al cargar síntomas.</p>';
  }
}

function limpiarSeleccion() {
  sintomasSeleccionados.clear();
  document.querySelectorAll('.sintoma-chip input').forEach(cb => {
    cb.checked = false;
    cb.closest('.sintoma-chip').classList.remove('selected');
  });
}

async function hacerDiagnostico() {
  if (sintomasSeleccionados.size === 0) {
    alert('Selecciona al menos un síntoma.');
    return;
  }
  const lista = [...sintomasSeleccionados];
  console.log('Enviando síntomas:', lista);

  const btn = document.getElementById('btn-diagnosticar');
  btn.textContent = 'Analizando...';
  btn.disabled = true;

  try {
    const res  = await fetch(`${API}/diagnosticar`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ sintomas: lista })
    });
    const data = await res.json();
    console.log('Respuesta:', data);
    mostrarResultados(data.diagnosticos);
  } catch (err) {
    console.error('Error diagnosticando:', err);
    alert('Error al conectar con el servidor.');
  } finally {
    btn.textContent = 'Diagnosticar';
    btn.disabled = false;
  }
}

function mostrarResultados(diagnosticos) {
  const container = document.getElementById('resultados-container');
  container.innerHTML = '';

  if (!diagnosticos || diagnosticos.length === 0) {
    container.innerHTML = '<p class="empty">No se encontraron fallas relacionadas.</p>';
  } else {
    diagnosticos.forEach(d => {
      const badgeClass = d.porcentaje >= 70 ? 'badge-high' : d.porcentaje >= 40 ? 'badge-mid' : 'badge-low';
      const card = document.createElement('div');
      card.className = 'diag-card';
      card.innerHTML = `
        <div class="diag-header">
          <span class="diag-nombre">${d.nombre_falla}</span>
          <span class="badge ${badgeClass}">${d.porcentaje}% coincidencia</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width:${d.porcentaje}%"></div></div>
        <p class="diag-rec">💡 ${d.recomendacion}</p>`;
      container.appendChild(card);
    });
  }

  show('section-resultados');
  hide('section-sintomas');
  hide('section-historial');
}

let chartDona   = null;
let chartBarras = null;

async function mostrarHistorial() {
  const container = document.getElementById('historial-container');
  container.innerHTML = '<p class="loading">Cargando...</p>';
  show('section-historial');
  hide('section-resultados');
  hide('section-sintomas');

  try {
    const res     = await fetch(`${API}/historial`);
    const data    = await res.json();
    const historial = data.historial;

    renderCharts(historial);
    container.innerHTML = '';

    if (!historial.length) {
      container.innerHTML = '<p class="empty">No hay diagnósticos en el historial.</p>';
      return;
    }

    [...historial].reverse().forEach(h => {
      const top  = h.diagnosticos[0];
      const item = document.createElement('div');
      item.className = 'historial-item';
      item.innerHTML = `
        <div class="historial-meta">#${h.id} · ${h.fecha}</div>
        <div class="historial-falla">🔴 ${top?.nombre_falla ?? 'Sin diagnóstico'} (${top?.porcentaje ?? 0}%)</div>
        <div class="historial-sintomas">Síntomas: ${h.sintomas.join(', ')}</div>`;
      container.appendChild(item);
    });

  } catch (err) {
    console.error('Error cargando historial:', err);
    container.innerHTML = '<p class="loading">Error al cargar historial.</p>';
  }
}

function renderCharts(historial) {
  const frecuencia = {};
  historial.forEach(h => {
    const top = h.diagnosticos[0];
    if (top) frecuencia[top.nombre_falla] = (frecuencia[top.nombre_falla] || 0) + 1;
  });

  const labelsD = Object.keys(frecuencia);
  const valuesD = Object.values(frecuencia);
  const colores = ['#4f8ef7','#e05252','#f0a04b','#4caf7d','#a78bfa','#f472b6','#34d399','#fb923c'];

  if (chartDona) chartDona.destroy();
  chartDona = new Chart(document.getElementById('chart-dona'), {
    type: 'doughnut',
    data: {
      labels:   labelsD,
      datasets: [{ data: valuesD, backgroundColor: colores.slice(0, labelsD.length), borderColor: '#1a1d27', borderWidth: 3 }]
    },
    options: {
      plugins: { legend: { position: 'bottom', labels: { color: '#8b90a8', font: { size: 11 }, boxWidth: 12 } } }
    }
  });

  const porFecha = {};
  historial.forEach(h => {
    const fecha = h.fecha.split(' ')[0];
    porFecha[fecha] = (porFecha[fecha] || 0) + 1;
  });
  const labelsB = Object.keys(porFecha).slice(-7);
  const valuesB = labelsB.map(f => porFecha[f]);

  if (chartBarras) chartBarras.destroy();
  chartBarras = new Chart(document.getElementById('chart-barras'), {
    type: 'bar',
    data: {
      labels:   labelsB,
      datasets: [{ label: 'Diagnósticos', data: valuesB, backgroundColor: 'rgba(79,142,247,0.6)', borderColor: '#4f8ef7', borderWidth: 1, borderRadius: 6 }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#8b90a8' }, grid: { color: '#2e3248' } },
        y: { ticks: { color: '#8b90a8', stepSize: 1 }, grid: { color: '#2e3248' }, beginAtZero: true }
      }
    }
  });
}

async function limpiarHistorial() {
  if (!confirm('¿Limpiar todo el historial?')) return;
  await fetch(`${API}/historial`, { method: 'DELETE' });
  mostrarHistorial();
}

function mostrarSintomas() {
  show('section-sintomas');
  hide('section-resultados');
  hide('section-historial');
}

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }