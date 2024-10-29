import mongoose, { Schema, type Document } from 'mongoose';

const VinmonopolProductSchema = new Schema({
  ageLimit: Number,
  allergens: String,
  bioDynamic: Boolean,
  buyable: Boolean,
  code: String,
  color: String,
  contentCharacteristics: [{
    name: String,
    readableValue: String,
    value: String,
  }],
  contentIngredients: [{
    code: String,
    formattedValue: String,
    readableValue: String,
  }],
  contentIsGoodFor: [{
    code: String,
    name: String,
  }],
  contentStoragePotentialCode: String,
  contentStoragePotentialFormattedValue: String,
  contentStyleCode: String,
  contentStyleDescription: String,
  contentStyleName: String,
  contentTraits: [{
    formattedValue: String,
    name: String,
    readableValue: String,
  }],
  cork: String,
  description: String,
  distributor: String,
  distributorId: Number,
  districtCode: String,
  districtName: String,
  districtSearchQuery: String,
  districtUrl: String,
  eco: Boolean,
  environmentalPackaging: Boolean,
  expired: Boolean,
  fairTrade: Boolean,
  gluten: Boolean,
  images: [{
    altText: String,
    format: String,
    imageType: String,
    url: String,
  }],
  kosher: Boolean,
  litrePriceFormattedValue: String,
  litrePriceReadableValue: String,
  litrePriceValue: Number,
  mainCategoryCode: String,
  mainCategoryName: String,
  mainCountryCode: String,
  mainCountryName: String,
  mainCountrySearchQuery: String,
  mainCountryUrl: String,
  mainProducerCode: String,
  mainProducerName: String,
  mainProducerSearchQuery: String,
  mainProducerUrl: String,
  name: String,
  packageType: String,
  priceFormattedValue: String,
  priceReadableValue: String,
  priceValue: Number,
  productSelection: String,
  releaseMode: Boolean,
  similarProducts: Boolean,
  smell: String,
  status: String,
  statusNotification: Boolean,
  summary: String,
  sustainable: Boolean,
  taste: String,
  url: String,
  volumeFormattedValue: String,
  volumeReadableValue: String,
  volumeValue: Number,
  wholeSaler: String,
  year: String,
  // Previously virtual fields, now stored in the database. They are pre-computed by the python scraper already.
  parsedSize: Number,
  pricePerLiter: Number,
  alcoholPerNok: Number,
  absoluteUrl: String,
});

export interface IVinmonopolProduct extends Document {
  ageLimit: number;
  allergens?: string;
  bioDynamic: boolean;
  buyable: boolean;
  code: string;
  color?: string;
  contentCharacteristics: Array<{
    name: string;
    readableValue: string;
    value: string;
  }>;
  contentIngredients: Array<{
    code: string;
    formattedValue: string;
    readableValue: string;
  }>;
  contentIsGoodFor: Array<{
    code: string;
    name: string;
  }>;
  contentStoragePotentialCode?: string;
  contentStoragePotentialFormattedValue?: string;
  contentStyleCode?: string;
  contentStyleDescription?: string;
  contentStyleName?: string;
  contentTraits: Array<{
    formattedValue: string;
    name: string;
    readableValue: string;
  }>;
  cork?: string;
  description: string;
  distributor: string;
  distributorId: number;
  districtCode?: string;
  districtName?: string;
  districtSearchQuery?: string;
  districtUrl?: string;
  eco: boolean;
  environmentalPackaging: boolean;
  expired: boolean;
  fairTrade: boolean;
  gluten: boolean;
  images: Array<{
    altText: string;
    format: string;
    imageType: string;
    url: string;
  }>;
  kosher: boolean;
  litrePriceFormattedValue: string;
  litrePriceReadableValue: string;
  litrePriceValue: number;
  mainCategoryCode: string;
  mainCategoryName: string;
  mainCountryCode: string;
  mainCountryName: string;
  mainCountrySearchQuery: string;
  mainCountryUrl: string;
  mainProducerCode: string;
  mainProducerName: string;
  mainProducerSearchQuery: string;
  mainProducerUrl: string;
  name: string;
  packageType?: string;
  priceFormattedValue: string;
  priceReadableValue: string;
  priceValue: number;
  productSelection: string;
  releaseMode: boolean;
  similarProducts: boolean;
  smell?: string;
  status: string;
  statusNotification: boolean;
  summary: string;
  sustainable: boolean;
  taste?: string;
  url: string;
  volumeFormattedValue: string;
  volumeReadableValue: string;
  volumeValue: number;
  wholeSaler: string;
  year?: string;
  parsedSize: number;
  pricePerLiter: number;
  alcoholPerNok: number;
  absoluteUrl: string;
}

const VinmonopolProduct = mongoose.models.VinmonopolProduct ?? mongoose.model<IVinmonopolProduct>('VinmonopolProduct', VinmonopolProductSchema, "VinmonopolProducts");

export default VinmonopolProduct;