require('dotenv').config();
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const solicitacaoRoutes = require('./routes/solicitacaoRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({
    status: 'online',
    servico: 'Coleta Certa Back-end (Node.js)',
    iaUrl: process.env.IA_API_URL || 'http://localhost:8000',
  });
});

app.use('/api', solicitacaoRoutes);

app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(413).json({ erro: 'A imagem excede o limite máximo de 10 MB.' });
    }
    return res.status(400).json({ erro: `Erro no upload: ${err.message}` });
  }
  next(err);
});

app.listen(PORT, () => {
  console.log(`Servidor Coleta Certa rodando em http://localhost:${PORT}`);
});