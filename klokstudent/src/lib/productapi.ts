import mongoose from 'mongoose';
import VinmonopolProduct from './models/vinmonopolproduct';

const URI = process.env.MONGODB_URI ?? 'mongodb://localhost:27017/klokstudent';

async function connectToDatabase() {
  try {
    await mongoose.connect(URI);
    console.log('Mongoose connected to', URI);
  } catch (error) {
    console.error('Mongoose connection error:', error);
  }

  mongoose.connection.on('disconnected', () => {
    console.log('Mongoose disconnected');
  });
}

export default connectToDatabase;