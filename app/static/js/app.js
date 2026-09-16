// State variables to keep track of current jobs and selected filter
let allJobs = [];
let currentFilter = 'all';

// When the browser finishes loading the HTML, start our app!
document.addEventListener('DOMContentLoaded', () => {
  loadJobs();
});

// ==========================================
// 1. Fetch All Jobs from FastAPI Backend
// ==========================================
async function loadJobs() {
  try {
    const response = await fetch('/api/jobs/');
    if (!response.ok) throw new Error('Failed to fetch jobs');
    
    allJobs = await response.json();
    updateMetrics(allJobs);
    renderJobs(allJobs);
  } catch (error) {
    console.error('Error loading jobs:', error);
  }
}

// ==========================================
// 2. Update the 4 Metric Cards at the Top
// ==========================================
function updateMetrics(jobs) {
  const total = jobs.length;
  const applied = jobs.filter(j => j.status === 'Applied').length;
  const interviewing = jobs.filter(j => j.status === 'Interviewing').length;
  const offer = jobs.filter(j => j.status === 'Offer').length;

  document.getElementById('metricTotal').textContent = total;
  document.getElementById('metricApplied').textContent = applied;
  document.getElementById('metricInterviewing').textContent = interviewing;
  document.getElementById('metricOffer').textContent = offer;
}

// ==========================================
// 3. Render Job Cards into the HTML Grid
// ==========================================
function renderJobs(jobs) {
  const container = document.getElementById('jobsContainer');
  const emptyState = document.getElementById('emptyState');

  // Filter based on active tab
  let filtered = jobs;
  if (currentFilter !== 'all') {
    filtered = jobs.filter(j => j.status.toLowerCase() === currentFilter.toLowerCase());
  }

  // If no jobs match, show the Empty State graphic
  if (filtered.length === 0) {
    container.innerHTML = '';
    emptyState.classList.remove('hidden');
    return;
  }

  // Otherwise, hide empty state and build the cards
  emptyState.classList.add('hidden');

  container.innerHTML = filtered.map(job => {
    // Pick color badge based on status
    let statusBadge = '';
    if (job.status === 'Applied') {
      statusBadge = `<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">Applied</span>`;
    } else if (job.status === 'Interviewing') {
      statusBadge = `<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-purple-500/15 text-purple-400 border border-purple-500/30">Interviewing</span>`;
    } else if (job.status === 'Offer') {
      statusBadge = `<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">Offer 🎉</span>`;
    } else {
      statusBadge = `<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30">Rejected</span>`;
    }

    const appliedDate = new Date(job.applied_date).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric'
    });

    return `
      <div class="bg-[#131b2e] border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg transition-all flex flex-col justify-between group">
        <div>
          <div class="flex items-start justify-between gap-2 mb-3">
            <div>
              <h3 class="text-base font-bold text-white group-hover:text-indigo-400 transition-colors">${job.company}</h3>
              <p class="text-xs font-semibold text-slate-300 mt-0.5">${job.role}</p>
            </div>
            ${statusBadge}
          </div>

          <div class="space-y-1.5 text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800/80">
            <div class="flex items-center">
              <i class="fa-solid fa-location-dot w-4 text-slate-500 mr-1.5"></i>
              <span>${job.location || 'Remote'}</span>
            </div>
            ${job.salary ? `
            <div class="flex items-center text-emerald-400 font-medium">
              <i class="fa-solid fa-indian-rupee-sign w-4 mr-1.5"></i>
              <span>${job.salary}</span>
            </div>` : ''}
            <div class="flex items-center text-slate-500 text-[11px]">
              <i class="fa-regular fa-calendar w-4 mr-1.5"></i>
              <span>Applied on ${appliedDate}</span>
            </div>
          </div>

          ${job.notes ? `
          <div class="mt-3 p-2.5 rounded-xl bg-[#0B0F19]/60 border border-slate-800/60 text-xs text-slate-300">
            <p class="font-semibold text-[10px] uppercase text-indigo-400 tracking-wider mb-1">Notes</p>
            <p class="line-clamp-2">${job.notes}</p>
          </div>` : ''}
        </div>

        <!-- Card Footer Actions -->
        <div class="flex items-center justify-between mt-4 pt-3 border-t border-slate-800/60 text-xs">
          ${job.job_url ? `
            <a href="${job.job_url}" target="_blank" class="text-indigo-400 hover:text-indigo-300 font-medium inline-flex items-center">
              <i class="fa-solid fa-arrow-up-right-from-square mr-1 text-[10px]"></i> View Job
            </a>` : `<span></span>`}

          <div class="flex items-center space-x-2">
            <button onclick="openEditModal(${job.id})" class="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition-all cursor-pointer" title="Edit">
              <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <button onclick="deleteJob(${job.id})" class="text-slate-400 hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition-all cursor-pointer" title="Delete">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ==========================================
// 4. Status Filter Tabs Logic
// ==========================================
function filterByStatus(status) {
  currentFilter = status;

  // Update tab visual styles
  document.querySelectorAll('.status-tab').forEach(tab => {
    if (tab.dataset.status.toLowerCase() === status.toLowerCase()) {
      tab.className = 'status-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all bg-indigo-600 text-white';
    } else {
      tab.className = 'status-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition-all';
    }
  });

  renderJobs(allJobs);
}

// ==========================================
// 5. Modal Management (Open, Close, Edit)
// ==========================================
function openCreateModal() {
  document.getElementById('jobId').value = '';
  document.getElementById('modalTitle').innerHTML = '<i class="fa-solid fa-briefcase text-indigo-400 mr-2"></i> Track New Application';
  document.getElementById('jobForm').reset();
  document.getElementById('jobModal').classList.remove('hidden');
}

function openEditModal(id) {
  const job = allJobs.find(j => j.id === id);
  if (!job) return;

  document.getElementById('jobId').value = job.id;
  document.getElementById('modalTitle').innerHTML = '<i class="fa-solid fa-pen-to-square text-indigo-400 mr-2"></i> Edit Application';
  document.getElementById('companyInput').value = job.company;
  document.getElementById('roleInput').value = job.role;
  document.getElementById('locationInput').value = job.location || '';
  document.getElementById('salaryInput').value = job.salary || '';
  document.getElementById('statusInput').value = job.status;
  document.getElementById('jobUrlInput').value = job.job_url || '';
  document.getElementById('notesInput').value = job.notes || '';

  document.getElementById('jobModal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('jobModal').classList.add('hidden');
}

// Close modal if clicking outside the dialog box
window.onclick = function(event) {
  const modal = document.getElementById('jobModal');
  if (event.target === modal) {
    closeModal();
  }
};

// ==========================================
// 6. Handle Form Submit (Create OR Update)
// ==========================================
async function handleFormSubmit(event) {
  event.preventDefault(); // Prevents page reload!

  const jobId = document.getElementById('jobId').value;
  const payload = {
    company: document.getElementById('companyInput').value,
    role: document.getElementById('roleInput').value,
    location: document.getElementById('locationInput').value || 'Remote',
    salary: document.getElementById('salaryInput').value || null,
    status: document.getElementById('statusInput').value,
    job_url: document.getElementById('jobUrlInput').value || null,
    notes: document.getElementById('notesInput').value || null
  };

  try {
    let response;
    if (jobId) {
      // UPDATE existing job (PUT)
      response = await fetch(`/api/jobs/${jobId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } else {
      // CREATE new job (POST)
      response = await fetch('/api/jobs/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }

    if (!response.ok) throw new Error('Failed to save job');

    closeModal();
    await loadJobs(); // Reload data from SQLite smoothly!
  } catch (error) {
    alert('Error saving application: ' + error.message);
  }
}

// ==========================================
// 7. Delete Job Application
// ==========================================
async function deleteJob(id) {
  if (!confirm('Are you sure you want to delete this job application?')) return;

  try {
    const response = await fetch(`/api/jobs/${id}`, {
      method: 'DELETE'
    });

    if (!response.ok) throw new Error('Failed to delete job');
    await loadJobs(); // Refresh grid
  } catch (error) {
    alert('Error deleting application: ' + error.message);
  }
}