export interface GENE_MODEL_INPUTS {
  cultivo: 'Maíz' | 'Sorgo' | 'Tomate' | 'Sandía' | 'Algodón';
  temperatura: number;
  humedadRelativa: number;
  intensidadLuminica: number;
  pH: number;
  humedadSuelo: number;
  carbonoOrganico: number;
  nitrogenoTotal: number;
  fosforoSoluble: number;
  texturaSuelo:
    | 'Arenoso'
    | 'Franco Arenoso'
    | 'Franco'
    | 'Franco Arcilloso'
    | 'Arcilloso'
    | 'limoso';
  aguaPorcentual: number;
  nacl: number;
  cd: number;
  al: number;
}
