
export const GLOESHAUGEN_LOCATION: { latitude: number, longitude: number } = {
    latitude: 63.415570,
    longitude: 10.404534
};

// products we want to continously scrape: TODO: make this configurable
export const PRODUCTS: Array<string> = ["3420106", "3901", "1206002", "20001", "1334902", "1206801", "12077202"];
export const DATABASE_NAME = "klokstudent";
export const DATABASE_URL = `mongodb://localhost:27017/${DATABASE_NAME}`;
export const TIMEZONE = 'Europe/Oslo';