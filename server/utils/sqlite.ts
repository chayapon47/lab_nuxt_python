import Database from 'better-sqlite3'
import { resolve } from 'node:path'
let db: Database.Database | undefined
export function getDb() {
  if (!db) {
    db = new Database(resolve(process.cwd(), 'server/data/training.db'))
    db.pragma('foreign_keys = ON')
  }
  return db
}
