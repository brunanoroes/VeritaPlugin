chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === "install") {
        chrome.tabs.create({ url: chrome.runtime.getURL("setup.html") });
    }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analisarTexto") {
        chrome.storage.local.get("openaiKey", ({ openaiKey }) => {
            fetch("http://localhost:8080/VeritaPlugin/CategorizeData", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: request.message, api_key: openaiKey || "" })
            })
            .then(res => {
                if (!res.ok) throw new Error(`Erro da API: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log("Resposta da API:", data);
                sendResponse({ success: true, result: data });
            })
            .catch(err => {
                console.error("Erro ao chamar API:", err);
                sendResponse({ success: false, error: err.message });
            });
        });

        return true;
    }
});
