# Groww App Reviews — Weekly Pulse (MCP)

Turn recent **public Google Play Store reviews** for Groww into a short weekly product pulse (themes, user quotes, and actionable insights) and deliver it via **Gmail / Google Docs using MCP automation**.

---

## 🌐 Working Prototype

Frontend: https://app-reviews-analyser.vercel.app/

---

## 📌 Project Overview

This project analyzes Groww Play Store reviews from the last **8–12 weeks** and generates a structured weekly product intelligence report:

- Top product themes (max 5)
- Real user quotes
- Weekly insight summary
- Actionable recommendations
- Automated email draft via MCP workflow

Built for the **NextLeap Learn in Public Challenge**.

---

## 📁 Folder Structure

```txt
inputs/raw/       # Raw Play Store review dataset
data/             # Cleaned submission dataset
data/working/     # Intermediate processing outputs
artifacts/        # Weekly pulse reports
docs/             # Architecture & design decisions
scripts/          # Data pipeline & LLM workflow
frontend/         # Next.js dashboard UI