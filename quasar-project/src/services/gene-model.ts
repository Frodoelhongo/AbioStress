// src/services/gene-model.ts
import { api } from './api';

export type Cultivo = 'Maíz' | 'Sorgo' | 'Tomate' | 'Sandía' | 'Algodón';
export const SUPPORTED_CROPS: Cultivo[] = ['Sandía'];

export interface GENE_MODEL_INPUTS {
  cultivo: Cultivo;
  temperatura: number;
  humedadRelativa: number;
  intensidadLuminica: number;
  pH: number;
  humedadSuelo: number;
  carbonoOrganico: number;
  nitrogenoTotal: number;
  fosforoSoluble: number;
  texturaSuelo: 'Arenoso' | 'Franco Arenoso' | 'Franco' | 'Franco Arcilloso' | 'Arcilloso';
  aguaPorcentual: number;
  nacl: number;
  cd: number;
  al: number;
}

export interface GenePrediction {
  predicted_line: string;
  probabilities: Record<string, number>;
  genes: Array<{ gene: string; score?: number; count?: number; stresses?: string[] }>;
}

export class UnsupportedCropError extends Error {
  constructor(public cultivo: Cultivo) {
    super(`El cultivo "${cultivo}" aún no está habilitado`);
    this.name = 'UnsupportedCropError';
  }
}

/** Llama al backend /predict (ojo: el backend actual no usa 'cultivo') */
export async function predictGenes(input: GENE_MODEL_INPUTS): Promise<GenePrediction> {
  if (!SUPPORTED_CROPS.includes(input.cultivo)) {
    throw new UnsupportedCropError(input.cultivo);
  }

  const payload = {
    temperatura: input.temperatura,
    humedadRelativa: input.humedadRelativa,
    intensidadLuminica: input.intensidadLuminica,
    pH: input.pH,
    humedadSuelo: input.humedadSuelo,
    carbonoOrganico: input.carbonoOrganico,
    nitrogenoTotal: input.nitrogenoTotal,
    fosforoSoluble: input.fosforoSoluble,
    texturaSuelo: input.texturaSuelo,
    aguaPorcentual: input.aguaPorcentual,
    nacl: input.nacl,
    cd: input.cd,
    al: input.al,
  };

  const { data } = await api.post<GenePrediction>('/predict', payload);
  return data;
}

// (Opcional) meta del backend
export async function fetchMeta() {
  const { data } = await api.get('/meta');
  return data as {
    class_names: string[];
    numeric: string[];
    categorical: string[];
  };
}
