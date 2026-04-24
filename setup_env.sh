# Apague o venv corrompido
rm -rf venv

# Crie um novo venv usando explicitamente o Python 3.12
python3.12 -m venv venv

# Ative o venv
source venv/bin/activate

# Atualize o pip antes de qualquer coisa
pip install --upgrade pip

# Instale as dependências (sem tentar compilar seu projeto local ainda)
pip install pyspark databricks-connect databricks-feature-engineering pandas pyyaml