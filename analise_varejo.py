"""Pipeline reproduzível de análise exploratória de dados de varejo."""
import argparse, json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLUNAS = {"DATA","CO_ID","CL_ID","CL_GENERO","CL_EC","CL_FHL","CL_SEG","PR_ID","PR_CAT","PR_NOME"}
ESTADO_CIVIL = {1:"Casado ou união estável",2:"Divorciado",3:"Separado",4:"Solteiro",5:"Viúvo"}

def validar_estrutura(df):
    faltantes = sorted(COLUNAS - set(df.columns))
    if faltantes:
        raise ValueError("Colunas obrigatórias ausentes: " + ", ".join(faltantes))
    if df.empty:
        raise ValueError("A base está vazia.")

def carregar_base(caminho, sep=";", encoding="utf-8-sig"):
    arquivo = Path(caminho)
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
    df = pd.read_csv(arquivo, sep=sep, encoding=encoding, low_memory=False)
    validar_estrutura(df)
    return df

def preparar_dados(df):
    validar_estrutura(df)
    out = df.copy()
    out["CL_GENERO_NORM"] = out["CL_GENERO"].astype("string").str.strip().str.upper()
    out["CL_SEG_NORM"] = out["CL_SEG"].astype("string").str.strip().str.upper()
    out["PR_CAT_NORM"] = out["PR_CAT"].astype("string").str.strip().str.upper().replace({"#N/D":"ND", "":pd.NA})
    out["DATA_TRATADA"] = pd.to_datetime(out["DATA"], dayfirst=True, errors="coerce")
    out["CL_EC_DESCRICAO"] = pd.to_numeric(out["CL_EC"], errors="coerce").map(ESTADO_CIVIL)
    out["CL_FHL_NUM"] = pd.to_numeric(out["CL_FHL"], errors="coerce")
    return out

def gerar_relatorio_qualidade(df):
    linhas=[]
    for col in df.columns:
        vazios = int(df[col].astype("string").str.strip().eq("").fillna(False).sum()) if (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])) else 0
        linhas.append({"coluna":col,"valores_nulos":int(df[col].isna().sum()),"textos_vazios":vazios,"total_registros":len(df)})
    return pd.DataFrame(linhas)

def _distribuicao(serie, nome):
    tab=serie.value_counts(dropna=False).rename_axis(nome).reset_index(name="registros")
    tab["percentual_registros"]=(tab["registros"]/max(len(serie),1)*100).round(2)
    return tab

def gerar_tabelas(preparado):
    a=preparado.loc[preparado["CL_SEG_NORM"].eq("A")]
    if a.empty:
        genero=pd.DataFrame(columns=["genero","clientes_distintos","compras_distintas","registros_itens"])
    else:
        genero=a.groupby("CL_GENERO_NORM",dropna=False).agg(clientes_distintos=("CL_ID","nunique"),compras_distintas=("CO_ID","nunique"),registros_itens=("CO_ID","size")).reset_index().rename(columns={"CL_GENERO_NORM":"genero"})
    return {"categorias":_distribuicao(preparado["PR_CAT_NORM"],"categoria"),"segmento_a_categorias":_distribuicao(a["PR_CAT_NORM"],"categoria"),"segmento_a_genero":genero}

def analisar_dataframe(df, diretorio_saida):
    validar_estrutura(df)
    out=Path(diretorio_saida); out.mkdir(parents=True,exist_ok=True)
    p=preparar_dados(df); q=gerar_relatorio_qualidade(df); tabs=gerar_tabelas(p)
    filhos=p["CL_FHL_NUM"].dropna()
    resumo={"dimensoes":{"registros":len(df),"colunas":len(df.columns),"clientes_distintos":int(df["CL_ID"].nunique()),"compras_distintas":int(df["CO_ID"].nunique())},
      "qualidade":{"valores_nulos_total":int(df.isna().sum().sum()),"linhas_duplicadas_excedentes":int(df.duplicated().sum()),"linhas_em_grupos_duplicados":int(df.duplicated(keep=False).sum()),"datas_nao_convertidas":int(p["DATA_TRATADA"].isna().sum()),"estados_civis_sem_mapeamento":int(p["CL_EC_DESCRICAO"].isna().sum()),"categorias_nao_informadas":int(p["PR_CAT_NORM"].isna().sum())},
      "numero_de_filhos_por_registro":{"media":round(float(filhos.mean()),4) if len(filhos) else None,"minimo":float(filhos.min()) if len(filhos) else None,"maximo":float(filhos.max()) if len(filhos) else None},
      "nota_metodologica":"Distribuições por gênero e segmento são calculadas sobre linhas/registros, não sobre clientes únicos. A base está em nível de item."}
    (out/"resumo_analise.json").write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding="utf-8")
    q.to_csv(out/"relatorio_qualidade.csv",index=False,encoding="utf-8-sig")
    for nome,tab in tabs.items(): tab.to_csv(out/f"{nome}.csv",index=False,encoding="utf-8-sig")
    for coluna,arquivo,titulo in [("categoria","registros_por_categoria.png","Registros por categoria"),("CL_SEG_NORM","registros_por_segmento.png","Registros por segmento")]:
        serie=p[coluna] if coluna=="CL_SEG_NORM" else p["PR_CAT_NORM"]
        dados=_distribuicao(serie,coluna).dropna()
        if len(dados):
            fig,ax=plt.subplots(figsize=(9,5))
            if coluna=="categoria":
                dados=dados.sort_values("registros"); ax.barh(dados[coluna].astype(str),dados["registros"])
            else: ax.bar(dados[coluna].astype(str),dados["registros"])
            ax.set(title=titulo,ylabel="Registros (itens)"); ax.grid(axis="x" if coluna=="categoria" else "y",alpha=.25); fig.tight_layout(); fig.savefig(out/arquivo,dpi=150); plt.close(fig)
    return resumo

def main():
    ap=argparse.ArgumentParser(description="Análise exploratória reproduzível de uma base de varejo.")
    ap.add_argument("--input",required=True); ap.add_argument("--output-dir",default="outputs"); ap.add_argument("--sep",default=";"); ap.add_argument("--encoding",default="utf-8-sig")
    args=ap.parse_args(); df=carregar_base(args.input,args.sep,args.encoding); r=analisar_dataframe(df,args.output_dir)
    print(json.dumps(r["dimensoes"],ensure_ascii=False,indent=2)); print(f"Relatórios gerados em: {Path(args.output_dir).resolve()}")

if __name__=="__main__": main()
