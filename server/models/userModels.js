import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  song: {
    title: { type: String, required: true },
    artist: { type: String, required: true },
    link: { type: String, required: true },
  },

  message: { type: String, required: true },
  sender_name: { type: String, default: 'Anonymous' },
  recipient_name: { type: String, required: true },
  created_at: { type: Date, default: Date.now },
});

const Dedication = mongoose.model('Dedication', DedicationSchema);
export default Dedication;
