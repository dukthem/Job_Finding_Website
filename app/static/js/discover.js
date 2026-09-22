/**
 * CareerPulse - Discover Jobs & ATS Matcher Frontend Engine
 */

let currentResumeFile = null;
let currentResumeText = "";

// DOM Initialization
document.addEventListener("DOMContentLoaded", () => {
    initDropzone();
    initFilterForm();
    initTopCompaniesModal();
    searchJobs();
});

// 1. DRAG & DROP RESUME SCANNER
function initDropzone() {
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("resumeFileInput");
    const dropzoneText = document.getElementById("dropzoneText");
    const clearBtn = document.getElementById("clearResumeBtn");

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener("click", (e) => {
        if (e.target !== clearBtn) fileInput.click();
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) handleFileUpload(e.target.files[0]);
    });

    ["dragenter", "dragover"].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.add("border-indigo-500", "bg-indigo-950/30");
        });
    });

    ["dragleave", "drop"].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.remove("border-indigo-500", "bg-indigo-950/30");
        });
    });

    dropzone.addEventListener("drop", (e) => {
        if (e.dataTransfer.files.length > 0) handleFileUpload(e.dataTransfer.files[0]);
    });

    clearBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        currentResumeFile = null;
        currentResumeText = "";
        fileInput.value = "";
        dropzoneText.textContent = "Click or drag resume here";
        clearBtn.classList.add("hidden");
        document.getElementById("detectedSkillsSection").classList.add("hidden");
        document.getElementById("detectedSkillsChips").innerHTML = "";
        searchJobs();
    });
}

function handleFileUpload(file) {
    currentResumeFile = file;
    document.getElementById("dropzoneText").innerHTML = `
        <span class="text-indigo-400 font-bold">${escapeHtml(file.name)}</span>
        <div class="text-[10px] text-emerald-400 mt-0.5"><i class="fa-solid fa-check"></i> Loaded & Ready to Scan</div>
    `;
    document.getElementById("clearResumeBtn").classList.remove("hidden");
    searchJobs();
}

// 2. SEARCH & FILTERING ENGINE
function initFilterForm() {
    const form = document.getElementById("discoverFilterForm");
    const resetBtn = document.getElementById("resetFiltersBtn");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        searchJobs();
    });

    resetBtn.addEventListener("click", () => {
        form.reset();
        searchJobs();
    });
}

async function searchJobs() {
    const loadingIndicator = document.getElementById("loadingIndicator");
    const jobCardsGrid = document.getElementById("jobCardsGrid");
    const emptyState = document.getElementById("emptyState");
    const resultsCount = document.getElementById("resultsCount");

    loadingIndicator.classList.remove("hidden");
    loadingIndicator.classList.add("flex");

    const query = document.getElementById("keywordInput").value.trim();
    const category = document.getElementById("categorySelect").value || "all";
    const region = document.getElementById("locationInput").value.trim() || "all";

    try {
        let response;

        if (currentResumeFile) {
            const formData = new FormData();
            formData.append("file", currentResumeFile);
            if (query) formData.append("query", query);
            if (category) formData.append("category", category);
            if (region) formData.append("region", region);

            response = await fetch("/api/discover/search-file", {
                method: "POST",
                body: formData
            });
        } else {
            const payload = {
                resume_text: currentResumeText,
                query: query,
                category: category,
                region: region
            };

            response = await fetch("/api/discover/search-text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
        }

        if (!response.ok) throw new Error("Search request failed");

        const data = await response.json();

        // Render detected skills from resume
        renderSkillsChips(data.detected_skills || []);

        // Results count
        resultsCount.textContent = data.count || (data.jobs ? data.jobs.length : 0);

        if (data.jobs && data.jobs.length > 0) {
            emptyState.classList.add("hidden");
            jobCardsGrid.innerHTML = data.jobs.map(job => createJobCardHTML(job)).join("");
        } else {
            jobCardsGrid.innerHTML = "";
            emptyState.classList.remove("hidden");
        }

    } catch (err) {
        console.error("Error fetching jobs:", err);
        jobCardsGrid.innerHTML = `<div class="col-span-full text-center text-rose-400 py-8">Failed to load jobs.</div>`;
    } finally {
        loadingIndicator.classList.add("hidden");
        loadingIndicator.classList.remove("flex");
    }
}

function renderSkillsChips(skills) {
    const section = document.getElementById("detectedSkillsSection");
    const chipsContainer = document.getElementById("detectedSkillsChips");

    if (!skills || skills.length === 0) {
        section.classList.add("hidden");
        chipsContainer.innerHTML = "";
        return;
    }

    section.classList.remove("hidden");
    chipsContainer.innerHTML = skills.map(skill => `
        <span class="px-2 py-0.5 rounded-md text-[11px] font-medium bg-indigo-500/15 text-indigo-300 border border-indigo-500/25 flex items-center gap-1">
            <i class="fa-solid fa-code text-[9px] text-indigo-400"></i> ${escapeHtml(skill)}
        </span>
    `).join("");
}

// 3. JOB CARD GENERATOR
function createJobCardHTML(job) {
    const title = job.title || job.role || "Software Engineer";
    const company = job.company || "Tech Company";
    const category = job.company_category || job.category || "General Tech";
    const location = job.location || "Remote";
    const salary = job.salary || "Competitive";
    const jobUrl = job.job_url || job.url || "#";
    const score = job.ats_score !== undefined ? job.ats_score : job.match_score;

    // ATS Match Score badge
    let matchBadgeHTML = "";
    if (score !== undefined && score > 0) {
        const scoreColor = score >= 70 ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10" :
                           score >= 40 ? "text-amber-400 border-amber-500/30 bg-amber-500/10" :
                           "text-slate-400 border-slate-700 bg-slate-800/40";
        matchBadgeHTML = `
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold border ${scoreColor} flex items-center gap-1">
                <i class="fa-solid fa-bolt text-[10px]"></i> ${score}% ATS Match
            </span>
        `;
    }

    // Skills pills
    const skills = (job.matched_skills && job.matched_skills.length > 0) 
        ? job.matched_skills 
        : (job.required_skills || []).slice(0, 4);

    const skillsHTML = skills.map(s => `
        <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 border border-slate-700/60">${escapeHtml(s)}</span>
    `).join("");

    // Dynamic Recruiter Link
    let recruiterUrl = `https://www.linkedin.com/search/results/people/?keywords=technical+recruiter+${encodeURIComponent(company)}`;
    if (job.recruiter && job.recruiter.linkedin) {
        recruiterUrl = job.recruiter.linkedin;
    }

    // JSON payload encoded safely for the Track button
    const trackPayload = encodeURIComponent(JSON.stringify({
        company: company,
        role: title,
        location: location,
        salary: salary,
        job_url: jobUrl
    }));

    return `
    <div class="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 hover:border-indigo-500/40 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all duration-200 hover:-translate-y-1">
        <div>
            <div class="flex items-center justify-between gap-2 mb-3">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold border bg-indigo-500/10 text-indigo-400 border-indigo-500/20">
                    ${escapeHtml(category)}
                </span>
                ${matchBadgeHTML}
            </div>

            <h3 class="text-base font-bold text-white leading-snug line-clamp-1">${escapeHtml(title)}</h3>
            <div class="text-xs font-semibold text-indigo-300 mt-1 flex items-center gap-1.5">
                <i class="fa-regular fa-building text-[11px] text-indigo-400"></i> ${escapeHtml(company)}
            </div>

            <div class="flex flex-wrap items-center gap-y-1 gap-x-3 text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800/60">
                <span class="flex items-center gap-1">
                    <i class="fa-solid fa-location-dot text-[11px] text-slate-500"></i> ${escapeHtml(location)}
                </span>
                <span class="flex items-center gap-1 font-medium text-emerald-400">
                    <i class="fa-solid fa-indian-rupee-sign text-[11px]"></i> ${escapeHtml(salary)}
                </span>
            </div>

            <div class="flex flex-wrap gap-1.5 mt-3">
                ${skillsHTML}
            </div>
        </div>

        <div class="pt-4 mt-4 border-t border-slate-800/60 flex items-center justify-between gap-2">
            <a href="${escapeHtml(recruiterUrl)}" target="_blank" rel="noopener noreferrer"
               class="px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-sky-400 hover:text-sky-300 border border-slate-700/60 text-xs font-medium transition-colors flex items-center gap-1.5"
               title="Find Hiring Managers on LinkedIn">
                <i class="fa-brands fa-linkedin"></i>
                <span class="hidden sm:inline">Recruiter</span>
            </a>

            <div class="flex items-center gap-1.5">
                <button onclick="trackJobDirect('${trackPayload}', this)"
                        class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-medium transition-all flex items-center gap-1.5">
                    <i class="fa-solid fa-plus text-[10px]"></i> Track
                </button>

                <a href="${escapeHtml(jobUrl)}" target="_blank" rel="noopener noreferrer"
                   class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition-colors flex items-center gap-1">
                    Apply <i class="fa-solid fa-arrow-up-right-from-square text-[9px] ml-0.5"></i>
                </a>
            </div>
        </div>
    </div>
    `;
}

// 4. ONE-CLICK TRACK TO DASHBOARD
async function trackJobDirect(encodedData, buttonElement) {
    try {
        const job = JSON.parse(decodeURIComponent(encodedData));

        const payload = {
            company: job.company,
            role: job.role,
            location: job.location || "Remote",
            salary: job.salary || "Competitive",
            status: "Applied",
            job_url: job.job_url || null,
            notes: "Tracked directly from Discover Jobs engine."
        };

        // Notice trailing slash /api/jobs/ matching backend router!
        const response = await fetch("/api/jobs/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to save application");

        buttonElement.classList.remove("bg-indigo-600/20", "text-indigo-300");
        buttonElement.classList.add("bg-emerald-500/20", "text-emerald-300", "border-emerald-500/40");
        buttonElement.innerHTML = `<i class="fa-solid fa-check text-[10px]"></i> Tracked!`;
        buttonElement.disabled = true;

    } catch (err) {
        console.error("Error tracking job:", err);
        alert("Could not track job. Check if the server is running.");
    }
}

// 5. TOP 200 COMPANIES DIRECTORY MODAL
function initTopCompaniesModal() {
    const modal = document.getElementById("companiesModal");
    const openBtn = document.getElementById("openCompaniesModalBtn");
    const closeBtn = document.getElementById("closeCompaniesModalBtn");
    const pills = document.querySelectorAll("#companyCategoryPills .cat-pill");

    if (!modal || !openBtn) return;

    openBtn.addEventListener("click", () => {
        modal.classList.remove("hidden");
        loadModalCompanies("");
    });

    closeBtn.addEventListener("click", () => modal.classList.add("hidden"));

    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.add("hidden");
    });

    pills.forEach(pill => {
        pill.addEventListener("click", () => {
            pills.forEach(p => {
                p.classList.remove("bg-indigo-600", "text-white");
                p.classList.add("bg-slate-800", "text-slate-400");
            });
            pill.classList.add("bg-indigo-600", "text-white");
            pill.classList.remove("bg-slate-800", "text-slate-400");

            loadModalCompanies(pill.getAttribute("data-cat"));
        });
    });
}

async function loadModalCompanies(category) {
    const container = document.getElementById("modalCompaniesList");
    container.innerHTML = `<div class="col-span-full text-center text-slate-500 py-6"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Loading Directory...</div>`;

    try {
        const url = category ? `/api/discover/top-companies?category=${encodeURIComponent(category)}` : `/api/discover/top-companies`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("Failed to load companies");

        const data = await res.json();
        const companies = data.companies || [];

        if (companies.length === 0) {
            container.innerHTML = `<div class="col-span-full text-center text-slate-500 py-6">No companies found.</div>`;
            return;
        }

        container.innerHTML = companies.map(comp => {
            const recruiterUrl = `https://www.linkedin.com/search/results/people/?keywords=technical+recruiter+${encodeURIComponent(comp.name)}`;
            return `
            <div class="bg-slate-950/60 border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between hover:border-slate-700 transition-colors">
                <div>
                    <h4 class="text-sm font-bold text-white">${escapeHtml(comp.name)}</h4>
                    <span class="inline-block mt-0.5 text-[10px] font-medium text-indigo-400">${escapeHtml(comp.category || 'Tech')}</span>
                </div>
                <div class="flex items-center gap-2">
                    <a href="${escapeHtml(recruiterUrl)}" target="_blank" rel="noopener noreferrer"
                       class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 text-xs font-medium flex items-center gap-1 transition-colors"
                       title="Search Recruiters on LinkedIn">
                        <i class="fa-brands fa-linkedin text-sm"></i>
                    </a>
                    <a href="${escapeHtml(comp.career_url || comp.careers_url || '#')}" target="_blank" rel="noopener noreferrer"
                       class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-medium flex items-center gap-1 transition-all">
                        Careers <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                    </a>
                </div>
            </div>
            `;
        }).join("");

    } catch (err) {
        console.error("Error loading top companies:", err);
        container.innerHTML = `<div class="col-span-full text-center text-rose-400 py-6">Failed to load directory.</div>`;
    }
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}