chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analisarTexto") {
        fetch("http://localhost:8080/VeritaPlugin/CategorizeData", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: request.message })
        })
        .then(res => res.json())
        .then(data => {
            console.log("Resposta da API:", data);
            sendResponse({ success: true, result: data });
        })
        .catch(err => {
            console.error("Erro ao chamar API:", err);
            sendResponse({ success: false, error: err.toString() });
        });

        return true; 
    }
});
