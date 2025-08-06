
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
