let currentStep = 1;
const TOTAL_STEPS = 5;

function goTo(step) {
    document.getElementById(`step-${currentStep}`)?.classList.remove("active");

    for (let i = 1; i <= TOTAL_STEPS; i++) {
        const dot  = document.getElementById(`dot-${i}`);
        const line = document.getElementById(`line-${i}`);
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
}

async function checkConnection() {
    const badge  = document.getElementById("status-badge");
    const btnFin = document.getElementById("btn-finish");

    badge.className = "status-badge waiting";
    badge.innerHTML = "<span>⏳</span> Verificando...";
    btnFin.disabled = true;

    try {
        const res = await fetch("http://localhost:8080/VeritaPlugin/health", {
            signal: AbortSignal.timeout(5000)
        });
        if (res.ok) {
            badge.className = "status-badge ok";
            badge.innerHTML = "<span>✓</span> Servidor conectado com sucesso!";
            btnFin.disabled = false;
        } else {
            throw new Error(`Status ${res.status}`);
        }
    } catch {
        badge.className = "status-badge erro";
        badge.innerHTML = "<span>✗</span> Servidor não encontrado. Verifique se o <strong>iniciar.bat</strong> está aberto e tente novamente.";
    }
}

function finish() {
    document.querySelector(".steps-bar").style.display = "none";
    for (let i = 1; i <= TOTAL_STEPS; i++) {
        document.getElementById(`step-${i}`)?.classList.remove("active");
    }
    document.getElementById("step-done").classList.add("active");
    chrome.storage.local.set({ setupComplete: true });
}

document.addEventListener("DOMContentLoaded", () => {
    // Etapa 1
    document.getElementById("btn-1-next").addEventListener("click", () => goTo(2));

    // Etapa 2
    document.getElementById("btn-2-back").addEventListener("click", () => goTo(1));
    document.getElementById("acceptTerms").addEventListener("change", (e) => {
        document.getElementById("btn-accept").disabled = !e.target.checked;
    });
    document.getElementById("btn-accept").addEventListener("click", () => goTo(3));

    // Etapa 3
    document.getElementById("btn-3-back").addEventListener("click", () => goTo(2));
    document.getElementById("btn-3-next").addEventListener("click", () => goTo(4));

    // Etapa 4
    document.getElementById("btn-4-back").addEventListener("click", () => goTo(3));
    document.getElementById("btn-4-next").addEventListener("click", () => goTo(5));

    // Etapa 5
    document.getElementById("btn-5-back").addEventListener("click", () => goTo(4));
    document.getElementById("btn-check").addEventListener("click", checkConnection);
    document.getElementById("btn-finish").addEventListener("click", finish);

    // Tela final
    document.getElementById("btn-open-fb").addEventListener("click", () => {
        chrome.tabs.create({ url: "https://www.facebook.com" });
        window.close();
    });
});
