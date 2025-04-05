import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config();

const connectToDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log(`Database successfully connected`);
  } catch (err) {
    console.log(`Error connecting to database: ', err`);
  }
};

export default connectToDB;
