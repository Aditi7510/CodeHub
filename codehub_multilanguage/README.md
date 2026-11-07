# CodeHub – Multi-Language Coding Platform

A beginner-friendly local coding playground built with Python Flask, HTML, CSS and JavaScript. It can execute Python, Java and JavaScript (Node.js) programs.

## 1. Requirements

Install these on your computer and make sure each command works in Command Prompt:

- Python 3
- Java JDK (includes `javac` and `java`)
- Node.js (includes `node`)

Check installations:

```bash
python --version
javac -version
java -version
node --version
```

On some Windows systems, use `py` instead of `python`. If so, change `["python", ...]` in `app.py` to `["py", ...]`.

## 2. Open the project

Extract the ZIP, open the `codehub_multilanguage` folder in VS Code, then open its terminal.

## 3. Install Flask

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## 4. Run the platform

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

Choose Python, Java or JavaScript, edit the sample program, optionally enter standard input, and click **Run Code**.

## 5. Project structure

```text
codehub_multilanguage/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── app.js
```

## Important security note

This is a local learning/demo project, not a secure public online judge. Programs run as processes on the same computer as the Flask server. A timeout and temporary working directory are provided, but they are **not a security sandbox**. Run only code you trust, keep the server bound to localhost, and do not expose it to the internet or accept code from other users. A public deployment needs isolated containers or a dedicated sandbox service with CPU, memory, filesystem and network restrictions.
