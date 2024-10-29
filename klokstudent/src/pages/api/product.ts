import VinmonopolProduct from 'lib/lib/models/vinmonopolproduct';
import connectToDatabase from 'lib/lib/productapi';
import { NextApiRequest, NextApiResponse } from 'next';

const DEFAULT_LIMIT = 20;
const INVALID_OFFSET_ERROR = { error: 'Invalid offset value' };
const DB_CONNECTION_ERROR = { error: 'Error fetching products' };
const METHOD_NOT_ALLOWED_ERROR = (method: string) => `Method ${method} Not Allowed`;

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET']);
    return res.status(405).end(METHOD_NOT_ALLOWED_ERROR(req.method!));
  }

  const { offset = '0', dbId = '' } = req.query;
  const offsetValue = parseInt(offset as string, 10);
  const dbIdValue = dbId as string;

  if (isNaN(offsetValue) || offsetValue < 0) {
    return res.status(400).json(INVALID_OFFSET_ERROR);
  }

  try {
    await connectToDatabase();

    if (dbIdValue) {
      const product = await fetchProductById(dbIdValue);
      if (product) {
        return res.status(200).json(product);
      }
      return res.status(500).json(DB_CONNECTION_ERROR);
    }

    const products = await fetchProducts(offsetValue);
    return res.status(200).json(products);
    
  } catch (error) {
    return res.status(500).json(DB_CONNECTION_ERROR);
  }
}

async function fetchProductById(id: string) {
  try {
    return await VinmonopolProduct.findById(id).exec();
  } catch {
    return null;
  }
}

async function fetchProducts(offset: number) {
  return await VinmonopolProduct.find({})
    .skip(offset)
    .limit(DEFAULT_LIMIT)
    .exec();
}