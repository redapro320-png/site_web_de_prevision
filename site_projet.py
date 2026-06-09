# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 00:19:20 2026

@author: User
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import io

st.set_page_config(page_title="PAPETIS 2026", layout="wide")
st.title("📊 PAPETIS DISTRIBUTION — Prévisions 2026")

fichier = st.file_uploader("📂 Charger le fichier Excel", type=["xlsx"])

if fichier:
    xls = pd.ExcelFile(fichier)

    df = pd.read_excel(xls, sheet_name="Ventes globales", skiprows=3)
    df.columns = ["Annee", "Mois", "Nom_Mois", "t", "Ventes"]
    df = df.dropna(subset=["t"]).copy()
    df["t"] = df["t"].astype(int)
    df["Ventes"] = df["Ventes"].astype(float)

    df_fam = pd.read_excel(xls, sheet_name="Ventes par famille", skiprows=3)
    df_fam.columns = ["Annee","Mois","Nom_Mois","t",
                      "Cahiers","Classeurs","Ecriture","Technique","Manuels","Bureau","Total"]

    # ── MCO ──
    t = df["t"].values
    y = df["Ventes"].values
    n = len(t)
    a = (n*(t*y).sum() - t.sum()*y.sum()) / (n*(t**2).sum() - t.sum()**2)
    b = (y.sum() - a*t.sum()) / n
    df["Tendance"] = a*df["t"] + b
    df["Ratio"] = df["Ventes"] / df["Tendance"]
    r2 = 1 - ((y - (a*t+b))**2).sum() / ((y - y.mean())**2).sum()

    # ── Coefficients ──
    moyennes = df.groupby("Mois")["Ratio"].mean()
    coeffs = moyennes * (12 / moyennes.sum())

    # ── Prévisions ──
    noms_complets = ["Janvier","Février","Mars","Avril","Mai","Juin",
                     "Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    records = []
    for i, mois in enumerate(range(1, 13)):
        t_val = 61 + i
        tt = a*t_val + b
        cs = coeffs[mois]
        records.append({
            "t": t_val, "Annee": 2026, "Mois": mois,
            "Nom_Mois": noms_complets[mois-1],
            "Tendance": round(tt, 2),
            "Coeff": round(cs, 4),
            "Prevision": round(tt*cs, 1)
        })
    df_prev = pd.DataFrame(records)

    # ── KPIs ──
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CA Total 2025", f"{df[df['Annee']==2025]['Ventes'].sum():.0f} kMAD")
    col2.metric("Prévision Total 2026", f"{df_prev['Prevision'].sum():.0f} kMAD")
    col3.metric("Tendance (pente)", f"{a:.2f} kMAD/mois")
    col4.metric("R²", f"{r2:.4f}")

    # ── Graphique principal ──
    st.markdown("---")
    st.subheader("📈 Historique + Prévisions")
    noms_mois = ["Janv","Févr","Mars","Avr","Mai","Juin","Juil","Août","Sept","Oct","Nov","Déc"]

    fig1, ax = plt.subplots(figsize=(14, 6))
    ax.axvspan(60.5, 72.5, color="#FFF3E0", alpha=0.7, zorder=0)
    ax.axvline(x=60.5, color="#CCCCCC", linewidth=1.5, linestyle="--", zorder=1)
    t_ligne = np.arange(1, 73)
    ax.plot(t_ligne, a*t_ligne+b, color="#888780", linewidth=1.2, linestyle="--",
            label=f"Tendance MCO : Tt = {a:.2f}·t + {b:.2f}")
    ax.plot(df["t"], df["Ventes"], color="#185FA5", linewidth=1.8,
            marker="o", markersize=3.5, label="Ventes réelles 2021–2025")
    ax.plot(df_prev["t"], df_prev["Prevision"], color="#D85A30", linewidth=2,
            marker="D", markersize=5, label="Prévisions 2026")
    ax.set_xlabel("Période (t)")
    ax.set_ylabel("Ventes (kMAD)")
    ax.set_title(f"Ventes historiques et prévisions 2026 | R² = {r2:.4f}")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    plt.tight_layout()
    st.pyplot(fig1)

    # ── Coefficients saisonniers ──
    st.subheader("📅 Coefficients saisonniers")
    fig2, ax2 = plt.subplots(figsize=(11, 5))
    couleurs = ["#D85A30" if coeffs[m] > 1 else "#185FA5" for m in range(1, 13)]
    bars = ax2.bar(range(1, 13), [coeffs[m] for m in range(1, 13)],
                   color=couleurs, edgecolor="white", alpha=0.85)
    ax2.axhline(y=1, color="#888780", linewidth=1.2, linestyle="--")
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(noms_mois)
    for bar, m in zip(bars, range(1, 13)):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.03,
                 f"{coeffs[m]:.3f}", ha="center", fontsize=8.5, fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)

    # ── Prévisions 2026 barres ──
    st.subheader("📊 Prévisions mensuelles 2026")
    fig3, ax3 = plt.subplots(figsize=(11, 5))
    couleurs2 = ["#D85A30" if m in [8,9] else "#185FA5" for m in range(1, 13)]
    bars2 = ax3.bar(range(1, 13), df_prev["Prevision"],
                    color=couleurs2, edgecolor="white", alpha=0.85)
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(noms_mois)
    for bar, val in zip(bars2, df_prev["Prevision"]):
        ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
                 f"{val:.0f}", ha="center", fontsize=8.5, fontweight="bold")
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3)

    # ── Table prévisions ──
    st.subheader("📋 Tableau des prévisions 2026")
    st.dataframe(df_prev, use_container_width=True)

    # ── Export Excel ──
    st.markdown("---")
    st.subheader("💾 Exporter les résultats")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df[["Annee","Mois","Nom_Mois","t","Ventes","Tendance","Ratio"]].to_excel(
            writer, sheet_name="Historique_MCO", index=False)
        pd.DataFrame({
            "Mois": range(1, 13),
            "Nom_Mois": noms_complets,
            "Coeff_Saisonnier": [round(coeffs[m], 4) for m in range(1, 13)]
        }).to_excel(writer, sheet_name="Coefficients_Saisonniers", index=False)
        df_prev.to_excel(writer, sheet_name="Previsions_2026", index=False)

    st.download_button(
        label="📥 Télécharger Excel",
        data=buffer.getvalue(),
        file_name="papetis_resultats_2026.xlsx",
        mime="application/vnd.ms-excel"
    )