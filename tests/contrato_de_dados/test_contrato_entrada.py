import os
import sys

# Adiciona a pasta 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join("./", "src")))

import pandera.polars as pa
import polars as pl
import pytest

from src.modulos.contrato_de_dados import contrato_entrada
