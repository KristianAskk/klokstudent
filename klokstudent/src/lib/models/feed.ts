/* eslint-disable @typescript-eslint/prefer-nullish-coalescing */
import mongoose, { Schema, model, Document } from 'mongoose';
import { IStore } from './store';

const feedSchema = new Schema({
  productId: {type: mongoose.Types.ObjectId,required:true, ref: 'VinmonopolProduct'},
  oldStock: { type: Number, required: true },
  newStock: { type: Number, required: true },
  date: { type: Date, required: true, default: Date.now },
  storeId: { type: mongoose.Types.ObjectId,required:true, ref: 'Store' },
});

export interface IFeed extends Document {
  productId: string;
  oldStock: number;
  newStock: number;
  date: Date;
  storeId: string;
}

// KAN IKKE HA S{N GOOFY OPERATOR}
const Feed = mongoose.models.Feed || model<IFeed>('Feed', feedSchema, 'Feeds');

export default Feed;