const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Middleware pour analyser les corps JSON
app.use(express.json());

// Point de terminaison pour les notifications Calendly
app.post('/', (req, res) => {
  const event = req.body;

  // Log l'événement reçu pour vérification
  console.log('Événement reçu :', event);

  // Ajouter ici la logique pour envoyer un message via WhatsApp ou SMS
  // Par exemple, envoyer un message de confirmation à vous et au client

  // Répondre à Calendly pour dire que l'événement a été reçu
  res.status(200).send('Notification reçue');
});

app.listen(port, () => {
  console.log(`Serveur en écoute sur le port ${port}`);
});