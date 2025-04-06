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
const corsOptions = {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:5173', 'http://localhost:3000'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // Specify allowed HTTP methods
  };
  app.use(cors(corsOptions));
//MIDDLEWARE TO PARSE JSON TO OBJECT
app.use(express.json());

app.get('/api', (req, res) => {
    return res.status(200).json({ message: 'GET request successful' });
  });
  
  app.post('/api', (req, res) => {
    return res.status(201).json({ message: 'POST request successful' });
  });

//404 Not found handler
app.use('*', (req, res) => {
  return res.status(404).send('Not found');
});

//Error Handler
app.use((err, req, res, next) => {
  console.log('error', err);
  const statusCode = err.status|| 500;; 
  const message = err.message || 'Internal Server Error';
  return res.status(statusCode).send({ message: message });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});
