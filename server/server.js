import express from 'express';
const app = express();
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();
//MONGODB MODULE
import ConnectionDB from './db.js';
//SET DB CONNECTION
ConnectionDB();
//SET CORS POLICIES
const corsOptions = { origin: ['http://localhost:5173'] };
app.use(cors(corsOptions));
//MIDDLEWARE TO PARSE JSON TO OBJECT
app.use(express.json());

app.get('/api', (req, res) => {
  return res.status(200).json(res.locals);
});

app.post('/api', (req, res) => {
  return res.status(201).json(res.locals);
});

//404 Not found handler
app.use('*', (req, res) => {
  return res.status(404).send('Not found');
});

//Error Handler
app.use((err, req, res, next) => {
  console.log('error', err);
  const statusCode = err.status; 
  const message = err.message.err;
  return res.status(statusCode).send({ message: message });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});
