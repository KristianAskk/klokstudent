import Head from "next/head";
import Link from "next/link";
// import react stuff
import { useState, useEffect, use } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Store from "lib/lib/models/store";
import { IStore } from "lib/lib/models/store";
import { check } from "prettier";
import { IFeed } from "lib/lib/models/feed";

// const Stores = ({ stores }: { stores: IStore[] }) => {
//   return (
//     <div className="flex flex-col items-center">
//       {stores.map((store) => (
//         <div key={store.name} className="border rounded-lg p-4 m-2 w-1/2 text-center">
//           <p className="text-gray-600">{store.addressFormattedAddress}</p>
//         </div>
//       ))}
//     </div>
//   );
// };

// const fetchStoreData = async (): Promise<IStore[]> => {
//   try {
//     const { data }: { data: IStore[] } = await axios.get("/api/stores");
//     return data;
//   } catch (error) {
//     console.error("Failed to fetch stores:", error);
//     return [];
//   }
// }

const Feed = ({ feedUpdates }: { feedUpdates: IFeed[] }) => { 
  return (
    
    


    <div className="flex flex-col items-center"></div>  )
}

export default function Home() {

  const [feed, setFeed] = useState<IFeed[]>([]);




  useEffect(() => {
    const fetchFeeds = async () => {
      try {
        

      }



  // useEffect(() => {
  //   const fetchStores = async () => {
  //     try {
  //       const { data }: { data: IStore[] } = await axios.get("/api/stores");
  //       setStores(data);
  //     } catch (error) {
  //       console.error("Failed to fetch stores:", error);
  //     }
  //   };
  //   void fetchStores();
  // }, [])


  return (
    <>
      <Head>
        <title>Klok Student</title>
        <meta name="description" content="Klok Student" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" />


      </Head>
      <h1 className="text-3xl font-bold text-center">Klok Student</h1>
      
      
      
    </>
  );
}
