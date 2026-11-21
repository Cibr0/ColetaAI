const express = require('express');
const upload = require('../config/upload');
const { criarSolicitacao } = require('../controllers/solicitacaoController');

const router = express.Router();

router.post('/solicitacoes', upload.single('imagem'), criarSolicitacao);

module.exports = router;