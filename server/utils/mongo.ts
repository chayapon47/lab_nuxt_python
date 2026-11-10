import { MongoClient, type Db } from 'mongodb'
let client: MongoClient | undefined
let db: Db | undefined
export async function getMongo(event: any): Promise<Db> {
  if (db) return db
  const cfg = useRuntimeConfig(event)
  if (!client) client = new MongoClient(String(cfg.mongoUri), { serverSelectionTimeoutMS: 3000 })
  await client.connect()
  db = client.db(String(cfg.mongoDbName))
  return db
}
