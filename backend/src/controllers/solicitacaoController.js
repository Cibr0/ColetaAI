const { analisarImagemResiduos } = require('../services/iaService');

async function criarSolicitacao(req, res) {
  try {
    if (!req.file) {
      return res.status(400).json({
        erro: 'É obrigatório enviar uma imagem no campo "imagem".',
      });
    }

    const { endereco, descricao, latitude, longitude } = req.body;

    const resultadoIA = await analisarImagemResiduos(req.file);

    if (!resultadoIA.aprovada) {
      return res.status(422).json({
        mensagem: 'Solicitação de coleta rejeitada na validação automática.',
        status: resultadoIA.status,
        motivo: resultadoIA.motivo,
        analiseIA: resultadoIA.ia,
      });
    }

    const solicitacaoRegistrada = {
      id: Date.now(),
      status: resultadoIA.status,
      endereco: endereco || 'Não informado',
      descricao: descricao || '',
      coordenadas: latitude && longitude ? { latitude, longitude } : null,
      imagemOriginal: req.file.originalname,
      analiseIA: resultadoIA.ia,
      criadoEm: new Date().toISOString(),
    };

    return res.status(201).json({
      mensagem: 'Solicitação de coleta aprovada e criada com sucesso!',
      solicitacao: solicitacaoRegistrada,
    });
  } catch (error) {
    const statusCode = error.statusCode || 500;
    return res.status(statusCode).json({
      erro: error.message || 'Erro interno ao processar a solicitação.',
    });
  }
}

module.exports = { criarSolicitacao };