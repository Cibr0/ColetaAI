const axios = require('axios');

const IA_API_URL = process.env.IA_API_URL || 'http://localhost:8000';
const CONFIDENCE_THRESHOLD = parseFloat(process.env.CONFIDENCE_THRESHOLD || '0.70');

async function analisarImagemResiduos(file) {
  const formData = new FormData();
  const blob = new Blob([file.buffer], { type: file.mimetype });

  // O campo 'imagem' deve coincidir exatamente com o endpoint /validar-foto do FastAPI
  formData.append('imagem', blob, file.originalname);

  try {
    const response = await axios.post(`${IA_API_URL}/validar-foto`, formData, {
      timeout: 15000,
    });

    const { classificacao, probabilidades } = response.data;
    const scoreValida = probabilidades.valida ?? 0;
    const scoreInvalida = probabilidades.invalida ?? 0;

    if (classificacao === 'valida' && scoreValida >= CONFIDENCE_THRESHOLD) {
      return {
        aprovada: true,
        status: 'APROVADA',
        motivo: 'Resíduos descartados identificados com confiança suficiente.',
        ia: {
          classificacao,
          confiancaAplicada: scoreValida,
          limiarMinimo: CONFIDENCE_THRESHOLD,
          probabilidades,
        },
      };
    }

    const motivoRejeicao =
      classificacao === 'invalida'
        ? 'A imagem enviada não apresenta resíduos válidos para solicitação de coleta.'
        : `Confiança insuficiente na análise (${(scoreValida * 100).toFixed(1)}%). Envie uma foto mais nítida e próxima dos resíduos.`;

    return {
      aprovada: false,
      status: 'REJEITADA',
      motivo: motivoRejeicao,
      ia: {
        classificacao,
        confiancaAplicada: Math.max(scoreValida, scoreInvalida),
        limiarMinimo: CONFIDENCE_THRESHOLD,
        probabilidades,
      },
    };
  } catch (error) {
    if (error.response) {
      const err = new Error(error.response.data?.detail || 'Falha na validação da imagem pela IA.');
      err.statusCode = error.response.status;
      throw err;
    }

    const err = new Error('O serviço de Inteligência Artificial (ColetaAI) está indisponível no momento.');
    err.statusCode = 503;
    throw err;
  }
}

module.exports = { analisarImagemResiduos };