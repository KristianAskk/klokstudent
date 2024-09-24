import mongoose, { Schema, Document } from 'mongoose';
import { IVinmonopolProduct } from './VinmonopolProduct';

const StoreSchema = new Schema({

  addressFormattedAddress: String,
  addressId: String,
  addressLine1: String,
  displayName: String,
  formattedDistance: String,
  geoPointLatitude: Number,
  geoPointLongitude: Number,
  pointOfServiceId: String,
  name: String,

  stockInfo: [{
    product: { type: Schema.Types.ObjectId, ref: 'VinmonopolProduct' },
    productId: String,
    stockLevels: [{
      timestamp: Date,
      level: Number
    }]
  }]
});

export interface IStore extends Document {
  addressFormattedAddress: string;
  addressId: string;
  addressLine1: string;
  displayName: string;
  formattedDistance: string;
  geoPointLatitude: number;
  geoPointLongitude: number;
  pointOfServiceId: string;
  name: string;
  stockInfo: Array<{
    product: mongoose.Types.ObjectId | IVinmonopolProduct;
    productId: string;
    stockLevels: Array<{
      timestamp: Date;
      level: number;
    }>;
  }>;
}

const Store = mongoose.model<IStore>('Store', StoreSchema, "Stores");

export default Store;