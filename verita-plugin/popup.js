document.getElementById("selectBtn").addEventListener("click", async () => {
    const resultBox = document.getElementById("result");

    // injeta o script de seleção na aba ativa
    await chrome.scripting.executeScript({
        target: { tabId: (await chrome.tabs.query({ active: true, lastFocusedWindow: true }))[0].id },
        files: ["selector.js"]
    });

    resultBox.textContent = "Modo de seleção ativado — clique em algum elemento...";
});
chrome.runtime.onMessage.addListener((req) => {
    if (req.action === "resultadoAPI") {
        document.getElementById("result").textContent =
            JSON.stringify(req.result, null, 2);
    }
});
