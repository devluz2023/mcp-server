import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency


# =========================================================
# PSI interno (auto-baseline)
# =========================================================
def calculate_psi(series):
    """
    PSI usando própria distribuição como referência interna
    """

    expected = series.sample(frac=0.5, random_state=42)
    actual = series.drop(expected.index)

    expected_perc = expected.value_counts(normalize=True)
    actual_perc = actual.value_counts(normalize=True)

    all_keys = set(expected_perc.index).union(set(actual_perc.index))

    psi = 0
    for key in all_keys:
        e = expected_perc.get(key, 0.0001)
        a = actual_perc.get(key, 0.0001)
        psi += (a - e) * np.log(a / e)

    return psi


# =========================================================
# DRIFT NUMÉRICO INTERNO
# =========================================================
def numeric_drift(series):
    sample = series.sample(frac=0.5, random_state=42)
    rest = series.drop(sample.index)

    stat, p = ks_2samp(sample, rest)

    return {
        "ks_statistic": float(stat),
        "p_value": float(p),
        "drift_detected": bool(p < 0.05)
    }


# =========================================================
# DRIFT CATEGÓRICO INTERNO
# =========================================================
def categorical_drift(series):
    sample = series.sample(frac=0.5, random_state=42)
    rest = series.drop(sample.index)

    s1 = sample.value_counts()
    s2 = rest.value_counts()

    all_cat = set(s1.index).union(set(s2.index))

    v1 = [s1.get(c, 0) for c in all_cat]
    v2 = [s2.get(c, 0) for c in all_cat]

    chi2, p, _, _ = chi2_contingency([v1, v2])

    return {
        "chi2": float(chi2),
        "p_value": float(p),
        "drift_detected": bool(p < 0.05)
    }


# =========================================================
# ID DRIFT INTERNO
# =========================================================
def id_drift(series):
    sample = series.sample(frac=0.5, random_state=42)
    rest = series.drop(sample.index)

    s1 = set(sample)
    s2 = set(rest)

    return {
        "new_ids": len(s2 - s1),
        "missing_ids": len(s1 - s2),
        "coverage": len(s1 & s2) / max(len(s1), 1)
    }


# =========================================================
# PIPELINE ÚNICO (SEM PARÂMETROS)
# =========================================================
def run_drift_single_table(df):
    results = {}

    # =========================
    # NUMÉRICAS
    # =========================
    numeric_cols = ["preco", "frete", "pagamento_valor"]

    for col in numeric_cols:
        results[col] = numeric_drift(df[col])

    # =========================
    # CATEGÓRICAS
    # =========================
    cat_cols = [
        "cidade_cliente",
        "estado_cliente",
        "status_pedido",
        "categoria",
        "pagamento_tipo"
    ]

    for col in cat_cols:
        results[col] = categorical_drift(df[col])

    # =========================
    # PSI GLOBAL (exemplo preço)
    # =========================
    results["psi_preco"] = calculate_psi(df["preco"])

    # =========================
    # IDs
    # =========================
    results["id_cliente"] = id_drift(df["id_cliente"])

    return results



