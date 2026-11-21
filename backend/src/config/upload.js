const multer = require('multer');

const TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024; // 10 MB

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: TAMANHO_MAXIMO_BYTES,
  },
});

module.exports = upload;