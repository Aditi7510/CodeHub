from flask import Flask, render_template, request, jsonify
import os
import subprocess
import tempfile
from pathlib import Path

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # 64 KB request limit

TIMEOUT_SECONDS = 5
OUTPUT_LIMIT = 12000

DEFAULT_CODE = {
    "python": 'name = input("Enter your name: ")\nprint("Hello,", name)',
    "java": 'import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        System.out.print("Enter your name: ");\n        String name = sc.nextLine();\n        System.out.println("Hello, " + name);\n    }\n}',
    "javascript": 'const name = prompt("Enter your name: ");\nconsole.log("Hello, " + name);'
}

@app.get("/")
def home():
    return render_template("index.html", default_code=DEFAULT_CODE)

@app.post("/run")
def run_code():
    data = request.get_json(silent=True) or {}
    language = data.get("language", "")
    code = data.get("code", "")
    user_input = data.get("input", "")

    if language not in ("python", "java", "javascript"):
        return jsonify(error="Please select a supported language."), 400
    if not isinstance(code, str) or not code.strip():
        return jsonify(error="Write some code before running it."), 400
    if len(code) > 50000:
        return jsonify(error="Code is too long (maximum 50 KB)."), 400
    if not isinstance(user_input, str) or len(user_input) > 20000:
        return jsonify(error="Input is too long."), 400

    with tempfile.TemporaryDirectory(prefix="codehub_") as temp_dir:
        workdir = Path(temp_dir)

        if language == "python":
            source = workdir / "main.py"
            source.write_text(code, encoding="utf-8")
            command = ["python", str(source)]

        elif language == "javascript":
            source = workdir / "main.js"
            source.write_text(code, encoding="utf-8")
            command = ["node", str(source)]

        else:
            source = workdir / "Main.java"
            source.write_text(code, encoding="utf-8")
            compile_result = subprocess.run(
                ["javac", "Main.java"],
                cwd=workdir,
                input="",
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS
            )
            if compile_result.returncode != 0:
                return jsonify(output=(compile_result.stderr or compile_result.stdout)[:OUTPUT_LIMIT],
                               status="Compilation error")
            command = ["java", "-cp", str(workdir), "Main"]

        try:
            result = subprocess.run(
                command,
                cwd=workdir,
                input=user_input,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS
            )
            output = result.stdout
            if result.stderr:
                output += ("\n" if output else "") + result.stderr
            return jsonify(
                output=(output or "(Program finished with no output.)")[:OUTPUT_LIMIT],
                status="Success" if result.returncode == 0 else f"Exited with code {result.returncode}"
            )
        except subprocess.TimeoutExpired:
            return jsonify(output=f"Execution timed out after {TIMEOUT_SECONDS} seconds.",
                           status="Time limit exceeded")
        except FileNotFoundError as exc:
            missing = "Python" if language == "python" else ("Node.js" if language == "javascript" else "Java JDK")
            return jsonify(output=f"{missing} was not found. Install it and add it to PATH.",
                           status="Runtime not installed")
        except Exception as exc:
            return jsonify(output=str(exc)[:OUTPUT_LIMIT], status="Execution error")

if __name__ == "__main__":
    # Local development only. Do not expose this server to the public internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
