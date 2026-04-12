console.log("VeritaPlugin carregado - botão flutuante ativado.");

// ── BOOTSTRAP ────────────────────────────────────────────────────────────────

function injectBootstrap() {
    if (document.getElementById("veritaplugin-bootstrap")) return;
    const link = document.createElement("link");
    link.id   = "veritaplugin-bootstrap";
    link.rel  = "stylesheet";
    link.href = chrome.runtime.getURL("bootstrap.min.css");
    document.head.appendChild(link);
}


// ── BOTÃO FLUTUANTE ───────────────────────────────────────────────────────────

function injectFloatingButton() {
    if (document.getElementById("veritaplugin-floating-btn")) return;

    const btn = document.createElement("button");
    btn.id        = "veritaplugin-floating-btn";
    btn.innerText = "Analisar Post";
    btn.className = "btn btn-primary fw-semibold shadow position-fixed";

    // Apenas o que Bootstrap não cobre com classes
    btn.style.bottom = "20px";
    btn.style.right  = "20px";
    btn.style.zIndex = "999999999";

    document.body.appendChild(btn);
    console.log("Botão VeritaPlugin injetado na página.");

    btn.onclick = () => startSelectionMode();
}


// ── MODO DE SELEÇÃO ───────────────────────────────────────────────────────────

function startSelectionMode() {
    alert("Modo de seleção ativado! Clique em qualquer elemento para analisar.");

    const highlight   = (el) => { el.style.outline = "3px solid red"; };
    const unhighlight = (el) => { el.style.outline = ""; };

    const onMouseOver = (e) => highlight(e.target);
    const onMouseOut  = (e) => unhighlight(e.target);

    const onClick = (e) => {
        e.preventDefault();
        e.stopPropagation();

        document.removeEventListener("mouseover", onMouseOver);
        document.removeEventListener("mouseout",  onMouseOut);
        document.removeEventListener("click",     onClick, true);

        showLoadingOverlay();

        chrome.runtime.sendMessage(
            { action: "analisarTexto", message: e.target.innerText || "" },
            (response) => {
                hideLoadingOverlay();
                if (!response) { alert("Erro: sem resposta."); return; }
                showVeritaPluginResult(response.result);
            }
        );
    };

    document.addEventListener("mouseover", onMouseOver);
    document.addEventListener("mouseout",  onMouseOut);
    document.addEventListener("click",     onClick, true);
}


// ── MODAL DE RESULTADO ────────────────────────────────────────────────────────

function showVeritaPluginResult(data) {
    injectBootstrap();

    const old = document.getElementById("veritaplugin-modal");
    if (old) old.remove();

    const eSeguro    = data.categoria === "Seguro";
    const alertClass = eSeguro ? "alert-success" : "alert-warning";
    const icon       = eSeguro ? "✓" : "⚠";
    const title      = eSeguro ? "SEGURO" : "ATENÇÃO";
    const subtitle   = eSeguro
        ? "Ameaças não foram detectadas"
        : `Possível golpe de '${data.categoria}'`;

    const modal = document.createElement("div");
    modal.id        = "veritaplugin-modal";
    modal.className = "position-fixed top-50 start-50 translate-middle";
    modal.style.zIndex = "999999999999";
    modal.style.width  = "300px";

    modal.innerHTML = `
        <div class="card shadow">
            <div class="card-body p-3">

                <!-- Header -->
                <div class="d-flex align-items-center gap-2 mb-3 fw-bold text-primary">
                    🛡️ VeritaPlugin
                </div>

                <!-- Status -->
                <div class="alert ${alertClass} d-flex align-items-center gap-2 py-2 px-3 mb-3">
                    <span class="fw-bold fs-5">${icon}</span>
                    <div>
                        <div class="fw-bold">${title}</div>
                        <div class="small">${subtitle}</div>
                    </div>
                </div>

                <!-- Explicação -->
                <div class="card bg-light mb-2">
                    <div class="card-body py-2 px-3">
                        <div class="fw-bold small">Explicação:</div>
                        <div class="small text-secondary">${data.explicacao || "—"}</div>
                    </div>
                </div>

                <!-- Base legal -->
                <div class="card bg-light mb-2">
                    <div class="card-body py-2 px-3">
                        <div class="fw-bold small">Base legal:</div>
                        <div class="small text-secondary">${data.baseLegal || "—"}</div>
                    </div>
                </div>

                <!-- Ações recomendadas -->
                <div class="card bg-light mb-3">
                    <div class="card-body py-2 px-3">
                        <div class="fw-bold small">Ações recomendadas:</div>
                        <div class="small text-secondary">${data.acaoRecomendada || "—"}</div>
                    </div>
                </div>

                <!-- Botão fechar -->
                <button id="veritaplugin-close-btn" class="btn btn-primary w-100">
                    Fechar
                </button>

            </div>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById("veritaplugin-close-btn").onclick = () => modal.remove();
}


// ── LOADING OVERLAY ───────────────────────────────────────────────────────────

function showLoadingOverlay() {
    if (document.getElementById("veritaplugin-loading")) return;
    injectBootstrap();

    const overlay = document.createElement("div");
    overlay.id        = "veritaplugin-loading";
    overlay.className = "position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-dark bg-opacity-50";
    overlay.style.zIndex        = "9999999999999";
    overlay.style.backdropFilter = "blur(2px)";

    overlay.innerHTML = `
        <div class="spinner-border text-light" style="width:3.5rem;height:3.5rem;" role="status">
            <span class="visually-hidden">Carregando...</span>
        </div>
    `;

    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById("veritaplugin-loading");
    if (overlay) overlay.remove();
}


// ── INICIALIZAÇÃO ─────────────────────────────────────────────────────────────

setTimeout(injectFloatingButton, 1500);
