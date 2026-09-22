/**
 * CareerPulse - Discover Jobs & ATS Matcher Frontend Engine
 * Handles live job searches, resume file uploads, ATS scoring, and tracking.
 */

// Global State
let currentResumeFile = null;
let currentResumeText = "";
let currentPage = 1;
const pageSize = 20;

// Category Badge Color Map
const categoryStyles = {
    "Big Tech": "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    "Product SaaS & AI": "bg-purple-500/10 text-purple-400 border-purple-500/20",
    "Fintech": "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    "European Tech": "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    "Indian Unicorns": "bg-amber-500/10 text-amber-400 border-amber-500/20",
    "IT Services": "bg-blue-500/10 text-blue-400 border-blue-500/20",
    "General Tech": "bg-slate-500/10 text-slate-400 border-slate-500/20"
};

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
    initDropzone();
    initFilterForm();
    initTopCompaniesModal();
    // Initial fetch on page load
    searchJobs();
});

// ==========================================
// 1. DRAG-AND-DROP RESUME SCANNER
// ==========================================
function initDropzone() {
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("resumeFileInput");
    const dropzoneText = document.getElementById("dropzoneText");
    const clearBtn = document.getElementById("clearResumeBtn");

    if (!dropzone || !fileInput) return;

    // Click to select file
    dropzone.addEventListener("click", (e) => {
        if (e.target !== clearBtn) fileInput.click();
    });

    // File selected via picker
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Drag-and-drop events
    ["dragenter", "dragover"].forEach(event => {
        dropzone.addEventListener(event, (e) => {
            e.preventDefault();
            dropzone.classList.add("border-indigo-500", "bg-indigo-950/30");
        });
    });

    ["dragleave", "drop"].forEach(event => {
        dropzone.addEventListener(event, (e) => {
            e.preventDefault();
            dropzone.classList.remove("border-indigo-500", "bg-indigo-950/30");
        });
    });

    dropzone.addEventListener("drop", (e) => {
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    // Clear resume button
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
    const validExtensions = [".pdf", ".docx", ".doc"];
    const fileExt = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();

    if (!validExtensions.includes(fileExt)) {
        alert("Please upload a PDF or DOCX file.");
        return;
    }

    currentResumeFile = file;
    document.getElementById("dropzoneText").innerHTML = `
        <span class="text-indigo-400 font-bold">${escapeHtml(file.name)}</span>
        <div class="text-[10px] text-emerald-400 mt-0.5"><i class="fa-solid fa-check"></i> Loaded & Ready to Scan</div>
    `;
    document.getElementById("clearResumeBtn").classList.remove("hidden");

    // Automatically trigger search with this file
    searchJobs();
}

// ==========================================
// 2. SEARCH & FILTERING ENGINE
// ==========================================
function initFilterForm() {
    const form = document.getElementById("discoverFilterForm");
    const resetBtn = document.getElementById("resetFiltersBtn");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        currentPage = 1;
        searchJobs();
    });

    resetBtn.addEventListener("click", () => {
        form.reset();
        currentPage = 1;
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

    const keyword = document.getElementById("keywordInput").value.trim() || null;
    const category = document.getElementById("categorySelect").value || null;
    const location = document.getElementById("locationInput").value.trim() || null;
    const minSalary = document.getElementById("minSalaryInput").value ? parseFloat(document.getElementById("minSalaryInput").value) : null;

    try {
        let response;

        if (currentResumeFile) {
            // MULTIPART FORM DATA for file upload
            const formData = new FormData();
            formData.append("file", currentResumeFile);
            if (keyword) formData.append("keyword", keyword);
            if (category) formData.append("category", category);
            if (location) formData.append("location", location);
            if (minSalary) formData.append("min_salary_lpa", minSalary);
            formData.append("page", currentPage);
            formData.append("page_size", pageSize);

            response = await fetch("/api/discover/search-file", {
                method: "POST",
                body: formData
            });
        } else {
            // JSON PAYLOAD for standard text search
            const payload = {
                resume_text: currentResumeText,
                keyword: keyword,
                category: category,
                location: location,
                min_salary_lpa: minSalary,
                page: currentPage,
                page_size: pageSize
            };

            response = await fetch("/api/discover/search-text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
        }

        if (!response.ok) throw new Error("Search request failed");

        const data = await response.json();

        // Update skills chips if resume was scanned
        renderSkillsChips(data.matched_skills || []);

        // Update counts and cards
        resultsCount.textContent = data.total || 0;

        if (data.jobs && data.jobs.length > 0) {
            emptyState.classList.add("hidden");
            jobCardsGrid.innerHTML = data.jobs.map(job => createJobCardHTML(job)).join("");
        } else {
            jobCardsGrid.innerHTML = "";
            emptyState.classList.remove("hidden");
        }

    } catch (err) {
        console.error("Error fetching jobs:", err);
        jobCardsGrid.innerHTML = `<div class="col-span-full text-center text-rose-400 py-8">Failed to fetch jobs. Please try again.</div>`;
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

// ==========================================
// 3. JOB CARD GENERATOR
// ==========================================
function createJobCardHTML(job) {
    const catStyle = categoryStyles[job.category] || categoryStyles["General Tech"];
    
    // Match score badge
    let matchBadgeHTML = "";
    if (job.match_score !== undefined && job.match_score > 0) {
        const scoreColor = job.match_score >= 70 ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10" :
                           job.match_score >= 40 ? "text-amber-400 border-amber-500/30 bg-amber-500/10" :
                           "text-slate-400 border-slate-700 bg-slate-800/40";
        matchBadgeHTML = `
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold border ${scoreColor} flex items-center gap-1 shadow-sm">
                <i class="fa-solid fa-bolt text-[10px]"></i> ${job.match_score}% ATS Match
            </span>
        `;
    }

    // Skills preview pills
    const skills = job.matched_skills && job.matched_skills.length > 0 
        ? job.matched_skills 
        : (job.tags || []).slice(0, 4);

    const skillsHTML = skills.map(s => `
        <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 border border-slate-700/60">${escapeHtml(s)}</span>
    `).join("");

    // Job Object for Track to Dashboard Button
    const jobDataJSON = encodeURIComponent(JSON.stringify({
        company: job.company,
        role: job.role,
        category: job.category,
        location: job.location,
        salary: job.salary_str,
        portal_url: job.url
    }));

    return `
    <div class="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 hover:border-indigo-500/40 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all duration-200 hover:-translate-y-1">
        <div>
            <!-- Top Header: Category & Match Score -->
            <div class="flex items-center justify-between gap-2 mb-3">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${catStyle}">
                    ${escapeHtml(job.category || 'Tech')}
                </span>
                ${matchBadgeHTML}
            </div>

            <!-- Job Title & Company -->
            <h3 class="text-base font-bold text-white leading-snug line-clamp-1">${escapeHtml(job.role)}</h3>
            <div class="text-xs font-semibold text-indigo-300 mt-1 flex items-center gap-1.5">
                <i class="fa-regular fa-building text-[11px] text-indigo-400"></i> ${escapeHtml(job.company)}
            </div>

            <!-- Details: Location & Salary -->
            <div class="flex flex-wrap items-center gap-y-1 gap-x-3 text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800/60">
                <span class="flex items-center gap-1">
                    <i class="fa-solid fa-location-dot text-[11px] text-slate-500"></i> ${escapeHtml(job.location || 'Remote')}
                </span>
                <span class="flex items-center gap-1 font-medium text-emerald-400">
                    <i class="fa-solid fa-indian-rupee-sign text-[11px]"></i> ${escapeHtml(job.salary_str || 'Competitive')}
                </span>
                <span class="text-[10px] text-slate-500 uppercase">
                    ${job.source === 'arbeitnow_live' ? '⚡ Live Feed' : '⭐ Curated'}
                </span>
            </div>

            <!-- Skills Pills -->
            <div class="flex flex-wrap gap-1.5 mt-3">
                ${skillsHTML}
            </div>
        </div>

        <!-- Action Footer -->
        <div class="pt-4 mt-4 border-t border-slate-800/60 flex items-center justify-between gap-2">
            <!-- LinkedIn Recruiter Search -->
            <a href="${escapeHtml(job.recruiter_search_url)}" target="_blank" rel="noopener noreferrer"
               class="px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-sky-400 hover:text-sky-300 border border-slate-700/60 text-xs font-medium transition-colors flex items-center gap-1.5"
               title="Find Hiring Managers & Recruiters on LinkedIn">
                <i class="fa-brands fa-linkedin"></i>
                <span class="hidden sm:inline">Recruiter</span>
            </a>

            <div class="flex items-center gap-1.5">
                <!-- Track to Dashboard Button -->
                <button onclick="trackJobDirect('${jobDataJSON}', this)"
                        class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-medium transition-all flex items-center gap-1.5">
                    <i class="fa-solid fa-plus text-[10px]"></i> Track
                </button>

                <!-- Apply Direct Link -->
                <a href="${escapeHtml(job.url)}" target="_blank" rel="noopener noreferrer"
                   class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition-colors flex items-center gap-1">
                    Apply <i class="fa-solid fa-arrow-up-right-from-square text-[9px] ml-0.5"></i>
                </a>
            </div>
        </div>
    </div>
    `;
}

// ==========================================
// 4. ONE-CLICK TRACK JOB TO DASHBOARD
// ==========================================
async function trackJobDirect(encodedJobData, buttonElement) {
    try {
        const job = JSON.parse(decodeURIComponent(encodedJobData));

        // Get today's date formatted as YYYY-MM-DD
        const todayStr = new Date().toISOString().split("T")[0];

        const payload = {
            company: job.company,
            role: job.role,
            category: job.category || "General Tech",
            location: job.location || "Remote",
            salary: job.salary || "Competitive",
            status: "Applied",
            applied_date: todayStr, // <-- Added today's date to fix 422!
            portal_url: job.portal_url || "",
            notes: "Tracked directly from Discover Jobs engine."
        };

        const response = await fetch("/api/jobs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errData = await response.json();
            console.error("422 Validation Error details:", errData);
            throw new Error("Failed to save application");
        }

        // UI Feedback: Button transforms to "Tracked!"
        buttonElement.classList.remove("bg-indigo-600/20", "text-indigo-300");
        buttonElement.classList.add("bg-emerald-500/20", "text-emerald-300", "border-emerald-500/40");
        buttonElement.innerHTML = `<i class="fa-solid fa-check text-[10px]"></i> Tracked!`;
        buttonElement.disabled = true;

    } catch (err) {
        console.error("Error tracking job:", err);
        alert("Could not track job. Check browser console for details.");
    }
}

// ==========================================
// 5. TOP 200 COMPANIES DIRECTORY MODAL
// ==========================================
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

    closeBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    // Close on outside backdrop click
    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.add("hidden");
    });

    // Category filter pills inside modal
    pills.forEach(pill => {
        pill.addEventListener("click", () => {
            pills.forEach(p => {
                p.classList.remove("bg-indigo-600", "text-white");
                p.classList.add("bg-slate-800", "text-slate-400");
            });
            pill.classList.add("bg-indigo-600", "text-white");
            pill.classList.remove("bg-slate-800", "text-slate-400");

            const selectedCat = pill.getAttribute("data-cat");
            loadModalCompanies(selectedCat);
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
        // Safe extraction whether backend returns {companies: [...]} or directly [...]
        const companies = (data && data.companies) ? data.companies : (Array.isArray(data) ? data : []);

        if (companies.length === 0) {
            container.innerHTML = `<div class="col-span-full text-center text-slate-500 py-6">No companies found in this category.</div>`;
            return;
        }

        container.innerHTML = companies.map(comp => `
            <div class="bg-slate-950/60 border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between hover:border-slate-700 transition-colors">
                <div>
                    <h4 class="text-sm font-bold text-white">${escapeHtml(comp.name)}</h4>
                    <span class="inline-block mt-0.5 text-[10px] font-medium text-indigo-400">${escapeHtml(comp.category)}</span>
                </div>
                <div class="flex items-center gap-2">
                    <a href="${escapeHtml(comp.recruiter_search_url)}" target="_blank" rel="noopener noreferrer"
                       class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 text-xs font-medium flex items-center gap-1 transition-colors"
                       title="Search Recruiters on LinkedIn">
                        <i class="fa-brands fa-linkedin text-sm"></i>
                    </a>
                    <a href="${escapeHtml(comp.careers_url)}" target="_blank" rel="noopener noreferrer"
                       class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-medium flex items-center gap-1 transition-all">
                        Careers <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                    </a>
                </div>
            </div>
        `).join("");

    } catch (err) {
        console.error("Error loading top companies:", err);
        container.innerHTML = `<div class="col-span-full text-center text-rose-400 py-6">Failed to load directory.</div>`;
    }
}

// Helper utility to prevent XSS
function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}