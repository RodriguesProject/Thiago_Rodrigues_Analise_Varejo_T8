import tempfile, unittest
import pandas as pd
from analise_varejo import validar_estrutura, preparar_dados, analisar_dataframe

class TestPipelineVarejo(unittest.TestCase):
    def setUp(self):
        self.df=pd.DataFrame([
            ["01/02/2019",100,1,"M",4,1,"C",10,"ALIMENTOS","ARROZ"],
            ["02/02/2019",101,2,"F",1,0,"A",12,"#N/D","ITEM"],
            ["02/02/2019",101,2,"F",1,0,"A",12,"#N/D","ITEM"],
        ],columns=["DATA","CO_ID","CL_ID","CL_GENERO","CL_EC","CL_FHL","CL_SEG","PR_ID","PR_CAT","PR_NOME"])
    def test_colunas_e_base_vazia(self):
        with self.assertRaises(ValueError): validar_estrutura(pd.DataFrame({"DATA":[1]}))
        with self.assertRaises(ValueError): validar_estrutura(self.df.iloc[:0])
    def test_preparacao_preserva_origem(self):
        original=self.df.copy(deep=True); p=preparar_dados(self.df)
        pd.testing.assert_frame_equal(self.df,original)
        self.assertEqual(p.loc[1,"PR_CAT_NORM"],"ND")
        self.assertEqual(p.loc[0,"CL_EC_DESCRICAO"],"Solteiro")
    def test_exportacoes(self):
        with tempfile.TemporaryDirectory() as d:
            r=analisar_dataframe(self.df,d)
            self.assertEqual(r["dimensoes"]["clientes_distintos"],2)
            self.assertEqual(r["qualidade"]["linhas_duplicadas_excedentes"],1)
            from pathlib import Path
            for f in ["resumo_analise.json","relatorio_qualidade.csv","categorias.csv","segmento_a_categorias.csv","segmento_a_genero.csv","registros_por_categoria.png","registros_por_segmento.png"]:
                self.assertTrue((Path(d)/f).exists(),f)
if __name__=="__main__": unittest.main()
