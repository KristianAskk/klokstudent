import axios from 'axios';
import { Schema, model, connect, disconnect } from 'mongoose';
import * as fs from 'fs/promises';
import * as path from 'path';
import { DateTime } from 'luxon';
import cron from 'node-cron';
import { GLOESHAUGEN_LOCATION, PRODUCTS, DATABASE_NAME, DATABASE_URL, TIMEZONE } from './config'; 
import { Store, VinmonopolProduct } from './models';



interface StoreFinderStockSearchPageResponse {
  stores: StoreResponse[];
}

interface StoreResponse {
  pointOfService: {
    address: {
      formattedAddress: string;
      id: string;
      line1: string;
    };
    displayName: string;
    formattedDistance: string;
    geoPoint: {
      latitude: number;
      longitude: number;
    };
    id: string;
    name: string;
  };
  stockInfo: {
    stockLevel: number;
  };
}

async function initVinmonopolProducts(): Promise<void> {
  const filePath = path.join(__dirname, 'vinmonopol_products.json');

  try {
    const data = await fs.readFile(filePath, 'utf8');
    const products = JSON.parse(data);

    await connect(DATABASE_URL);

    for (const product of products) {
      const updatedProduct = await VinmonopolProduct.findOneAndUpdate(
        { code: product.code },
        product,
        { upsert: true, new: true, setDefaultsOnInsert: true }
      );
      console.log(`Saved/Updated product ${updatedProduct.name}`);
    }

    console.log('Vinmonopol products have been initialized.');
  } catch (error) {
    console.error('Error initializing Vinmonopol products:', error);
  } finally {
    await disconnect();
  }
}

function createUrl(productId: string, longitude: number, latitude: number): string {
  return `https://www.vinmonopolet.no/vmpws/v2/vmp/products/${productId}/stock?pageSize=10&currentPage=0&fields=BASIC&latitude=${latitude}&longitude=${longitude}`;
}

async function fetchStoreData(productId: string): Promise<StoreResponse[]> {
  const url = createUrl(productId, GLOESHAUGEN_LOCATION.longitude, GLOESHAUGEN_LOCATION.latitude);
  console.log(`Fetching ${url}`);
  const response = await axios.get<StoreFinderStockSearchPageResponse>(url);
  return response.data.stores;
}

async function updateOrCreateStore(store: StoreResponse): Promise<InstanceType<typeof Store>> {
  let storeObject = await Store.findOne({ pointOfServiceId: store.pointOfService.id });
  if (!storeObject) {
    storeObject = new Store({
      addressFormattedAddress: store.pointOfService.address.formattedAddress,
      addressId: store.pointOfService.address.id,
      addressLine1: store.pointOfService.address.line1,
      displayName: store.pointOfService.displayName,
      formattedDistance: store.pointOfService.formattedDistance,
      geoPointLatitude: store.pointOfService.geoPoint.latitude,
      geoPointLongitude: store.pointOfService.geoPoint.longitude,
      pointOfServiceId: store.pointOfService.id,
      name: store.pointOfService.name,
      stockInfo: []
    });
    await storeObject.save();
    console.log(`Store ${storeObject.addressFormattedAddress} has been created`);
  }
  return storeObject;
}

async function updateStockInfo(storeObject: InstanceType<typeof Store>, store: StoreResponse, productId: string): Promise<void> {
  const product = await VinmonopolProduct.findOne({ code: productId });
  if (!product) {
    console.log(`Could not find product ${productId}`);
    return;
  }

  let stockInfo = storeObject.stockInfo.find(info => info.productId === productId);
  if (!stockInfo) {
    stockInfo = {
      product: product,
      productId: productId,
      stockLevels: []
    };
    storeObject.stockInfo.push(stockInfo);
  }

  const currentStock = store.stockInfo.stockLevel;
  const lastStock = stockInfo.stockLevels[stockInfo.stockLevels.length - 1];

  if (!lastStock || lastStock.level !== currentStock) {
    stockInfo.stockLevels.push({
      timestamp: new Date(),
      level: currentStock
    });
    await storeObject.save();
    console.log(`Updated stock for ${product.name} in ${storeObject.addressFormattedAddress}: ${currentStock}`);
  }
}

function isWithinOperatingHours(): boolean {
  const now = DateTime.now().setZone(TIMEZONE);
  const day = now.weekday;
  const hour = now.hour;
  const minute = now.minute;

  // Oepningstidene til vinmonopolet...
  if (day >= 1 && day <= 5) {
    return (hour > 10 || (hour === 10 && minute >= 0)) && (hour < 18 || (hour === 18 && minute === 0));
  } else if (day === 6) {
    return (hour > 10 || (hour === 10 && minute >= 0)) && (hour < 16 || (hour === 16 && minute === 0));
  }
  return false;
}

async function runDataFetch(): Promise<void> {
  try {
    await connect(DATABASE_URL);

    for (const productId of PRODUCTS) {
      const stores = await fetchStoreData(productId);
      for (const store of stores) {
        const storeObject = await updateOrCreateStore(store);
        await updateStockInfo(storeObject, store, productId);
      }
    }
  } catch (error) {
    console.error('Error in data fetch:', error);
  } finally {
    await disconnect();
  }
}

function mainLoop(): void {
  console.log('Entering main loop...');

  cron.schedule('*/10 * * * * *', () => {
    const now = DateTime.now().setZone(TIMEZONE);
    if (isWithinOperatingHours()) {
      console.log('Running data fetch at', now.toLocaleString(DateTime.DATETIME_FULL));
      runDataFetch();
    } else {
      console.log('Stores are closed, skipping data fetch', now.toLocaleString(DateTime.DATETIME_FULL));
    }
  });
}

mainLoop();