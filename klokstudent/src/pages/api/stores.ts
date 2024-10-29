import { type NextApiRequest, type NextApiResponse } from 'next';
import Store from 'lib/lib/models/store';
import connectToDatabase from 'lib/lib/productapi';

async function getStores(limit: number, offset: number, dbId: string | null, res: NextApiResponse) {
    try {
        await connectToDatabase();
        let stores;
        if (dbId) {
            stores = await Store.findById(dbId).exec();
            if (!stores) {
                return res.status(404).json({ error: 'Store not found' });
            }
        } else {
            stores = await Store.find({})
                .skip(offset)
                .limit(limit)
                .exec();
        }
        res.status(200).json(stores);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching stores' });
    }
}

function validateQueryParams(limit: string, offset: string) {
    const limitValue = parseInt(limit, 10);
    const offsetValue = parseInt(offset, 10);
    if (isNaN(limitValue) || isNaN(offsetValue) || limitValue < 0 || offsetValue < 0) {
        return { isValid: false, limitValue: 0, offsetValue: 0 };
    }
    return { isValid: true, limitValue, offsetValue };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'GET') {
        const { limit = '30', offset = '0', dbId = null } = req.query;
        const { isValid, limitValue, offsetValue } = validateQueryParams(limit as string, offset as string);

        if (!isValid) {
            return res.status(400).json({ error: 'Invalid limit or offset value' });
        }

        await getStores(limitValue, offsetValue, dbId as string | null, res);
    } else {
        res.setHeader('Allow', ['GET']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}