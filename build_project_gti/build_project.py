# NOTE: This project is for Proof of Concept (POC) purposes only. It is not intended for production use.
import os

# --- File Content ---

# 1. HTML Content for index.html
html_content = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your_Product_Detections - GTI Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>">
    <meta name="description" content="Google Threat Intelligence Demo - Analyze IOCs, vulnerabilities, and threat indicators">
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="text-slate-800 overflow-x-hidden">
    <!-- Loading Spinner -->
    <div id="loadingSpinner" class="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50 hidden">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        <span class="ml-3 text-slate-600">Loading...</span>
    </div>

    <div id="mainContent" class="container mx-auto p-4 md:p-8 transition-all duration-300">
        <!-- Header -->
        <header class="mb-6 fade-in">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl md:text-4xl font-bold text-slate-900">Your_Product_Detections</h1>
                    <p class="text-slate-500 mt-1">Google Threat Intelligence Demo</p>
                </div>
                <div class="text-xs text-slate-500 text-right">
                    <p>Data as of: <span class="font-medium text-slate-600" id="currentDate"></span></p>
                    <p class="mt-1">Status: <span id="connectionStatus" class="font-medium">Checking...</span></p>
                </div>
            </div>
        </header>

        <!-- Configuration Section -->
        <div id="configSection" class="bg-white rounded-lg shadow-md p-4 border border-slate-200 mb-8 config-closed fade-in">
            <div id="configHeader" class="flex justify-between items-center cursor-pointer">
                <h2 class="text-lg font-semibold text-slate-800 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 text-amber-500"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path></svg>
                    Configuration
                </h2>
                <div class="flex items-center gap-3">
                    <div id="apiKeyStatus" class="w-4 h-4 rounded-full transition-colors tooltip" data-tooltip="API Key Status"></div>
                    <button id="configToggleBtn" class="p-1 rounded hover:bg-slate-100 transition-colors" aria-label="Toggle configuration">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-slate-500"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                </div>
            </div>
            <div id="configContent" class="pt-4 mt-4 border-t border-slate-200 hidden">
                <div class="space-y-4">
                    <div>
                        <label for="gtiApiKey" class="block text-sm font-medium text-slate-700 mb-1">Google Threat Intelligence API Key</label>
                        <div class="relative">
                            <input type="password" id="gtiApiKey" class="block w-full rounded-md border-slate-300 bg-slate-50 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm text-slate-900 pr-10" placeholder="Enter your GTI API Key" autocomplete="off">
                            <button type="button" id="toggleApiKeyVisibility" class="absolute inset-y-0 right-0 pr-3 flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 hover:text-slate-600"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                            </button>
                        </div>
                        <p class="text-xs text-slate-500 mt-1">Your API key is stored locally and never transmitted to external servers.</p>
                    </div>
                    <div class="flex justify-between items-center">
                        <button id="clearConfigBtn" class="text-sm text-red-600 hover:text-red-700 font-medium">Clear Stored Key</button>
                        <button id="saveConfigBtn" class="text-sm bg-indigo-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-indigo-500 transition-colors">Verify & Save API Key</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 fade-in">
            <!-- Card 1 -->
            <div class="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                <div class="flex items-center">
                    <div class="p-2 bg-blue-100 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-600"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.72"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.72-1.72"></path></svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-slate-500">URL Matches</p>
                        <p class="text-2xl font-bold text-slate-900" id="urlCount">0</p>
                    </div>
                </div>
            </div>
            <!-- Card 2 -->
            <div class="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                <div class="flex items-center">
                    <div class="p-2 bg-green-100 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-600"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-slate-500">File Hash Matches</p>
                        <p class="text-2xl font-bold text-slate-900" id="fileCount">0</p>
                    </div>
                </div>
            </div>
            <!-- Vulnerability Card -->
            <div class="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                <div class="flex items-center">
                    <div class="p-2 bg-purple-100 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-600"><path d="m8 2 1.88 1.88"></path><path d="M14.12 3.88 18 2"></path><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"></path><path d="M12 20c-3.3 0-6-2.7-6-6v-3a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3c0 3.3-2.7 6-6 6"></path><path d="M12 20v-9"></path><path d="M6.53 9C4.6 9.3 3 11 3 13"></path><path d="M20.47 9c1.9 0.3 3.5 2 3.5 4"></path></svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-slate-500">Vuln Matches</p>
                        <p class="text-2xl font-bold text-slate-900" id="vulnCount">0</p>
                    </div>
                </div>
            </div>
            <!-- Card 4 -->
            <div class="bg-white rounded-lg shadow-md p-4 border border-slate-200">
                <div class="flex items-center">
                    <div class="p-2 bg-red-100 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-600"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-slate-500">High Risk IOCs</p>
                        <p class="text-2xl font-bold text-slate-900" id="highRiskCount">-</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- URL Matches Table -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden mb-8 border border-slate-200 fade-in">
            <div class="flex justify-between items-center p-4 border-b border-slate-200">
                <h2 class="text-xl font-semibold text-slate-800 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 text-blue-500"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.72"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.72-1.72"></path></svg>
                    URL MATCHES
                </h2>
                <button id="refreshUrls" class="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path></svg>
                    Refresh
                </button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                    <thead class="bg-slate-100 text-xs text-slate-500 uppercase tracking-wider">
                        <tr>
                            <th class="table-cell">URL/IP</th>
                            <th class="table-cell">GTI Score</th>
                            <th class="table-cell">IOC Ingest Time</th>
                            <th class="table-cell">First Seen</th>
                            <th class="table-cell">Last Seen</th>
                            <th class="table-cell">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200" id="url-iocs-body">
                        <!-- Rows will be dynamically injected here -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Files Matches Table -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden mb-8 border border-slate-200 fade-in">
            <div class="flex justify-between items-center p-4 border-b border-slate-200">
                <h2 class="text-xl font-semibold text-slate-800 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 text-green-500"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    FILE HASH MATCHES
                </h2>
                <button id="refreshFiles" class="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path></svg>
                    Refresh
                </button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                    <thead class="bg-slate-100 text-xs text-slate-500 uppercase tracking-wider">
                        <tr>
                            <th class="table-cell">FILE HASH (SHA256)</th>
                            <th class="table-cell">GTI Score</th>
                            <th class="table-cell">IOC Ingest Time</th>
                            <th class="table-cell">First Seen</th>
                            <th class="table-cell">Last Seen</th>
                            <th class="table-cell">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200" id="file-iocs-body">
                       <!-- Rows will be dynamically injected here -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Vulnerability Matches Table -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden mb-8 border border-slate-200 fade-in">
            <div class="flex justify-between items-center p-4 border-b border-slate-200">
                <h2 class="text-xl font-semibold text-slate-800 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 text-purple-500"><path d="m8 2 1.88 1.88"></path><path d="M14.12 3.88 18 2"></path><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"></path><path d="M12 20c-3.3 0-6-2.7-6-6v-3a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3c0 3.3-2.7 6-6 6"></path><path d="M12 20v-9"></path><path d="M6.53 9C4.6 9.3 3 11 3 13"></path><path d="M20.47 9c1.9 0.3 3.5 2 3.5 4"></path></svg>
                    VULNERABILITY MATCHES
                </h2>
                <span class="text-xs text-slate-400">Static Data</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                    <thead class="bg-slate-100 text-xs text-slate-500 uppercase tracking-wider">
                        <tr>
                            <th class="table-cell">CVE ID</th>
                            <th class="table-cell">Risk</th>
                            <th class="table-cell">Description</th>
                            <th class="table-cell">Exploitation</th>
                            <th class="table-cell">In Wild</th>
                            <th class="table-cell">Published</th>
                            <th class="table-cell">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200" id="vulnerability-iocs-body">
                       <!-- Rows will be dynamically injected here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- GTI Widget Slider -->
    <div id="gtiSlider" style="width: 50vw;" class="fixed top-0 right-0 h-full bg-white shadow-2xl transform translate-x-full transition-transform duration-300 ease-in-out z-50 flex flex-col border-l border-slate-300">
        <div class="flex h-1.5 w-full flex-shrink-0">
            <div class="w-1/4 bg-blue-500"></div>
            <div class="w-1/4 bg-red-500"></div>
            <div class="w-1/4 bg-yellow-500"></div>
            <div class="w-1/4 bg-green-500"></div>
        </div>
        <div id="resizeHandle"></div>
        <div class="relative flex-grow">
            <div class="absolute top-2 right-3 flex gap-2 z-10">
                <button id="fullscreenGtiSlider" class="text-slate-400 hover:text-slate-800 text-xl font-bold tooltip" data-tooltip="Fullscreen" aria-label="Fullscreen widget">⛶</button>
                <button id="closeGtiSlider" class="text-slate-400 hover:text-slate-800 text-3xl font-bold" aria-label="Close widget">&times;</button>
            </div>
            <div id="gtiWidgetContainer" class="w-full h-full overflow-auto">
                <!-- Iframe will be added by JS -->
            </div>
        </div>
    </div>
    <div id="sliderOverlay" class="fixed inset-0 bg-black bg-opacity-40 hidden z-40 transition-opacity duration-300"></div>

    <!-- Vulnerability Details Slider -->
    <div id="vulnerabilitySlider" style="width: 50vw;" class="fixed top-0 right-0 h-full bg-white shadow-2xl transform translate-x-full transition-transform duration-300 ease-in-out z-50 flex flex-col border-l border-slate-300">
        <div class="flex h-1.5 w-full flex-shrink-0">
            <div class="w-1/4 bg-purple-500"></div>
            <div class="w-1/4 bg-purple-600"></div>
            <div class="w-1/4 bg-purple-700"></div>
            <div class="w-1/4 bg-purple-800"></div>
        </div>
        <div class="relative flex-grow">
            <div class="absolute top-2 right-3 flex gap-2 z-10">
                <button id="closeVulnerabilitySlider" class="text-slate-400 hover:text-slate-800 text-3xl font-bold" aria-label="Close widget">&times;</button>
            </div>
            <div id="vulnerabilityWidgetContainer" class="w-full h-full overflow-auto p-6">
                <!-- Vulnerability details will be rendered here by JS -->
            </div>
        </div>
    </div>
    <div id="vulnSliderOverlay" class="fixed inset-0 bg-black bg-opacity-40 hidden z-40 transition-opacity duration-300"></div>

    <script src="js/data.js"></script>
    <script src="js/script.js"></script>
</body>
</html>
'''

# 2. CSS Content for style.css
css_content = r'''
body {
    font-family: 'Inter', sans-serif;
    background-color: #f1f5f9;
}
.table-cell {
    padding: 0.75rem 1rem;
    vertical-align: middle;
}
.indicator-link {
    color: #2563eb;
    cursor: pointer;
    text-decoration: none;
    word-break: break-all;
    transition: color 0.2s;
}
.indicator-link:hover {
    text-decoration: underline;
    color: #1d4ed8;
}
.gti-logo-link {
    cursor: pointer;
}
.gti-logo {
    width: 1.25rem;
    height: 1.25rem;
    transition: transform 0.2s;
}
.gti-logo-link:hover .gti-logo {
    transform: scale(1.1);
}
#configToggleBtn svg {
    transition: transform 0.3s ease;
}
.config-closed #configToggleBtn svg {
    transform: rotate(-90deg);
}
@keyframes pulse {
    50% { opacity: .6; }
}
.status-orange {
    animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
#resizeHandle {
    position: absolute;
    left: -5px;
    top: 0;
    height: 100%;
    width: 10px;
    cursor: col-resize;
    z-index: 100;
}
#resizeHandle:hover {
    background-color: rgba(79, 70, 229, 0.5);
}
.loading-skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}
@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
.fade-in {
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.tooltip {
    position: relative;
}
.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #374151;
    color: white;
    padding: 0.5rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
    z-index: 1000;
}
.tooltip:hover::after {
    opacity: 1;
}
.score-badge {
    transition: all 0.2s ease;
}
.score-badge:hover {
    transform: scale(1.05);
}
.risk-critical {
    background-color: #ef4444; /* red-500 */
    color: white;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
@media (max-width: 768px) {
    #gtiSlider {
        width: 100vw !important;
    }
    .table-cell {
        padding: 0.5rem;
        font-size: 0.875rem;
    }
}
'''

# 3. JavaScript Content for data.js
data_js_content = r'''
// --- Static Data ---
const urlIocs = [
    { id: "https://skyslope.com@securedatas.info/verification/verifyuridentityonline?email=info@isrreports.com", ingest: "30 Mins Ago", first: "5 Days Ago", last: "5 Days Ago" },
    { id: "http://tracking.mimeeting.net/tracking/botclick?msgid=f1QnWpG_gxeGDySH5dpYYQ2&c=1952454385774808418", ingest: "1 Hour Ago", first: "1 Hour Ago", last: "1 Hour Ago" },
    { id: "https://196.251.117.226:7117/gate/", ingest: "14 Hours Ago", first: "3 Hours Ago", last: "1 Day Ago" }
];

const fileIocs = [
    { id: "9432b623f19a6980256123fbc4c5c6f27be5fbfb8ea67ee577af6d651ebc3649", ingest: "2 Hours Ago", first: "13 Days Ago", last: "13 Days Ago" },
    { id: "1c783c253435b450cbd2eeb01830eca20d71145bd63c1cdbe655d88f4d65143d", ingest: "1 Hours Ago", first: "2 Day Ago", last: "2 Hours Ago" },
    { id: "72b5838dfa34b7d405d664c48e9b4aee72b4e10ac5f9f4cc124045dcd6d311a8", ingest: "1 Day Ago", first: "1 Month Ago", last: "1 Month Ago" }
];

const vulnerabilityIocs = [
    { 
        cve: "CVE-2025-31324",
        updated: "6 days ago",
        published: "2025-04-22",
        mve: "MVE-2025-10681",
        description: "An Improper Authorization vulnerability exists that, when exploited, allows a remote attacker to execute arbitrary code.",
        risk: "CRITICAL",
        exploitState: "Confirmed",
        inWild: true,
        iocs: 12
    },
    { 
        cve: "CVE-2024-1709",
        updated: "8 days ago",
        published: "2024-02-19",
        mve: "MVE-2024-2354",
        description: "An Authentication Bypass vulnerability exists that, when exploited, allows a remote attacker to obtain unauthorized access.",
        risk: "CRITICAL",
        exploitState: "Wide",
        inWild: true,
        iocs: 8
    },
    { 
        cve: "CVE-2023-46805",
        updated: "8 days ago",
        published: "2024-01-10",
        mve: "MVE-2023-25396",
        description: "A Path Traversal vulnerability exists that, when exploited, allows a remote attacker to obtain unauthorized access.",
        risk: "CRITICAL",
        exploitState: "Wide",
        inWild: true,
        iocs: 11
    }
];
'''

# 4. JavaScript Content for script.js
script_js_content = r'''
document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const gtiApiKeyInput = document.getElementById('gtiApiKey');
    const saveConfigBtn = document.getElementById('saveConfigBtn');
    const clearConfigBtn = document.getElementById('clearConfigBtn');
    const toggleApiKeyVisibilityBtn = document.getElementById('toggleApiKeyVisibility');
    const gtiSlider = document.getElementById('gtiSlider');
    const closeGtiSliderBtn = document.getElementById('closeGtiSlider');
    const fullscreenGtiSliderBtn = document.getElementById('fullscreenGtiSlider');
    const gtiWidgetContainer = document.getElementById('gtiWidgetContainer');
    const sliderOverlay = document.getElementById('sliderOverlay');
    const configSection = document.getElementById('configSection');
    const configHeader = document.getElementById('configHeader');
    const configContent = document.getElementById('configContent');
    const apiKeyStatus = document.getElementById('apiKeyStatus');
    const resizeHandle = document.getElementById('resizeHandle');
    const mainContent = document.getElementById('mainContent');
    const urlIocsBody = document.getElementById('url-iocs-body');
    const fileIocsBody = document.getElementById('file-iocs-body');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const currentDate = document.getElementById('currentDate');
    const connectionStatus = document.getElementById('connectionStatus');
    const refreshUrlsBtn = document.getElementById('refreshUrls');
    const refreshFilesBtn = document.getElementById('refreshFiles');
    const highRiskCount = document.getElementById('highRiskCount');
    const urlCountEl = document.getElementById('urlCount');
    const fileCountEl = document.getElementById('fileCount');
    const vulnCountEl = document.getElementById('vulnCount');
    const vulnerabilityIocsBody = document.getElementById('vulnerability-iocs-body');
    const vulnerabilitySlider = document.getElementById('vulnerabilitySlider');
    const closeVulnerabilitySliderBtn = document.getElementById('closeVulnerabilitySlider');
    const vulnerabilityWidgetContainer = document.getElementById('vulnerabilityWidgetContainer');
    const vulnSliderOverlay = document.getElementById('vulnSliderOverlay');
    
    let isKeyVerified = false;
    let highRiskCounter = 0;

    // --- Utility Functions ---
    const formatCurrentDate = () => {
        const now = new Date();
        return now.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const updateConnectionStatus = (status) => {
        const statusColors = {
            'connected': 'text-green-600',
            'disconnected': 'text-red-600',
            'checking': 'text-amber-600'
        };
        connectionStatus.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        connectionStatus.className = `font-medium ${statusColors[status] || 'text-slate-600'}`;
    };

    const showLoading = (show = true) => {
        loadingSpinner.classList.toggle('hidden', !show);
    };

    const copyToClipboard = async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            showCustomAlert('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
            showCustomAlert('Failed to copy to clipboard', 'error');
        }
    };

    function showCustomAlert(message, type = 'info') {
        document.querySelectorAll('.custom-alert').forEach(e => e.remove());
        const alertColors = { 
            success: 'bg-green-500 text-white', 
            error: 'bg-red-500 text-white',
            warning: 'bg-amber-500 text-white',
            info: 'bg-blue-500 text-white'
        };
        const alertDiv = document.createElement('div');
        alertDiv.className = `custom-alert fixed top-5 right-5 py-2 px-4 rounded-lg shadow-lg text-sm z-50 ${alertColors[type]} fade-in`;
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        setTimeout(() => { 
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 4000);
    }

    // --- UI Handlers (IOCs) ---
    const createIocRow = (ioc) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-100/60 transition-colors duration-200';
        tr.setAttribute('data-indicator', ioc.id);
        
        const truncatedId = ioc.id.length > 60 ? ioc.id.substring(0, 60) + '...' : ioc.id;
        
        tr.innerHTML = `
            <td class="table-cell">
                <div class="flex items-center space-x-2">
                    <a href="#" class="indicator-link gti-trigger tooltip" data-tooltip="Click to view in GTI widget">${truncatedId}</a>
                    <button class="copy-btn text-slate-400 hover:text-slate-600 tooltip" data-tooltip="Copy full IOC" data-copy="${ioc.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                    </button>
                </div>
            </td>
            <td class="table-cell score-cell">
                <span class="text-xs font-semibold px-2 py-1 rounded-full bg-slate-200 text-slate-600 loading-skeleton score-badge">...</span>
            </td>
            <td class="table-cell">${ioc.ingest}</td>
            <td class="table-cell">${ioc.first}</td>
            <td class="table-cell">${ioc.last}</td>
            <td class="table-cell">
                <div class="flex space-x-2">
                    <button class="gti-trigger text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded hover:bg-indigo-200 transition-colors">View Details</button>
                </div>
            </td>
        `;
        return tr;
    };

    const populateIocTables = () => {
        urlIocsBody.innerHTML = '';
        fileIocsBody.innerHTML = '';
        urlIocs.forEach(ioc => urlIocsBody.appendChild(createIocRow(ioc)));
        fileIocs.forEach(ioc => fileIocsBody.appendChild(createIocRow(ioc)));
        
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                copyToClipboard(btn.dataset.copy);
            });
        });
    };

    const enrichRow = async (row, apiKey) => {
        const indicator = row.dataset.indicator;
        const scoreCell = row.querySelector('.score-cell');
        const scoreBadge = scoreCell.querySelector('.score-badge');
        const endpoint = `https://www.virustotal.com/api/v3/gtiwidget?query=${encodeURIComponent(indicator)}`;
        
        try {
            const response = await fetch(endpoint, {
                headers: { 'x-apikey': apiKey, 'x-tool': 'Your_Product-siem-demo' }
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            
            if (data.data && data.data.url) {
                row.setAttribute('data-widget-url', data.data.url);
            }

            let score = data.data?.gti_assessment?.threat_score?.value;
            if (score !== undefined) {
                let colorClass = 'bg-green-200 text-green-800';
                if (score >= 30) {
                    colorClass = 'bg-red-200 text-red-800';
                    highRiskCounter++;
                } else if (score >= 2) {
                    colorClass = 'bg-amber-200 text-amber-800';
                }
                scoreBadge.className = `text-xs font-bold px-2 py-1 rounded-full ${colorClass} score-badge`;
                scoreBadge.textContent = score;
                scoreBadge.onclick = (e) => {
                    e.preventDefault();
                    const widgetUrl = row.dataset.widgetUrl;
                    openGtiSlider(indicator, widgetUrl);
                };
            } else {
                scoreBadge.className = 'text-xs font-semibold px-2 py-1 rounded-full bg-slate-200 text-slate-600 score-badge';
                scoreBadge.textContent = 'N/A';
            }
            scoreBadge.classList.remove('loading-skeleton');
        } catch (error) {
            console.error(`Enrichment failed for ${indicator}:`, error);
            scoreBadge.className = 'text-xs font-semibold px-2 py-1 rounded-full bg-gray-200 text-gray-600 score-badge';
            scoreBadge.textContent = 'Error';
            scoreBadge.title = error.message;
            scoreBadge.classList.remove('loading-skeleton');
        }
    };
    
    const enrichAllIocRows = async (apiKey) => {
        showLoading(true);
        highRiskCounter = 0;
        const rows = document.querySelectorAll('tr[data-indicator]');
        
        for (let i = 0; i < rows.length; i++) {
            await enrichRow(rows[i], apiKey);
            if (i < rows.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 200));
            }
        }
        
        highRiskCount.textContent = highRiskCounter;
        showLoading(false);
    };

    // --- UI Handlers (Vulnerabilities) ---
    const createVulnerabilityRow = (vuln) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-100/60 transition-colors duration-200';
        tr.innerHTML = `
            <td class="table-cell font-mono text-slate-700">${vuln.cve}</td>
            <td class="table-cell"><span class="risk-critical">${vuln.risk}</span></td>
            <td class="table-cell text-slate-600">${vuln.description}</td>
            <td class="table-cell font-medium">${vuln.exploitState}</td>
            <td class="table-cell font-medium">${vuln.inWild ? 'Yes' : 'No'}</td>
            <td class="table-cell">${vuln.published}</td>
            <td class="table-cell">
                <button class="vuln-details-trigger text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded hover:bg-purple-200 transition-colors" data-cve-id="${vuln.cve}">
                    Enrich
                </button>
            </td>
        `;
        return tr;
    };

    const populateVulnerabilitiesTable = () => {
        vulnerabilityIocsBody.innerHTML = '';
        vulnerabilityIocs.forEach(vuln => {
            vulnerabilityIocsBody.appendChild(createVulnerabilityRow(vuln));
        });
    };
    
    const openVulnerabilitySlider = async (cveId) => {
        if (!isKeyVerified) {
            showCustomAlert('A valid GTI API Key is required to enrich vulnerabilities.', 'error');
            return;
        }

        vulnerabilitySlider.classList.remove('translate-x-full');
        vulnSliderOverlay.classList.remove('hidden');
        mainContent.style.paddingRight = `${vulnerabilitySlider.offsetWidth}px`;

        vulnerabilityWidgetContainer.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-slate-600">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mb-4"></div>
                <span class="text-sm font-medium">Enriching ${cveId}...</span>
                <span class="text-xs text-slate-400 mt-1">Fetching latest intelligence from Google TI</span>
            </div>`;

        const apiKey = localStorage.getItem('gti_apiKey');
        const objectId = `vulnerability--${cveId.toLowerCase()}`;
        const url = `https://www.virustotal.com/api/v3/collections/${objectId}`;

        try {
            const response = await fetch(url, { headers: { 'x-apikey': apiKey } });

            if (!response.ok) {
                let errorMsg = `Error: ${response.status}. Could not fetch data.`;
                if (response.status === 403) {
                    errorMsg = "Access Denied. Vulnerability Intelligence requires a Google TI Enterprise or Enterprise Plus license.";
                } else if (response.status === 404) {
                    errorMsg = `Vulnerability ${cveId} not found in Google's intelligence database.`;
                }
                throw new Error(errorMsg);
            }

            const json = await response.json();
            const data = json.data.attributes;
            const references = data.references?.map(ref => `<li><a href="${ref.url}" target="_blank" rel="noopener noreferrer" class="text-indigo-600 hover:underline">${ref.url}</a></li>`).join('') || '<li>No references found.</li>';

            vulnerabilityWidgetContainer.innerHTML = `
                <h2 class="text-2xl font-bold text-slate-900">${data.cve_id}</h2>
                <p class="text-sm text-slate-500 mb-4">Last Modified: ${new Date(data.last_modification_date * 1000).toDateString()}</p>
                
                <div class="prose prose-sm max-w-none">
                    <p class="lead">${data.description}</p>
                    <hr>
                    <h3 class="font-semibold">References</h3>
                    <ul class="list-disc pl-5 space-y-1">${references}</ul>
                </div>
            `;

        } catch (error) {
             vulnerabilityWidgetContainer.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full text-red-600 bg-red-50 p-4 rounded-lg">
                     <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-3"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    <h3 class="text-lg font-bold mb-2">Enrichment Failed</h3>
                    <p class="text-sm text-center text-red-700">${error.message}</p>
                </div>`;
        }
    };

    const closeVulnerabilitySlider = () => {
        vulnerabilitySlider.classList.add('translate-x-full');
        vulnSliderOverlay.classList.add('hidden');
        mainContent.style.paddingRight = '';
    };

    // --- Config and API Key Logic ---
    const setStatusIndicator = (status, message) => {
        apiKeyStatus.classList.remove('bg-red-500', 'bg-amber-500', 'bg-green-500', 'status-orange');
        let colorClass = '';
        switch (status) {
            case 'verified': 
                colorClass = 'bg-green-500'; 
                isKeyVerified = true;
                updateConnectionStatus('connected');
                break;
            case 'verifying': 
                colorClass = 'bg-amber-500'; 
                apiKeyStatus.classList.add('status-orange'); 
                isKeyVerified = false;
                updateConnectionStatus('checking');
                break;
            default: 
                colorClass = 'bg-red-500'; 
                isKeyVerified = false;
                updateConnectionStatus('disconnected');
                break;
        }
        apiKeyStatus.classList.add(colorClass);
        apiKeyStatus.setAttribute('data-tooltip', message);
    };

    const toggleConfig = () => {
        configContent.classList.toggle('hidden');
        configSection.classList.toggle('config-closed');
    };

    const verifyApiKey = async (apiKey) => {
        if (!apiKey) {
            setStatusIndicator('error', 'API Key not provided.');
            return false;
        }
        setStatusIndicator('verifying', 'Verifying API Key...');
        try {
            const response = await fetch(`https://www.virustotal.com/api/v3/ip_addresses/8.8.8.8`, {
                headers: { 'x-apikey': apiKey }
            });
            if (response.ok) {
                setStatusIndicator('verified', 'API Key is valid and saved.');
                localStorage.setItem('gti_apiKey', apiKey);
                showCustomAlert('API Key verified and saved!', 'success');
                if (!configContent.classList.contains('hidden')) toggleConfig();
                await enrichAllIocRows(apiKey);
                return true;
            } else {
                 setStatusIndicator('error', 'API Key is invalid.');
                 localStorage.removeItem('gti_apiKey');
                 isKeyVerified = false;
                 showCustomAlert('Invalid API Key. Please try again.', 'error');
                 return false;
            }
        } catch (error) {
            console.error("API Key verification failed:", error);
            setStatusIndicator('error', 'Could not verify API Key.');
            showCustomAlert('An error occurred during verification.', 'error');
            return false;
        }
    };

    const clearApiKey = () => {
        localStorage.removeItem('gti_apiKey');
        gtiApiKeyInput.value = '';
        setStatusIndicator('error', 'API Key cleared.');
        isKeyVerified = false;
        showCustomAlert('API Key cleared successfully.', 'success');
        
        document.querySelectorAll('.score-badge').forEach(badge => {
            badge.className = 'text-xs font-semibold px-2 py-1 rounded-full bg-slate-200 text-slate-600 score-badge';
            badge.textContent = '...';
        });
        highRiskCount.textContent = '-';
    };

    const toggleApiKeyVisibility = () => {
        const input = gtiApiKeyInput;
        const button = toggleApiKeyVisibilityBtn;
        if (input.type === 'password') {
            input.type = 'text';
            button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 hover:text-slate-600"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>';
        } else {
            input.type = 'password';
            button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 hover:text-slate-600"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
        }
    };

    // --- Slider Logic (GTI) ---
    const openGtiSlider = (indicator, widgetUrl) => {
        if (!isKeyVerified) {
            showCustomAlert('A valid GTI API Key is required.', 'error');
            if (configContent.classList.contains('hidden')) toggleConfig();
            gtiApiKeyInput.focus();
            return;
        }
        
        if (!widgetUrl) {
            showCustomAlert('Report URL not available. It might still be loading.', 'warning');
            return;
        }
        
        gtiSlider.classList.remove('translate-x-full');
        sliderOverlay.classList.remove('hidden');
        mainContent.style.paddingRight = `${gtiSlider.offsetWidth}px`;

        gtiWidgetContainer.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-slate-600">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-4"></div>
                <span class="text-sm">Loading GTI widget...</span>
                <span class="text-xs text-slate-400 mt-2">Analyzing: ${indicator.length > 50 ? indicator.substring(0, 50) + '...' : indicator}</span>
            </div>
        `;
        
        setTimeout(() => {
            const iframe = document.createElement('iframe');
            iframe.id = 'gtiWidget';
            iframe.className = 'w-full h-full border-0';
            iframe.sandbox = 'allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-forms';
            iframe.src = widgetUrl;
            gtiWidgetContainer.innerHTML = '';
            gtiWidgetContainer.appendChild(iframe);
        }, 100);
    };

    const closeGtiSlider = () => {
        gtiSlider.classList.add('translate-x-full');
        sliderOverlay.classList.add('hidden');
        mainContent.style.paddingRight = '';
        setTimeout(() => { gtiWidgetContainer.innerHTML = ''; }, 300);
    };

    // --- Event Listeners Setup ---
    configHeader.addEventListener('click', toggleConfig);
    saveConfigBtn.addEventListener('click', () => verifyApiKey(gtiApiKeyInput.value.trim()));
    clearConfigBtn.addEventListener('click', clearApiKey);
    toggleApiKeyVisibilityBtn.addEventListener('click', toggleApiKeyVisibility);
    closeGtiSliderBtn.addEventListener('click', closeGtiSlider);
    sliderOverlay.addEventListener('click', closeGtiSlider);
    closeVulnerabilitySliderBtn.addEventListener('click', closeVulnerabilitySlider);
    vulnSliderOverlay.addEventListener('click', closeVulnerabilitySlider);

    refreshUrlsBtn.addEventListener('click', () => {
        if (isKeyVerified) enrichAllIocRows(localStorage.getItem('gti_apiKey'));
        else showCustomAlert('Please configure a valid API key first.', 'warning');
    });
    refreshFilesBtn.addEventListener('click', () => {
        if (isKeyVerified) enrichAllIocRows(localStorage.getItem('gti_apiKey'));
        else showCustomAlert('Please configure a valid API key first.', 'warning');
    });
    
    document.body.addEventListener('click', function(event) {
        const gtiTrigger = event.target.closest('.gti-trigger');
        if (gtiTrigger) {
            event.preventDefault();
            const row = gtiTrigger.closest('tr[data-indicator]');
            if (row) {
                const indicator = row.dataset.indicator;
                const widgetUrl = row.dataset.widgetUrl;
                openGtiSlider(indicator, widgetUrl);
            }
        }
        const vulnTrigger = event.target.closest('.vuln-details-trigger');
        if (vulnTrigger) {
            event.preventDefault();
            const cveId = vulnTrigger.dataset.cveId;
            openVulnerabilitySlider(cveId);
        }
    });

    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            if (!gtiSlider.classList.contains('translate-x-full')) closeGtiSlider();
            if (!vulnerabilitySlider.classList.contains('translate-x-full')) closeVulnerabilitySlider();
        }
    });
    
    // --- Initial Load ---
    const init = async () => {
        currentDate.textContent = formatCurrentDate();
        
        populateIocTables();
        populateVulnerabilitiesTable();

        urlCountEl.textContent = urlIocs.length;
        fileCountEl.textContent = fileIocs.length;
        vulnCountEl.textContent = vulnerabilityIocs.length;
        
        const savedApiKey = localStorage.getItem('gti_apiKey');
        if (savedApiKey) {
            gtiApiKeyInput.value = savedApiKey;
            await verifyApiKey(savedApiKey);
        } else {
            setStatusIndicator('error', 'API Key not provided.');
            updateConnectionStatus('disconnected');
        }
    };
    
    init();
});
'''

# --- Script to Build Project ---
def create_project_structure():
    """Creates the necessary directories and files for the web app."""
    print("Building project structure...")

    # Create directories
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    print("Directories 'css' and 'js' created.")

    # File paths
    files_to_create = {
        "index.html": html_content,
        os.path.join("css", "style.css"): css_content,
        os.path.join("js", "data.js"): data_js_content,
        os.path.join("js", "script.js"): script_js_content
    }

    # Write content to files
    for path, content in files_to_create.items():
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully created {path}")
        except IOError as e:
            print(f"Error writing to file {path}: {e}")

    print("\nProject build complete!")
    print("You can now open 'index.html' in your browser.")

if __name__ == "__main__":
    create_project_structure()