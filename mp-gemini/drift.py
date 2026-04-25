import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
from databricks.connect import DatabricksSession


def run_drift():
    """
    Calcula drift simples em uma tabela do Databricks Lake
    e retorna um único resultado consolidado.
    """

    spark = DatabricksSession.builder.getOrCreate()

    df = spark.table("pedido.default.cliente").sample(0.05).toPandas()

    # =========================
    # DRIFT NUMÉRICO (KS)
    # =========================
    sample = df["preco"].sample(frac=0.5, random_state=42)
    rest = df["preco"].drop(sample.index)

    ks_stat, ks_p = ks_2samp(sample, rest)

    # =========================
    # DRIFT CATEGÓRICO (CHI2)
    # =========================
    s1 = df["status_pedido"].sample(frac=0.5, random_state=42)
    s2 = df["status_pedido"].drop(s1.index)

    c1 = s1.value_counts()
    c2 = s2.value_counts()

    cats = set(c1.index).union(set(c2.index))

    v1 = [c1.get(x, 0) for x in cats]
    v2 = [c2.get(x, 0) for x in cats]

    chi2, chi_p, _, _ = chi2_contingency([v1, v2])

    # =========================
    # PSI SIMPLES
    # =========================
    expected = df["preco"].sample(frac=0.5, random_state=42)
    actual = df["preco"].drop(expected.index)

    e = expected.value_counts(normalize=True)
    a = actual.value_counts(normalize=True)

    all_keys = set(e.index).union(set(a.index))

    psi = sum(
        (a.get(k, 0.0001) - e.get(k, 0.0001)) *
        np.log(a.get(k, 0.0001) / e.get(k, 0.0001))
        for k in all_keys
    )

    # =========================
    # RESULTADO ÚNICO
    # =========================
    return {
        "drift_preco_ks": {
            "statistic": float(ks_stat),
            "p_value": float(ks_p),
            "drift": bool(ks_p < 0.05)
        },
        "drift_status_chi2": {
            "statistic": float(chi2),
            "p_value": float(chi_p),
            "drift": bool(chi_p < 0.05)
        },
        "psi_preco": float(psi),
        "overall_drift": bool(ks_p < 0.05 or chi_p < 0.05 or psi > 0.2)
    }