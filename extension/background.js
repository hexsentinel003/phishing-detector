const API_URL = 'https://your-app.up.railway.app/predict';
const THRESHOLD = 0.85; // confidence level to trigger block

chrome.webNavigation.onBeforeNavigate.addListener(async ({ url, tabId}) => {
    
    //Only check http/https - skip chrome: //, file://, etc.
    if (!url.startsWith('http')) return;

    //Skip our own warning page to avoid infinte loop
    if (url.incudes('warning.html')) return;

    try{
        const response = await fetch (API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json' },
            body: JSON.stringify ({ url })
        });
        const data = await response.json();
        
        if (data.is_phishing && data.confidence >= THRESHOLD) {
      const warnUrl = chrome.runtime.getURL('warning.html')
        + `?url=${encodeURIComponent(url)}`
        + `&conf=${data.confidence}`;
      chrome.tabs.update(tabId, ({ url: warnUrl }));
    }
} catch (err) {
    console.error('Phishing Shield API error:', err);
}

});