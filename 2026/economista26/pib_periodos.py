"""
Busca a serie do PIB real do Brasil (variacao % ao ano) desde 1970 no Banco
Mundial (dado compilado a partir das Contas Nacionais do IBGE - a serie
trimestral do SGS/Banco Central so comeca em 1996 e nao cobre o periodo
pedido) e gera um grafico de linha destacando os periodos:
Milagre Economico, Decada Perdida, Lula 1 e 2, Dilma, Temer,
Bolsonaro/pandemia e Lula 3.
"""

import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 1) Busca o dado -------------------------------------------------------
URL = (
    "https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.KD.ZG"
    "?format=json&date=1970:2025&per_page=100"
)
resp = requests.get(URL, timeout=30)
resp.raise_for_status()
records = resp.json()[1]

df = pd.DataFrame(
    [(int(r["date"]), r["value"]) for r in records if r["value"] is not None],
    columns=["ano", "variacao_pib"],
).sort_values("ano").reset_index(drop=True)

df.to_csv("dados/pib_brasil_1970_atual.csv", index=False)
print(df.tail())

# 2) Periodos a destacar --------------------------------------------------
periodos = [
    ("Milagre\nEconômico",       1970, 1973, "#282f6b"),
    ("Década\nPerdida",          1980, 1989, "#b22200"),
    ("Lula 1 e 2",               2003, 2010, "#224f20"),
    ("Dilma",                    2011, 2016, "#5f487c"),
    ("Temer",                    2016, 2018, "#b35c1e"),
    ("Bolsonaro/\npandemia",     2019, 2022, "#419391"),
    ("Lula 3",                   2023, df["ano"].max(), "#839c56"),
]

# 3) Grafico ----------------------------------------------------------------
plt.rcParams["font.family"] = "sans-serif"
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=200)
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

ymax_data = df["variacao_pib"].max()
ymin_data = df["variacao_pib"].min()
ax.set_ylim(ymin_data - 3.5, ymax_data + 9)

for i, (label, ini, fim, cor) in enumerate(periodos):
    ax.axvspan(ini - 0.5, fim + 0.5, color=cor, alpha=0.16, lw=0)
    y_label = ymax_data + (3.2 if i % 2 == 0 else 6.2)
    ax.text(
        (ini + fim) / 2, y_label, label,
        ha="center", va="bottom", fontsize=8.5, color=cor, fontweight="bold",
    )

ax.plot(df["ano"], df["variacao_pib"], color="#282f6b", lw=1.6, zorder=5)
ax.scatter(df["ano"], df["variacao_pib"], color="#282f6b", s=10, zorder=6)
ax.axhline(0, color="#666666", lw=0.8, ls="--", zorder=1)

ax.set_ylabel("Variação real do PIB (% a.a.)", fontsize=10)
ax.set_xlabel("")
ax.set_xlim(1969, df["ano"].max() + 1)
ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
ax.tick_params(labelsize=9)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

fig.suptitle(
    "PIB do Brasil: variação real anual (1970–{})".format(df["ano"].max()),
    fontsize=13, color="#282f6b", x=0.02, ha="left", y=0.995,
)
ax.text(
    1969, ymin_data - 3.0,
    "Fonte: Banco Mundial (World Development Indicators), a partir de dados do IBGE.",
    fontsize=7, color="#666666",
)

fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("imgs/pib_brasil_periodos.png", transparent=True, bbox_inches="tight")
print("Grafico salvo em imgs/pib_brasil_periodos.png")
