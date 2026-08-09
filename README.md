<div align="center">
  <div>&nbsp;</div>

# GTI Widget: Dynamic Threat Intelligence Dashboard

[![Proof of Concept](https://img.shields.io/badge/Status-Proof_of_Concept-yellow)](#)
[![Google Threat Intelligence](https://img.shields.io/badge/Integration-GTI-blue)](#)
[![Level: Beginner Friendly](https://img.shields.io/badge/Level-Beginner_Friendly-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

</div>

A low-friction, fully modular web widget for Google Threat Intelligence (GTI). Built with HTML, Tailwind CSS, and Vanilla JavaScript, it allows users to dynamically analyze Indicators of Compromise (IOCs), vulnerabilities, and other threat intelligence data by interacting with the GTI API directly from a responsive sliding pane. Every component is swappable and designed for quick integration into existing dashboards.

> **⚠️ NOTE:** This project is for **Proof of Concept (POC) purposes only**. It is not intended for production use. Do not hardcode sensitive keys or credentials in this repository.

---

## 🚀 Quickstart

```bash
git clone git@github.com:Muybi3n/gti_widget_modular.git
cd gti_widget_modular
```

Configure your environment and run:

```bash
python3 build_project_gti/build_project.py
# Then open index.html in your browser
```

## 🏗️ Architecture & Integration

This project is built to be easily adaptable and integrated into existing workflows:

- **Frontend:** Tailwind CSS for styling, Vanilla JS for logic.
- **Backend/API:** Directly calls GTI API endpoints securely from the client.
- **Deployment:** Static HTML/JS, deployable anywhere.

## 🛡️ Security Best Practices

- **API Keys:** Never hardcode your GTI API keys into the source code.
- **Environment Variables:** Always use environment variables or secure credential vaults to manage access.
- **Scope:** Ensure your API token has only the necessary permissions required for the integration.

## 🧪 Verification & Testing

Once configured, run the application and verify that the API returns the expected threat context without throwing authentication errors. Detailed test cases will be added as the project grows.

## 🔧 Troubleshooting

- **API Authentication Errors:** Ensure your environment variables are set correctly and that your token has not expired.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Since this is a POC, feel free to fork and adapt it to your specific use cases.
