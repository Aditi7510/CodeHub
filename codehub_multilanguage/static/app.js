const language = document.getElementById("language");
const code = document.getElementById("code");
const stdin = document.getElementById("stdin");
const output = document.getElementById("output");
const statusLabel = document.getElementById("status");
const runBtn = document.getElementById("runBtn");
const filename = document.getElementById("filename");

const fileNames = { python: "main.py", java: "Main.java", javascript: "main.js" };

function setStatus(message, type = "") {
  statusLabel.textContent = message;
  statusLabel.className = "status " + type;
}

language.addEventListener("change", () => {
  code.value = window.DEFAULT_CODE[language.value];
  filename.textContent = fileNames[language.value];
  output.textContent = "Your program output will appear here...";
  setStatus("Ready");
});

document.getElementById("resetBtn").addEventListener("click", () => {
  code.value = window.DEFAULT_CODE[language.value];
  stdin.value = "";
  output.textContent = "Code reset. Ready to run.";
  setStatus("Ready");
});

document.getElementById("clearBtn").addEventListener("click", () => {
  code.value = "";
  output.textContent = "Editor cleared.";
  setStatus("Ready");
  code.focus();
});

runBtn.addEventListener("click", async () => {
  runBtn.disabled = true;
  runBtn.textContent = "Running...";
  output.textContent = "Executing your program...";
  setStatus("Running");

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        language: language.value,
        code: code.value,
        input: stdin.value
      })
    });
    const result = await response.json();
    output.textContent = result.output || result.error || "No output.";
    const failed = !response.ok || (result.status && !["Success"].includes(result.status));
    setStatus(result.status || (response.ok ? "Success" : "Error"), failed ? "error" : "success");
  } catch (error) {
    output.textContent = "Could not connect to the CodeHub server. Make sure Flask is running.";
    setStatus("Connection error", "error");
  } finally {
    runBtn.disabled = false;
    runBtn.innerHTML = "<span>▶</span> Run Code";
  }
});

// Insert a tab in the editor instead of moving focus.
code.addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    event.preventDefault();
    const start = code.selectionStart;
    const end = code.selectionEnd;
    code.setRangeText("    ", start, end, "end");
  }
});
