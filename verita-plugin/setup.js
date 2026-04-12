let currentStep = 1;
const TOTAL_STEPS = 5;

function goTo(step) {
    document.getElementById(`step-${currentStep}`)?.classList.remove("active");

    for (let i = 1; i <= TOTAL_STEPS; i++) {
        const dot  = document.getElementById(`dot-${i}`);
        const line = document.getElementById(`line-${i}`);
        if (!dot) continue;
        if (i < step) {
            dot.classList.remove("active");
            dot.classList.add("done");
            dot.textContent = "✓";
        } else if (i === step) {
            dot.classList.add("active");
            dot.classList.remove("done");
            dot.textContent = i;
        } else {
            dot.classList.remove("active", "done");
            dot.textContent = i;
        }
        if (line) {
            i < step ? line.classList.add("done") : line.classList.remove("done");
        }
    }

    currentStep = step;
    document.getElementById(`step-${step}`)?.classList.add("active");

    // Ao entrar no step 3, roda a detecção automática
    if (step === 3) autoDetectServer();
}

// ── AUTO DETECÇÃO DO SERVIDOR ──────────────────────────────────────────────

async function autoDetectServer() {
    const badge        = document.getElementById("detect-badge");
    const instructions = document.getElementById("install-instructions");
    const btnNext      = document.getElementById("btn-3-next");

    badge.className = "status-badge waiting";
    badge.innerHTML = "<span>⏳</span> Verificando se o servidor já está rodando...";
    instructions.style.display = "none";
    btnNext.disabled = true;

    try {
        const res = await fetch("http://localhost:8080/VeritaPlugin/health", {
            signal: AbortSignal.timeout(4000)
        });
        if (res.ok) {
            badge.className = "status-badge ok";
            badge.innerHTML = "<span>✓</span> Servidor detectado! Você pode continuar.";
            btnNext.disabled = false;
            return;
        }
        throw new Error();
    } catch {
        badge.className = "status-badge erro";
        badge.innerHTML = "<span>✗</span> Servidor não encontrado. Siga as instruções abaixo:";
        instructions.style.display = "block";
    }
}

// ── CONCLUSÃO ──────────────────────────────────────────────────────────────

function finish() {
    const key = document.getElementById("apiKeyInput2").value.trim();
    const err = document.getElementById("key-error2");
    if (!key.startsWith("sk-")) {
        err.style.display = "block";
        return;
    }
    err.style.display = "none";
    chrome.storage.local.set({ openaiKey: key, setupComplete: true }, () => {
        document.querySelector(".steps-bar").style.display = "none";
        for (let i = 1; i <= TOTAL_STEPS; i++) {
            document.getElementById(`step-${i}`)?.classList.remove("active");
        }
        document.getElementById("step-done").classList.add("active");
    });
}

// ── LISTENERS ──────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {

    // Etapa 1
    document.getElementById("btn-1-next").addEventListener("click", () => goTo(2));

    // Etapa 2 — Termos
    document.getElementById("btn-2-back").addEventListener("click", () => goTo(1));
    document.getElementById("acceptTerms").addEventListener("change", (e) => {
        document.getElementById("btn-accept").disabled = !e.target.checked;
    });
    document.getElementById("btn-accept").addEventListener("click", () => goTo(3));

    // Etapa 3 — Servidor
    document.getElementById("btn-3-back").addEventListener("click", () => goTo(2));
    document.getElementById("btn-3-recheck").addEventListener("click", autoDetectServer);
    document.getElementById("btn-3-next").addEventListener("click", () => goTo(5));
    document.getElementById("btn-3-python").addEventListener("click", () => goTo(4));

    // Etapa 4 — Python (fallback)
    document.getElementById("btn-4-back").addEventListener("click", () => goTo(3));

    // Etapa 5 — Chave + Concluir
    document.getElementById("btn-5-back").addEventListener("click", () => goTo(3));
    document.getElementById("btn-toggle-key2").addEventListener("click", () => {
        const input = document.getElementById("apiKeyInput2");
        input.type = input.type === "password" ? "text" : "password";
    });
    document.getElementById("btn-finish").addEventListener("click", finish);

    // Tela final
    document.getElementById("btn-open-fb").addEventListener("click", () => {
        chrome.tabs.create({ url: "https://www.facebook.com" });
        window.close();
    });

    // Preenche a chave já salva, se houver
    chrome.storage.local.get("openaiKey", ({ openaiKey }) => {
        if (openaiKey) {
            document.getElementById("apiKeyInput2").value = openaiKey;
        }
    });
});
