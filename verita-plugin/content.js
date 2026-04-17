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
    injectBootstrap();

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


// ── TOAST ─────────────────────────────────────────────────────────────────────

function showToast(mensagem, tipo = "info") {
    injectBootstrap();

    const old = document.getElementById("veritaplugin-toast");
    if (old) old.remove();

    const cores = {
        info:  { bg: "#e8f0fe", border: "#1877F2", icon: "ℹ️", texto: "#1558c0" },
        erro:  { bg: "#fdecea", border: "#c0392b", icon: "✗",  texto: "#c0392b" },
    };
    const c = cores[tipo] || cores.info;

    const toast = document.createElement("div");
    toast.id = "veritaplugin-toast";
    toast.style.cssText = `
        position: fixed;
        top: 24px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 99999999999;
        background: ${c.bg};
        border: 1.5px solid ${c.border};
        border-radius: 12px;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.13);
        font-family: Arial, sans-serif;
        font-size: 0.92rem;
        color: ${c.texto};
        font-weight: 600;
        max-width: 420px;
        animation: verita-fadein .2s ease;
    `;

    toast.innerHTML = `
        <img src="${chrome.runtime.getURL('icon.png')}" style="width:22px;height:22px;object-fit:contain;flex-shrink:0;">
        <span>${mensagem}</span>
    `;

    if (!document.getElementById("veritaplugin-toast-style")) {
        const style = document.createElement("style");
        style.id = "veritaplugin-toast-style";
        style.textContent = `
            @keyframes verita-fadein { from { opacity:0; top:10px; } to { opacity:1; top:24px; } }
            @keyframes verita-fadeout { from { opacity:1; } to { opacity:0; } }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    if (tipo === "info") {
        setTimeout(() => {
            toast.style.animation = "verita-fadeout .3s ease forwards";
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}


// ── MODO DE SELEÇÃO ───────────────────────────────────────────────────────────

function startSelectionMode() {
    injectBootstrap();

    // Toast com botão cancelar
    const oldToast = document.getElementById("veritaplugin-toast");
    if (oldToast) oldToast.remove();

    const toast = document.createElement("div");
    toast.id = "veritaplugin-toast";
    toast.style.cssText = `
        position: fixed;
        top: 24px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 99999999999;
        background: #e8f0fe;
        border: 1.5px solid #1877F2;
        border-radius: 12px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.13);
        font-family: Arial, sans-serif;
        font-size: 0.92rem;
        color: #1558c0;
        font-weight: 600;
        max-width: 460px;
    `;
    toast.innerHTML = `
        <img src="${chrome.runtime.getURL('icon.png')}" style="width:40px;height:40px;object-fit:contain;flex-shrink:0;">
        <span>Clique em qualquer publicação para analisar.</span>
        <button id="veritaplugin-cancel-btn" style="
            margin-left:8px;background:#e53935;border:none;
            border-radius:8px;color:#fff;font-size:0.85rem;font-weight:700;
            padding:6px 14px;cursor:pointer;white-space:nowrap;flex-shrink:0;
            box-shadow: 0 2px 6px rgba(229,57,53,0.3);
        ">✕ Sair da seleção</button>
    `;
    document.body.appendChild(toast);

    const highlight = (el) => {
        if (el.innerText && el.innerText.trim().length > 0) {
            el.style.outline = "3px solid #1877F2";
            el.style.borderRadius = "6px";
            el.classList.add("border", "border-primary", "bg-primary-subtle", "text-primary-emphasis", "rounded", "p-2");
        }
    };

    const unhighlight = (el) => {
        el.style.outline = "";
        el.style.borderRadius = "";
        el.classList.remove("border", "border-primary", "bg-primary-subtle", "text-primary-emphasis", "rounded", "p-2");
    };
    const onMouseOver = (e) => highlight(e.target);
    const onMouseOut  = (e) => unhighlight(e.target);

    function cancelar() {
        document.removeEventListener("mouseover", onMouseOver);
        document.removeEventListener("mouseout",  onMouseOut);
        document.removeEventListener("click",     onClick, true);
        document.removeEventListener("keydown",   onKeyDown);
        // Remove outline de qualquer elemento que ainda esteja destacado
        document.querySelectorAll("[style*='outline']").forEach(el => el.style.outline = "");
        toast.remove();
    }

    function onKeyDown(e) {
        if (e.key === "Escape") cancelar();
    }

    document.getElementById("veritaplugin-cancel-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        cancelar();
    });

    document.addEventListener("keydown", onKeyDown);

    const onClick = (e) => {
        if (e.target.id === "veritaplugin-cancel-btn") return;

        e.preventDefault();
        e.stopPropagation();

        document.removeEventListener("mouseover", onMouseOver);
        document.removeEventListener("mouseout",  onMouseOut);
        document.removeEventListener("click",     onClick, true);
        document.removeEventListener("keydown",   onKeyDown);
        document.querySelectorAll("[style*='outline']").forEach(el => el.style.outline = "");
        toast.remove();

        showLoadingOverlay();

        chrome.runtime.sendMessage(
            { action: "analisarTexto", message: e.target.innerText || "" },
            (response) => {
                hideLoadingOverlay();
                if (!response || !response.success) {
                    showToast("Erro ao analisar: " + (response?.error || "Sem resposta do servidor."), "erro");
                    return;
                }
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

    const eSeguro = data.categoria === "Seguro";
    const statusStyle = eSeguro
        ? "background:#d4f5e2;border:1.5px solid #4cbb7f;color:#1e7a45;border-radius:10px;"
        : "background:#fff3e0;border:1.5px solid #f5a623;color:#b85c00;border-radius:10px;";
    const icon    = eSeguro ? "✅" : "⚠️";
    const title   = eSeguro ? "SEGURO" : "ATENÇÃO";
    const subtitle = eSeguro
        ? "Ameaças não foram detectadas"
        : `Possível golpe de '${data.categoria}'`;

    const modal = document.createElement("div");
    modal.id = "veritaplugin-modal";
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 999999999999;
        width: min(35rem, 92vw);
        max-height: 90vh;
        display: flex;
        flex-direction: column;
    `;

    modal.innerHTML = `
        <div class="card shadow" style="display:flex;flex-direction:column;max-height:90vh;overflow:hidden;">
            <div class="card-body p-3" style="display:flex;flex-direction:column;overflow:hidden;">

                <!-- Header -->
                <div class="d-flex align-items-center gap-2 mb-3 fw-bold fs-2" style="flex-shrink:0;">
                    <img src="${chrome.runtime.getURL('icon.png')}" style="width:5rem;height:4rem;">
                    <span style="letter-spacing:0;"><span style="color:#1CE47E;">Verita</span><span style="color:#164CEE;">Plugin</span></span>
                </div>

                <!-- Status -->
                <div style="${statusStyle}flex-shrink:0;" class="d-flex align-items-center gap-3 py-2 px-3 mb-3">
                    <span style="font-size:1.4rem;line-height:1;">${icon}</span>
                    <div>
                        <div style="font-weight:700;font-size:1.2rem;">${title}</div>
                        <div style="font-size:1rem;opacity:0.85;">${subtitle}</div>
                    </div>
                </div>

                <!-- Conteúdo com scroll -->
                <div style="overflow-y:auto;flex:1;min-height:0;">

                    <!-- Explicação -->
                    <div class="card bg-light mb-2">
                        <div class="card-body py-2 px-3">
                            <div class="fw-bold">Explicação:</div>
                            <div class="text-secondary" style="font-size:1.05rem;">${data.explicacao || "—"}</div>
                        </div>
                    </div>

                    <!-- Base legal -->
                    <div class="card bg-light mb-2">
                        <div class="card-body py-2 px-3">
                            <div class="fw-bold">Base legal:</div>
                            <div class="text-secondary" style="font-size:1.05rem;">${data.baseLegal || "—"}</div>
                        </div>
                    </div>

                    <!-- Ações recomendadas -->
                    <div class="card bg-light mb-3">
                        <div class="card-body py-2 px-3">
                            <div class="fw-bold">Ações recomendadas:</div>
                            <div class="text-secondary" style="font-size:1.05rem;">${data.acaoRecomendada || "—"}</div>
                        </div>
                    </div>

                </div>

                <!-- Rodapé fixo -->
                <div style="flex-shrink:0;">
                    <div style="font-size:0.78rem;color:#888;text-align:center;margin-bottom:10px;">
                        O VeritaPlugin pode cometer erros. Confira informações importantes.
                    </div>
                    <button id="veritaplugin-close-btn" class="btn btn-primary w-100">
                        Fechar
                    </button>
                </div>

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
