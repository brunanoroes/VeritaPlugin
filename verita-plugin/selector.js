// evita múltiplas ativações
if (window.veritapluginSelecting) {
    alert("Seleção já está ativa.");
    return;
}
window.veritapluginSelecting = true;

let lastEl = null;

// destaque azul ao passar o mouse
function highlight(e) {
    if (lastEl) lastEl.style.outline = "";
    lastEl = e.target;
    lastEl.style.outline = "2px solid #4A90E2";
}

function select(e) {
    e.preventDefault();
    e.stopPropagation();

    document.removeEventListener("mouseover", highlight);
    document.removeEventListener("click", select, true);

    if (lastEl) lastEl.style.outline = "";

    window.veritapluginSelecting = false;

    const text = (e.target.innerText || "").trim();

    chrome.runtime.sendMessage({
        action: "analisarTexto",
        message: text
    });

    alert("Elemento capturado! Enviando para análise...");
}

document.addEventListener("mouseover", highlight);
document.addEventListener("click", select, true);
