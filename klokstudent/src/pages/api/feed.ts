/* eslint-disable @typescript-eslint/no-unsafe-assignment */

import { NextApiRequest, NextApiResponse } from "next";
import Feed from "lib/lib/models/feed";

import connectToDatabase from "lib/lib/productapi";
import Store from "lib/lib/models/store";
import VinmonopolProduct from "lib/lib/models/vinmonopolproduct";

const DEFAULT_LIMIT = 30;
const INVALID_OFFSET_ERROR = { error: "Invalid offset value" };
const DB_CONNECTION_ERROR = { error: "Error fetching feeds" };
const METHOD_NOT_ALLOWED_ERROR = (method: string) => `Method ${method} Not Allowed`;

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET']);
    return res.status(405).end(METHOD_NOT_ALLOWED_ERROR(req.method!));
  }

  const { offset = '0'} = req.query;
  const offsetValue = parseInt(offset as string, 10);
  if (isNaN(offsetValue)) {
    return res.status(400).json(INVALID_OFFSET_ERROR);
  }

  // TOOD DO THIS SHIT RIGHT HERE> 
  const db = await connectToDatabase();
  const feeds = await Feed.find({}).sort({ date: -1 }).skip(offsetValue).limit(DEFAULT_LIMIT);
}
